"""Rackhouse prototypes, round 2: R11-R20 (following R05) and B11-B20
(following B06).

Rule for every part: each clip point is a FULLY ENCLOSED opening (a loop,
window, slot or box), so a clipped carabiner can't fall off in any
direction, whether it's in a closet, in the car, in a pack or at the crag.

Parts are flat, rounded plates with no wall posts (nothing to snag in a
pack). Each one hangs from its own enclosed hang loop: a closet hook, a
car grab handle or headrest, a pack haul loop or an anchor sling.

The build checks, for every declared clip opening:
  * it is a closed hole in the part (not an open hook or notch);
  * it is at least 14 mm across everywhere, so carabiner wire passes;
  * the narrowest web of material next to it, the part the carabiner
    closes around, is 5-12 mm wide (strong enough, and thin enough to clip);
plus single solid, STL round-trip and 210 mm bed fit.

    python3 designs/prototypes2.py
"""

import json
import os
import sys

import numpy as np
from manifold3d import CrossSection as CS

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rackhouse_designs import (circle, rect, rounded_rect, stadium, text, slab_with_edge_break,
                               assert_inside, to_trimesh, on_bed, stl_roundtrip_ok)

OUT = os.path.join(HERE, "prototypes2")
MIN_HOLE = 14.0
WEB_MIN, WEB_MAX = 5.0, 12.0
MAX_OPENING_AREA = 600.0   # mm^2: a clip opening merged into a neighbour fails
MAX_BED = 210.0


# ------------------------------------------------------------- geometry kit

def polar(r, a_deg):
    """Angle measured from straight down (0) toward +x."""
    a = np.radians(a_deg)
    return r * np.sin(a), -r * np.cos(a)


def annulus(r_in, r_out, cx=0.0, cy=0.0):
    return circle(r_out, cx, cy) - circle(r_in, cx, cy)


def hang_loop(cy, hole_r=12.0, web=9.0):
    """Enclosed hang loop at the top: a round eye big enough for a hook,
    a carabiner or a sling."""
    return circle(hole_r + web, 0, cy), circle(hole_r, 0, cy)


def window(cx, cy, along, across, angle_deg):
    """Rounded slot: `along` is its long dimension, at angle_deg."""
    return stadium(cx, cy, along, across, angle_deg)


def d_loop(cx, cy, a_deg, w=26.0, h=33.0, hole_w=15.0, hole_h=16.0, web=8.0):
    """Closed loop sticking out from (cx, cy) in direction a_deg (0 = down).
    The clip bar at the far end is `web` mm thick."""
    outer = rounded_rect(-w / 2, -h, w / 2, 3, 6)
    hole = rounded_rect(-hole_w / 2, -h + web, hole_w / 2, -h + web + hole_h, 5)
    return outer.rotate(a_deg).translate((cx, cy)), hole.rotate(a_deg).translate((cx, cy)), \
        polar(h - web - hole_h / 2, a_deg)


class Proto:
    def __init__(self, pid, name, summary, solid, holes, clip_points, T=9.0, label_xy=(0, 0),
                 label_size=6.0, hang="", notes=""):
        self.pid, self.name, self.summary = pid, name, summary
        self.solid, self.holes, self.clip_points = solid, holes, clip_points
        self.T, self.label_xy, self.label_size, self.hang, self.notes = T, label_xy, label_size, hang, notes

    def outline(self):
        return self.solid - self.holes

    def build(self, marks=None):
        """marks: optional list of (text, size, x, y) debossed instead of the
        prototype ID (the production versions carry the brand and warning)."""
        cs = self.outline()
        if marks:
            label = None
            for txt, size, x, y in marks:
                t = text(txt, size, x, y)
                label = t if label is None else label + t
        else:
            label = text(self.pid, self.label_size, *self.label_xy)
        assert_inside(label, cs, 1.0, f"{self.pid} label")
        part = slab_with_edge_break(cs, self.T) - label.extrude(2).translate((0, 0, self.T - 0.8))
        self.cs = cs
        return part.rotate((90, 0, 0)), part            # use (hanging), print (flat, label up)


