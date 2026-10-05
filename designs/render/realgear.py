"""Lifelike climbing gear for the product renders.

Geometry follows real gear, not icons:
  * carabiners: asymmetric-D frames (about 98 x 56 mm, 10 mm stock, an
    oval I-beam spine) with a wire gate, a straight solid gate or a bent
    gate, a hinge rivet, and an open frame where the gate is;
  * quickdraws: a 12 cm dogbone (two sewn end loops, a thick sewn body
    with bar tacks), a rubber keeper and a bent-gate bottom carabiner;
  * cams: single-axle, four-lobe units sized to the common 0.3-4
    expansion ranges (23-115 mm), log-spiral lobes at a 13.75 degree
    camming angle, axle, springs, cable stem, trigger bar and trigger
    wires, thumb loop, and a sewn sling with a bar tack, coloured by size
    the way most racks are.

Everything hangs physically: each carabiner passes through its own
product opening and rests on the web it closes around (see gear.py), and
each quickdraw or cam hangs from that carabiner's basket. A piece that
would pass through the product or another piece swings forward, twists
on its sling or rolls, by the smallest amount that clears, which is
where it would come to rest leaning on its neighbour.

Meshes are plain arrays (millimetres): V (n,3), F (m,3) and per-corner
UVs (m,3,2) measured in mm along and around each strap, wire or tube, so
the renderer can lay webbing weave and cable twist on them.
"""

import numpy as np
from scipy.spatial import cKDTree

TAN_CAM = np.tan(np.radians(13.75))
# common cam sizes 0.3 .. 4: expanded width (mm), colour, stem length (mm)
CAM_SIZES = [
    (23.4, "#2f6fc8", 78), (26.7, "#9aa0a8", 80), (33.5, "#7a4fb0", 86), (41.2, "#3f9a4f", 92),
    (52.1, "#c8372b", 98), (64.9, "#dcb22c", 106), (87.9, "#2f6fc8", 118), (114.7, "#9aa0a8", 128),
]


# ------------------------------------------------------------------ meshes

class Mesh:
    def __init__(self, V, F, FUV=None):
        self.V = np.asarray(V, float)
        self.F = np.asarray(F, np.int64)
        self.FUV = None if FUV is None else np.asarray(FUV, float)

    def transformed(self, M):
        V = self.V @ M[:3, :3].T + M[:3, 3]
        return Mesh(V, self.F, self.FUV)

    @staticmethod
    def merge(meshes):
        meshes = [m for m in meshes if m is not None and len(m.F)]
        V, F, U, off = [], [], [], 0
        for m in meshes:
            V.append(m.V)
            F.append(m.F + off)
            U.append(m.FUV if m.FUV is not None else np.zeros((len(m.F), 3, 2)))
            off += len(m.V)
        if not meshes:
            return Mesh(np.zeros((0, 3)), np.zeros((0, 3), np.int64), np.zeros((0, 3, 2)))
        return Mesh(np.vstack(V), np.vstack(F), np.vstack(U))

    def sample(self, spacing=2.0, rng=None):
        """Points spread over the surface, about one per spacing^2 mm^2."""
        rng = rng or np.random.default_rng(1)
        a, b, c = (self.V[self.F[:, i]] for i in range(3))
        area = 0.5 * np.linalg.norm(np.cross(b - a, c - a), axis=1)
        n = max(50, int(area.sum() / spacing ** 2))
        idx = rng.choice(len(area), n, p=area / area.sum())
        r1, r2 = rng.random(n), rng.random(n)
        s = np.sqrt(r1)
        return a[idx] * (1 - s)[:, None] + b[idx] * (s * (1 - r2))[:, None] + c[idx] * (s * r2)[:, None]


def norm(v):
    return v / np.linalg.norm(v, axis=-1, keepdims=True)


def resample(pts, step, closed):
    pts = np.asarray(pts, float)
    P = np.vstack([pts, pts[:1]]) if closed else pts
    seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
    s = np.concatenate([[0], np.cumsum(seg)])
    n = max(4, int(np.ceil(s[-1] / step)))
    t = np.linspace(0, s[-1], n, endpoint=not closed)
    return np.stack([np.interp(t, s, P[:, k]) for k in range(P.shape[1])], 1)


