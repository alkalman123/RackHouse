"""Rackhouse carabiner-holder prototypes: 10 ring-style (R01-R10) and 10
straight-bar (B01-B10) candidates to print and test before one goes on the
site.

Every prototype follows two rules the build checks:
  * every clip point is at most 12 x 12 mm in cross-section, so a standard
    climbing carabiner closes around it easily;
  * the clip rail stands at least 20 mm off the wall (25-30 mm here), so a
    carabiner can wrap all the way around it.

Construction (all parts): a front rail printed face down on the bed, with
standoff posts printed straight up from it. Screws go through countersunk
holes in the front and through the posts into the wall, so the part is
held rigidly at several points instead of hanging from one.

    python3 designs/prototypes.py

Writes designs/prototypes/<ID>-<name>.stl (print orientation),
designs/prototypes/use/<ID>.stl (on-the-wall orientation, for renders) and
designs/prototypes/prototype-report.json.
"""

import json
import os
import sys

import numpy as np
from manifold3d import CrossSection as CS, Manifold as M

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from rackhouse_designs import (circle, rect, rounded_rect, stadium, text, slab_with_edge_break,
                               assert_inside, to_trimesh, on_bed, stl_roundtrip_ok)

OUT = os.path.join(HERE, "prototypes")
MAX_CLIP = 12.0          # max clip-point cross-section, each direction (mm)
MIN_CLEARANCE = 20.0     # min free space behind a clip rail (mm)
MAX_BED = 210.0          # largest XY footprint allowed
SCREW_R, SINK_R, SINK_H = 2.3, 5.0, 2.7   # #8 wood screw, 90-degree countersink


# ----------------------------------------------------------------- helpers

def ring_band(r_mid, w):
    return circle(r_mid + w / 2.0) - circle(r_mid - w / 2.0)


def polar(r, a_deg):
    """Point at radius r, angle measured from straight down (0) toward +x."""
    a = np.radians(a_deg)
    return r * np.sin(a), -r * np.cos(a)


def radial_fin(r_from, r_to, a_deg, width=4.0):
    """A divider fin along a radius, from r_from to r_to."""
    x0, y0 = polar(r_from, a_deg)
    x1, y1 = polar(r_to, a_deg)
    length = abs(r_to - r_from) + width
    ang = np.degrees(np.arctan2(y1 - y0, x1 - x0))
    return stadium((x0 + x1) / 2, (y0 + y1) / 2, length, width, ang)


def coat_hook(x, y_attach, width=8.0, throat=14.0, tip=10.0, entry=16.0):
    """Open hook hanging from y_attach: a stem of `width` centred on x runs
    down, curls toward +x and turns up into a tip. `throat` is the gap
    between stem and tip; `entry` is the clear height between the top of
    the tip and y_attach, so a carabiner or strap can get over the tip."""
    y_turn = y_attach - tip - entry
    stem = rect(x - width / 2, y_turn, x + width / 2, y_attach + 2)
    cx = x + width / 2 + throat / 2
    r_in, r_out = throat / 2, throat / 2 + width
    curl = (circle(r_out, cx, y_turn) - circle(r_in, cx, y_turn)) ^ rect(x - width / 2 - 1, y_turn - r_out - 1,
                                                                            cx + r_out + 1, y_turn)
    tx = x + width / 2 + throat + width / 2
    tip_cs = stadium(tx, y_turn + tip / 2, tip + width, width, 90)
    return stem + curl + tip_cs


def d_loop(cx, cy, a_deg, outer_w=20.0, outer_h=28.0, bar=8.0, side=5.0):
    """A closed gear loop hanging away from the rail in direction a_deg
    (0 = straight down). The clip bar is the far end, `bar` mm thick."""
    lp = rounded_rect(-outer_w / 2, -outer_h, outer_w / 2, 2, 5) - rounded_rect(
        -outer_w / 2 + side, -outer_h + bar, outer_w / 2 - side, -6, 3)
    return lp.rotate(a_deg).translate((cx, cy))


