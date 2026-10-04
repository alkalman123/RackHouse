"""Rackhouse product designs — original parametric source.

Every product here is modeled from functional requirements (bottle and
cupholder diameters, finger-edge depths, carabiner clearances, print-bed
size), not derived from any third-party model. Run this file to rebuild
every STL:

    pip install manifold3d trimesh matplotlib
    python3 designs/rackhouse_designs.py

Outputs:
    models/*.stl               use orientation (site 3D viewer + renders)
    designs/print-ready/*.stl  print orientation, sitting on the bed at z=0

All dimensions in millimetres.
"""

import json
import os

import numpy as np
import manifold3d as m3d
from manifold3d import CrossSection as CS, Manifold as M, FillRule
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath

m3d.set_circular_segments(120)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


# ---------------------------------------------------------------- 2D helpers

def circle(r, cx=0.0, cy=0.0):
    return CS.circle(r).translate((cx, cy))


def rect(x0, y0, x1, y1):
    return CS.square((x1 - x0, y1 - y0)).translate((x0, y0))


def rounded_rect(x0, y0, x1, y1, r):
    return rect(x0, y0, x1, y1).offset(-r).offset(r)


def stadium(cx, cy, length, width, angle_deg):
    half = (length - width) / 2.0
    a = np.radians(angle_deg)
    dx, dy = half * np.cos(a), half * np.sin(a)
    return CS.batch_hull([circle(width / 2.0, cx - dx, cy - dy),
                          circle(width / 2.0, cx + dx, cy + dy)])


def text(s, size, cx=0.0, cy=0.0):
    fp = FontProperties(family="DejaVu Sans", weight="bold")
    polys = [p for p in TextPath((0, 0), s, size=size, prop=fp).to_polygons() if len(p) >= 3]
    cs = CS(polys, FillRule.EvenOdd).simplify(0.01)
    x0, y0, x1, y1 = cs.bounds()
    return cs.translate((cx - (x0 + x1) / 2.0, cy - (y0 + y1) / 2.0))


def polygon(pts):
    cs = CS([np.asarray(pts, dtype=float)], FillRule.EvenOdd)
    return cs


def slab_with_edge_break(shape, thickness, brk=0.6):
    """Extrude with a small stepped edge break top and bottom (also offsets
    first-layer squish so edges stay crisp)."""
    inset = shape.offset(-brk)
    return (inset.extrude(brk)
            + shape.extrude(thickness - 2 * brk).translate((0, 0, brk))
            + inset.extrude(brk).translate((0, 0, thickness - brk)))


# --------------------------------------------------------------- Gatekeeper

