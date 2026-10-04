"""Builds img/rockring-dimensions.jpg and img/drawbar-dimensions.jpg from the
real CAD outlines in rackhouse_designs.py."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
IMG = os.path.join(os.path.dirname(HERE), "img")

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import numpy as np
import rackhouse_designs as r

INK, ACC, BG, FILL = "#20232a", "#d85c2a", "#f4f2ee", "#c9ced3"


def front_outline(print_part, z_mid):
    """Undo the face-down print rotation and slice through the front plate."""
    return print_part.rotate((0, -180, 0)).slice(z_mid)


def draw_outline(ax, cs):
    """One compound path, filled even-odd, so holes stay open."""
    verts, codes = [], []
    for poly in cs.to_polygons():
        poly = np.asarray(poly)
        verts += list(poly) + [poly[0]]
        codes += [Path.MOVETO] + [Path.LINETO] * (len(poly) - 1) + [Path.CLOSEPOLY]
    path = Path(verts, codes)
    ax.add_patch(PathPatch(path, fc=FILL, ec=INK, lw=1.6, fill=True))


def hdim(ax, x0, x1, y_feat0, y_feat1, y, label, color=INK):
    ax.plot([x0, x0], [y_feat0, y], color=color, lw=.8)
    ax.plot([x1, x1], [y_feat1, y], color=color, lw=.8)
    ax.annotate("", (x0, y), (x1, y), arrowprops=dict(arrowstyle="<->", color=color, lw=1.4))
    ax.text((x0 + x1) / 2, y + 2.5, label, ha="center", va="bottom", fontsize=13, fontweight="bold", color=color)


def vdim(ax, y0, y1, x_feat0, x_feat1, x, label, color=INK):
    ax.plot([x_feat0, x], [y0, y0], color=color, lw=.8)
    ax.plot([x_feat1, x], [y1, y1], color=color, lw=.8)
    ax.annotate("", (x, y0), (x, y1), arrowprops=dict(arrowstyle="<->", color=color, lw=1.4))
    ax.text(x + 3, (y0 + y1) / 2, label, ha="left", va="center", fontsize=13, fontweight="bold", color=color, rotation=90)


def note(ax, xy, xytext, label):
    ax.annotate(label, xy, xytext, fontsize=11, color=INK, ha="left",
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.1))


def rock_ring_drawing():
    _, pp, _ = r.rock_ring()
    cs = front_outline(pp, 7.0)
    x0, y0, x1, y1 = cs.bounds()
    fig, ax = plt.subplots(figsize=(11, 10.5), dpi=130)
    fig.patch.set_facecolor(BG)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_facecolor(BG)
    draw_outline(ax, cs)
    hdim(ax, x0, x1, 0, 0, y1 + 22, f"{x1 - x0:.0f} mm")
    vdim(ax, y0, y1, 0, 16, x1 + 14, f"{y1 - y0:.0f} mm")
    hdim(ax, -92, -72, 0, 0, 10, "20 mm band", color=ACC)
    note(ax, (-46, -53), (-52, -30), "15 numbered clip notches\n(band is 14 × 14 mm\nat each notch)")
    note(ax, (11.5, 33), (8, 4), "Helmet hook\n(13 mm throat for\nthe chin strap)")
    note(ax, (2, 103), (-88, 124), "Keyhole: hangs on one screw")
    ax.text(x0, y0 - 20, "Depth: 14 mm band + 12 mm standoff feet = 26 mm off the wall",
            fontsize=12, color=INK)
    ax.set_xlim(x0 - 10, x1 + 30); ax.set_ylim(y0 - 28, y1 + 40)
    fig.suptitle("Rock Ring V3: full-rack gear ring", fontsize=16, fontweight="bold", color=INK, x=0.06, ha="left")
    fig.savefig(os.path.join(IMG, "rockring-dimensions.jpg"), facecolor=BG, bbox_inches="tight",
                pad_inches=0.3, pil_kwargs={"quality": 90})
    plt.close(fig)


def draw_bar_drawing():
    _, pp, _ = r.draw_bar()
    cs = front_outline(pp, 4.0)
    x0, y0, x1, y1 = cs.bounds()
    fig, ax = plt.subplots(figsize=(14, 5.4), dpi=130)
    fig.patch.set_facecolor(BG)
    ax.set_aspect("equal"); ax.axis("off"); ax.set_facecolor(BG)
    draw_outline(ax, cs)
    hdim(ax, x0, x1, y1, y1, y1 + 14, f"{x1 - x0:.0f} mm")
    vdim(ax, y0, y1, x1, x1, x1 + 8, f"{y1 - y0:.0f} mm")
    hdim(ax, -11, 11, 33, 33, y1 + 3, "22 mm pitch", color=ACC)
    note(ax, (0, 5), (-30, -18), "Clip around the 11 mm bottom rail")
    note(ax, (-88, 12), (-122, -18), "Keyhole (×2)")
    ax.text(x0, y0 - 34, "7 slots, 13 × 22 mm · 8 mm bar + 12 mm standoffs = 20 mm off the wall",
            fontsize=12, color=INK)
    ax.set_xlim(x0 - 30, x1 + 22); ax.set_ylim(y0 - 40, y1 + 24)
    fig.suptitle("Draw Bar: quickdraw & gear rail", fontsize=16, fontweight="bold", color=INK, x=0.06, ha="left")
    fig.savefig(os.path.join(IMG, "drawbar-dimensions.jpg"), facecolor=BG, bbox_inches="tight",
                pad_inches=0.3, pil_kwargs={"quality": 90})
    plt.close(fig)


if __name__ == "__main__":
    rock_ring_drawing()
    draw_bar_drawing()
    print("ok")