# -------------------------------------------------------------- the checks

def _point_in_poly(pt, poly):
    x, y = pt
    inside = False
    n = len(poly)
    for i in range(n):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % n]
        if (y0 > y) != (y1 > y) and x < (x1 - x0) * (y - y0) / (y1 - y0) + x0:
            inside = not inside
    return inside


def _signed_area(poly):
    p = np.asarray(poly)
    return 0.5 * np.sum(p[:, 0] * np.roll(p[:, 1], -1) - np.roll(p[:, 0], -1) * p[:, 1])


def _densify(poly, step=0.8):
    p = np.asarray(poly)
    out = []
    for i in range(len(p)):
        a, b = p[i], p[(i + 1) % len(p)]
        n = max(1, int(np.ceil(np.linalg.norm(b - a) / step)))
        for k in range(n):
            out.append(a + (b - a) * k / n)
    return np.array(out)


def check_clip_openings(cs, clip_points):
    """For every clip opening: it must be a separate closed hole at least
    MIN_HOLE wide; every web around it must be >= WEB_MIN (strength); and
    the web a carabiner actually closes around (from the opening to the
    outside edge or to a large open area, NOT to another clip opening)
    must be <= WEB_MAX. Returns the wrap webs; raises on failure."""
    polys = cs.to_polygons()
    areas = [_signed_area(p) for p in polys]
    outer_sign = np.sign(areas[int(np.argmax(np.abs(areas)))])
    results = []
    dense = [_densify(p) for p in polys]
    for pt in clip_points:
        # the opening is the smallest hole polygon containing the clip point
        cands = [i for i, p in enumerate(polys) if np.sign(areas[i]) != outer_sign and _point_in_poly(pt, p)]
        if not cands:
            raise SystemExit(f"clip point {pt} is not inside an enclosed opening")
        hi = min(cands, key=lambda i: abs(areas[i]))
        hole_cs = CS([np.asarray(polys[hi])[::-1] if areas[hi] < 0 else np.asarray(polys[hi])])
        wide_enough = hole_cs.offset(-MIN_HOLE / 2 + 0.05).area() > 0
        h = dense[hi]

        def min_dist(idx):
            pts_ = np.vstack([dense[j] for j in idx])
            return float(np.sqrt(((h[:, None, :] - pts_[None, :, :]) ** 2).sum(-1).min()))

        any_web = min_dist([j for j in range(len(polys)) if j != hi])
        free = [j for j in range(len(polys)) if j != hi and
                (np.sign(areas[j]) == outer_sign or abs(areas[j]) > MAX_OPENING_AREA)]
        wrap = min_dist(free)
        separate = abs(areas[hi]) <= MAX_OPENING_AREA
        if (not wide_enough or not separate or any_web < WEB_MIN - 0.05
                or not (WEB_MIN - 0.05 <= wrap <= WEB_MAX + 0.05)):
            raise SystemExit(f"opening at {pt}: wide_enough={wide_enough} separate={separate} "
                             f"(area {abs(areas[hi]):.0f}) min web={any_web:.1f} wrap web={wrap:.1f}")
        results.append(round(wrap, 1))
    return results


# ------------------------------------------------------- ring line (R05 ->)

def loop_ring(pid, name, summary, R, band, angles, loop_kw=None, hang_y=None, T=9.0, extra=None):
    loop_kw = loop_kw or {}
    solid = annulus(R - band / 2, R + band / 2)
    holes = None
    pts = []
    for a in angles:
        o, h, _ = d_loop(*polar(R + band / 2 - 2, a), a, **loop_kw)
        solid = solid + o
        holes = h if holes is None else holes + h
        lw = loop_kw.get("h", 33.0)
        web = loop_kw.get("web", 8.0)
        hh = loop_kw.get("hole_h", 16.0)
        pts.append(polar(R + band / 2 - 2 + lw - web - hh / 2, a))
    hy = hang_y if hang_y is not None else R + band / 2 + 10
    ho, hh_ = hang_loop(hy)
    solid = solid + ho + rect(-14, R, 14, hy)
    holes = holes + hh_
    if extra:
        s2, h2, p2 = extra
        solid = solid + s2
        if h2 is not None:
            holes = holes + h2
        pts += p2
    return Proto(pid, name, summary, solid, holes, pts, T=T, label_xy=(0, -R), label_size=5.0,
                 hang="Top eye: hook, carabiner or sling")


