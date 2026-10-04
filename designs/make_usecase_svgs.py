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
    hy0 = jy + 58                                  # straps end at the helmet's rim
    # hung by the chin strap, a helmet hangs crown-down with its opening up
    b.append(f'  <path d="M{jx-88:.0f} {hy0:.0f} C {jx-88:.0f} {hy0+104:.0f} {jx+88:.0f} {hy0+104:.0f} {jx+88:.0f} {hy0:.0f} Z" fill="#f2f2f2" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    b.append(f'  <path d="M{jx-50:.0f} {hy0+40:.0f} h28 M{jx+22:.0f} {hy0+40:.0f} h28" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    b.append(f'  <rect x="{jx-96:.0f}" y="{hy0-5:.0f}" width="192" height="10" rx="5" fill="{INK}"/>')
    # callouts
    b.append('  <g font-family="Helvetica, Arial, sans-serif" font-size="15" font-weight="700" fill="#15191c">'
             '<text x="560" y="90">Gear slots: clip cams + draws</text>'
             '<text x="560" y="112" font-weight="400" fill="#4b5157">4 slots, carabiner-sized</text>'
             '<text x="40" y="500">J-hook: helmet hangs by its strap</text>'
             '<text x="40" y="522" font-weight="400" fill="#4b5157">no unbuckling, no strap stretch</text></g>')
    return svg("Illustration of the Gatekeeper hanging from a wall hook, cams clipped through its gear slots and a helmet hanging from the J-hook", "\n".join(b))


def front_outline(print_part, z_mid):
    """Undo the face-down print rotation and slice through the front plate."""
    return print_part.rotate((0, -180, 0)).slice(z_mid)


def cam_svg(cx, cy, size, color):
    """Stylised cam hanging from a carabiner whose top is at (cx, cy)."""
    lobe_w, lobe_h = 7 + 5 * size, 11 + 7 * size
    return (f'<g transform="translate({cx:.0f},{cy:.0f})" stroke="{INK}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
            f'<rect x="-8" y="-4" width="16" height="38" rx="8" fill="none" stroke="{color}" stroke-width="4.5"/>'
            f'<line x1="0" y1="34" x2="0" y2="74" stroke-width="5"/>'
            f'<g fill="{color}"><ellipse cx="{-lobe_w * .55:.1f}" cy="{86 + lobe_h * .3:.1f}" rx="{lobe_w * .55:.1f}" ry="{lobe_h * .62:.1f}" transform="rotate(-18 {-lobe_w * .55:.1f} {86 + lobe_h * .3:.1f})"/>'
            f'<ellipse cx="{lobe_w * .55:.1f}" cy="{86 + lobe_h * .3:.1f}" rx="{lobe_w * .55:.1f}" ry="{lobe_h * .62:.1f}" transform="rotate(18 {lobe_w * .55:.1f} {86 + lobe_h * .3:.1f})"/></g>'
            f'<rect x="-3.5" y="72" width="7" height="{24 + lobe_h * .9:.0f}" rx="3" fill="{INK}"/></g>')


def rockring_scene():
    cs = front_outline(r.rock_ring()[1], 7.0)
    s, tx, ty = 1.6, 400, 16 + 114 * 1.6            # model top (y=114) lands at y=16
    X = lambda x: tx + x * s
    Y = lambda y: ty - y * s
    b = ['  <g stroke="#15191c" stroke-opacity=".10" stroke-width="3">'
         + "".join(f'<line x1="{x}" y1="20" x2="{x}" y2="540"/>' for x in (90, 250, 550, 710)) + "</g>"]
    b.append(f'  <circle cx="{X(0):.0f}" cy="{Y(101):.0f}" r="5" fill="{INK}"/>')
    b.append(f'  <path d="{path_d(cs.to_polygons(), s, tx, ty)}" fill="{ROCK}" fill-rule="evenodd" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
    # cams clipped through the numbered notches, sized smallest to biggest
    colors = ["#8a8f96", "#7b4fa0", "#3a8f4f", "#c03b2b", "#d8b52a", "#3a6fc0", "#8a8f96", "#7b4fa0", "#3a8f4f", "#c03b2b", "#d8b52a"]
    for i, k in enumerate(range(2, 13)):
        a = np.radians((k - 7) * 18.0)
        nx, ny = 75 * np.sin(a), -75 * np.cos(a)
        b.append("  " + cam_svg(X(nx), Y(ny), 0.7 + i * 0.3, colors[i]))
    # helmet hanging from the hook by its chin strap, in front of the ring
    hx, hy = X(11.5), Y(48 - 6.5)
    b.append(f'  <path d="M{hx - 4:.0f} {hy:.0f} L{hx - 120:.0f} {hy + 60:.0f} M{hx + 4:.0f} {hy:.0f} L{hx + 120:.0f} {hy + 60:.0f}" stroke="{INK}" stroke-width="4" fill="none"/>')
    top = hy + 60                                  # rim of the helmet, where the straps end
    b.append('  <g opacity=".88">')
    # hung by the chin strap, the helmet hangs crown-down with its opening up
    b.append(f'  <path d="M{hx - 132:.0f} {top:.0f} C {hx - 132:.0f} {top + 150:.0f} {hx + 132:.0f} {top + 150:.0f} {hx + 132:.0f} {top:.0f} Z" fill="#f2f2f2" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')
    b.append(f'  <path d="M{hx - 70:.0f} {top + 62:.0f} h40 M{hx + 30:.0f} {top + 62:.0f} h40" stroke="{INK}" stroke-width="4" stroke-linecap="round"/>')
    b.append(f'  <rect x="{hx - 142:.0f}" y="{top - 6:.0f}" width="284" height="12" rx="6" fill="{INK}"/>')
    b.append('  </g>')
    b.append('  <g font-family="Helvetica, Arial, sans-serif" font-size="15" font-weight="700" fill="#15191c">'
             '<text x="24" y="56">15 numbered notches</text>'
             '<text x="24" y="76" font-weight="400" fill="#4b5157">clip each cam in size order</text>'
             '<text x="610" y="56">Helmet hook</text>'
             '<text x="590" y="76" font-weight="400" fill="#4b5157">hang it by the chin strap</text></g>')
    return svg("Illustration of the Rock Ring on a wall: a full set of cams clipped around its numbered notches in size order, and a helmet hanging from the hook in the middle", "\n".join(b))


def quickdraw_svg(cx, cy, color):
    return (f'<g transform="translate({cx:.0f},{cy:.0f})" stroke-linecap="round" stroke-linejoin="round">'
            f'<rect x="-11" y="-14" width="22" height="58" rx="11" fill="none" stroke="#9aa1a8" stroke-width="5"/>'
            f'<rect x="-9" y="36" width="18" height="58" rx="5" fill="{color}" stroke="{INK}" stroke-width="2"/>'
            f'<rect x="-11" y="86" width="22" height="58" rx="11" fill="none" stroke="#9aa1a8" stroke-width="5"/></g>')


def drawbar_scene():
    cs = front_outline(r.draw_bar()[1], 4.0)
    s, tx, ty = 3.0, 400, 70 + 44 * 3.0
    X = lambda x: tx + x * s
    Y = lambda y: ty - y * s
    b = ['  <g stroke="#15191c" stroke-opacity=".10" stroke-width="3">'
         + "".join(f'<line x1="{x}" y1="20" x2="{x}" y2="540"/>' for x in (60, 740)) + "</g>"]
    b.append(f'  <circle cx="{X(-88):.0f}" cy="{Y(24):.0f}" r="5" fill="{INK}"/><circle cx="{X(88):.0f}" cy="{Y(24):.0f}" r="5" fill="{INK}"/>')
    b.append(f'  <path d="{path_d(cs.to_polygons(), s, tx, ty)}" fill="{EMBER}" fill-rule="evenodd" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/>')
    b.append(f'  <text x="{X(0):.0f}" y="{Y(38.6) + 5:.0f}" text-anchor="middle" font-family="Helvetica, Arial, sans-serif" font-weight="800" font-size="13" letter-spacing="1.5" fill="#8f3a17">RACKHOUSE  ·  NOT FOR CLIMBING</text>')
    sling_colors = [ICE, "#3a8f4f", SAND, "#c03b2b", ICE, "#3a8f4f", SAND]
    for k in range(7):
        x = (k - 3) * 22.0
        if k == 5:   # one slot with a sling and a few nuts instead of a draw
            b.append(f'  <g transform="translate({X(x):.0f},{Y(22) - 10:.0f})"><rect x="-11" y="-4" width="22" height="58" rx="11" fill="none" stroke="#9aa1a8" stroke-width="5"/>'
                     f'<path d="M-6 54 C -40 120 -30 230 0 250 C 30 230 40 120 6 54" fill="none" stroke="{SAND}" stroke-width="7"/></g>')
            continue
        b.append("  " + quickdraw_svg(X(x), Y(22) - 4, sling_colors[k]))
    b.append('  <g font-family="Helvetica, Arial, sans-serif" font-size="15" font-weight="700" fill="#15191c">'
             '<text x="60" y="480">7 slots: clip quickdraws, slings or extra gear</text>'
             '<text x="60" y="502" font-weight="400" fill="#4b5157">Two screws through the keyholes, 20 mm off the wall</text></g>')
    return svg("Illustration of the Draw Bar on a wall with six quickdraws and a sling clipped through its slots", "\n".join(b))


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
    for name, fn in (("gatekeeper", gatekeeper_scene), ("rockring", rockring_scene), ("drawbar", drawbar_scene), ("cupcradle", cupcradle_scene)):
        with open(os.path.join(IMG, f"usecase-{name}.svg"), "w") as f:
            f.write(fn())
    print("ok")
