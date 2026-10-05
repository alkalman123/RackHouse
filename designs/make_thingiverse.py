"""Builds designs/rackhouse-thingiverse-upload.zip and the organizer
sections of business/THINGIVERSE-UPLOAD.md.

One folder per design: files/ (STL), images/ (5), LICENSE.txt,
DESCRIPTION.md. The Gatekeeper and Cup Cradle folders are carried over
from the existing zip; the seven organizers are generated from
designs/products-report.json and the site renders.
"""
import io
import json
import os
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ZIP = os.path.join(HERE, "rackhouse-thingiverse-upload.zip")
DOC = os.path.join(ROOT, "business", "THINGIVERSE-UPLOAD.md")
SITE = "https://alkalman123.github.io/RackHouse/"
KEEP = ("rackhouse-gatekeeper-v3/", "rackhouse-cup-cradle-v2/")

ORG = {
    "gear-board": ("Gear Board", "Trad Rack & Quickdraw Wall Board", "ember",
                   "Your whole rack on one board: 18 fully enclosed slots in three rows of six. Quickdraws on the bottom row, cams and nuts on the rows above, each hanging through its own window so nothing tangles.",
                   "trad rack, quickdraw, gear board, cam rack, gear organizer, carabiner holder, wall rack, garage organization"),
    "crag-ring": ("Crag Ring", "Gear Ring with Carry Handle", "rock",
                  "A light 7 mm gear ring with 11 fully enclosed windows and a hand-size carry handle. Rack your cams, carry it to the crag like a bag, then clip the handle to a sling or a tree.",
                  "trad rack, gear ring, carry handle, cam rack, crag, gear organizer, carabiner holder"),
    "rock-ring": ("Rock Ring", "Flat Trad Gear Ring", "sand",
                  "A flat gear ring with 13 fully enclosed windows: a single rack of cams plus nuts in size order around the ring. Nothing sticks out, so it packs flat and never snags.",
                  "trad rack, gear ring, cam rack, gear organizer, carabiner holder, wall hanger"),
    "double-ring": ("Double Ring", "Two-Row Gear Ring for Cams & Draws", "ice",
                    "A two-row gear ring with 20 fully enclosed windows: 13 around the outside for cams and 7 on the inner row for quickdraws, nuts and a nut tool.",
                    "trad rack, gear ring, quickdraw, cam rack, gear organizer, carabiner holder"),
    "sport-board": ("Sport Board", "Quickdraw Wall Board", "moss",
                    "A two-row board for a sport rack: 7 closed slots below and 6 above, whose quickdraws hang through a long window so the rows never tangle.",
                    "quickdraw, sport climbing, gear board, gear organizer, carabiner holder, wall rack"),
    "approach-bar": ("Approach Bar", "Ultralight Quickdraw Bar", "ink",
                     "An ultralight 6 mm bar for 7 quickdraws, about 36 g: light enough to live in your pack.",
                     "quickdraw, ultralight, gear bar, gear organizer, carabiner holder, backpack"),
    "pocket-bar": ("Pocket Bar", "4-Slot Carabiner Bar", "ember",
                   "A 130 mm bar with 4 enclosed slots for a pack lid, glovebox or crag bag: a nut tool, a couple of draws, a belay device and a locker.",
                   "carabiner holder, quickdraw, nut tool, gear organizer, glovebox, backpack"),
}
VER = "v1"


def license_text():
    return open(os.path.join(HERE, "LICENSE")).read()