def r11():
    return loop_ring("R11", "full-loop-ring", "R05 all the way around: 10 closed loops, a top eye to hang it anywhere. No wall posts.",
                     62.0, 14.0, [-135, -105, -75, -45, -15, 15, 45, 75, 105, 135])


def window_ring(pid, name, summary, r_in, r_out, n, skip_top=40.0, hang=True, T=9.0, web=8.0, across=16.0,
                along=22.0, extra=None, inner_row=None, label_y=None):
    solid = annulus(r_in, r_out)
    holes = None
    pts = []
    r_w = r_out - web - across / 2
    angles = np.linspace(-180 + skip_top, 180 - skip_top, n)
    for a in angles:
        x, y = polar(r_w, a)
        tang = np.degrees(np.arctan2(*polar(1, a)[::-1])) + 90
        wdw = window(x, y, along, across, tang)
        holes = wdw if holes is None else holes + wdw
        pts.append((x, y))
    if inner_row:
        n2, r2 = inner_row
        for a in np.linspace(-180 + skip_top + 10, 180 - skip_top - 10, n2):
            x, y = polar(r2, a)
            tang = np.degrees(np.arctan2(*polar(1, a)[::-1])) + 90
            holes = holes + window(x, y, along, across, tang)
            pts.append((x, y))
    if hang:
        ho, hh = hang_loop(r_out + 6)
        solid = solid + ho + rect(-14, r_out - 6, 14, r_out + 6)
        holes = holes + hh
    if extra:
        s2, h2, p2 = extra
        solid = solid + s2
        if h2 is not None:
            holes = holes + h2
        pts += p2
    ly = label_y if label_y is not None else (r_in + r_out) / 2
    return Proto(pid, name, summary, solid, holes, pts, T=T, label_xy=(0, ly),
                 hang="Top eye: hook, carabiner or sling")


def r12():
    return window_ring("R12", "window-ring", "A wide flat ring with 13 closed windows punched through it: nothing sticks out, so it packs flat and won't snag.",
                       56.0, 88.0, 13)


def r13():
    return loop_ring("R13", "compact-loop-ring", "Pack-size R05: 140 mm across with 8 closed loops. Fits in a pack lid or a door pocket.",
                     46.0, 12.0, [-135, -100, -65, -30, 30, 65, 100, 135],
                     loop_kw=dict(w=24, h=30, hole_w=14, hole_h=15, web=8))


def r14():
    # "box" ring: a rounded-square frame with square boxes around it
    S, band = 64.0, 14.0
    solid = rounded_rect(-S - band / 2, -S - band / 2, S + band / 2, S + band / 2, 18) - rounded_rect(
        -S + band / 2, -S + band / 2, S - band / 2, S - band / 2, 12)
    holes = None
    pts = []
    spots = [(x, -S - band / 2 + 2, 0) for x in (-48, -16, 16, 48)] + \
            [(-S - band / 2 + 2, y, -90) for y in (-36, -4, 28)] + [(S + band / 2 - 2, y, 90) for y in (-36, -4, 28)]
    for x, y, a in spots:
        o, h, _ = d_loop(x, y, a, 26, 30, 16, 16, 8)
        solid = solid + o
        holes = h if holes is None else holes + h
        pts.append((x + polar(30 - 8 - 8, a)[0], y + polar(30 - 8 - 8, a)[1]))
    ho, hh = hang_loop(S + band / 2 + 12)
    solid = solid + ho + rect(-14, S, 14, S + band / 2 + 12)
    holes = holes + hh
    return Proto("R14", "box-ring", "A rounded-square frame with 10 square boxes around three sides: the \"box\" version of R05.",
                 solid, holes, pts, label_xy=(0, S - 2), hang="Top eye: hook, carabiner or sling")


