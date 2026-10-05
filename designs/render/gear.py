"""Builds 3D gear mock-up scenes for the product renders: each product with
carabiners clipped through its real openings and quickdraws or a trad rack
of cams hanging from them.

Placement is physical, not eyeballed: every carabiner passes through its
own opening, rests on the web it closes around (designs/products-report.json
gives each opening's hang direction), and is tilted forward only as far as
needed so its wire never passes through solid plastic or through another
opening.

    python3 designs/render/gear.py

Writes designs/render/scenes/<product>/*.stl (one file per material) and
designs/render/scenes/scenes.json, which make_images.py renders.
"""

import json
import os
import sys

import numpy as np
import trimesh

HERE = os.path.dirname(os.path.abspath(__file__))
DESIGNS = os.path.dirname(HERE)
ROOT = os.path.dirname(DESIGNS)
sys.path.insert(0, DESIGNS)
import prototypes2 as P
from products import CATALOG

SCENES = os.path.join(HERE, "scenes")
WIRE_R = 4.5                       # carabiner wire radius (9 mm stock)
BINER_W, BINER_L = 24.0, 58.0      # carabiner centreline width x length

# cam unit colours, smallest to largest (common anodizing convention)
CAM_COLORS = ["#8a8f96", "#7b4fa0", "#3a8f4f", "#c03b2b", "#d8b52a", "#3a6fc0", "#8a8f96", "#7b4fa0"]
SLING_COLORS = ["#2f7fd0", "#e2582a", "#3aa35b", "#d4b12f", "#8c4fc2", "#d13c55"]
METAL = "#c9ced4"


# ------------------------------------------------------------ mesh helpers

def tube(points, radius, closed=True, segs=12, normal=None):
    """Tube mesh along a planar polyline; `normal` is the curve plane's normal."""
    pts = np.asarray(points, float)
    n = len(pts)
    if closed:
        tang = np.roll(pts, -1, 0) - np.roll(pts, 1, 0)
    else:
        tang = np.gradient(pts, axis=0)
    tang /= np.linalg.norm(tang, axis=1, keepdims=True)
    nrm = np.asarray(normal, float) / np.linalg.norm(normal)
    side = np.cross(tang, nrm)
    ang = np.linspace(0, 2 * np.pi, segs, endpoint=False)
    verts = (pts[:, None, :] + radius * (np.cos(ang)[None, :, None] * nrm[None, None, :]
                                          + np.sin(ang)[None, :, None] * side[:, None, :])).reshape(-1, 3)
    faces = []
    rings = n if closed else n - 1
    for i in range(rings):
        j = (i + 1) % n
        for k in range(segs):
            k2 = (k + 1) % segs
            a, b, c, d = i * segs + k, i * segs + k2, j * segs + k2, j * segs + k
            faces += [[a, b, c], [a, c, d]]
    m = trimesh.Trimesh(verts, np.array(faces), process=False)
    if not closed:
        m = trimesh.util.concatenate([m, _cap(pts[0], tang[0], radius, segs), _cap(pts[-1], tang[-1], radius, segs)])
    return m


def _cap(center, axis, radius, segs):
    s = trimesh.creation.icosphere(subdivisions=1, radius=radius)
    s.apply_translation(center)
    return s


def box(center, size):
    b = trimesh.creation.box(extents=size)
    b.apply_translation(center)
    return b


def cylinder(p0, p1, radius, segs=20):
    return trimesh.creation.cylinder(radius=radius, segment=[p0, p1], sections=segs)


def disc(center, radius, thickness, axis):
    c = trimesh.creation.cylinder(radius=radius, height=thickness, sections=36)
    z = np.array([0, 0, 1.0])
    axis = np.asarray(axis, float) / np.linalg.norm(axis)
    if not np.allclose(axis, z):
        c.apply_transform(trimesh.geometry.align_vectors(z, axis))
    c.apply_translation(center)
    return c