class Proto:
    def __init__(self, pid, name, summary, front, posts, screws, T=10.0, S=25.0,
                 label_xy=(0, 0), label_size=5.0, clip=(12.0, 10.0), notes=""):
        self.pid, self.name, self.summary, self.notes = pid, name, summary, notes
        self.front, self.posts, self.screws = front, posts, screws
        self.T, self.S, self.label_xy, self.label_size, self.clip = T, S, label_xy, label_size, clip

    def build(self):
        T, S = self.T, self.S
        bosses = None
        for (x, y) in self.posts:
            b = circle(9.0, x, y)
            bosses = b if bosses is None else bosses + b
        outline = self.front + bosses
        holes2d = None
        for (x, y) in self.screws:
            h = circle(SCREW_R, x, y)
            holes2d = h if holes2d is None else holes2d + h
        label = text(self.pid, self.label_size, *self.label_xy)
        assert_inside(label, outline - holes2d.offset(3.0), 1.0, f"{self.pid} label")

        front = slab_with_edge_break(outline, T) - label.extrude(2).translate((0, 0, T - 0.8))
        posts_cs = None
        for (x, y) in self.posts:
            c = circle(7.5, x, y)
            posts_cs = c if posts_cs is None else posts_cs + c
        back = (posts_cs.offset(-0.6).extrude(0.8).translate((0, 0, -S))
                + posts_cs.extrude(S - 0.6 + 0.2).translate((0, 0, -S + 0.6)))
        part = front + back
        for (x, y) in self.screws:
            part = part - M.cylinder(S + T + 2, SCREW_R).translate((x, y, -S - 1))
            part = part - M.cylinder(SINK_H + 0.01, SCREW_R, SINK_R).translate((x, y, T - SINK_H))
        self.part = part
        return part.rotate((90, 0, 0)), part.rotate((0, 180, 0))


# --------------------------------------------------------- ring prototypes

def tab_with_post(y_post=96.0, half=28.0, y_base=78.0):
    return CS.batch_hull([circle(15, 0, y_post), rect(-half, y_base, half, y_base + 6)])


def helmet_hook_top(r_in, width=10.0, throat=14.0, entry=20.0):
    """Helmet hook hanging from the top inside of a ring, roughly centred."""
    return coat_hook(-throat / 2 - 6, r_in, width, throat, 12, entry)


def fins_between(r_from, r_to, n_pos, pitch):
    """Dividers bounding n_pos clip positions centred on the bottom."""
    half = n_pos * pitch / 2.0
    out = None
    for k in range(n_pos + 1):
        f = radial_fin(r_from, r_to, -half + k * pitch)
        out = f if out is None else out + f
    return out


def r01():
    R, w = 85.0, 12.0
    band = ring_band(R, w)
    fins = fins_between(R - w / 2 + 1, R - w / 2 - 8, 12, 18.0)
    front = band + fins + tab_with_post() + helmet_hook_top(R - w / 2)
    posts = [(0, 96), polar(R, 0), polar(R, 128), polar(R, -128)]
    return Proto("R01", "fin-ring", "Thin 12 x 10 mm clip band with 12 positions split by fins on the inner edge; helmet hook at the top.",
                 front, posts, [(0, 96), polar(R, 0)], label_xy=(0, 82))


def r02():
    R, w = 80.0, 12.0
    band = ring_band(R, w)
    fins = fins_between(R + w / 2 - 1, R + w / 2 + 8, 12, 18.0)
    front = band + fins + tab_with_post(96, 26, 78) + helmet_hook_top(R - w / 2)
    posts = [(0, 96), polar(R, 0), polar(R, 128), polar(R, -128)]
    return Proto("R02", "outer-fin-ring", "Same thin band, dividers on the outside edge so the inside stays clear for the helmet.",
                 front, posts, [(0, 96), polar(R, 0)], label_xy=(0, 81))


def r03():
    R, w, notch = 85.0, 16.0, 5.0
    band = ring_band(R, w)
    r_in = R - w / 2
    body = band + tab_with_post() + helmet_hook_top(r_in)
    for k in range(13):
        a = -108 + k * 18
        if abs(a) < 1e-6:
            continue
        body = body - circle(notch + 1.0, *polar(r_in - 1.0, a))
    posts = [(0, 96), polar(R, 0), polar(R, 128), polar(R, -128)]
    return Proto("R03", "notched-ring", "Closest to the ring you liked: wider band with deep notches; the band is 11 x 10 mm at every notch.",
                 body, posts, [(0, 96), polar(R, 0)], label_xy=(0, 82), clip=(11.0, 10.0))