def r15():
    return window_ring("R15", "double-window-ring", "Two rows of closed windows: 13 on the outside for cams, 7 on the inside for nuts and draws.",
                       38.0, 90.0, 13, inner_row=(7, 52.0), label_y=70.0)


def r16():
    # window ring with a big enclosed helmet loop hanging below
    r_in, r_out = 36.0, 66.0
    helmet_solid = rounded_rect(-34, -r_out - 46, 34, -r_out + 4, 16)
    helmet_hole = rounded_rect(-24, -r_out - 36, 24, -r_out - 10, 10)
    p = window_ring("R16", "ring-helmet-loop", "Window ring with a big closed helmet loop underneath: thread the chin strap through, and the helmet hangs below the rack.",
                    r_in, r_out, 9, skip_top=40, extra=(helmet_solid, helmet_hole, []))
    p.notes = "Helmet loop opening 48 x 26 mm: unbuckle the chin strap, thread it through, buckle."
    return p


def r17():
    # loop ring with a horizontal cross brace for a heavy rack
    R, band = 62.0, 14.0
    brace = rect(-R, -6, R, 6)
    return loop_ring("R17", "braced-loop-ring", "R11 with a cross brace through the middle so it stays round under a heavy double rack.",
                     R, band, [-135, -105, -75, -45, -15, 15, 45, 75, 105, 135], extra=(brace, None, []))


def r18():
    # octagon frame with windows on each flat side
    r_out, band = 92.0, 34.0
    oct_out = CS([np.array([polar(r_out, 22.5 + 45 * k) for k in range(8)])])
    oct_in = CS([np.array([polar(r_out - band, 22.5 + 45 * k) for k in range(8)])])
    solid = oct_out.offset(-6).offset(6) - oct_in.offset(-6).offset(6)
    apothem = r_out * np.cos(np.radians(22.5))
    holes = None
    pts = []
    for k in range(8):
        a = 45 * k
        if a == 180:
            continue
        for off in (-13, 13):
            cx, cy = polar(apothem - 8 - 7.5, a)
            tx, ty = np.cos(np.radians(a)), np.sin(np.radians(a))
            x, y = cx + off * tx, cy + off * ty
            wdw = window(x, y, 18, 15, a)
            holes = wdw if holes is None else holes + wdw
            pts.append((x, y))
    ho, hh = hang_loop(apothem + 10)
    solid = solid + ho + rect(-14, apothem - 8, 14, apothem + 10)
    holes = holes + hh
    return Proto("R18", "octagon-ring", "Octagon frame with two closed windows on each of seven flat sides: 14 spots that sit flat on a shelf too.",
                 solid, holes, pts, label_xy=(0, apothem - 15), hang="Top eye: hook, carabiner or sling")


def r19():
    # racetrack with windows, flat bottom row
    half, r_in, r_out = 40.0, 32.0, 62.0
    outer = CS.batch_hull([circle(r_out, -half, 0), circle(r_out, half, 0)])
    inner = CS.batch_hull([circle(r_in, -half, 0), circle(r_in, half, 0)])
    solid = outer - inner
    rw = r_out - 8 - 8
    holes = None
    pts = []
    for x in (-28, 0, 28):
        wdw = window(x, -rw, 22, 16, 0)
        holes = wdw if holes is None else holes + wdw
        pts.append((x, -rw))
    for cx, sgn in ((-half, -1), (half, 1)):
        for a in (55, 95, 135):
            x, y = polar(rw, sgn * a)
            tang = np.degrees(np.arctan2(*polar(1, sgn * a)[::-1])) + 90
            holes = holes + window(cx + x, y, 22, 16, tang)
            pts.append((cx + x, y))
    ho, hh = hang_loop(r_out + 10)
    solid = solid + ho + rect(-14, r_out - 6, 14, r_out + 10)
    holes = holes + hh
    return Proto("R19", "racetrack-window-ring", "Stretched ring with a flat bottom: 3 windows in a straight row plus 3 up each side, 9 in all.",
                 solid, holes, pts, label_xy=(0, (r_in + r_out) / 2), hang="Top eye: hook, carabiner or sling")


