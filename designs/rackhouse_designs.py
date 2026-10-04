"""Rackhouse product designs — original parametric source.

Every product here is modeled from functional requirements (bottle and
cupholder diameters, carabiner gate openings and clearances, rack sizes,
print-bed size), not derived from any third-party model. Run this file to
rebuild every STL:

    pip install manifold3d trimesh networkx matplotlib
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
    first-layer squish so edges stay crisp). The pieces overlap by 0.2 mm so
    the union fuses into one solid instead of three face-touching ones."""
    inset = shape.offset(-brk)
    return (inset.extrude(brk + 0.2)
            + shape.extrude(thickness - 2 * brk).translate((0, 0, brk))
            + inset.extrude(brk + 0.2).translate((0, 0, thickness - brk - 0.2)))


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

def keyhole(cx, cy, head_r=5.5, shank_w=5.6, travel=10.0):
    """Keyhole through the front plate: drop the screw head through the round
    hole, then let the part slide down so the shank rides up the slot."""
    return circle(head_r, cx, cy) + stadium(cx, cy + travel / 2.0, travel + shank_w, shank_w, 90)


def keyhole_pocket(cx, cy, head_r=5.5, head_channel=11.0, travel=10.0):
    """Clearance behind the keyhole (inside the standoff) for the screw head."""
    return circle(head_r, cx, cy) + stadium(cx, cy + travel / 2.0, travel + head_channel, head_channel, 90)


def assert_inside(feature, region, margin, label):
    """Fail the build if `feature` comes closer than `margin` mm to the edge
    of `region` (used to keep debossed text off thin edges)."""
    spill = feature.offset(margin) - region
    if spill.area() > 1e-3:
        raise ValueError(f"{label}: {spill.area():.2f} mm^2 within {margin} mm of an edge")


def rock_ring():
    """Full-rack gear ring + helmet hook. You clip carabiners straight onto
    the ring band like racking on a gear sling; 15 numbered notches on the
    inner edge keep each piece in its own spot instead of sliding to the
    bottom. A coat-hook style horn inside the top holds a helmet by its chin
    strap. Hangs on one screw through a keyhole; three standoff feet hold it
    12 mm off the wall so carabiners can wrap behind the band."""
    T = 14.0            # band thickness (front to back)
    STANDOFF = 12.0     # clearance behind the band for carabiners
    R_IN, R_OUT = 72.0, 92.0
    N_POS, PITCH_DEG = 15, 18.0
    NOTCH_R = 6.0       # notch depth into the inner edge

    ring = circle(R_OUT) - circle(R_IN)
    tab = CS.batch_hull([circle(16, 0, 98), rect(-34, 80, 34, 86)])
    # helmet horn: stem down from the top inner edge, curling up into a hook
    # 10 mm wide stem and curl, 13 mm throat, rounded tip
    stem = rect(-5, 48, 5, 76)
    curl = (circle(16.5, 11.5, 48) - circle(6.5, 11.5, 48)) ^ rect(-6, 25, 30, 48)
    tip = stadium(23, 53, 20, 10, 90)
    horn = stem + curl + tip
    outline = ring + tab + horn

    # numbered rack positions, evenly spaced around the bottom (0 deg = straight down)
    angles = [(k - (N_POS - 1) / 2.0) * PITCH_DEG for k in range(N_POS)]
    body = outline
    labels = None
    for i, a in enumerate(angles):
        ar = np.radians(a)
        ux, uy = np.sin(ar), -np.cos(ar)
        body = body - circle(NOTCH_R, R_IN * ux, R_IN * uy)
        lab = text(str(i + 1), 5.0, 86.5 * ux, 86.5 * uy)
        labels = lab if labels is None else labels + lab

    hole = keyhole(0, 96)
    body = body - hole
    band_text = text("RACKHOUSE", 5.2, 0, 83.5) + text("NOT FOR CLIMBING", 3.6, 0, 76.6)

    # every label must sit on solid band with margin (not over a notch or edge)
    assert_inside(labels, body, 1.2, "rack numbers")
    assert_inside(band_text, body, 1.0, "band text")

    front = slab_with_edge_break(body, T)
    front = front - (labels + band_text).extrude(2).translate((0, 0, T - 0.8))

    # standoff feet on the back: one around the keyhole, two on the lower band
    # (at +/-45 deg, midway between rack positions so carabiners clear them)
    feet = circle(13, 0, 97) ^ (outline - hole)
    feet = feet - keyhole_pocket(0, 96)
    for a in (-45.0, 45.0):
        ar = np.radians(a)
        feet = feet + circle(6.0, 82 * np.sin(ar), -82 * np.cos(ar))
    for a in (-45.0, 45.0):
        assert min(abs(a - p) for p in angles) >= PITCH_DEG / 2 - 1e-6
    back = feet.offset(-0.6).extrude(0.8).translate((0, 0, -STANDOFF)) + feet.extrude(STANDOFF - 0.6 + 0.2).translate((0, 0, -STANDOFF + 0.6))
    part = front + back                                 # front face at z=T, wall side at z=-STANDOFF

    use_part = part.rotate((90, 0, 0))                  # on the wall: y -> up, front faces -y
    print_part = part.rotate((0, 180, 0))               # face down: smooth front, feet on top, no supports
    meta = {"rack_positions": N_POS, "band_mm": [R_OUT - R_IN, T], "band_at_notch_mm": [R_OUT - R_IN - NOTCH_R, T],
            "standoff_mm": STANDOFF, "outer_diameter_mm": 2 * R_OUT}
    return use_part, print_part, meta


