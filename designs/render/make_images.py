"""Renders every site product image.

    python3 -m http.server 8790 --bind 127.0.0.1     # from the repo root
    python3 designs/render/gear.py                    # gear scenes
    python3 designs/render/make_images.py [product ...]

For each product and colorway: 'gear' (loaded with quickdraws or a trad
rack, hanging on its pegs), 'hero' (three-quarter), 'front' and 'edge'.
Writes img/products/<id>-<color>-<view>.jpg and two dark hero shots.
All images are 3D renders of the real product files, not photographs.
"""

import json
import math
import os
import subprocess
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
RAW = os.path.join(HERE, "raw")
OUT = os.path.join(ROOT, "img", "products")
PORT = int(os.environ.get("RENDER_PORT", "8790"))

COLORWAYS = {
    "rock":  {"hex": "#63707c", "bg": ((234, 236, 237), (206, 211, 215))},
    "moss":  {"hex": "#55805a", "bg": ((232, 237, 229), (205, 215, 199))},
    "ice":   {"hex": "#4a90c2", "bg": ((228, 236, 242), (198, 215, 227))},
    "sand":  {"hex": "#c9a86a", "bg": ((241, 234, 220), (223, 209, 182))},
    "ink":   {"hex": "#2a2d31", "bg": ((232, 232, 232), (205, 205, 207))},
    "ember": {"hex": "#d85c2a", "bg": ((248, 229, 218), (238, 199, 177))},
}
VIEWS = {
    "gear":  dict(elev=12, azim=-68, zoom=0.95),
    "hero":  dict(elev=16, azim=-62, zoom=1.0),
    "front": dict(elev=4, azim=-90, zoom=1.0),
    "edge":  dict(elev=24, azim=-25, zoom=1.0),
}


def trim(img, pad=30):
    bb = img.getbbox()
    l, t, r, b = bb
    return img.crop((max(0, l - pad), max(0, t - pad), min(img.width, r + pad), min(img.height, b + pad)))


def linear_bg(size, top, bottom):
    w, h = size
    g = Image.new("RGB", (1, h))
    for y in range(h):
        t = y / (h - 1)
        g.putpixel((0, y), tuple(int(top[i] + (bottom[i] - top[i]) * t) for i in range(3)))
    return g.resize((w, h))


def radial_bg(size, center, edge, cxr=0.62, cyr=0.42):
    w, h = size
    yy, xx = np.mgrid[0:h, 0:w]
    cx, cy = w * cxr, h * cyr
    maxr = math.hypot(max(cx, w - cx), max(cy, h - cy))
    d = np.clip(np.hypot(xx - cx, yy - cy) / maxr, 0, 1)[..., None]
    arr = (np.array(center)[None, None, :] * (1 - d) + np.array(edge)[None, None, :] * d).astype("uint8")
    return Image.fromarray(arr, "RGB")


def composite(prod_path, bg, scale, shadow_alpha=95):
    W, H = bg.size
    bg = bg.convert("RGBA")
    prod = trim(Image.open(prod_path).convert("RGBA"))
    r = min(W * scale / prod.width, H * scale / prod.height)
    tw, th = int(prod.width * r), int(prod.height * r)
    prod = prod.resize((tw, th), Image.LANCZOS)
    px, py = (W - tw) // 2, (H - th) // 2
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(sh)
    sw, shh = int(tw * 0.6), max(8, int(tw * 0.08))
    cx, cy = W // 2, py + th - int(th * 0.01)
    d.ellipse([cx - sw // 2, cy - shh // 2, cx + sw // 2, cy + shh // 2], fill=(0, 0, 0, shadow_alpha))
    sh = sh.filter(ImageFilter.GaussianBlur(max(6, int(tw * 0.04))))
    bg = Image.alpha_composite(bg, sh)
    bg.alpha_composite(prod, (px, py))
    return bg.convert("RGB")


def main(only=None):
    scenes = json.load(open(os.path.join(HERE, "scenes", "scenes.json")))
    pids = [p for p in scenes if not only or p in only]
    os.makedirs(RAW, exist_ok=True)
    os.makedirs(OUT, exist_ok=True)
    jobs = []
    for pid in pids:
        for ck, cw in COLORWAYS.items():
            product = {"stl": f"models/{pid}.stl", "color": cw["hex"], "roughness": 0.62}
            for vk, v in VIEWS.items():
                parts = [product] + (scenes[pid]["parts"] if vk == "gear" else [])
                jobs.append({"out": os.path.join(RAW, f"{pid}-{ck}-{vk}.png"),
                             "opts": dict(parts=parts, size=1400, **v)})
    for pid in ("gear-board", "crag-ring"):
        if pid in pids:
            parts = [{"stl": f"models/{pid}.stl", "color": "#d85c2a", "roughness": 0.62}] + scenes[pid]["parts"]
            jobs.append({"out": os.path.join(RAW, f"{pid}-dark.png"),
                         "opts": dict(parts=parts, size=1600, elev=10, azim=-64, zoom=0.95)})
    with open(os.path.join(RAW, "jobs.json"), "w") as f:
        json.dump(jobs, f)
    subprocess.run([sys.executable, os.path.join(HERE, "drive.py"), os.path.join(RAW, "jobs.json"), str(PORT)], check=True)

    for pid in pids:
        for ck, cw in COLORWAYS.items():
            for vk in VIEWS:
                scale = 0.80 if vk == "gear" else 0.74
                img = composite(os.path.join(RAW, f"{pid}-{ck}-{vk}.png"), linear_bg((1400, 1400), *cw["bg"]), scale)
                img.save(os.path.join(OUT, f"{pid}-{ck}-{vk}.jpg"), quality=88, optimize=True, progressive=True)
    for pid in ("gear-board", "crag-ring"):
        if pid in pids:
            img = composite(os.path.join(RAW, f"{pid}-dark.png"), radial_bg((2000, 1400), (58, 30, 18), (10, 11, 10)),
                            0.84, shadow_alpha=150)
            img.save(os.path.join(OUT, f"{pid}-hero-dark.jpg"), quality=88, optimize=True, progressive=True)
    print("rendered", len(jobs), "views for", ", ".join(pids))


if __name__ == "__main__":
    main(sys.argv[1:] or None)