def catmull_closed(P, n=12):
    P = np.asarray(P, float)
    k = len(P)
    out = []
    for i in range(k):
        p0, p1, p2, p3 = P[(i - 1) % k], P[i], P[(i + 1) % k], P[(i + 2) % k]
        for t in np.linspace(0, 1, n, endpoint=False):
            out.append(0.5 * (2 * p1 + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t
                              + (-p0 + 3 * p1 - 3 * p2 + p3) * t ** 3))
    return np.array(out)


def sweep(pts, half_u, half_v, closed=False, up=None, segs=16, power=2.0, caps=True):
    """Tube along pts with a superellipse cross-section: half-width half_u
    along U (perpendicular to the tangent and to `up`), half_v along V
    (`up` made perpendicular to the tangent). up: one vector, one per point,
    or None for a rotation-minimizing frame. half_u/half_v: scalar or per
    point. Returns a Mesh with UVs in mm (along, around)."""
    pts = np.asarray(pts, float)
    N = len(pts)
    if closed:
        T = np.roll(pts, -1, 0) - np.roll(pts, 1, 0)
    else:
        T = np.gradient(pts, axis=0)
    T = norm(T)
    if up is None:
        ref = np.array([0, 0, 1.0]) if abs(T[0, 2]) < 0.9 else np.array([1.0, 0, 0])
        Vv = np.zeros_like(pts)
        v = norm(ref - (ref @ T[0]) * T[0])
        for i in range(N):
            v = v - (v @ T[i]) * T[i]
            v = v / np.linalg.norm(v)
            Vv[i] = v
    else:
        up = np.broadcast_to(np.asarray(up, float), pts.shape)
        Vv = norm(up - (np.sum(up * T, 1))[:, None] * T)
    U = np.cross(Vv, T)
    hu = np.broadcast_to(np.asarray(half_u, float), (N,))
    hv = np.broadcast_to(np.asarray(half_v, float), (N,))
    ang = np.linspace(0, 2 * np.pi, segs, endpoint=False)
    c, s = np.cos(ang), np.sin(ang)
    e = 2.0 / power
    cu = np.sign(c) * np.abs(c) ** e
    sv = np.sign(s) * np.abs(s) ** e
    V = (pts[:, None, :] + (hu[:, None] * cu[None, :])[..., None] * U[:, None, :]
         + (hv[:, None] * sv[None, :])[..., None] * Vv[:, None, :]).reshape(-1, 3)
    # UV in mm: along-curve arc length, around-perimeter length
    seg = np.linalg.norm(np.diff(np.vstack([pts, pts[:1]]) if closed else pts, axis=0), axis=1)
    along = np.concatenate([[0], np.cumsum(seg)])
    perim = np.pi * (hu.mean() + hv.mean())
    around = np.linspace(0, perim, segs + 1)
    F, FUV = [], []
    rings = N if closed else N - 1
    for i in range(rings):
        j = (i + 1) % N
        for k in range(segs):
            k2 = (k + 1) % segs
            a, b, cc, d = i * segs + k, i * segs + k2, j * segs + k2, j * segs + k
            ua, ub = along[i], along[i + 1]
            F += [[a, d, cc], [a, cc, b]]
            FUV += [[(ua, around[k]), (ub, around[k]), (ub, around[k + 1])],
                    [(ua, around[k]), (ub, around[k + 1]), (ua, around[k + 1])]]
    V = list(V)
    if not closed and caps:
        for ring, sign in ((0, -1), (N - 1, 1)):
            ci = len(V)
            V.append(pts[ring])
            for k in range(segs):
                k2 = (k + 1) % segs
                a, b = ring * segs + k, ring * segs + k2
                F.append([ci, b, a] if sign < 0 else [ci, a, b])
                FUV.append([(0, 0), (0, 0), (0, 0)])
    m = Mesh(np.array(V), np.array(F), np.array(FUV))
    return orient_outward(m)


