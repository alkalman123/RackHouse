"""Photoreal product images, rendered with Blender Cycles (path tracing).

    pip install bpy==4.2.0 manifold3d trimesh scipy matplotlib pillow
    python3 designs/render/photoreal.py [product ...] [--views gear,hero,front,edge,dark] [--samples N]

For each product: a lifelike rack (realgear.py) clipped through the real
product openings and hung physically, rendered in six colourways from
four angles, plus dark hero shots, composited onto the site backgrounds.
Writes img/products/<id>-<color>-<view>.jpg and <id>-hero-dark.jpg.

These are 3D renders of the production files, not photographs.
"""

import argparse
import json
import math
import os
import sys
import time

import numpy as np
import trimesh
from matplotlib.path import Path as MPath
from scipy.ndimage import distance_transform_edt

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGNS = os.path.dirname(HERE)
ROOT = os.path.dirname(DESIGNS)
sys.path.insert(0, HERE)
sys.path.insert(0, DESIGNS)

import realgear as G                                # noqa: E402
from gear import Plate, plan                         # noqa: E402
from products import CATALOG                         # noqa: E402
from make_images import COLORWAYS, composite, linear_bg, radial_bg   # noqa: E402

OUT = os.path.join(ROOT, "img", "products")
RAW = os.path.join(HERE, "raw-cycles")
VIEWS = {
    "gear": dict(elev=12, azim=-68, fill=0.80),
    "hero": dict(elev=16, azim=-62, fill=0.74),
    "front": dict(elev=4, azim=-90, fill=0.74),
    "edge": dict(elev=24, azim=-25, fill=0.74),
}
DARK = dict(elev=10, azim=-64)
QD_SLINGS = ["#2f7fd0", "#e2582a", "#3aa35b", "#d4b12f", "#8c4fc2", "#d13c55"]
QD_BOTTOM = ["#2f6fc8", "#c8372b", "#3f9a4f", "#dcb22c", "#7a4fb0", "#c8372b"]


# ------------------------------------------------------------ plate field

class PlateField:
    """Product plate as a 2D distance field (x, z) and a slab in y."""

    def __init__(self, cs, T, res=0.4):
        polys = [np.asarray(p) for p in cs.to_polygons()]
        allp = np.vstack(polys)
        self.x0, self.z0 = allp.min(0) - 6
        x1, z1 = allp.max(0) + 6
        self.res = res
        nx, nz = int((x1 - self.x0) / res) + 1, int((z1 - self.z0) / res) + 1
        gx, gz = np.meshgrid(self.x0 + np.arange(nx) * res, self.z0 + np.arange(nz) * res, indexing="ij")
        pts = np.c_[gx.ravel(), gz.ravel()]
        inside = np.zeros(len(pts), bool)
        for p in polys:
            inside ^= MPath(p).contains_points(pts)
        self.solid = inside.reshape(nx, nz)
        self.dist = distance_transform_edt(~self.solid) * res      # free cell -> nearest solid
        self.T = T

    def inside(self, pts, margin=1.0):
        pts = np.asarray(pts)
        dy = np.maximum(0, np.abs(pts[:, 1] + self.T / 2) - self.T / 2)
        near = dy < margin
        out = np.zeros(len(pts), bool)
        if not near.any():
            return out
        q = pts[near]
        ix = np.clip(((q[:, 0] - self.x0) / self.res).round().astype(int), 0, self.solid.shape[0] - 1)
        iz = np.clip(((q[:, 2] - self.z0) / self.res).round().astype(int), 0, self.solid.shape[1] - 1)
        need = np.sqrt(np.maximum(0, margin ** 2 - dy[near] ** 2))
        out[near] = self.solid[ix, iz] | (self.dist[ix, iz] < need)
        return out


# ---------------------------------------------------------- carabiner fit