def cam_lobe(axle_c, axle, across, R, thickness, flip):
    """A spiral cam lobe pivoting on the axle: a log-spiral sector that
    widens from 0.55R to R, plus a hub. `flip` mirrors it across the stem."""
    from manifold3d import CrossSection as CS
    th = np.radians(np.linspace(-150.0, -15.0, 60))
    k = np.log(1 / 0.55) / (th[-1] - th[0])
    r = 0.55 * R * np.exp(k * (th - th[0]))
    pts = [(0.0, 0.0)] + [(ri * np.cos(t), ri * np.sin(t)) for ri, t in zip(r, th)]
    if flip:
        pts = [(-u, v) for u, v in pts][::-1]
    shape = CS([np.array(pts)]) + CS.circle(4.5, 24)
    mesh = shape.extrude(thickness).translate((0, 0, -thickness / 2)).to_mesh()
    v = np.asarray(mesh.vert_properties)[:, :3]
    up = np.array([0.0, 0.0, 1.0])
    world = axle_c[None, :] + v[:, 0:1] * across[None, :] + v[:, 1:2] * up[None, :] + v[:, 2:3] * axle[None, :]
    return trimesh.Trimesh(world, np.asarray(mesh.tri_verts), process=False)


def biner_centerline(n=160):
    """Rounded-rectangle 'D' in local (a, b): a = 0 at the top, increasing
    along the hang direction; b across, centred on 0."""
    t = np.linspace(0, 2 * np.pi, n, endpoint=False)
    e = 2 / 4.0
    b = BINER_W / 2 * np.sign(np.cos(t)) * np.abs(np.cos(t)) ** e
    a = BINER_L / 2 + BINER_L / 2 * np.sign(np.sin(t)) * np.abs(np.sin(t)) ** e
    return a, b


# ------------------------------------------------------- plate open-space

class Plate:
    """2D occupancy of a product in its plate plane (x, z), for clearance tests."""

    def __init__(self, cs, clip_points, T):
        self.polys = [np.asarray(p) for p in cs.to_polygons()]
        self.areas = [P._signed_area(p) for p in self.polys]
        self.outer_sign = np.sign(self.areas[int(np.argmax(np.abs(self.areas)))])
        self.dense = np.vstack([P._densify(p, 0.6) for p in self.polys])
        self.T = T
        self.clip_points = clip_points

    def hole_index(self, pt):
        c = [i for i, p in enumerate(self.polys) if np.sign(self.areas[i]) != self.outer_sign and P._point_in_poly(pt, p)]
        return min(c, key=lambda i: abs(self.areas[i])) if c else None

    def solid(self, pt):
        inside_outer = any(np.sign(self.areas[i]) == self.outer_sign and P._point_in_poly(pt, p)
                           for i, p in enumerate(self.polys))
        return inside_outer and self.hole_index(pt) is None

    def clearance(self, pt):
        return float(np.sqrt(((self.dense - np.asarray(pt)) ** 2).sum(1).min()))

    def free_distance(self, pt, own_hole):
        """In-plane distance from a point to material the wire must avoid
        (solid plastic, or another clip opening, which stays free). 0 if the
        point is inside such material."""
        if self.solid(pt):
            return 0.0
        hi = self.hole_index(pt)
        if hi is not None and hi != own_hole and abs(self.areas[hi]) <= P.MAX_OPENING_AREA:
            return 0.0
        return self.clearance(pt)

    def wire_clear(self, q, own_hole, r):
        """Exact clearance test for a wire of radius r centred at 3D point q
        against the plate, a prism of thickness T centred on y = -T/2."""
        dy = max(0.0, abs(q[1] + self.T / 2) - self.T / 2)
        need = r - 0.3
        if dy >= need:
            return True
        return self.free_distance((q[0], q[2]), own_hole) >= np.sqrt(need ** 2 - dy ** 2)