def orient_outward(m):
    """Flip faces if the (closed) mesh came out inside-out."""
    v0, v1, v2 = (m.V[m.F[:, i]] for i in range(3))
    vol = np.sum(np.einsum("ij,ij->i", v0, np.cross(v1, v2))) / 6.0
    if vol < 0:
        m.F = m.F[:, ::-1]
        if m.FUV is not None:
            m.FUV = m.FUV[:, ::-1]
    return m


def extrude_polygon(poly, thickness, axis_center=0.0, holes=()):
    """Prism from a 2D polygon (u, v) along w, centred on w=axis_center,
    minus circular holes (cx, cy, r). Returns Mesh in (u, v, w)."""
    from manifold3d import CrossSection as CS
    cs = CS([np.asarray(poly, float)])
    for cx, cy, r in holes:
        cs = cs - CS.circle(r, 32).translate((cx, cy))
    man = cs.extrude(thickness).translate((0, 0, axis_center - thickness / 2))
    mm = man.to_mesh()
    V = np.asarray(mm.vert_properties)[:, :3]
    F = np.asarray(mm.tri_verts)
    return Mesh(V, F)


def cylinder(p0, p1, r, segs=20):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    pts = np.linspace(p0, p1, 3)
    return sweep(pts, r, r, segs=segs)


def frame_matrix(origin, ex, ey, ez):
    M = np.eye(4)
    M[:3, 0], M[:3, 1], M[:3, 2], M[:3, 3] = ex, ey, ez, origin
    return M


def rot(axis, ang):
    axis = np.asarray(axis, float) / np.linalg.norm(axis)
    x, y, z = axis
    c, s, C = np.cos(ang), np.sin(ang), 1 - np.cos(ang)
    return np.array([[c + x * x * C, x * y * C - z * s, x * z * C + y * s],
                     [y * x * C + z * s, c + y * y * C, y * z * C - x * s],
                     [z * x * C - y * s, z * y * C + x * s, c + z * z * C]])


# --------------------------------------------------------------- carabiner

# Asymmetric-D centreline in (a, b): a runs down from the top apex (where
# it rests on a web or a sling), b across; spine at +b, gate at -b.
_BINER_CTRL = [(0, 0), (1.7, 6.25), (6.25, 10.8), (12.5, 12.6), (30, 15.5), (50, 17), (66, 17), (79, 13),
               (88, 3), (88, -9), (82, -18), (70, -23), (52, -22), (32, -16.5), (12.5, -12.6), (6.25, -10.8),
               (1.7, -6.25)]