def gatekeeper():
    """Hanging gear organizer + helmet hook. Pear (HMS-style) frame with
    stadium gear slots, a stiffening name rail, a hang tab, and an open
    J-hook so a helmet hangs by its chin strap without unbuckling."""
    T = 10.0
    FRAME_W = 22.0
    outer = CS.batch_hull([circle(52, 0, 12), circle(36, 0, -44)])
    inner = outer.offset(-FRAME_W)
    frame = outer - inner

    tab = CS.batch_hull([circle(16, 0, 66), rect(-20, 48, 20, 56)])
    rail = rect(-40, 3, 40, 21)

    hook_cy = -106.0
    hook = circle(21, 0, hook_cy) - circle(11.5, 0, hook_cy)
    neck = rect(-8, hook_cy + 15, 8, -76)
    hook_gap = rect(-4.5, 0, 4.5, 34).rotate(-55).translate((0, hook_cy))

    body = frame + tab + rail + neck + hook
    body = body - hook_gap - circle(6.5, 0, 68)

    # Gear slots, evenly spaced along the frame's centreline, mirrored L/R.
    centre = outer.offset(-FRAME_W / 2.0).to_polygons()[0]
    centre = np.vstack([centre, centre[:1]])
    seg = np.linalg.norm(np.diff(centre, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    top_i = int(np.argmax(centre[:-1, 1] - 0.001 * np.abs(centre[:-1, 0])))
    # walk from the top point along the left (x<0) side
    pts_left = []
    order = list(range(top_i, len(centre) - 1)) + list(range(0, top_i))
    acc, prev = 0.0, centre[top_i]
    walk = []
    for i in order:
        p = centre[i]
        acc += np.linalg.norm(p - prev)
        prev = p
        walk.append((acc, p))
    # make sure we walk the left half (x <= 0)
    if np.mean([p[0] for a, p in walk[:20]]) > 0:
        walk = [(walk[-1][0] - a, p) for a, p in reversed(walk)]
        walk.sort(key=lambda t: t[0])
    half = [(a, p) for a, p in walk if p[0] <= 0.5]
    L = half[-1][0]

    def allowed(a, p):
        if a < 26 or a > L - 22:            # tab at top, hook neck at bottom
            return False
        if -8 <= p[1] <= 32:                # where the rail meets the frame
            return False
        return True

    arcs = np.array([a for a, p in half])
    def point_at(a):
        i = int(np.clip(np.searchsorted(arcs, a), 1, len(half) - 1))
        (a0, p0), (a1, p1) = half[i - 1], half[i]
        t = 0 if a1 == a0 else (a - a0) / (a1 - a0)
        return p0 + t * (p1 - p0), (p1 - p0)

    SLOT_L, SLOT_W, PITCH = 20.0, 11.0, 30.0
    runs, cur = [], []
    for a in np.arange(0, L, 0.5):
        p, _ = point_at(a)
        if allowed(a, p):
            cur.append(a)
        elif cur:
            runs.append(cur); cur = []
    if cur:
        runs.append(cur)
    centres = []
    for run in runs:
        lo, hi = run[0] + SLOT_L / 2, run[-1] - SLOT_L / 2
        if hi < lo:
            continue
        n = int((hi - lo) // PITCH) + 1
        span = (n - 1) * PITCH
        start = lo + ((hi - lo) - span) / 2
        centres += [start + k * PITCH for k in range(n)]
    slots = []
    for a in centres:
        p, d = point_at(a)
        ang = np.degrees(np.arctan2(d[1], d[0]))
        slots.append(stadium(p[0], p[1], SLOT_L, SLOT_W, ang))
        slots.append(stadium(-p[0], p[1], SLOT_L, SLOT_W, 180 - ang))
    for sl in slots:
        body = body - sl

    part = slab_with_edge_break(body, T)
    # wordmark + a permanent "not a climbing carabiner" warning on the rail
    marks = text("RACKHOUSE", 7.5, 0, 15) + text("NOT FOR CLIMBING", 5, 0, 7)
    wordmark = marks.extrude(2).translate((0, 0, T - 0.8))
    part = part - wordmark

    print_part = part                                  # flat on the bed
    use_part = part.rotate((90, 0, 0))                 # hanging, y -> z
    meta = {"gear_slots": len(slots), "thickness_mm": T}
    return use_part, print_part, meta


# ---------------------------------------------------------------- Rock Ring

def rock_ring():
    """Portable edge lift block. T-profile: grip under either flange
    overhang (19 mm and 11 mm edges), load hangs from a cord or loading pin
    through the channel in the stem."""
    LENGTH = 100.0
    flange = rounded_rect(-28, 40, 28, 58, 5)
    stem = rounded_rect(-9, 0, 17, 44, 4)
    profile = (flange + stem).offset(3).offset(-3)     # 3 mm fillets in the corners
    prism = profile.extrude(LENGTH)
    # (u, v, e) -> (x=e, y=u, z=v)
    body = prism.transform(np.array([[0, 0, 1, -LENGTH / 2],
                                     [1, 0, 0, 0],
                                     [0, 1, 0, 0]], dtype=float))
    # 14 mm loading channel with 45-degree countersinks at both ends, cut as a
    # single revolved tool so the countersink and bore share vertices.
    a = LENGTH / 2
    channel = CS([np.array([(0, -a - 1), (10.6, -a - 1), (7.0, -a + 2.6),
                            (7.0, a - 2.6), (10.6, a + 1), (0, a + 1)], dtype=float)]).revolve()
    body = body - channel.rotate((0, 90, 0)).translate((0, 4, 14))

    marks = (text("RACKHOUSE", 9, 0, 0)
             + text("19", 6, 38, -16)
             + text("11", 6, 38, 16))
    body = body - marks.extrude(2).translate((0, 0, 58 - 0.8))

    use_part = body
    print_part = body.rotate((0, -90, 0))              # stand it on its end
    meta = {"edge_depths_mm": [19, 11], "channel_diameter_mm": 14}
    return use_part, print_part, meta


# --------------------------------------------------------------- Cup Cradle

def cup_cradle():
    """Wide-mouth Nalgene car-cupholder adapter. Tapered, ribbed stem seats
    in roughly 69-79 mm cupholders; 45-degree support-free flare; open cup
    with arch windows and a drain channel down through the stem."""
    outer = polygon([
        (0, 0), (29.3, 0), (30.0, 0.7), (31.0, 62.0), (50.5, 81.5),
        (50.5, 133.0), (49.9, 134.6), (48.8, 135.4), (47.7, 135.4),
        (47.0, 134.6), (47.0, 84.0), (0, 84.0),
    ])
    body = outer.revolve()
    bore = polygon([(0, -1), (25.0, -1), (25.0, 52.0), (0, 77.0)]).revolve()
    body = body - bore
    body = body - M.cylinder(18, 3.5, 3.5).translate((0, 0, 70))      # drain

    rib = polygon([(29.0, 2.0), (31.5, 2.0), (34.5, 10.0), (39.5, 58.0),
                   (39.5, 70.5), (29.0, 70.5)]).extrude(2.0)
    # (u=r, v=z, e=thickness) -> (x=u, y=-e, z=v), centred on y
    rib = rib.transform(np.array([[1, 0, 0, 0],
                                  [0, 0, -1, 1.0],
                                  [0, 1, 0, 0]], dtype=float))
    for k in range(8):
        body = body + rib.rotate((0, 0, 22.5 + 45 * k))

    def radial(cs2d, phi):
        prism = cs2d.extrude(22)
        # (u, v, e) -> (x=e, y=u, z=v), pushed out to the cup wall
        prism = prism.transform(np.array([[0, 0, 1, 40.0],
                                          [1, 0, 0, 0],
                                          [0, 1, 0, 0]], dtype=float))
        return prism.rotate((0, 0, phi))

    arch = rect(-9, 92, 9, 116) + polygon([(-9, 115.9), (9, 115.9), (0, 125)])
    gate = circle(10.5, 0, 107) - rect(-12, 108, 12, 111)
    body = body - radial(gate, 45)
    for phi in (135, 225, 315):
        body = body - radial(arch, phi)

    meta = {"cup_inner_diameter_mm": 94.0, "cupholder_fit_mm": [69, 79]}
    return body, body, meta


# ----------------------------------------------------------------- export

def to_trimesh(part):
    import trimesh
    mesh = part.to_mesh()
    verts = np.asarray(mesh.vert_properties)[:, :3]
    faces = np.asarray(mesh.tri_verts)
    # process=False: manifold3d output is already a closed, exactly-indexed mesh;
    # trimesh tolerance-merging would weld distinct vertices on fine text detail.
    return trimesh.Trimesh(verts, faces, process=False)


def on_bed(part):
    (x0, y0, z0, x1, y1, z1) = part.bounding_box()
    return part.translate((-(x0 + x1) / 2, -(y0 + y1) / 2, -z0))


def build():
    os.makedirs(os.path.join(ROOT, "models"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "print-ready"), exist_ok=True)
    report = {}
    for name, fn in (("gatekeeper", gatekeeper), ("rock-ring", rock_ring), ("cup-cradle", cup_cradle)):
        use_part, print_part, meta = fn()
        # collapse sub-micron sliver edges left by booleans so the mesh stays
        # manifold after the float32 rounding every STL file applies
        use_part = use_part.simplify(0.001)
        print_part = on_bed(print_part.simplify(0.001))
        for part, path in ((use_part, os.path.join(ROOT, "models", f"{name}.stl")),
                           (print_part, os.path.join(HERE, "print-ready", f"rackhouse-{name}.stl"))):
            tm = to_trimesh(part)
            tm.export(path)
        tm = to_trimesh(print_part)
        bb = print_part.bounding_box()
        vol_cm3 = print_part.volume() / 1000.0
        report[name] = {
            "status": str(print_part.status()),
            "watertight": bool(tm.is_watertight),
            "winding_consistent": bool(tm.is_winding_consistent),
            "bodies": len(tm.split(only_watertight=False)),
            "print_bbox_mm": [round(bb[3] - bb[0], 1), round(bb[4] - bb[1], 1), round(bb[5] - bb[2], 1)],
            "solid_volume_cm3": round(vol_cm3, 1),
            "pla_mass_100pct_g": round(vol_cm3 * 1.24, 0),
            "triangles": int(print_part.num_tri()),
            **meta,
        }
    with open(os.path.join(HERE, "build-report.json"), "w") as f:
        json.dump(report, f, indent=2)
    print(json.dumps(report, indent=2))
    return report


if __name__ == "__main__":
    build()