def place_biner(plate, clip, biner, max_tilt=85.0, others=None):
    """Carabiner through its opening, apex resting on the web it closes
    round, tilted toward the viewer only as far as its frame needs to
    clear the plastic and the other openings. Returns the local->world
    matrix or None."""
    px, pz = clip["xy"]
    d = np.array(clip["dir"], float)
    own = plate.hole_index((px, pz))
    s = 0.0
    while plate.hole_index((px + d[0] * s, pz + d[1] * s)) == own:
        s += 0.25
    face = np.array([px, pz]) + d * s
    s2 = s
    while plate.solid((px + d[0] * s2, pz + d[1] * s2)):
        s2 += 0.25
    web_mid = np.array([px, pz]) + d * (s + s2) / 2
    yc = -plate.T / 2
    d3 = np.array([d[0], 0.0, d[1]])
    ey = np.array([0.0, 1.0, 0.0])
    nz = np.cross(d3, ey)
    test = biner.centerline3()[::2]
    for tilt in np.arange(0.0, max_tilt + 0.1, 2.5):
        th = np.radians(tilt)
        A = np.cos(th) * d3 - np.sin(th) * ey
        B = np.sin(th) * d3 + np.cos(th) * ey
        Rm = np.c_[A, B, nz]
        # the round top rests on the strip's two corners: lift it until clear
        for lift in np.arange(0.0, 9.1, 0.5):
            top = face - d * (G.Biner.ROD_R + 0.4 + lift)
            topw = np.array([top[0], yc, top[1]])
            if plate.hole_index((top[0], top[1])) != own:
                break
            for pv in (topw, np.array([web_mid[0], yc, web_mid[1]])):
                origin = pv + _rot_in_plane(topw - pv, d3, ey, th)
                w = test @ Rm.T + origin
                if others is not None and len(others.data):
                    dd, _ = others.query(w)
                    if dd.min() < 2 * G.Biner.ROD_R + 0.6:
                        continue
                if not _encloses_only_web(plate, w, yc, d, face, s2 - s, px, pz):
                    continue
                if all(plate.wire_clear(q, own, G.Biner.ROD_R + 0.2) for q in w):
                    return G.frame_matrix(origin, A, B, nz)
    return None


def _encloses_only_web(plate, w, yc, d, face, web, px, pz):
    """The loop crosses the plate's mid-plane twice: once in its own
    opening, once on the far side of the web. Between the web and that
    second crossing there must be no plastic, or the carabiner would be
    wrapped round more of the product than the strip it is clipped to."""
    sgn = np.sign(w[:, 1] - yc)
    idx = np.where(sgn != np.roll(sgn, -1))[0]
    if len(idx) < 2:
        return False
    # in-plane distance (along the hang direction) of each crossing below the web face
    along = [((w[i, 0] - face[0]) * d[0] + (w[i, 2] - face[1]) * d[1]) for i in idx]
    far = max(along)
    for t in np.arange(web + 0.6, far, 0.5):
        if plate.solid((face[0] + d[0] * t, face[1] + d[1] * t)):
            return False
    return True


def _rot_in_plane(v, d3, ey, th):
    ra, rb = v @ d3, v @ ey
    rest = v - ra * d3 - rb * ey
    return (ra * np.cos(th) + rb * np.sin(th)) * d3 + (-ra * np.sin(th) + rb * np.cos(th)) * ey + rest


# ------------------------------------------------------------- scene build

def cam_dir(view):
    el, az = math.radians(view["elev"]), math.radians(view["azim"])
    return np.array([math.cos(el) * math.cos(az), math.cos(el) * math.sin(az), math.sin(el)])