def r04():
    R, w = 64.0, 12.0
    band = ring_band(R, w)
    r_out = R + w / 2
    hooks = None
    for x in (-60.0, -30.0, 0.0, 30.0, 60.0):
        y = -np.sqrt(r_out ** 2 - x ** 2) + 2.0          # attach just inside the outer edge
        # throat centred under x: stem centre = x - (width/2 + throat/2)
        h = coat_hook(x - 10.0, y, 7.0, 13.0, 8.0, 16.0)
        hooks = h if hooks is None else hooks + h
    front = band + hooks + tab_with_post(82, 24, 64) + helmet_hook_top(R - w / 2, entry=16)
    posts = [(0, 82), polar(R, 90), polar(R, -90), polar(R, 128), polar(R, -128)]
    return Proto("R04", "hook-ring", "Five open J-hooks hang from the bottom: drop a carabiner on, no gate to open.",
                 front, posts, [(0, 82), polar(R, 90), polar(R, -90)], label_xy=(0, 68), clip=(7.0, 10.0),
                 notes="Hooks: 7 x 10 mm section, 13 mm throat, 16 mm entry above each tip, 3 mm between hooks.")


def r05():
    R, w = 74.0, 12.0
    band = ring_band(R, w)
    loops = None
    for a in (-75, -50, -25, 0, 25, 50, 75):
        lp = d_loop(*polar(R + w / 2 - 1, a), a, 20, 26, 8, 5)
        loops = lp if loops is None else loops + lp
    front = band + loops + tab_with_post(88, 24, 70) + helmet_hook_top(R - w / 2)
    posts = [(0, 88), polar(R, 12.5), polar(R, 128), polar(R, -128)]
    return Proto("R05", "gear-loop-ring", "Seven closed gear loops around the bottom, like the loops on a harness: one piece per loop.",
                 front, posts, [(0, 88), polar(R, 12.5)], label_xy=(0, 74), clip=(8.0, 10.0),
                 notes="Clip onto the outer bar of each loop (8 x 10 mm).")


def r06():
    Ro, Ri, w = 88.0, 58.0, 10.0
    outer, inner = ring_band(Ro, w), ring_band(Ri, w)
    spokes = None
    for a in (60, -60, 180):
        x0, y0 = polar(Ri, a)
        x1, y1 = polar(Ro, a)
        sp = stadium((x0 + x1) / 2, (y0 + y1) / 2, Ro - Ri + 10, 10, np.degrees(np.arctan2(y1 - y0, x1 - x0)))
        spokes = sp if spokes is None else spokes + sp
    fins = fins_between(Ro - w / 2 + 1, Ro - w / 2 - 7, 10, 20.0) + fins_between(Ri - w / 2 + 1, Ri - w / 2 - 6, 6, 26.0)
    front = outer + inner + spokes + fins + tab_with_post(96, 26, 80) + helmet_hook_top(Ri - w / 2, entry=12)
    posts = [(0, 96), polar(Ro, 0), polar(Ri, 0), polar(Ro, 130), polar(Ro, -130)]
    return Proto("R06", "double-ring", "Two rings: the outer one for cams (10 spots), the inner one for nuts and draws (6 spots).",
                 front, posts, [(0, 96), polar(Ro, 0)], label_xy=(0, 83), clip=(10.0, 10.0))


def r07():
    R, w = 85.0, 12.0
    band = ring_band(R, w)
    hub = circle(14, 0, 12)
    spokes = None
    for a in (150, -150):
        x1, y1 = polar(R, a)
        sp = stadium(x1 / 2, (12 + y1) / 2, np.hypot(x1, y1 - 12) + 10, 10, np.degrees(np.arctan2(y1 - 12, x1)))
        spokes = sp if spokes is None else spokes + sp
    fins = fins_between(R - w / 2 + 1, R - w / 2 - 8, 12, 18.0)
    hook = coat_hook(-12, -1, 10, 14, 12, 14)
    front = band + hub + spokes + fins + hook + tab_with_post()
    posts = [(0, 96), (0, 12), polar(R, 0), polar(R, 128), polar(R, -128)]
    return Proto("R07", "hub-ring", "Ring with a center hub screwed to the wall; the helmet hook comes off the hub, so it's the strongest helmet mount.",
                 front, posts, [(0, 96), (0, 12), polar(R, 0)], label_xy=(0, 82))