class Biner:
    """A carabiner in local coordinates: x = a (down), y = b, z = plane normal."""
    ROD_R = 5.0

    def __init__(self, gate="wire", scale=1.0):
        c = catmull_closed([(a * scale, b * scale) for a, b in _BINER_CTRL], 10)
        c = resample(c, 1.2, closed=True)
        top = np.argmin(c[:, 0])
        c = np.roll(c, -top, 0)
        c[:, 1] -= c[0, 1]                                 # apex at b = 0
        self.curve = c                                     # closed, starts at the apex
        self.gate = gate
        n = len(c)
        front = np.where(c[:, 1] < -2)[0]
        # hinge: low on the gate side; nose: high on the gate side
        self.hinge = int(front[np.argmin(np.abs(c[front, 0] - 60 * scale))])
        self.nose = int(front[np.argmin(np.abs(c[front, 0] - 9 * scale))])
        self.n = n

    def centerline3(self):
        return np.c_[self.curve, np.zeros(len(self.curve))]

    def bottom_index(self):
        return int(np.argmax(self.curve[:, 0]))

    def meshes(self, color):
        c3 = self.centerline3()
        n = self.n
        h, no = self.hinge, self.nose
        # frame: from nose over the apex, down the spine, round the basket to the hinge
        idx = list(range(no, n)) + list(range(0, h + 1)) if no > h else list(range(no, h + 1))
        # walk the long way round (nose -> apex -> spine -> basket -> hinge)
        if not (0 in idx or len(idx) > n / 2):
            idx = list(range(h, n)) + list(range(0, no + 1))
        fr = c3[idx]
        b = fr[:, 1]
        spine = np.clip((b - 6) / 6, 0, 1)                 # 0 round .. 1 I-beam spine
        hu = 5.0 - 0.8 * spine                             # in-plane half width
        hv = 5.0 + 1.1 * spine                             # out-of-plane half thickness
        # the nose end tapers into a hook
        taper = np.clip(np.arange(len(fr)) / 6.0, 0.55, 1.0)
        hu, hv = hu * taper, hv * taper
        frame = sweep(fr, hu, hv, up=[0, 0, 1], segs=20, power=2.3)
        parts = {f"alu-{color}": [frame]}
        p_h, p_n = c3[h], c3[no]
        L = np.linalg.norm(p_n - p_h)
        t = np.linspace(0, 1, 24)
        out = norm(np.array([0.0, -1.0, 0.0]) * 1 + 0 * p_h)   # outward of the gate side
        chord = p_h[None, :] + t[:, None] * (p_n - p_h)[None, :]
        if self.gate == "wire":
            bow = chord + out * (1.2 * np.sin(np.pi * t))[:, None]
            w1 = bow + np.array([0, 0, 2.6])
            w2 = bow - np.array([0, 0, 2.6])
            th = np.linspace(0, np.pi, 10)[1:-1]
            tip = p_n + (p_n - p_h) / L * 2.0
            arc = tip[None, :] + np.c_[np.zeros_like(th), np.zeros_like(th), 2.6 * np.cos(th)] \
                + ((p_n - p_h) / L)[None, :] * (1.6 * np.sin(th))[:, None]
            wire = np.vstack([w1, arc, w2[::-1]])
            parts["steel"] = [sweep(resample(wire, 0.8, False), 1.05, 1.05, segs=10)]
        else:
            dip = -4.5 if self.gate == "bent" else 1.0
            g = chord + out * (dip * np.sin(np.pi * t))[:, None]
            parts[f"alu-{color}"].append(sweep(g, 3.3, 3.9, up=[0, 0, 1], segs=16, power=2.4))
            # spring-plunger end at the nose
            parts.setdefault("steel", []).append(cylinder(p_n - (p_n - p_h) / L * 3, p_n + (p_n - p_h) / L * 0.5, 2.0, 12))
        # hinge rivet
        parts.setdefault("steel", []).append(cylinder(p_h + [0, 0, -6.4], p_h + [0, 0, 6.4], 1.9, 14))
        return parts

    def basket_point(self, M):
        """World point where a sling or a wire rests (lowest centreline point)
        and the rod direction there."""
        c3 = self.centerline3() @ M[:3, :3].T + M[:3, 3]
        i = int(np.argmin(c3[:, 2]))
        tang = norm(c3[(i + 1) % self.n] - c3[i - 1])
        return c3[i], tang


# ----------------------------------------------------------------- slings

def strap_loop_path(r_top, r_bot, z_bot, neck_top, neck_bot, gap=1.6, step=0.8):
    """Closed teardrop-ish loop in the (y, z) plane: semicircle of radius
    r_top round the origin, two strands down to z_bot where it wraps a
    rod of radius r_bot. neck_* = z range where the strands are sewn
    together (they pinch to +-gap)."""
    pts = []
    th = np.linspace(np.pi, 0, 24)
    pts += [(r_top * np.cos(t), r_top * np.sin(t)) for t in th]           # over the top rod
    zs = np.linspace(0, z_bot, 40)[1:-1]
    for z in zs:                                                           # right strand down
        pts.append((_strand(z, r_top, r_bot, z_bot, neck_top, neck_bot, gap), z))
    th = np.linspace(0, -np.pi, 20)
    pts += [(r_bot * np.cos(t), z_bot + r_bot * np.sin(t)) for t in th]   # under the bottom rod
    for z in zs[::-1]:                                                     # left strand up
        pts.append((-_strand(z, r_top, r_bot, z_bot, neck_top, neck_bot, gap), z))
    yz = resample(np.array(pts), step, closed=True)
    return np.c_[np.zeros(len(yz)), yz]