def place_biner(plate, clip, max_tilt=80.0):
    """Returns (centreline points Nx3, plane normal, bottom point) or None."""
    px, pz = clip["xy"]
    d = np.array(clip["dir"], float)
    own = plate.hole_index((px, pz))
    # walk from the opening centre along d to the web face
    s = 0.0
    while plate.hole_index((px + d[0] * s, pz + d[1] * s)) == own:
        s += 0.25
    face = np.array([px, pz]) + d * s
    # the web the carabiner closes around runs from `face` to `web_end`
    s2 = s
    while plate.solid((px + d[0] * s2, pz + d[1] * s2)):
        s2 += 0.25
    web_mid = np.array([px, pz]) + d * (s + s2) / 2
    top = face - d * (WIRE_R + 0.4)
    yc = -plate.T / 2
    a, b = biner_centerline()
    d3 = np.array([d[0], 0.0, d[1]])
    ey = np.array([0.0, 1.0, 0.0])
    normal = np.cross(d3, ey)
    base = (np.array([top[0], yc, top[1]])[None, :] + a[:, None] * d3[None, :] + b[:, None] * ey[None, :])
    pivots = [np.array([top[0], yc, top[1]]), np.array([web_mid[0], yc, web_mid[1]])]
    for tilt in np.arange(0.0, max_tilt + 0.1, 2.5):
        th = np.radians(tilt)
        for pv in pivots:
            rel = base - pv
            ra = rel @ d3
            rb = rel @ ey
            # rotate forward (toward -y, the viewer) in the (d3, ey) plane
            na = ra * np.cos(th) + rb * np.sin(th)
            nb = -ra * np.sin(th) + rb * np.cos(th)
            pts = pv[None, :] + na[:, None] * d3[None, :] + nb[:, None] * ey[None, :]
            if all(plate.wire_clear(q, own, WIRE_R) for q in pts):
                bottom = pts[int(np.argmax(pts @ d3))]
                return pts, normal, bottom, tilt
    return None


# ------------------------------------------------------------- gear items

def quickdraw(bottom, k):
    """Dogbone + bottom carabiner hanging straight down from `bottom`."""
    parts = {"sling": [], "metal": []}
    x, y, z = bottom
    top = z - WIRE_R + 3
    length = 92.0
    parts["sling"].append(box((x, y, top - length / 2), (3.0, 14.0, length)))
    a, b = biner_centerline()
    bz = top - length + 5
    pts = np.stack([x + b, np.full_like(a, y), bz - a], 1)
    parts["metal"].append(tube(pts, WIRE_R * 0.9, normal=(0, 1, 0)))
    return parts, SLING_COLORS[k % len(SLING_COLORS)]


def cam(bottom, size, k):
    """A cam hanging head-down from its sewn sling (clipped at `bottom`)."""
    x, y, z = bottom
    parts = {"sling": [], "metal": [], "lobes": []}
    sling_len = 44.0
    top = z - WIRE_R + 2
    parts["sling"].append(box((x, y, top - sling_len / 2), (2.5, 12.0, sling_len)))
    stem_top = top - sling_len + 4
    stem_len = 70.0 + size * 6
    parts["metal"].append(cylinder((x, y, stem_top), (x, y, stem_top - stem_len), 3.2))
    trig_z = stem_top - stem_len * 0.35
    alt = k % 2 == 1                  # alternate lobe planes so neighbours don't clash
    across = np.array([0.0, 1.0, 0.0]) if alt else np.array([1.0, 0.0, 0.0])
    axle = np.array([1.0, 0.0, 0.0]) if alt else np.array([0.0, 1.0, 0.0])
    c = np.array([x, y, trig_z])
    parts["metal"].append(cylinder(c - across * 17, c + across * 17, 2.6))
    hz = stem_top - stem_len
    parts["metal"].append(cylinder(np.array([x, y, hz]) - axle * 13, np.array([x, y, hz]) + axle * 13, 3.0))
    R = 11.0 + size * 3.4
    hub = np.array([x, y, hz])
    for i, off in enumerate((-10.0, -4.0, 4.0, 10.0)):
        parts["lobes"].append(cam_lobe(hub + axle * off, axle, across, R, 3.2, flip=(i in (1, 2))))
    return parts, CAM_COLORS[size % len(CAM_COLORS)]