def description(pid, r):
    name, sub, _, blurb, _ = ORG[pid]
    w, h, t = r["size_mm"]
    return f"""# {name}: {sub.lower()}

{blurb}

- **Every opening is fully enclosed.** Once a carabiner's gate closes through it, it can't slide off in any direction: on a wall, in a car, in a pack or at the crag.
- **{r['openings']} clip openings**, each at least 14 mm wide, with a {r['clip_web_mm'][0]:g}-{r['clip_web_mm'][1]:g} mm strip a carabiner gate closes around.
- **Hangs from:** {r['hang'].lower()}.
- **RACKHOUSE / NOT FOR CLIMBING** debossed into the face.

Size: {w:g} x {h:g} mm, {t:g} mm thick. About {r['est_weight_g']} g.

## Printing
Prints **flat, text up**, exactly as exported, **no supports**. Fits a 210 mm bed (Ender 3, Prusa MK3/MK4, Bambu A1/P1/X1).
0.2 mm layers, **4 walls, 30% gyroid**. PLA+ indoors, PETG if it lives in a hot car.

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0). Print and remix it for yourself. Please don't sell prints or files. Commercial rights are reserved by Rackhouse Supply Co.; contact rackhousesupplyco@gmail.com for a commercial license.

**Not climbing equipment.** Never use this part in a climbing, rescue or fall-protection system.

Don't have a printer? Buy one printed to order in six colors at {SITE}
"""


def images(pid, color):
    p = f"img/products/{pid}"
    alt = "rock" if color != "rock" else "moss"
    return [f"{p}-{color}-gear.jpg", f"{p}-dimensions.jpg", f"{p}-{color}-hero.jpg", f"{p}-{alt}-front.jpg", f"{p}-ink-gear.jpg"]


def doc_section(pid, r):
    name, sub, _, _, tags = ORG[pid]
    folder = f"rackhouse-{pid}-{VER}"
    title = f"{name} - {sub} (Rackhouse)"
    return f"""## {title}

**Folder in the upload zip:** `{folder}/`

| Field on Thingiverse | Enter this |
|---|---|
| Thing name | {title} |
| Category | Hobby > Sport & Outdoors |
| License | **Creative Commons - Attribution - Non-Commercial - Share Alike** |
| This is a remix | **Leave OFF** (original design) |
| Tags | climbing, {tags}, rackhouse |
| Files | `files/` (the STL) and `LICENSE.txt` |
| Images | `images/` in numbered order. Image 01 becomes the thumbnail. The images are 3D renders: add a photo of your own print once you have one. |
| Print settings → Supports / Rafts | No / No |
| Print settings → Resolution | 0.2 mm |
| Print settings → Infill | 30% gyroid, 4 walls |
| Print settings → Filament | PLA+ or PETG |
| Print settings → Notes | Print flat, text up, as exported. |

**Description** (paste into the Summary/Description box; it's also in `DESCRIPTION.md`):

````markdown
{description(pid, r).rstrip()}
````

"""


def main():
    rep = json.load(open(os.path.join(HERE, "products-report.json")))
    old = zipfile.ZipFile(ZIP)
    kept = {n: old.read(n) for n in old.namelist() if n.startswith(KEEP) and not n.endswith("/")}
    old.close()
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        for pid, (_, _, color, _, _) in ORG.items():
            f = f"rackhouse-{pid}-{VER}/"
            z.write(os.path.join(HERE, "print-ready", f"rackhouse-{pid}.stl"), f + f"files/rackhouse-{pid}.stl")
            for i, im in enumerate(images(pid, color), 1):
                z.write(os.path.join(ROOT, im), f + f"images/{i:02d}-{os.path.basename(im)}")
            z.writestr(f + "LICENSE.txt", license_text())
            z.writestr(f + "DESCRIPTION.md", description(pid, rep[pid]))
        for n, data in kept.items():
            if n.endswith("LICENSE.txt"):
                data = license_text().encode()
            z.writestr(n, data)
    open(ZIP, "wb").write(buf.getvalue())

    s = open(DOC).read()
    a, b = "<!-- organizers:start -->", "<!-- organizers:end -->"
    i, j = s.index(a) + len(a), s.index(b)
    s = s[:i] + "\n\n" + "".join(doc_section(pid, rep[pid]) for pid in ORG) + "---\n\n" + s[j:]
    open(DOC, "w").write(s)
    print("zip:", len(kept), "kept files +", len(ORG), "organizer folders")


if __name__ == "__main__":
    main()