def _strand(z, r_top, r_bot, z_bot, neck_top, neck_bot, gap):
    if z > neck_top:
        t = (z - 0) / (neck_top - 0)
        return r_top + (gap - r_top) * (3 * t * t - 2 * t ** 3)
    if z < neck_bot:
        t = (z - neck_bot) / (z_bot - neck_bot)
        return gap + (r_bot - gap) * (3 * t * t - 2 * t ** 3)
    return gap


def twist_frame(pts, psi, z_from, z_to):
    """Rotate points about z by psi * w, w = 0 above z_from, 1 below z_to:
    a strap that twists between its top loop and the rest of the piece.
    Returns rotated points and the per-point strap-width direction."""
    w = np.clip((z_from - pts[:, 2]) / max(1e-6, z_from - z_to), 0, 1)
    w = w * w * (3 - 2 * w)
    ang = psi * w
    c, s = np.cos(ang), np.sin(ang)
    out = pts.copy()
    out[:, 0] = pts[:, 0] * c - pts[:, 1] * s
    out[:, 1] = pts[:, 0] * s + pts[:, 1] * c
    up = np.c_[c, s, np.zeros_like(c)]
    return out, up


def rot_z(M, psi):
    R = np.eye(4)
    R[:3, :3] = rot([0, 0, 1], psi)
    return R @ M


# --------------------------------------------------------------- quickdraw

def quickdraw(psi, sling_color, bottom_color="#2f6fc8"):
    """Hangs from the origin (centre of the rod it's clipped to); x is the
    rod direction, z up. psi: twist of the dogbone below its top loop."""
    parts = {}
    r = Biner.ROD_R + 1.7
    z_bot = -118.0
    loop = strap_loop_path(r, r, z_bot, -24, z_bot + 24, gap=2.2)
    pts, up = twist_frame(loop, psi, -10, -30)
    parts[f"sling-{sling_color}"] = [sweep(pts, 1.6, 6.0, closed=True, up=up, segs=14, power=5)]
    # sewn dogbone body (thick, stiff) with bar tacks
    zz = np.linspace(-22, z_bot + 22, 30)
    body = np.c_[np.zeros_like(zz), np.zeros_like(zz), zz]
    bpts, bup = twist_frame(body, psi, -10, -30)
    parts[f"sling-{sling_color}"].append(sweep(bpts, 3.4, 6.6, up=bup, segs=16, power=5))
    tacks = []
    for z0 in (-30, z_bot + 30):
        zz = np.linspace(z0 - 5, z0 + 5, 6)
        tp, tu = twist_frame(np.c_[np.zeros_like(zz), np.zeros_like(zz), zz], psi, -10, -30)
        tacks.append(sweep(tp, 3.65, 6.75, up=tu, segs=16, power=5))
    parts["thread-ffffff"] = tacks
    # rubber keeper round the bottom loop
    kz = z_bot + 9
    th = np.linspace(0, 2 * np.pi, 40, endpoint=False)
    ring = np.c_[7.8 * np.sign(np.cos(th)) * np.abs(np.cos(th)) ** 0.4,
                 4.2 * np.sign(np.sin(th)) * np.abs(np.sin(th)) ** 0.4, np.full_like(th, kz)]
    ring, _ = twist_frame(ring, psi, -10, -30)
    parts["rubber"] = [sweep(ring, 1.6, 4.0, closed=True, up=[0, 0, 1], segs=10, power=4)]
    # bottom carabiner (bent gate), plane = (z, strap width)
    b = Biner("bent", 0.95)
    sw = np.array([np.cos(psi), np.sin(psi), 0.0])
    M = frame_matrix(np.array([0, 0, z_bot]), np.array([0, 0, -1.0]), sw, np.cross([0, 0, -1.0], sw))
    for k, ms in b.meshes(bottom_color).items():
        parts.setdefault(k, []).extend(m.transformed(M) for m in ms)
    return parts


# --------------------------------------------------------------------- cam

