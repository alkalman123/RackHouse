"""Builds the site's use-case illustrations (img/usecase-*.svg) with each
product drawn from its real CAD outline in rackhouse_designs.py."""
import os, sys
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rackhouse_designs as r

IMG = os.path.join(os.path.dirname(HERE), "img")
INK, PAPER, EMBER, ICE, SAND, ROCK = "#15191c", "#efeadf", "#d85c2a", "#4a90c2", "#c9a86a", "#63707c"


def path_d(polys, s, tx, ty, flip=True):
    out = []
    for p in polys:
        p = np.asarray(p)
        xs = tx + p[:, 0] * s
        ys = ty - p[:, 1] * s if flip else ty + p[:, 1] * s
        out.append("M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in zip(xs, ys)) + " Z")
    return " ".join(out)


def svg(label, body):
    return (f'<svg viewBox="0 0 800 560" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{label}">\n'
            f'  <rect width="800" height="560" rx="20" fill="{PAPER}"/>\n{body}\n</svg>\n')


def gatekeeper_scene():
    cs = r.gatekeeper()[1].slice(5.0)
    s, tx, ty = 1.55, 400, 40 + 82 * 1.55          # model top (y=82) lands at y=40
    d = path_d(cs.to_polygons(), s, tx, ty)
    X = lambda x: tx + x * s
    Y = lambda y: ty - y * s
    b = []
    b.append('  <g stroke="#15191c" stroke-opacity=".10" stroke-width="3">'
             + "".join(f'<line x1="{x}" y1="40" x2="{x}" y2="520"/>' for x in (80, 260, 540, 720)) + "</g>")
    # wall hook through the hang hole (0,68)
    hx, hy = X(0), Y(68)
    b.append(f'  <rect x="{hx-7:.0f}" y="12" width="14" height="{hy-26:.0f}" rx="4" fill="{INK}"/>')
    b.append(f'  <path d="M{hx-6:.0f} {hy-14:.0f} Q {hx-10:.0f} {hy+12:.0f} {hx+4:.0f} {hy+10:.0f}" fill="none" stroke="{INK}" stroke-width="7" stroke-linecap="round"/>')
    b.append(f'  <path d="{d}" fill="{EMBER}" fill-rule="evenodd" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    b.append(f'  <text x="{X(0):.0f}" y="{Y(12)+5:.0f}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-weight="800" font-size="10" letter-spacing="1" fill="#8f3a17">RACKHOUSE</text>')

    def biner(cx, cy, ang, color):
        return (f'<g transform="translate({cx:.0f},{cy:.0f}) rotate({ang})">'
                f'<rect x="-9" y="-6" width="18" height="44" rx="9" fill="none" stroke="{color}" stroke-width="5"/></g>')

    def cam(cx, cy, color):
        return (f'<g transform="translate({cx:.0f},{cy:.0f})" stroke="{INK}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">'
                f'<path d="M0 0 C -14 6 -14 22 0 28 C 14 22 14 6 0 0 Z" fill="none" stroke-width="5"/>'
                f'<line x1="0" y1="28" x2="0" y2="78" stroke-width="6"/>'
                f'<g fill="{color}"><ellipse cx="-14" cy="96" rx="12" ry="19" transform="rotate(-22 -14 96)"/>'
                f'<ellipse cx="14" cy="96" rx="12" ry="19" transform="rotate(22 14 96)"/></g>'
                f'<rect x="-4" y="76" width="8" height="40" rx="3" fill="{INK}"/></g>')
    # carabiners clipped through the four gear slots, cams hanging beneath
    slot_pts = [(-41, -22, ICE), (-31, -50, SAND), (41, -22, "#55805a"), (31, -50, ROCK)]
    for i, (x, y, c) in enumerate(slot_pts):
        side = -1 if x < 0 else 1
        cx, cy = X(x) + side * 70 + side * (i % 2) * 34, Y(y) - 4
        b.append(f'  <path d="M{X(x):.0f} {Y(y):.0f} L{cx:.0f} {cy:.0f}" stroke="{c}" stroke-width="5" stroke-linecap="round"/>')
        b.append("  " + biner(cx, cy, 0, c))
        b.append("  " + cam(cx, cy + 40, c))
    # helmet hanging from the J-hook by its chin strap
    jx, jy = X(0), Y(-106) + 18 * s
    b.append(f'  <path d="M{jx-3:.0f} {jy-4:.0f} L{jx-60:.0f} {jy+58:.0f} M{jx+3:.0f} {jy-4:.0f} L{jx+60:.0f} {jy+58:.0f}" stroke="{INK}" stroke-width="4" fill="none"/>')
    hy0 = jy + 58
    b.append(f'  <path d="M{jx-88:.0f} {hy0+70:.0f} C {jx-88:.0f} {hy0-6:.0f} {jx+88:.0f} {hy0-6:.0f} {jx+88:.0f} {hy0+70:.0f} Z" fill="#f2f2f2" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    b.append(f'  <path d="M{jx-50:.0f} {hy0+20:.0f} h28 M{jx+22:.0f} {hy0+20:.0f} h28" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    b.append(f'  <rect x="{jx-96:.0f}" y="{hy0+66:.0f}" width="192" height="10" rx="5" fill="{INK}"/>')
    # callouts
    b.append('  <g font-family="Helvetica, Arial, sans-serif" font-size="15" font-weight="700" fill="#15191c">'
             '<text x="560" y="90">Gear slots: clip cams + draws</text>'
             '<text x="560" y="112" font-weight="400" fill="#4b5157">4 slots, carabiner-sized</text>'
             '<text x="40" y="500">J-hook: helmet hangs by its strap</text>'
             '<text x="40" y="522" font-weight="400" fill="#4b5157">no unbuckling, no strap stretch</text></g>')
    return svg("Illustration of the Gatekeeper hanging from a wall hook, cams clipped through its gear slots and a helmet hanging from the J-hook", "\n".join(b))


def rockring_scene():
    prof = (r.rounded_rect(-28, 40, 28, 58, 5) + r.rounded_rect(-9, 0, 17, 44, 4)).offset(3).offset(-3)
    s, tx, ty = 3.2, 400, 120 + 58 * 3.2
    X = lambda x: tx + x * s
    Y = lambda y: ty - y * s
    b = []
    d = path_d(prof.to_polygons(), s, tx, ty)
    # cord / loading pin hanging to a kettlebell
    cx, cy = X(4), Y(14)
    b.append(f'  <path d="M{cx-14:.0f} {cy:.0f} L{cx-30:.0f} 420 M{cx+14:.0f} {cy:.0f} L{cx+30:.0f} 420" stroke="{SAND}" stroke-width="8" stroke-linecap="round"/>')
    b.append(f'  <path d="{d}" fill="{ROCK}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>')
    b.append(f'  <circle cx="{cx:.0f}" cy="{cy:.0f}" r="{7*s:.0f}" fill="#2a2d31" stroke="{INK}" stroke-width="3"/>')
    b.append(f'  <path d="M{cx-18:.0f} {cy:.0f} A 18 18 0 0 0 {cx+18:.0f} {cy:.0f}" fill="none" stroke="{SAND}" stroke-width="8"/>')
    # kettlebell
    kx = cx
    b.append(f'  <path d="M{kx-32:.0f} 420 C {kx-40:.0f} 392 {kx+40:.0f} 392 {kx+32:.0f} 420" fill="none" stroke="{INK}" stroke-width="10" stroke-linecap="round"/>')
    b.append(f'  <circle cx="{kx:.0f}" cy="470" r="56" fill="#2a2d31"/>')
    b.append(f'  <rect x="{kx-44:.0f}" y="516" width="88" height="10" rx="5" fill="#2a2d31"/>')
    b.append(f'  <text x="{kx:.0f}" y="478" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-weight="800" font-size="20" fill="{PAPER}">20 kg</text>')
    # fingertips pinching the 19 mm edge from the left, thumb on top
    ex, ey = X(-28), Y(40)
    b.append(f'  <g fill="#e7b48f" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round">'
             f'<path d="M{ex-150:.0f} {ey-150:.0f} C {ex-60:.0f} {ey-150:.0f} {ex-30:.0f} {ey-60:.0f} {ex-20:.0f} {ey+10:.0f} L{ex+52:.0f} {ey+10:.0f} C {ex+64:.0f} {ey+10:.0f} {ex+64:.0f} {ey+34:.0f} {ex+50:.0f} {ey+34:.0f} L{ex-60:.0f} {ey+38:.0f} C {ex-120:.0f} {ey+40:.0f} {ex-170:.0f} {ey-20:.0f} {ex-170:.0f} {ey-80:.0f} Z"/>'
             f'<path d="M{ex-60:.0f} {ey-110:.0f} C {ex-20:.0f} {ey-120:.0f} {ex+30:.0f} {ey-90:.0f} {ex+40:.0f} {ey-66:.0f} C {ex+46:.0f} {ey-52:.0f} {ex+26:.0f} {ey-46:.0f} {ex+14:.0f} {ey-56:.0f} C {ex-6:.0f} {ey-72:.0f} {ex-36:.0f} {ey-76:.0f} {ex-60:.0f} {ey-70:.0f} Z"/></g>')
    b.append(f'  <g stroke="{INK}" stroke-width="2.5" stroke-linecap="round"><line x1="{ex+10:.0f}" y1="{ey+12:.0f}" x2="{ex+6:.0f}" y2="{ey+34:.0f}"/><line x1="{ex+32:.0f}" y1="{ey+12:.0f}" x2="{ex+30:.0f}" y2="{ey+34:.0f}"/></g>')
    b.append(f'  <g font-family="Helvetica, Arial, sans-serif" font-size="15" font-weight="700" fill="{INK}">'
             f'<text x="560" y="110">19 mm edge (left)</text><text x="560" y="132">11 mm edge (right)</text>'
             f'<text x="560" y="154" font-weight="400" fill="#4b5157">Flip it to change edge depth</text>'
             f'<text x="40" y="500">Cord or loading pin through the</text><text x="40" y="520">countersunk 14 mm channel</text></g>')
    b.append(f'  <path d="M{X(-28):.0f} {Y(40)+52:.0f} h{19*s:.0f}" stroke="{EMBER}" stroke-width="3"/><path d="M{X(17):.0f} {Y(40)+52:.0f} h{11*s:.0f}" stroke="{EMBER}" stroke-width="3"/>')
    return svg("Illustration of a hand pinching the Rock Ring's 19 mm edge with a kettlebell hanging from a cord through its channel", "\n".join(b))


def cupcradle_scene():
    outer = [(0, 0), (29.3, 0), (30.0, 0.7), (31.0, 62.0), (50.5, 81.5), (50.5, 133.0), (49.9, 134.6),
             (48.8, 135.4), (47.7, 135.4), (47.0, 134.6), (47.0, 84.0), (0, 84.0)]
    right = [(x, z) for x, z in outer if x > 0]
    sil = [(-x, z) for x, z in reversed(right[:6])] + right[:6]
    s = 1.55
    base_y = 520
    tx = 420
    X = lambda x: tx + x * s
    Y = lambda z: base_y - z * s
    b = []
    # dashboard console with a cupholder well (77 mm wide)
    top = Y(60)
    b.append(f'  <rect x="80" y="{top:.0f}" width="640" height="{560-top:.0f}" fill="#3a3f45"/>')
    b.append(f'  <rect x="80" y="{top-10:.0f}" width="640" height="14" rx="7" fill="#4c535a"/>')
    b.append(f'  <rect x="{X(-38.5):.0f}" y="{top:.0f}" width="{77*s:.0f}" height="{base_y-top+2:.0f}" fill="#1f2327"/>')
    b.append(f'  <rect x="{X(-38.5)-200:.0f}" y="{top:.0f}" width="{77*s:.0f}" height="{base_y-top+2:.0f}" fill="#1f2327"/>')
    b.append(f'  <rect x="{X(-38.5)-200:.0f}" y="{top-150:.0f}" width="{77*s:.0f}" height="160" rx="10" fill="#c9c2b3" stroke="{INK}" stroke-width="3"/>')
    b.append(f'  <text x="{X(-38.5)-200+77*s/2:.0f}" y="{top-70:.0f}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-size="12" fill="{INK}">coffee</text>')
    # Nalgene: 89 mm wide, sits on the cup floor at z=84
    nb, nw, nh = Y(84), 89 * s, 210 * s
    nl = X(-44.5)
    b.append(f'  <rect x="{nl:.0f}" y="{nb-nh:.0f}" width="{nw:.0f}" height="{nh:.0f}" rx="14" fill="{ICE}" fill-opacity=".55" stroke="{INK}" stroke-width="3"/>')
    b.append(f'  <rect x="{X(-31):.0f}" y="{nb-nh-34:.0f}" width="{62*s:.0f}" height="38" rx="6" fill="#2a2d31"/>')
    b.append(f'  <path d="M{X(0):.0f} {nb-nh-34:.0f} C {X(0):.0f} {nb-nh-62:.0f} {X(26):.0f} {nb-nh-62:.0f} {X(26):.0f} {nb-nh-30:.0f}" fill="none" stroke="#2a2d31" stroke-width="6"/>')
    for k in range(1, 6):
        yy = nb - k * 30 * s
        b.append(f'  <line x1="{nl+nw-20:.0f}" y1="{yy:.0f}" x2="{nl+nw-6:.0f}" y2="{yy:.0f}" stroke="{INK}" stroke-width="2"/>')
    # Cup Cradle silhouette (true profile) sits in the cupholder
    pts = " ".join(f"{X(x):.1f},{Y(z):.1f}" for x, z in sil)
    b.append(f'  <polygon points="{pts}" fill="{EMBER}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>')
    # ribs + arch window detail
    for x in (-22, 0, 22):
        b.append(f'  <line x1="{X(x):.0f}" y1="{Y(4):.0f}" x2="{X(x*1.15):.0f}" y2="{Y(58):.0f}" stroke="#8f3a17" stroke-width="3"/>')
    b.append(f'  <path d="M{X(-9):.0f} {Y(92):.0f} V{Y(116):.0f} L{X(0):.0f} {Y(125):.0f} L{X(9):.0f} {Y(116):.0f} V{Y(92):.0f} Z" fill="{ICE}" fill-opacity=".8" stroke="{INK}" stroke-width="2.5"/>')
    b.append(f'  <g font-family="Helvetica, Arial, sans-serif" font-size="15" font-weight="700" fill="{INK}">'
             f'<text x="560" y="120">94 mm cup fits</text><text x="560" y="140">wide-mouth Nalgenes</text>'
             f'<text x="560" y="180" font-weight="400" fill="#4b5157">Ribbed stem grips</text>'
             f'<text x="560" y="200" font-weight="400" fill="#4b5157">69–79 mm cupholders</text></g>')
    return svg("Illustration of the Cup Cradle seated in a car console cupholder, holding a wide-mouth Nalgene upright next to a coffee cup", "\n".join(b))


if __name__ == "__main__":
    for name, fn in (("gatekeeper", gatekeeper_scene), ("rockring", rockring_scene), ("cupcradle", cupcradle_scene)):
        with open(os.path.join(IMG, f"usecase-{name}.svg"), "w") as f:
            f.write(fn())
    print("ok")