def build_rack(pid):
    """World meshes by material (mm) for the gear on one product."""
    fn, title, marks, hangs = CATALOG[pid]
    rep = json.load(open(os.path.join(DESIGNS, "products-report.json")))[pid]
    p = fn()
    p.build(marks=marks)
    plate = Plate(p.cs, p.clip_points, p.T)
    field = PlateField(p.cs, p.T)
    obst = G.Obstacles(field)
    mats = {}

    def add(parts, M=None):
        for k, ms in parts.items():
            mats.setdefault(k.replace("#", ""), []).extend(m.transformed(M) if M is not None else m for m in ms)

    jobs = []
    placed_cl = []
    pl = plan(pid, rep["clips"])
    n_cams = sum(1 for kind, _ in pl.values() if kind == "cam")
    for k, (i, (kind, size)) in enumerate(sorted(pl.items())):
        if kind == "cam" and n_cams > len(G.CAM_SIZES) and size is not None:
            # more windows than sizes: spread 0.3..4 across them, doubling some (a double rack)
            size = int(round(size * (len(G.CAM_SIZES) - 1) / (n_cams - 1)))
        if kind == "cam" and pid == "gear-board" and size >= 6:
            continue                        # real-size gear from the top row would drape over the rest
        if kind == "cam":
            color = G.CAM_SIZES[size][1]
            b = G.Biner("wire")
            bcol = color
        else:
            b = G.Biner("straight")
            bcol = "#b8bcc2"
        from scipy.spatial import cKDTree
        placed = np.vstack(placed_cl) if placed_cl else np.zeros((0, 3))
        M = place_biner(plate, rep["clips"][i], b, others=cKDTree(placed) if len(placed) else None)
        if M is None:
            print(f"  {pid}: opening {i} skipped (no clear carabiner pose)")
            continue
        add(b.meshes(bcol.lstrip("#")), M)
        cl = b.centerline3() @ M[:3, :3].T + M[:3, 3]
        placed_cl.append(G.resample(cl, 1.0, True))
        obst.add_points(G.resample(cl, 1.0, True), G.Biner.ROD_R + 0.3)
        pivot, tang = b.basket_point(M)
        jobs.append((pivot, tang, kind, size, k, len(obst.clouds) - 1))
    view_dir = cam_dir(VIEWS["gear"])
    # hang the lowest pieces first; higher ones settle against them
    for pivot, tang, kind, size, k, own in sorted(jobs, key=lambda j: j[0][2]):
        if kind == "cam":
            fnp = (lambda s: (lambda psi: G.cam(s, psi)))(size)
        else:
            fnp = (lambda kk: (lambda psi: G.quickdraw(psi, QD_SLINGS[kk % 6], QD_BOTTOM[kk % 6])))(k)
        parts, f, wp, pose = G.hang(fnp, pivot, tang, obst, view_dir, ignore=(own,),
                                     bend_depth=48.0 if kind == "cam" else 30.0)
        if os.environ.get("RACK_DEBUG"):
            print("   ", kind, size, "drape %d swing %d twist %.0f roll %d" % pose)
        for key, ms in parts.items():
            mats.setdefault(key.replace("#", ""), []).extend(G.Mesh(f(m.V), m.F, m.FUV) for m in ms)
        obst.add_points(wp, 0.6)
    # wall hardware: steel screws with washers the product hangs on
    ys = []
    for key, ms in mats.items():
        for m in ms:
            ys.append(m.V[:, 1].max())
    wall = max([0.0] + ys) + 3.0
    for hx, hz in hangs:
        add({"steel": [G.cylinder([hx, wall, hz], [hx, -p.T - 3.0, hz], 2.1, 16),
                       G.cylinder([hx, -p.T - 3.0, hz], [hx, -p.T - 4.6, hz], 5.2, 24)]})
    return mats, wall


def hardware(pid):
    """Just the wall screws (no gear), for the product-only views."""
    fn, title, marks, hangs = CATALOG[pid]
    T = json.load(open(os.path.join(DESIGNS, "products-report.json")))[pid]["thickness_mm"]
    wall = 3.0
    ms = []
    for hx, hz in hangs:
        ms += [G.cylinder([hx, wall, hz], [hx, -T - 3.0, hz], 2.1, 16),
               G.cylinder([hx, -T - 3.0, hz], [hx, -T - 4.6, hz], 5.2, 24)]
    return {"steel": ms}, wall


def product_mesh(pid):
    t = trimesh.load(os.path.join(ROOT, "models", f"{pid}.stl"))
    return G.Mesh(np.asarray(t.vertices), np.asarray(t.faces))


# ----------------------------------------------------------------- render

def render_set(pid, views, samples, colors, rack=None):
    import bl
    os.makedirs(RAW, exist_ok=True)
    prod = product_mesh(pid)
    if rack is None and ("gear" in views or "dark" in views):
        t = time.time()
        rack = build_rack(pid)
        print(f"  {pid}: rack built in {time.time() - t:.0f}s")
    jobs = []
    for vk in views:
        if vk == "dark":
            jobs.append(("dark", "ember", dict(DARK, fill=0.97)))
        else:
            for ck in colors:
                jobs.append((vk, ck, VIEWS[vk]))
    for vk, ck, view in jobs:
        out_png = os.path.join(RAW, f"{pid}-{ck}-{vk}.png")
        sc = bl.reset(samples=samples, size=1400)
        if vk == "dark":
            sc.render.resolution_x, sc.render.resolution_y = 1600, 1120
        cw = COLORWAYS[ck]["hex"]
        objs = [bl.add_mesh("product", prod, f"pla-{cw.lstrip('#')}", sharp_angle=30)]
        if vk in ("gear", "dark"):
            mats, wall = rack
        else:
            mats, wall = hardware(pid)
        for key, ms in mats.items():
            objs.append(bl.add_mesh(key, G.Mesh.merge(ms), key, sharp_angle=40 if key.startswith("alu") else None))
        bl.shadow_wall(wall)
        frame(bl, objs, view)
        sc.render.filepath = out_png
        t = time.time()
        bl.bpy.ops.render.render(write_still=True)
        print(f"  {pid} {ck} {vk}: {time.time() - t:.0f}s", flush=True)
    return rack


