"""Builds img/products/<id>-dimensions.jpg for every product in
designs/products.py from its real CAD outline."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.dirname(HERE)

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import PathPatch
from matplotlib.path import Path
import numpy as np

from products import CATALOG

INK, ACC, BG, FILL = "#20232a", "#d85c2a", "#f4f2ee", "#c9ced3"

OPENING_TEXT = {
    "gear-board": "18 closed slots, 15 × 24 mm, in three rows of six",
    "crag-ring": "11 closed windows, 16 × 22 mm; 76 × 26 mm carry handle",
    "rock-ring": "13 closed windows, 16 × 22 mm",
    "double-ring": "20 closed windows, 16 × 22 mm: 13 outer, 7 inner",
    "sport-board": "13 closed slots, 15 × 24 mm: 7 below, 6 above a long window",
    "approach-bar": "7 closed slots, 14 × 22 mm",
    "pocket-bar": "4 closed slots, 15 × 24 mm",
}


def draw_outline(ax, cs):
    verts, codes = [], []
    for poly in cs.to_polygons():
        poly = np.asarray(poly)
        verts += list(poly) + [poly[0]]
        codes += [Path.MOVETO] + [Path.LINETO] * (len(poly) - 1) + [Path.CLOSEPOLY]
    ax.add_patch(PathPatch(Path(verts, codes), fc=FILL, ec=INK, lw=1.5))


def dim(ax, p0, p1, off, label, horiz):
    (x0, y0), (x1, y1) = p0, p1
    if horiz:
        ax.plot([x0, x0], [y0, off], color=INK, lw=.7)
        ax.plot([x1, x1], [y1, off], color=INK, lw=.7)
        ax.annotate("", (x0, off), (x1, off), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.3))
        ax.text((x0 + x1) / 2, off + 3, label, ha="center", va="bottom", fontsize=13, fontweight="bold", color=INK)
    else:
        ax.plot([x0, off], [y0, y0], color=INK, lw=.7)
        ax.plot([x1, off], [y1, y1], color=INK, lw=.7)
        ax.annotate("", (off, y0), (off, y1), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.3))
        ax.text(off + 3, (y0 + y1) / 2, label, ha="left", va="center", fontsize=13, fontweight="bold",
                color=INK, rotation=90)


def main():
    rep = json.load(open(os.path.join(HERE, "products-report.json")))
    for pid, (fn, title, marks, hangs) in CATALOG.items():
        p = fn()
        p.build(marks=marks)
        cs = p.cs
        x0, y0, x1, y1 = cs.bounds()
        w, h = x1 - x0, y1 - y0
        fig_w = 11 if w >= h else 9
        fig, ax = plt.subplots(figsize=(fig_w, fig_w * (h + 70) / (w + 70)), dpi=130)
        fig.patch.set_facecolor(BG)
        ax.set_aspect("equal"); ax.axis("off"); ax.set_facecolor(BG)
        draw_outline(ax, cs)
        dim(ax, (x0, y1), (x1, y1), y1 + 12, f"{w:.0f} mm", True)
        dim(ax, (x1, y0), (x1, y1), x1 + 10, f"{h:.0f} mm", False)
        r = rep[pid]
        lines = [OPENING_TEXT[pid],
                 f"{r['thickness_mm']:g} mm thick · clip strip {r['clip_web_mm'][1]:g} mm · about {r['est_weight_g']} g",
                 "Every opening is fully enclosed: a clipped carabiner can't fall off."]
        for i, line in enumerate(lines):
            ax.text(x0, y0 - 14 - i * 11, line, fontsize=12 if i < 2 else 11, color=INK if i < 2 else "#5a6168")
        ax.set_xlim(x0 - 8, x1 + 28)
        ax.set_ylim(y0 - 14 - len(lines) * 11 - 4, y1 + 30)
        fig.suptitle(title, fontsize=16, fontweight="bold", color=INK, x=0.06, ha="left")
        fig.savefig(os.path.join(ROOT, "img", "products", f"{pid}-dimensions.jpg"), facecolor=BG,
                    bbox_inches="tight", pad_inches=0.3, pil_kwargs={"quality": 88})
        plt.close(fig)
        print(pid, "drawing ok")


if __name__ == "__main__":
    main()
