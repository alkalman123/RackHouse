"""Rackhouse production designs: the seven carabiner organizers picked from
round-2 prototypes (designs/prototypes2.py), with the brand and the
NOT FOR CLIMBING warning debossed in place of the prototype ID.

    python3 designs/products.py

Writes, for each product id:
    models/<id>.stl                       hanging orientation (site 3D viewer, renders)
    designs/print-ready/rackhouse-<id>.stl print orientation, flat on the bed
and designs/products-report.json with every check, the size, an estimated
printed weight, and the clip openings (position + the direction a
carabiner hangs from each) that the gear renders use.
"""

import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import prototypes2 as P
from rackhouse_designs import to_trimesh, on_bed, stl_roundtrip_ok

NFC = "RACKHOUSE  ·  NOT FOR CLIMBING"

# id: (prototype, product name, marks, hook/peg centres for the renders: 4.5 mm
#      below the top of each hang hole, so a 4 mm peg sits in it)
CATALOG = {
    "gear-board": (P.b20, "The Gear Board", [(NFC, 4.4, 0, 158)], [(-80, 162 - 4.5), (80, 162 - 4.5)]),
    "crag-ring": (P.r20, "The Crag Ring", [("RACKHOUSE", 5.0, 0, 65), ("NOT FOR CLIMBING", 3.4, 0, 57.5)], [(0, 104 - 4.5)]),
    "rock-ring": (P.r12, "The Rock Ring", [("RACKHOUSE", 5.2, 0, 75), ("NOT FOR CLIMBING", 3.6, 0, 66.5)], [(0, 106 - 4.5)]),
    "double-ring": (P.r15, "The Double Ring", [("RACKHOUSE", 5.2, 0, 78), ("NOT FOR CLIMBING", 3.6, 0, 69.5)], [(0, 108 - 4.5)]),
    "sport-board": (P.b12, "The Sport Board", [(NFC, 3.6, 0, 92.6)], [(-86, 60.5 - 4.5), (86, 60.5 - 4.5)]),
    "approach-bar": (P.b18, "The Approach Bar", [(NFC, 3.8, 0, 35.2)], [(-86, 32 - 4.5), (86, 32 - 4.5)]),
    "pocket-bar": (P.b14, "The Pocket Bar", [(NFC, 3.0, 0, 39.0)], [(-51, 34 - 4.5), (51, 34 - 4.5)]),
}


def hang_direction(cs, pt):
    """Unit vector (in the plate plane, y up) from a clip opening toward the
    web a hanging carabiner rests on. Of the clippable webs (to the outside
    edge or a large window, at most WEB_MAX wide), gravity picks the one
    pointing most downward: the carabiner sits on that web and hangs from it."""
    polys = cs.to_polygons()
    areas = [P._signed_area(p) for p in polys]
    outer_sign = np.sign(areas[int(np.argmax(np.abs(areas)))])
    dense = [P._densify(p, 0.5) for p in polys]
    cands = [i for i, p in enumerate(polys) if np.sign(areas[i]) != outer_sign and P._point_in_poly(pt, p)]
    hi = min(cands, key=lambda i: abs(areas[i]))
    h = dense[hi]
    options = []
    for j in range(len(polys)):
        if j == hi:
            continue
        if not (np.sign(areas[j]) == outer_sign or abs(areas[j]) > P.MAX_OPENING_AREA):
            continue
        d = np.sqrt(((h[:, None, :] - dense[j][None, :, :]) ** 2).sum(-1))
        # every point of this boundary within clip reach of the opening
        for k in np.argwhere(d <= P.WEB_MAX + 0.5):
            v = dense[j][k[1]] - np.asarray(pt)
            options.append(v / np.linalg.norm(v))
    if not options:
        raise SystemExit(f"no clippable web next to {pt}")
    best = min(options, key=lambda v: v[1])          # most downward
    return [float(best[0]), float(best[1])]


def estimate_grams(stl_path):
    """Printed weight at 4 walls (~1.6 mm shell) + 30% gyroid, PLA+ 1.24 g/cm3."""
    import trimesh
    t = trimesh.load(stl_path)
    V, A = t.volume / 1000.0, t.area / 100.0
    shell = min(V, A * 0.16)
    return round((shell + (V - shell) * 0.30) * 1.24)


def build():
    report = {}
    for pid, (fn, title, marks, hangs) in CATALOG.items():
        p = fn()
        use_part, print_part = p.build(marks=marks)
        webs = P.check_clip_openings(p.cs, p.clip_points)
        use_part = use_part.simplify(0.001)
        print_part = on_bed(print_part.simplify(0.001))
        model = os.path.join(ROOT, "models", f"{pid}.stl")
        stl = os.path.join(HERE, "print-ready", f"rackhouse-{pid}.stl")
        to_trimesh(use_part).export(model)
        to_trimesh(print_part).export(stl)
        bb = print_part.bounding_box()
        size = [round(bb[3] - bb[0], 1), round(bb[4] - bb[1], 1), round(bb[5] - bb[2], 1)]
        checks = {
            "single_solid": len(print_part.decompose()) == 1,
            "stl_roundtrip_watertight": stl_roundtrip_ok(stl),
            "fits_210_bed": max(size[0], size[1]) <= P.MAX_BED,
            "clip_openings_enclosed_and_clippable": True,   # check_clip_openings raises otherwise
        }
        if not all(checks.values()):
            raise SystemExit(f"{pid} failed {checks}")
        clips = [{"xy": [round(float(x), 2), round(float(y), 2)], "dir": hang_direction(p.cs, (x, y))}
                 for (x, y) in p.clip_points]
        report[pid] = {
            "title": title, "prototype": p.pid, "summary": p.summary, "hang": p.hang, "notes": p.notes,
            "size_mm": size, "thickness_mm": p.T, "openings": len(p.clip_points),
            "clip_web_mm": [min(webs), max(webs)], "est_weight_g": estimate_grams(stl),
            "hang_points": hangs, "clips": clips, **checks,
        }
        print(pid, p.pid, size, len(clips), "openings", report[pid]["est_weight_g"], "g")
    with open(os.path.join(HERE, "products-report.json"), "w") as f:
        json.dump(report, f, indent=2)
    return report


if __name__ == "__main__":
    build()