def frame(bl, objs, view):
    """Studio lighting + an 85 mm camera, aimed and distanced so the
    product and its gear fill `fill` of the frame."""
    from bpy_extras.object_utils import world_to_camera_view
    from mathutils import Vector
    sc = bl.bpy.context.scene
    pts = np.vstack([np.array([o.matrix_world @ Vector(c) for c in o.bound_box]) for o in objs])
    lo, hi = pts.min(0), pts.max(0)
    c = (lo + hi) / 2
    d = cam_dir(view)
    fov = 2 * math.atan(18 / 85)
    dist = np.linalg.norm(hi - lo) / 2 / math.sin(fov / 2)
    cam = bl.camera(tuple(c), d, dist)
    corners = [Vector(p) for p in pts]
    for _ in range(4):
        bl.bpy.context.view_layer.update()
        ndc = np.array([tuple(world_to_camera_view(sc, cam, p))[:2] for p in corners])
        mn, mx = ndc.min(0), ndc.max(0)
        span = max(mx - mn)
        # re-aim at the projected centre, then scale distance to the fill
        right = np.array(cam.matrix_world.to_3x3() @ Vector((1, 0, 0)))
        up = np.array(cam.matrix_world.to_3x3() @ Vector((0, 1, 0)))
        off = ((mn + mx) / 2 - 0.5)
        w = 2 * dist * math.tan(fov / 2)
        c = c + right * off[0] * w + up * off[1] * w
        dist = dist * span / view["fill"]
        cam.location = tuple(c + d * dist)
        bl.look_at(cam, tuple(c))
    side = np.cross([0, 0, 1], d)
    side /= np.linalg.norm(side)
    k = max(dist, 0.6)
    s = k ** 2
    bl.area_light("key", tuple(c + (d * 0.9 + side * 0.7 + np.array([0, 0, 0.8])) * k), tuple(c), 0.9 * k, 80 * s)
    bl.area_light("fill", tuple(c + (d * 0.9 - side * 0.9 + np.array([0, 0, 0.1])) * k), tuple(c), 1.2 * k, 22 * s)
    bl.area_light("rim", tuple(c + (-d * 0.6 - side * 0.6 + np.array([0, 0, 0.9])) * k), tuple(c), 0.6 * k, 45 * s)


def _full(png, bg):
    from PIL import Image
    im = Image.open(png).convert("RGBA")
    if im.size != bg.size:
        im = im.resize(bg.size, Image.LANCZOS)
    out = bg.convert("RGBA")
    out.alpha_composite(im)
    return out.convert("RGB")


def finish(pid, views, colors):
    for vk in views:
        if vk == "dark":
            bg = radial_bg((1600, 1120), (58, 30, 18), (10, 11, 10))
            img = _full(os.path.join(RAW, f"{pid}-ember-dark.png"), bg)
            img.save(os.path.join(OUT, f"{pid}-hero-dark.jpg"), quality=88, optimize=True, progressive=True)
            continue
        for ck in colors:
            img = _full(os.path.join(RAW, f"{pid}-{ck}-{vk}.png"), linear_bg((1400, 1400), *COLORWAYS[ck]["bg"]))
            img.save(os.path.join(OUT, f"{pid}-{ck}-{vk}.jpg"), quality=88, optimize=True, progressive=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("products", nargs="*")
    ap.add_argument("--views", default="gear,hero,front,edge,dark")
    ap.add_argument("--colors", default=",".join(COLORWAYS))
    ap.add_argument("--samples", type=int, default=96)
    a = ap.parse_args()
    views = a.views.split(",")
    colors = a.colors.split(",")
    for pid in a.products or list(CATALOG):
        if "dark" in views and pid not in ("gear-board", "crag-ring"):
            v = [x for x in views if x != "dark"]
        else:
            v = views
        render_set(pid, v, a.samples, colors)
        finish(pid, v, colors)


if __name__ == "__main__":
    main()