def r08():
    R, w = 64.0, 12.0
    band = ring_band(R, w)
    # positions on the two sides; helmet J below the ring
    fins = None
    for a0 in (40, -40):
        sgn = 1 if a0 > 0 else -1
        for k in range(6):
            f = radial_fin(R - w / 2 + 1, R - w / 2 - 8, sgn * (40 + k * 18))
            fins = f if fins is None else fins + f
    _, jy = polar(R + w / 2 - 2, 0)
    gap = rect(-4.5, 0, 4.5, 30).rotate(-55).translate((0, jy - 26))
    neck = rect(-7, jy - 10, 7, jy + 2)
    jhook = (circle(20, 0, jy - 26) - circle(10, 0, jy - 26)) - gap + neck
    front = band + fins + jhook + tab_with_post(R + 16, 24, R - 6)
    posts = [(0, R + 16), polar(R, 94), polar(R, -94), polar(R, 0)]   # side posts sit on a divider
    return Proto("R08", "ring-helmet-below", "Smaller ring with the helmet on a J-hook underneath, so the helmet never covers the rack; 10 positions on the sides.",
                 front, posts, [(0, R + 16), polar(R, 0)], label_xy=(0, R + 1), notes="Helmet J-hook: 20 mm throat.")


def r09():
    R, w, half = 58.0, 12.0, 36.0
    outer = CS.batch_hull([circle(R + w / 2, -half, 0), circle(R + w / 2, half, 0)])
    inner = CS.batch_hull([circle(R - w / 2, -half, 0), circle(R - w / 2, half, 0)])
    band = outer - inner
    fins = None
    xs = [-half - 4 + k * (2 * half + 8) / 4 for k in range(5)]
    for x in xs:
        f = rect(x - 2, -(R - w / 2) - 1, x + 2, -(R - w / 2) + 8)
        fins = f if fins is None else fins + f
    for cx, sgn in ((-half, -1), (half, 1)):
        for a in (40, 62, 84, 106):
            x0, y0 = polar(R - w / 2 + 1, sgn * a)
            x1, y1 = polar(R - w / 2 - 8, sgn * a)
            f = stadium(cx + (x0 + x1) / 2, (y0 + y1) / 2, 13, 4, np.degrees(np.arctan2(y1 - y0, x1 - x0)))
            fins = fins + f
    front = band + fins + tab_with_post(R + 18, 30, R - 4) + helmet_hook_top(R - w / 2, entry=14)
    lx, ly = polar(R, -128)
    rx, ry = polar(R, 128)
    posts = [(0, R + 18), (0, -R), (-half + lx, ly), (half + rx, ry)]
    return Proto("R09", "racetrack-ring", "Stretched ring with a flat bottom: four spots in a straight row plus four up each curved side.",
                 front, posts, [(0, R + 18), (0, -R)], label_xy=(0, R + 3))


def r10():
    R, w = 86.0, 12.0
    band = ring_band(R, w)
    fins = fins_between(R - w / 2 + 1, R - w / 2 - 9, 12, 18.0)
    front = band + fins + tab_with_post(98, 28, 80) + helmet_hook_top(R - w / 2)
    posts = [(0, 98), polar(R, 0), polar(R, 72), polar(R, -72), polar(R, 128), polar(R, -128)]
    return Proto("R10", "heavy-ring", "Heavy-duty: 12 x 12 mm band, 30 mm off the wall, six posts and three screws for a big double rack.",
                 front, posts, [(0, 98), polar(R, 72), polar(R, -72)], T=12.0, S=30.0, label_xy=(0, 84), clip=(12.0, 12.0))


# ---------------------------------------------------------- bar prototypes

def end_blocks(x_centers, h, extra=10.0):
    out = None
    for xc in x_centers:
        b = rounded_rect(xc - 12, -extra, xc + 12, h + extra, 6)
        out = b if out is None else out + b
    return out


def top_fins(x_bounds, h, fin_h=8.0):
    out = None
    for x in x_bounds:
        f = stadium(x, h + fin_h / 2 - 0.5, fin_h + 4, 4, 90)
        out = f if out is None else out + f
    return out