# ----------------------------------------------------------------- Draw Bar

def draw_bar():
    """Straight wall rail for quickdraws and extra gear. Seven slots; clip a
    carabiner through a slot and around the 11 mm bottom rail. Two keyholes
    in end standoffs hold it 12 mm off the wall."""
    L, H, T, STANDOFF = 200.0, 44.0, 8.0, 12.0
    N_SLOTS, PITCH = 7, 22.0
    plate = rounded_rect(-L / 2, 0, L / 2, H, 6)
    slots = None
    for k in range(N_SLOTS):
        x = (k - (N_SLOTS - 1) / 2.0) * PITCH
        sl = stadium(x, 22, 22, 13, 90)
        slots = sl if slots is None else slots + sl
    holes = keyhole(-88, 14) + keyhole(88, 14)
    body = plate - slots - holes
    label = text("RACKHOUSE  ·  NOT FOR CLIMBING", 4.4, 0, 38.6)
    assert_inside(label, body, 1.2, "draw bar text")

    front = slab_with_edge_break(body, T) - label.extrude(2).translate((0, 0, T - 0.8))
    ends = rounded_rect(-L / 2, 0, -L / 2 + 24, H, 6) + rounded_rect(L / 2 - 24, 0, L / 2, H, 6)
    ends = ends - keyhole_pocket(-88, 14) - keyhole_pocket(88, 14)
    back = ends.offset(-0.6).extrude(0.8).translate((0, 0, -STANDOFF)) + ends.extrude(STANDOFF - 0.6 + 0.2).translate((0, 0, -STANDOFF + 0.6))
    part = front + back

    use_part = part.rotate((90, 0, 0))
    print_part = part.rotate((0, 180, 0))
    meta = {"slots": N_SLOTS, "slot_mm": [13, 22], "slot_pitch_mm": PITCH, "rail_mm": [11, T],
            "standoff_mm": STANDOFF, "length_mm": L}
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


def stl_roundtrip_ok(path):
    """Reload the exported STL the way a slicer does (merging coincident
    float32 vertices) and confirm it is still one closed solid."""
    import trimesh
    t = trimesh.load(path)
    return bool(t.is_watertight and len(t.split(only_watertight=False)) == 1)


def on_bed(part):
    (x0, y0, z0, x1, y1, z1) = part.bounding_box()
    return part.translate((-(x0 + x1) / 2, -(y0 + y1) / 2, -z0))


def build():
    os.makedirs(os.path.join(ROOT, "models"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "print-ready"), exist_ok=True)
    report = {}
    for name, fn in (("gatekeeper", gatekeeper), ("rock-ring", rock_ring), ("draw-bar", draw_bar), ("cup-cradle", cup_cradle)):
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
            "stl_roundtrip_watertight": stl_roundtrip_ok(os.path.join(HERE, "print-ready", f"rackhouse-{name}.stl")),
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