def lobe_shape(rmax, flip):
    """2D lobe round its axle at (0, 0): x outward, z up toward the stem.
    Fully expanded (hanging on a rack, springs relaxed) the largest radius
    points sideways and the log-spiral camming face falls away below the
    axle toward the head tip; a heel above the axle takes the trigger
    wire. Returns (CrossSection, trigger-wire attach point)."""
    from manifold3d import CrossSection as CS
    phi = np.radians(np.linspace(-12, 92, 80))           # angle below horizontal
    r = rmax * np.exp(-TAN_CAM * phi)
    s = np.cumsum(np.r_[0, np.hypot(np.diff(r * np.cos(phi)), np.diff(r * np.sin(phi)))])
    r = r - 0.35 * (np.sin(2 * np.pi * s / 2.2) > 0.55)  # shallow grooves across the face
    face = np.c_[r * np.cos(phi), -r * np.sin(phi)]
    # concave back edge from the end of the face back to the hub
    end = face[-1]
    tb = np.linspace(0, 1, 14)[1:-1]
    mid = end * 0.5 + np.array([0.16, 0.10]) * rmax
    back = ((1 - tb) ** 2)[:, None] * end + (2 * (1 - tb) * tb)[:, None] * mid
    poly = np.vstack([[[0.0, 0.0]], face, back])
    if _area(poly) < 0:
        poly = poly[::-1]
    hub_r = 4.2 + 0.05 * rmax
    ear = (0.30 * rmax * np.cos(np.radians(70)), 0.30 * rmax * np.sin(np.radians(70)))
    shape = CS([poly]) + CS.batch_hull([CS.circle(hub_r, 32), CS.circle(1.6 + 0.07 * rmax, 24).translate(ear)])
    if flip:
        shape = shape.mirror((1, 0))
        ear = (-ear[0], ear[1])
    return shape, ear


def _area(p):
    x, y = p[:, 0], p[:, 1]
    return 0.5 * np.sum(x * np.roll(y, -1) - np.roll(x, -1) * y)