# ------------------------------------------------------------ scene plans

def plan(pid, clips):
    """Which gear goes on which opening, for each product."""
    down = [i for i, c in enumerate(clips) if c["dir"][1] < -0.6]
    if pid == "gear-board":
        rows = {}
        for i in down:
            rows.setdefault(round(clips[i]["xy"][1]), []).append(i)
        ys = sorted(rows)
        g = {}
        for i in rows[ys[0]]:
            g[i] = ("qd", None)
        for k, i in enumerate(rows[ys[1]]):
            g[i] = ("cam", k)
        top_row = rows[ys[2]]
        g[top_row[0]] = ("cam", 6)
        g[top_row[-1]] = ("cam", 7)
        return g
    if pid in ("crag-ring", "rock-ring"):
        lower = sorted([i for i in down if clips[i]["xy"][1] < 30], key=lambda i: clips[i]["xy"][0])
        return {i: ("cam", k) for k, i in enumerate(lower)}
    if pid == "double-ring":
        g = {}
        outer = sorted([i for i in down if np.hypot(*clips[i]["xy"]) > 65 and clips[i]["xy"][1] < 30],
                       key=lambda i: clips[i]["xy"][0])
        for k, i in enumerate(outer):
            g[i] = ("cam", k)
        for i in down:
            if np.hypot(*clips[i]["xy"]) < 65:
                g[i] = ("qd", None)
        return g
    return {i: ("qd", None) for i in down}


def build_scene(pid):
    fn, title, marks, hangs = CATALOG[pid]
    rep = json.load(open(os.path.join(DESIGNS, "products-report.json")))[pid]
    p = fn()
    p.build(marks=marks)
    plate = Plate(p.cs, p.clip_points, p.T)
    groups = {"metal": [], "pegs": []}
    colors = {}
    placed = 0
    skipped = []
    for k, (i, (kind, size)) in enumerate(sorted(plan(pid, rep["clips"]).items())):
        res = place_biner(plate, rep["clips"][i])
        if res is None:
            skipped.append(i)
            continue
        pts, normal, bottom, tilt = res
        groups["metal"].append(tube(pts, WIRE_R, normal=normal))
        if kind == "qd":
            parts, col = quickdraw(bottom, k)
        else:
            parts, col = cam(bottom, size, k)
        for name, meshes in parts.items():
            if name == "metal":
                groups["metal"] += meshes
            else:
                key = f"{name}-{col.lstrip('#')}"
                groups.setdefault(key, []).extend(meshes)
                colors[key] = col
        placed += 1
    # pegs the product hangs on (from the wall, behind)
    for hx, hz in hangs:
        groups["pegs"].append(cylinder((hx, -p.T - 6, hz), (hx, 40.0, hz), 4.0))
    out = os.path.join(SCENES, pid)
    os.makedirs(out, exist_ok=True)
    files = []
    for key, meshes in groups.items():
        if not meshes:
            continue
        m = trimesh.util.concatenate(meshes)
        path = os.path.join(out, f"{key}.stl")
        m.export(path)
        if key == "metal":
            mat = {"color": METAL, "roughness": 0.32, "metalness": 0.55}
        elif key == "pegs":
            mat = {"color": "#3a3f45", "roughness": 0.5, "metalness": 0.3}
        elif key.startswith("lobes"):
            mat = {"color": colors[key], "roughness": 0.35, "metalness": 0.35}
        else:
            mat = {"color": colors[key], "roughness": 0.85, "metalness": 0.0}
        files.append({"stl": os.path.relpath(path, ROOT), **mat})
    print(pid, "placed", placed, "skipped", skipped)
    return {"parts": files, "placed": placed, "skipped": skipped}


def main():
    os.makedirs(SCENES, exist_ok=True)
    scenes = {pid: build_scene(pid) for pid in CATALOG}
    with open(os.path.join(SCENES, "scenes.json"), "w") as f:
        json.dump(scenes, f, indent=2)


if __name__ == "__main__":
    main()