def r20():
    # light crag ring with a hand-carry handle
    r_in, r_out = 46.0, 76.0
    handle_solid = rounded_rect(-48, r_out - 10, 48, r_out + 38, 18)
    handle_hole = rounded_rect(-38, r_out + 2, 38, r_out + 28, 12)
    p = window_ring("R20", "crag-carry-ring", "Light 7 mm crag ring with a hand-size carry handle on top: grab it like a bag, or clip the handle to a sling.",
                    r_in, r_out, 11, skip_top=48, hang=False, T=7.0, extra=(handle_solid, handle_hole, []), label_y=63)
    p.hang = "Hand-carry handle (76 x 26 mm opening); also clips to a sling or hook"
    return p


# ------------------------------------------------------- bar line (B06 ->)

def slot_plate(pid, name, summary, L=200.0, H=46.0, n=7, slot=(15.0, 24.0), bottom_web=9.0, T=9.0,
               end_holes=True, extra=None, label_xy=None, x_range=None, angle=90.0):
    solid = rounded_rect(-L / 2, 0, L / 2, H, 8)
    holes = None
    pts = []
    x0, x1 = x_range if x_range else (-L / 2 + 34, L / 2 - 34)
    y = bottom_web + slot[1] / 2
    for x in np.linspace(x0, x1, n):
        s = window(x, y, slot[1], slot[0], angle)
        holes = s if holes is None else holes + s
        pts.append((x, y))
    if end_holes:
        for ex in (-L / 2 + 14, L / 2 - 14):
            holes = holes + window(ex, H / 2, 24, 12, 90)
    if extra:
        s2, h2, p2 = extra
        solid = solid + s2
        if h2 is not None:
            holes = holes + h2
        pts += p2
    lx, ly = label_xy if label_xy else (0, (bottom_web + slot[1] + H) / 2 + 0.5)
    return Proto(pid, name, summary, solid, holes, pts, T=T, label_xy=(lx, ly), label_size=5.5,
                 hang="End slots: two hooks, two screws with washers, or a sling through both")


def b11():
    return slot_plate("B11", "portable-slot-plate", "B06 made portable: same closed slots, no wall posts, rounded all over; hangs from both end slots.")


def b12():
    # bottom row wraps the bottom edge; top row wraps the strip above a long
    # window, so its carabiners hang down through the window, clear of row 1
    L, H = 200.0, 97.0
    solid = rounded_rect(-L / 2, 0, L / 2, H, 8)
    holes = None
    pts = []
    for x in np.linspace(-66, 66, 7):
        holes = (window(x, 9 + 12, 24, 15, 90) if holes is None else holes + window(x, 9 + 12, 24, 15, 90))
        pts.append((x, 21))
    holes = holes + rounded_rect(-72, 39, 72, 55, 7)          # long window, 16 mm tall
    for x in np.linspace(-55, 55, 6):
        holes = holes + window(x, 64 + 12, 24, 15, 90)
        pts.append((x, 76))
    for ex in (-86, 86):
        holes = holes + window(ex, H / 2, 24, 12, 90)
    return Proto("B12", "two-row-slot-plate", "Two rows of closed slots: 7 below for quickdraws, 6 above whose carabiners hang down through a long window, so the rows never tangle.",
                 solid, holes, pts, label_xy=(-86, 84), label_size=4.6,
                 hang="End slots: two hooks, two screws with washers, or a sling through both")