def rail_bar(pid, name, summary, L=200.0, h=12.0, n=7, T=10.0, S=25.0, center_post=False, clip=(12.0, 10.0)):
    xe = L / 2 - 12
    rail = rect(-xe, 0, xe, h)
    blocks = end_blocks([-xe, xe], h)
    span_l, span_r = -xe + 12, xe - 12
    bounds = list(np.linspace(span_l, span_r, n + 1))
    posts = [(-xe, h / 2 + 5), (xe, h / 2 + 5)]
    screws = list(posts)
    if center_post:
        blocks = blocks + rounded_rect(-9, -6, 9, h + 6, 5)
        posts.append((0, h / 2))
        screws.append((0, h / 2))
        half = n // 2
        bounds = list(np.linspace(span_l, -12, half + 1)) + list(np.linspace(12, span_r, n - half + 1))
    front = rail + blocks + top_fins(bounds, h)
    return Proto(pid, name, summary, front, posts, screws, T=T, S=S, label_xy=(-xe, -4), label_size=4.6, clip=clip)


def b01():
    return rail_bar("B01", "fin-rail", "Straight 12 x 10 mm clip rail, 7 spots split by fins on top, 25 mm off the wall.")


def b02():
    return rail_bar("B02", "two-bay-rail", "Same rail with a third screw in the middle: two bays of 4 spots, stiffer under a full load.",
                    n=8, center_post=True)


def b03():
    L, xe, ys = 200.0, 88.0, 28.0
    spine = rect(-xe, ys, xe, ys + 12)
    blocks = rounded_rect(-xe - 12, ys - 10, -xe + 12, ys + 22, 6) + rounded_rect(xe - 12, ys - 10, xe + 12, ys + 22, 6)
    hooks = None
    for x in (-64.0, -32.0, 0.0, 32.0, 64.0):
        h = coat_hook(x - 11.0, ys, 8.0, 14.0, 9.0, 16.0)       # throat centred under x
        hooks = h if hooks is None else hooks + h
    posts = [(-xe, ys + 6), (xe, ys + 6)]
    return Proto("B03", "hook-bar", "Five open J-hooks under a straight spine: drop carabiners on without opening the gate.",
                 spine + blocks + hooks, posts, list(posts), label_xy=(-xe, ys - 4), label_size=4.6, clip=(8.0, 10.0),
                 notes="Hooks: 8 x 10 mm section, 14 mm throat, 16 mm entry above each tip.")


def b04():
    xe, h, gap = 88.0, 10.0, 38.0
    lower = rect(-xe, 0, xe, h)
    upper = rect(-xe, h + gap, xe, 2 * h + gap)
    blocks = rounded_rect(-xe - 12, -6, -xe + 12, 2 * h + gap + 6, 6) + rounded_rect(xe - 12, -6, xe + 12, 2 * h + gap + 6, 6)
    b_low = list(np.linspace(-xe + 12, xe - 12, 8))
    b_up = list(np.linspace(-xe + 12, xe - 12, 6))
    fins = None
    for x in b_low:
        f = stadium(x, h + 3, 10, 4, 90)
        fins = f if fins is None else fins + f
    for x in b_up:
        fins = fins + stadium(x, 2 * h + gap + 3, 10, 4, 90)
    posts = [(-xe, h + gap / 2), (xe, h + gap / 2)]
    return Proto("B04", "double-rail", "Two rails: the bottom one for 7 quickdraws, the top one for 5 slings or bigger gear.",
                 lower + upper + blocks + fins, posts, list(posts), label_xy=(-xe, 8), label_size=4.6, clip=(10.0, 10.0))


def b05():
    xe, h = 88.0, 12.0
    rail = rect(-xe, 0, xe, h)
    blocks = end_blocks([-xe, xe], h)
    bounds = list(np.linspace(-xe + 12, 24, 6))
    hook = coat_hook(38, 0, 10, 20, 14, 14)
    posts = [(-xe, h / 2 + 5), (xe, h / 2 + 5)]
    return Proto("B05", "rail-helmet-hook", "Five clip spots plus a big helmet hook at the end: a full mini gear wall in one bar.",
                 rail + blocks + top_fins(bounds, h) + hook, posts, list(posts), label_xy=(-xe, -4), label_size=4.6,
                 notes="Helmet hook: 20 mm throat.")