def cam(size, psi):
    """A cam hanging head-down from its sling, which is clipped round the
    rod at the origin (x = rod direction, z up). psi: twist below the
    sling's top loop."""
    width, color, stem_len = CAM_SIZES[size]
    rmax = width / 2
    parts = {}
    # sewn sling: over the rod, down to the thumb loop, bar-tacked
    S = 74.0
    rod_r = Biner.ROD_R + 1.2
    loop = strap_loop_path(rod_r, 3.4, -S, -26, -S + 10, gap=1.25)
    pts, up = twist_frame(loop, psi, -8, -26)
    parts[f"sling-{color}"] = [sweep(pts, 1.1, 5.2, closed=True, up=up, segs=12, power=5)]
    zz = np.linspace(-S + 12, -S + 24, 8)
    tp, tu = twist_frame(np.c_[np.zeros_like(zz), np.zeros_like(zz), zz], psi, -8, -26)
    parts["thread-f2f2f2"] = [sweep(tp, 2.6, 5.5, up=tu, segs=14, power=5)]

    # everything below is rigid and turned by psi
    R = np.eye(4)
    R[:3, :3] = rot([0, 0, 1], psi)
    rigid = {}
    # thumb loop (plane x-z), its top bar at z = -S
    th = np.linspace(0, 2 * np.pi, 60, endpoint=False)
    zc = -S - 11
    # teardrop thumb loop: wide at the top bar, narrowing into the stem
    tw = 13 * np.cos(th) * (0.75 + 0.25 * np.sin(th))
    oval = np.c_[tw, np.zeros_like(th), zc + 11 * np.sin(th)]
    rigid["plastic-3a3d42"] = [sweep(oval, 2.2, 2.9, closed=True, up=[0, 1, 0], segs=14)]
    z_stem_top = zc - 11
    z_trig = z_stem_top - 22
    z_ax = z_stem_top - stem_len
    # stem cable + swaged terminal at the head
    stem = np.c_[np.zeros(30), np.zeros(30), np.linspace(z_stem_top + 2, z_ax + 6, 30)]
    rigid["cable"] = [sweep(stem, 2.3, 2.3, segs=14)]
    rigid.setdefault("alu-b8bcc2", []).append(cylinder([0, 0, z_ax + 13], [0, 0, z_ax + 2], 3.4, 16))
    # trigger bar with finger scallops
    tx = np.linspace(-21, 21, 50)
    tz = z_trig - 3.0 * (np.abs(tx) / 21) ** 2
    trig = np.c_[tx, np.zeros_like(tx), tz]
    hz = 4.6 - 1.4 * np.cos(np.pi * tx / 10.5) ** 2 * (np.abs(tx) > 6)
    rigid.setdefault("plastic-3a3d42", []).append(sweep(trig, 2.6, hz, up=[0, 1, 0], segs=14, power=3))
    # head: four lobes on one axle (axle along y), outer pair to +x, inner pair to -x
    t = 4.2 + 0.035 * width
    c_in = 3.6
    ys_in = [-(c_in + t / 2), c_in + t / 2]
    ys_out = [-(c_in + t + 2.4 + t / 2), c_in + t + 2.4 + t / 2]
    lobes = []
    attach = []
    for ys, flip in ((ys_out, False), (ys_in, True)):
        shape, ear = lobe_shape(rmax, flip)
        sx = -1 if flip else 1
        if rmax > 15:                       # lightening holes in the bigger lobes
            from manifold3d import CrossSection as CS
            for ang, rr, hr in ((-40, 0.58, 0.14), (-80, 0.56, 0.10)):
                a = np.radians(ang)
                shape = shape - CS.circle(hr * rmax, 32).translate((sx * rr * rmax * np.cos(a), rr * rmax * np.sin(a)))
        man = shape.extrude(t).translate((0, 0, -t / 2)).to_mesh()
        m = orient_outward(Mesh(np.asarray(man.vert_properties)[:, :3], np.asarray(man.tri_verts)))
        for y in ys:
            # (u, v, w) -> (x = u, y = w + y, z = v + z_ax)
            M = frame_matrix(np.array([0, y, z_ax]), np.array([1.0, 0, 0]), np.array([0, 0, 1.0]), np.array([0, 1.0, 0]))
            lobes.append(m.transformed(M))
            attach.append(np.array([ear[0], y, z_ax + ear[1]]))
    rigid[f"alu-{color}"] = lobes
    half = abs(ys_out[1]) + t / 2 + 1.2
    rigid.setdefault("steel", []).append(cylinder([0, -half, z_ax], [0, half, z_ax], 2.4, 16))
    for sgn in (-1, 1):
        rigid["steel"].append(cylinder([0, sgn * half, z_ax], [0, sgn * (half + 1.6), z_ax], 3.6, 18))
    # torsion springs between the lobes
    for y0, y1 in ((ys_in[0] + t / 2, ys_in[1] - t / 2),):
        hel_t = np.linspace(0, 1, 120)
        hel = np.c_[3.4 * np.cos(hel_t * 2 * np.pi * 4), y0 + 0.4 + (y1 - y0 - 0.8) * hel_t,
                    z_ax + 3.4 * np.sin(hel_t * 2 * np.pi * 4)]
        rigid["steel"].append(sweep(hel, 0.45, 0.45, segs=8))
    # trigger wires: each trigger end to the two lobes on its side
    for p in attach:
        end = np.array([20.0 if p[0] > 0 else -20.0, 0.0, z_trig - 3])
        wire = np.linspace(end, p, 30)
        wire[:, 1] += np.sin(np.linspace(0, np.pi, 30)) * 0.0
        rigid["steel"].append(sweep(wire, 0.6, 0.6, segs=8))
    for k, ms in rigid.items():
        parts.setdefault(k, []).extend(m.transformed(R) for m in ms)
    return parts


# --------------------------------------------------------- hanging + contact

def parts_points(parts, spacing=2.2):
    allm = Mesh.merge([m for ms in parts.values() for m in ms])
    return allm.sample(spacing)


