"""Turn phone photos of printed prototypes into site-ready images.

    pip install pillow pillow-heif        # pillow-heif only for iPhone .HEIC files
    python3 tools/prep_photos.py gear-board IMG_1234.HEIC IMG_1235.jpg ...
    python3 tools/prep_photos.py crag-ring photos/crag/*.jpg --fit

For each photo: applies the phone's rotation, crops to a centred square
(or with --fit, fits the whole photo on a soft background), resizes to
1400 x 1400, strips all metadata (including GPS location, so your home
address doesn't leak), and saves img/photos/<product>-<n>.jpg.

Then it prints the lines to paste into SHOP.photos in js/store-data.js.
Add a short caption with --caption "Gear Board in Ember, loaded" (used as
the image's alt text and the Kickstarter caption).
"""

import argparse
import os
import sys

from PIL import Image, ImageFilter, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "img", "photos")
SIZE = 1400
PRODUCTS = ["gear-board", "crag-ring", "rock-ring", "double-ring", "sport-board", "approach-bar",
            "pocket-bar", "full-kit", "gatekeeper", "cup-cradle"]


def open_any(path):
    if path.lower().endswith((".heic", ".heif")):
        try:
            from pillow_heif import register_heif_opener
            register_heif_opener()
        except ImportError:
            sys.exit("HEIC photo: run  pip install pillow-heif  first (or export as JPEG).")
    return Image.open(path)


def square(im, fit):
    im = ImageOps.exif_transpose(im).convert("RGB")
    if not fit:
        return ImageOps.fit(im, (SIZE, SIZE), Image.LANCZOS, centering=(0.5, 0.45))
    bg = ImageOps.fit(im, (SIZE, SIZE), Image.LANCZOS).filter(ImageFilter.GaussianBlur(40))
    im.thumbnail((SIZE, SIZE), Image.LANCZOS)
    bg.paste(im, ((SIZE - im.width) // 2, (SIZE - im.height) // 2))
    return bg


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("product", choices=PRODUCTS)
    ap.add_argument("photos", nargs="+")
    ap.add_argument("--fit", action="store_true", help="keep the whole photo instead of cropping to a square")
    ap.add_argument("--caption", default="", help="short description, e.g. 'Crag Ring in Rock with a single rack'")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    existing = [f for f in os.listdir(OUT) if f.startswith(a.product + "-")]
    n = len(existing)
    lines = []
    for src in a.photos:
        n += 1
        out = os.path.join(OUT, f"{a.product}-{n}.jpg")
        img = square(open_any(src), a.fit)
        img.save(out, "JPEG", quality=85, optimize=True, progressive=True)   # no exif= -> metadata stripped
        rel = os.path.relpath(out, ROOT).replace(os.sep, "/")
        cap = (a.caption or f"Printed prototype, photo {n}").replace("'", "\\'")
        lines.append(f"      {{ src: '{rel}', alt: '{cap}' }},")
        print(f"saved {rel}")
    print(f"\nPaste into js/store-data.js, inside SHOP.photos['{a.product}'] = [ ... ]:\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