def b13():
    L, H = 200.0, 84.0
    grip_hole = rounded_rect(-48, 48, 48, 74, 12)      # 96 x 26 mm: room for four fingers
    p = slot_plate("B13", "carry-handle-bar", "Slot plate with a hand-grip cut-out on top: carry your whole sport rack to the crag like a toolbox.",
                   L=L, H=H, n=7, end_holes=False, extra=(rect(0, 0, 0.01, 0.01), grip_hole, []), label_xy=(0, 42.5))
    p.hang = "Hand grip (96 x 26 mm), which also hangs on a hook or clips to a sling"
    return p


def b14():
    return slot_plate("B14", "pocket-bar", "130 mm pocket version with 4 slots: fits a pack lid, a glovebox or a crag bag.",
                      L=130.0, H=44.0, n=4, x_range=(-30, 30), label_xy=(0, 39.0))


def b15():
    L, H = 200.0, 46.0
    helmet_solid = rounded_rect(L / 2 - 70, 0, L / 2, H + 26, 12)
    helmet_hole = rounded_rect(L / 2 - 60, 10, L / 2 - 10, H + 16, 10)
    p = slot_plate("B15", "bar-helmet-loop", "Five closed slots plus a big closed helmet loop at the end: rack and helmet on one bar.",
                   L=L, H=H, n=5, x_range=(-62, 26), end_holes=False, extra=(helmet_solid, helmet_hole, []),
                   label_xy=(-24, 40.0))
    p.solid = p.solid + rounded_rect(-L / 2, 0, -L / 2 + 30, H, 8)
    p.holes = p.holes + window(-L / 2 + 14, H / 2, 24, 12, 90)
    p.hang = "Left end slot plus the helmet loop's top bar"
    p.notes = "Helmet loop opening 50 x 52 mm: unbuckle the chin strap, thread it through, buckle."
    return p


def b16():
    L, H = 200.0, 44.0
    solid = rounded_rect(-L / 2, 0, L / 2, H, 8)
    holes = None
    pts = []
    for x in np.linspace(-66, 66, 7):
        b = rounded_rect(x - 8, 9, x + 8, 31, 4)
        holes = b if holes is None else holes + b
        pts.append((x, 20))
    for ex in (-86, 86):
        holes = holes + window(ex, H / 2, 24, 12, 90)
    return Proto("B16", "box-ladder", "Ladder of square boxes between two rails: lighter than the plate, same closed openings.",
                 solid, holes, pts, label_xy=(0, 37.5), label_size=5.5,
                 hang="End slots: two hooks, two screws with washers, or a sling through both")


def b17():
    # curved bar: an arc of a 260 mm radius ring
    R0, Rin, Rout = 260.0, 236.0, 282.0
    span = 43.0          # outer chord 2*282*sin(21.5 deg) = 207 mm
    ring = annulus(Rin, Rout, 0, R0)
    wedge = CS([np.array([(0, R0)] + [(R0 * 1.3 * np.sin(np.radians(a)), R0 - R0 * 1.3 * np.cos(np.radians(a)))
                                       for a in np.linspace(-span / 2, span / 2, 40)])])
    solid = (ring ^ wedge).offset(-6).offset(6)
    holes = None
    pts = []
    for a in np.linspace(-14, 14, 7):
        x, y = R0 * 0 + (Rout - 9 - 12) * np.sin(np.radians(a)), R0 - (Rout - 9 - 12) * np.cos(np.radians(a))
        holes = (window(x, y, 24, 15, 90 + a) if holes is None else holes + window(x, y, 24, 15, 90 + a))
        pts.append((x, y))
    for a in (-19.0, 19.0):
        x, y = (Rin + Rout) / 2 * np.sin(np.radians(a)), R0 - (Rin + Rout) / 2 * np.cos(np.radians(a))
        holes = holes + window(x, y, 22, 12, 90 + a)
    lr = Rin + 6
    return Proto("B17", "arc-bar", "Curved slot plate: carabiners fan out instead of bunching, and it sits nicely against a pack or a post.",
                 solid, holes, pts, label_xy=(0, R0 - lr - 1), label_size=5.0,
                 hang="End slots: two hooks or a sling through both (hangs as a smile)")