class Obstacles:
    """Everything already placed: product plate (as a distance field),
    carabiner rods and hung pieces (as point clouds)."""

    def __init__(self, plate_field):
        self.plate = plate_field
        self.clouds = []          # (tree, radius)

    def add_points(self, pts, radius):
        self.clouds.append((cKDTree(pts), radius))

    def hits(self, pts, margin=1.0, ignore=()):
        n = int(np.sum(self.plate.inside(pts, margin)))
        for i, (tree, r) in enumerate(self.clouds):
            if i in ignore:
                continue
            d, _ = tree.query(pts, distance_upper_bound=r + margin)
            n += int(np.sum(np.isfinite(d)))
        return n


def hang(piece_fn, pivot, rod_dir, obstacles, cam_dir, ignore=(), bend_depth=45.0,
         max_drape=40, max_swing=24, tol=12):
    """Find the resting pose of a piece hanging from `pivot`. The sling is
    flexible: over its top `bend_depth` mm it can drape forward over
    whatever is in front of it (a carabiner below, a neighbour), and the
    rigid part below then hangs plumb from there. Tries, in order: the
    piece's broad face toward the viewer, the least drape, the least
    swing; then twisted variants. Returns (parts, deform fn, world points, pose)."""
    rd = np.array([rod_dir[0], rod_dir[1], 0.0])
    rd = rd / (np.linalg.norm(rd) + 1e-9) if np.linalg.norm(rd) > 1e-6 else np.array([1.0, 0, 0])
    base_ang = np.arctan2(rd[1], rd[0])
    ch = np.array([cam_dir[0], cam_dir[1]])
    face = np.arctan2(ch[1], ch[0]) - np.pi / 2 - base_ang
    face = (face + np.pi / 2) % np.pi - np.pi / 2
    psis = [face + np.radians(d) for d in (0, 20, -20, 45, -45, 90)]
    cache = {}
    best = None
    for group in (psis[:3], psis[3:]):
        for drape in range(0, max_drape + 1, 4):
            for swing in range(0, max_swing + 1, 4):
                for psi in group:
                    if psi not in cache:
                        parts = piece_fn(psi)
                        cache[psi] = (parts, parts_points(parts))
                    parts, pts = cache[psi]
                    for roll in (0, 6, -6):
                        f = _deformer(pivot, base_ang, drape, bend_depth, swing, roll)
                        wp = f(pts)
                        h = obstacles.hits(wp, ignore=ignore)
                        if best is None or h < best[0]:
                            best = (h, psi, drape, swing, roll)
                        if h <= tol:
                            return parts, f, wp, (drape, swing, np.degrees(psi), roll)
    h, psi, drape, swing, roll = best
    print(f"   rests touching ({h} contact points)")
    parts, pts = cache[psi]
    f = _deformer(pivot, base_ang, drape, bend_depth, swing, roll)
    return parts, f, f(pts), (drape, swing, np.degrees(psi), roll)


def _deformer(pivot, base_ang, drape, depth, swing, roll):
    """Local piece points (x = rod direction, z up, origin at the rod) ->
    world: turned to the rod, the top `depth` mm of sling sheared forward
    (toward -y) by `drape` mm along a smooth curve, everything below that
    shifted by `drape`, then the whole piece swung/rolled about the pivot."""
    Rb = rot([0, 0, 1], base_ang)
    R2 = rot([1, 0, 0], -np.radians(swing)) @ rot([0, 1, 0], np.radians(roll))

    def f(p):
        q = p @ Rb.T
        t = np.clip(-q[:, 2] / depth, 0, 1)
        q[:, 1] -= drape * (t * t * (3 - 2 * t))
        return q @ R2.T + pivot
    return f


def _pose(pivot, base_ang, swing, roll):
    """Local piece frame (x = rod direction, z up) -> world, swung forward
    by `swing` degrees about the rod-perpendicular horizontal axis toward -y."""
    Rb = rot([0, 0, 1], base_ang)
    # swing so the bottom moves toward -y (the viewer)
    Rs = rot([1, 0, 0], -np.radians(swing))
    Rr = rot([0, 1, 0], np.radians(roll))
    M = np.eye(4)
    M[:3, :3] = Rs @ Rr @ Rb
    M[:3, 3] = pivot
    return M