def b06():
    L, H = 200.0, 46.0
    plate = rounded_rect(-L / 2, 0, L / 2, H, 6)
    slots = None
    for k in range(7):
        x = (k - 3) * 22.0
        s = stadium(x, 9 + 12, 24, 15, 90)
        slots = s if slots is None else slots + s
    posts = [(-88, 23), (88, 23)]
    return Proto("B06", "slot-plate", "The Draw Bar, fixed: bigger 15 x 24 mm slots, a 9 mm bottom rail and 25 mm of wall clearance.",
                 plate - slots, posts, list(posts), label_xy=(0, 40.5), label_size=4.6, clip=(9.0, 10.0))


def b07():
    return rail_bar("B07", "dense-comb", "Ten tightly spaced spots (17 mm apart) for a full set of quickdraws.", n=10)


def b08():
    xe, ys = 88.0, 30.0
    spine = rect(-xe, ys, xe, ys + 12)
    blocks = rounded_rect(-xe - 12, ys - 10, -xe + 12, ys + 22, 6) + rounded_rect(xe - 12, ys - 10, xe + 12, ys + 22, 6)
    loops = None
    for x in np.linspace(-63, 63, 6):
        lp = d_loop(x, ys + 1, 0, 20, 28, 8, 5)
        loops = lp if loops is None else loops + lp
    posts = [(-xe, ys + 6), (xe, ys + 6)]
    return Proto("B08", "gear-loop-bar", "Six closed gear loops hanging from a spine, like harness gear loops: nothing can slide.",
                 spine + blocks + loops, posts, list(posts), label_xy=(-xe, ys - 4), label_size=4.6, clip=(8.0, 10.0))


def b09():
    return rail_bar("B09", "compact-rail", "Short 150 mm version with 5 spots for a small space, a van or a nut/tool rack.", L=150.0, n=5)


def b10():
    return rail_bar("B10", "heavy-rail", "Heavy-duty 12 x 12 mm rail, 30 mm off the wall, three screws: 8 spots for heavy gear.",
                    h=12.0, n=8, T=12.0, S=30.0, center_post=True, clip=(12.0, 12.0))


PROTOS = [r01, r02, r03, r04, r05, r06, r07, r08, r09, r10, b01, b02, b03, b04, b05, b06, b07, b08, b09, b10]


def build():
    os.makedirs(os.path.join(OUT, "use"), exist_ok=True)
    report = {}
    for fn in PROTOS:
        p = fn()
        use_part, print_part = p.build()
        use_part = use_part.simplify(0.001)
        print_part = on_bed(print_part.simplify(0.001))
        stl = os.path.join(OUT, f"{p.pid}-{p.name}.stl")
        to_trimesh(print_part).export(stl)
        to_trimesh(use_part).export(os.path.join(OUT, "use", f"{p.pid}.stl"))
        bb = print_part.bounding_box()
        size = [round(bb[3] - bb[0], 1), round(bb[4] - bb[1], 1), round(bb[5] - bb[2], 1)]
        vol = print_part.volume() / 1000.0
        checks = {
            "single_solid": len(print_part.decompose()) == 1,
            "stl_roundtrip_watertight": stl_roundtrip_ok(stl),
            "fits_210_bed": max(size[0], size[1]) <= MAX_BED,
            "clip_section_ok": max(p.clip) <= MAX_CLIP and float(np.hypot(*p.clip)) <= 17.0,
            "wall_clearance_ok": p.S >= MIN_CLEARANCE,
        }
        if not all(checks.values()):
            raise SystemExit(f"{p.pid} failed checks: {checks}")
        report[p.pid] = {
            "name": p.name, "summary": p.summary, "notes": p.notes, "file": os.path.basename(stl),
            "print_size_mm": size, "clip_section_mm": list(p.clip), "wall_clearance_mm": p.S,
            "screws": len(p.screws), "est_weight_g": round(vol * 1.24 * 0.6), **checks,
        }
        print(p.pid, size, "ok")
    with open(os.path.join(OUT, "prototype-report.json"), "w") as f:
        json.dump(report, f, indent=2)
    return report


if __name__ == "__main__":
    build()