def b18():
    return slot_plate("B18", "ultralight-plate", "Ultralight 6 mm, 40 mm tall version of B11 for the pack: about half the weight.",
                      H=40.0, T=6.0, slot=(14.0, 22.0), bottom_web=8.0, label_xy=(0, 35.0))


def b19():
    return slot_plate("B19", "angled-slot-plate", "Six slots tilted 30 degrees so clipped pieces hang staggered and don't clash.",
                      H=50.0, n=6, angle=60.0, x_range=(-62, 62), label_xy=(0, 44.5))


def b20():
    # three rows; rows 2 and 3 each sit above a long window so every row
    # has its own wrap web and its carabiners hang clear of the row below
    L = 200.0
    rows = [0.0, 57.0, 114.0]                  # bottom of each row's wrap web
    H = 114 + 9 + 24 + 22
    solid = rounded_rect(-L / 2, 0, L / 2, H, 10)
    holes = None
    pts = []
    for i, y0 in enumerate(rows):
        if i:
            win = rounded_rect(-82, y0 - 16, 82, y0, 7)       # 16 mm window under the row
            holes = holes + win
        for x in np.linspace(-75, 75, 6):
            s_ = window(x, y0 + 9 + 12, 24, 15, 90)
            holes = s_ if holes is None else holes + s_
            pts.append((x, y0 + 9 + 12))
    for ex in (-80, 80):
        holes = holes + window(ex, H - 11, 24, 12, 0)
    return Proto("B20", "gear-board", "A gear board with 18 closed slots in three rows of six; each upper row hangs through its own window, so nothing tangles.",
                 solid, holes, pts, label_xy=(0, H - 11), label_size=5.5,
                 hang="Two top slots: hooks, screws with washers or a sling")


PROTOS = [r11, r12, r13, r14, r15, r16, r17, r18, r19, r20,
          b11, b12, b13, b14, b15, b16, b17, b18, b19, b20]


def build(only=None):
    os.makedirs(os.path.join(OUT, "use"), exist_ok=True)
    report = {}
    for fn in PROTOS:
        p = fn()
        if only and p.pid not in only:
            continue
        use_part, print_part = p.build()
        webs = check_clip_openings(p.cs, p.clip_points)
        use_part = use_part.simplify(0.001)
        print_part = on_bed(print_part.simplify(0.001))
        stl = os.path.join(OUT, f"{p.pid}-{p.name}.stl")
        to_trimesh(print_part).export(stl)
        to_trimesh(use_part).export(os.path.join(OUT, "use", f"{p.pid}.stl"))
        bb = print_part.bounding_box()
        size = [round(bb[3] - bb[0], 1), round(bb[4] - bb[1], 1), round(bb[5] - bb[2], 1)]
        checks = {
            "single_solid": len(print_part.decompose()) == 1,
            "stl_roundtrip_watertight": stl_roundtrip_ok(stl),
            "fits_210_bed": max(size[0], size[1]) <= MAX_BED,
            "all_clip_openings_enclosed": True,
        }
        if not all(checks.values()):
            raise SystemExit(f"{p.pid} failed: {checks} size={size}")
        report[p.pid] = {
            "name": p.name, "summary": p.summary, "notes": p.notes, "hang": p.hang,
            "file": os.path.basename(stl), "print_size_mm": size, "thickness_mm": p.T,
            "clip_openings": len(p.clip_points), "web_mm": [min(webs), max(webs)],
            "est_weight_g": round(print_part.volume() / 1000 * 1.24 * 0.6), **checks,
        }
        print(p.pid, size, len(p.clip_points), "openings, web", min(webs), "-", max(webs))
    path = os.path.join(OUT, "prototype-report.json")
    old = json.load(open(path)) if (only and os.path.exists(path)) else {}
    old.update(report)
    with open(path, "w") as f:
        json.dump(dict(sorted(old.items())), f, indent=2)
    return report


if __name__ == "__main__":
    build(sys.argv[1:] or None)
