# Posting the designs on Thingiverse (and licensing them)

Everything is prepared. Posting has to happen from **your** Thingiverse
account, because Thingiverse only publishes things under the logged-in
owner's name. That's also what puts the designs under your name and
license. It takes about 10 minutes per design.

## What you're uploading

`designs/rackhouse-thingiverse-upload.zip` (in the repo, or the copy sent
to you in chat) contains one folder per design:

```
rackhouse-gear-board-v1/    files/ (STL), images/ (5), LICENSE.txt, DESCRIPTION.md
rackhouse-crag-ring-v1/     same
rackhouse-rock-ring-v1/     same
rackhouse-double-ring-v1/   same
rackhouse-sport-board-v1/   same
rackhouse-approach-bar-v1/  same
rackhouse-pocket-bar-v1/    same
rackhouse-gatekeeper-v3/    same
rackhouse-cup-cradle-v2/    same
```

Post the Gear Board and Crag Ring first; they're the two lead products.
Rebuild the zip and the organizer sections below after any design change
with `python3 designs/make_thingiverse.py`.

## The license, and why this one

Pick **Creative Commons - Attribution - Non-Commercial - Share Alike**
(CC BY-NC-SA 4.0) on every upload.

- **You** keep full ownership and the only right to sell prints. A CC
  license is permission you give *other people*; it never limits the
  owner.
- **Everyone else** can print and remix for personal use, must credit
  Rackhouse, can't sell, and has to keep remixes non-commercial too.
- Want nobody posting modified versions at all? Choose
  *Attribution - Non-Commercial - No Derivatives* instead. You'll get less
  community remixing, which is free marketing.

**Do NOT mark these as a remix** of anything, including the old
Gatekeeper / Rock Ring / Cup Cradle things. They're new, original designs (see
`LEGAL-AND-ENTITY-FORMATION.md` §4c). Marking them as remixes would
attach the original creator's non-commercial license to your work.

## Step by step (per design)

1. Go to **thingiverse.com** and sign in (or create a free account; use
   the business email, rackhousesupplyco@gmail.com).
2. One-time profile setup: set the display name to **Rackhouse Supply Co.**,
   add the logo as your avatar, and put
   `https://alkalman123.github.io/RackHouse/` in the website field.
3. Click **Create** (top right), then **Upload a Thing**.
4. Drag in the STL from the design's `files/` folder, plus `LICENSE.txt`.
5. Fill in the fields from the table below for that design.
6. Upload the images from `images/` in numbered order (`01-…` becomes
   the thumbnail).
7. Leave **"This is a remix"** off and **"Work in progress"** off.
8. Click **Publish**. Copy the thing's URL into the table at the bottom
   of this file.

## Also post on Printables and MakerWorld (optional, recommended)

The same zip works on **printables.com** (Prusa) and **makerworld.com**
(Bambu Lab), which get more traffic than Thingiverse today. Choose the
same CC BY-NC-SA 4.0 license and don't tick any remix/"based on" option.
MakerWorld can also host a print profile (`.3mf`). After your first real
print, export your slicer project and upload it there.

---

<!-- organizers:start -->

## Gear Board - Trad Rack & Quickdraw Wall Board (Rackhouse)

**Folder in the upload zip:** `rackhouse-gear-board-v1/`

| Field on Thingiverse | Enter this |
|---|---|
| Thing name | Gear Board - Trad Rack & Quickdraw Wall Board (Rackhouse) |
| Category | Hobby > Sport & Outdoors |
| License | **Creative Commons - Attribution - Non-Commercial - Share Alike** |
| This is a remix | **Leave OFF** (original design) |
| Tags | climbing, trad rack, quickdraw, gear board, cam rack, gear organizer, carabiner holder, wall rack, garage organization, rackhouse |
| Files | `files/` (the STL) and `LICENSE.txt` |
| Images | `images/` in numbered order. Image 01 becomes the thumbnail. The images are 3D renders: add a photo of your own print once you have one. |
| Print settings → Supports / Rafts | No / No |
| Print settings → Resolution | 0.2 mm |
| Print settings → Infill | 30% gyroid, 4 walls |
| Print settings → Filament | PLA+ or PETG |
| Print settings → Notes | Print flat, text up, as exported. |

**Description** (paste into the Summary/Description box; it's also in `DESCRIPTION.md`):

````markdown
# Gear Board: trad rack & quickdraw wall board

Your whole rack on one board: 18 fully enclosed slots in three rows of six. Quickdraws on the bottom row, cams and nuts on the rows above, each hanging through its own window so nothing tangles.

- **Every opening is fully enclosed.** Once a carabiner's gate closes through it, it can't slide off in any direction: on a wall, in a car, in a pack or at the crag.
- **18 clip openings**, each at least 14 mm wide, with a 8-9 mm strip a carabiner gate closes around.
- **Hangs from:** two top slots: hooks, screws with washers or a sling.
- **RACKHOUSE / NOT FOR CLIMBING** debossed into the face.

Size: 200 x 169 mm, 9 mm thick. About 171 g.

## Printing
Prints **flat, text up**, exactly as exported, **no supports**. Fits a 210 mm bed (Ender 3, Prusa MK3/MK4, Bambu A1/P1/X1).
0.2 mm layers, **4 walls, 30% gyroid**. PLA+ indoors, PETG if it lives in a hot car.

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0). Print and remix it for yourself. Please don't sell prints or files. Commercial rights are reserved by Rackhouse Supply Co.; contact rackhousesupplyco@gmail.com for a commercial license.

**Not climbing equipment.** Never use this part in a climbing, rescue or fall-protection system.

Don't have a printer? Buy one printed to order in six colors at https://alkalman123.github.io/RackHouse/
````

## Crag Ring - Gear Ring with Carry Handle (Rackhouse)

**Folder in the upload zip:** `rackhouse-crag-ring-v1/`

| Field on Thingiverse | Enter this |
|---|---|
| Thing name | Crag Ring - Gear Ring with Carry Handle (Rackhouse) |
| Category | Hobby > Sport & Outdoors |
| License | **Creative Commons - Attribution - Non-Commercial - Share Alike** |
| This is a remix | **Leave OFF** (original design) |
| Tags | climbing, trad rack, gear ring, carry handle, cam rack, crag, gear organizer, carabiner holder, rackhouse |
| Files | `files/` (the STL) and `LICENSE.txt` |
| Images | `images/` in numbered order. Image 01 becomes the thumbnail. The images are 3D renders: add a photo of your own print once you have one. |
| Print settings → Supports / Rafts | No / No |
| Print settings → Resolution | 0.2 mm |
| Print settings → Infill | 30% gyroid, 4 walls |
| Print settings → Filament | PLA+ or PETG |
| Print settings → Notes | Print flat, text up, as exported. |

**Description** (paste into the Summary/Description box; it's also in `DESCRIPTION.md`):

````markdown
# Crag Ring: gear ring with carry handle

A light 7 mm gear ring with 11 fully enclosed windows and a hand-size carry handle. Rack your cams, carry it to the crag like a bag, then clip the handle to a sling or a tree.

- **Every opening is fully enclosed.** Once a carabiner's gate closes through it, it can't slide off in any direction: on a wall, in a car, in a pack or at the crag.
- **11 clip openings**, each at least 14 mm wide, with a 6-6 mm strip a carabiner gate closes around.
- **Hangs from:** hand-carry handle (76 x 26 mm opening); also clips to a sling or hook.
- **RACKHOUSE / NOT FOR CLIMBING** debossed into the face.

Size: 152 x 190 mm, 7 mm thick. About 72 g.

## Printing
Prints **flat, text up**, exactly as exported, **no supports**. Fits a 210 mm bed (Ender 3, Prusa MK3/MK4, Bambu A1/P1/X1).
0.2 mm layers, **4 walls, 30% gyroid**. PLA+ indoors, PETG if it lives in a hot car.

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0). Print and remix it for yourself. Please don't sell prints or files. Commercial rights are reserved by Rackhouse Supply Co.; contact rackhousesupplyco@gmail.com for a commercial license.

**Not climbing equipment.** Never use this part in a climbing, rescue or fall-protection system.

Don't have a printer? Buy one printed to order in six colors at https://alkalman123.github.io/RackHouse/
````

## Rock Ring - Flat Trad Gear Ring (Rackhouse)

**Folder in the upload zip:** `rackhouse-rock-ring-v1/`

| Field on Thingiverse | Enter this |
|---|---|
| Thing name | Rock Ring - Flat Trad Gear Ring (Rackhouse) |
| Category | Hobby > Sport & Outdoors |
| License | **Creative Commons - Attribution - Non-Commercial - Share Alike** |
| This is a remix | **Leave OFF** (original design) |
| Tags | climbing, trad rack, gear ring, cam rack, gear organizer, carabiner holder, wall hanger, rackhouse |
| Files | `files/` (the STL) and `LICENSE.txt` |
| Images | `images/` in numbered order. Image 01 becomes the thumbnail. The images are 3D renders: add a photo of your own print once you have one. |
| Print settings → Supports / Rafts | No / No |
| Print settings → Resolution | 0.2 mm |
| Print settings → Infill | 30% gyroid, 4 walls |
| Print settings → Filament | PLA+ or PETG |
| Print settings → Notes | Print flat, text up, as exported. |

**Description** (paste into the Summary/Description box; it's also in `DESCRIPTION.md`):

````markdown
# Rock Ring: flat trad gear ring

A flat gear ring with 13 fully enclosed windows: a single rack of cams plus nuts in size order around the ring. Nothing sticks out, so it packs flat and never snags.

- **Every opening is fully enclosed.** Once a carabiner's gate closes through it, it can't slide off in any direction: on a wall, in a car, in a pack or at the crag.
- **13 clip openings**, each at least 14 mm wide, with a 7.9-7.9 mm strip a carabiner gate closes around.
- **Hangs from:** top eye: hook, carabiner or sling.
- **RACKHOUSE / NOT FOR CLIMBING** debossed into the face.

Size: 176 x 203 mm, 9 mm thick. About 91 g.

## Printing
Prints **flat, text up**, exactly as exported, **no supports**. Fits a 210 mm bed (Ender 3, Prusa MK3/MK4, Bambu A1/P1/X1).
0.2 mm layers, **4 walls, 30% gyroid**. PLA+ indoors, PETG if it lives in a hot car.

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0). Print and remix it for yourself. Please don't sell prints or files. Commercial rights are reserved by Rackhouse Supply Co.; contact rackhousesupplyco@gmail.com for a commercial license.

**Not climbing equipment.** Never use this part in a climbing, rescue or fall-protection system.

Don't have a printer? Buy one printed to order in six colors at https://alkalman123.github.io/RackHouse/
````

## Double Ring - Two-Row Gear Ring for Cams & Draws (Rackhouse)

**Folder in the upload zip:** `rackhouse-double-ring-v1/`

| Field on Thingiverse | Enter this |
|---|---|
| Thing name | Double Ring - Two-Row Gear Ring for Cams & Draws (Rackhouse) |
| Category | Hobby > Sport & Outdoors |
| License | **Creative Commons - Attribution - Non-Commercial - Share Alike** |
| This is a remix | **Leave OFF** (original design) |
| Tags | climbing, trad rack, gear ring, quickdraw, cam rack, gear organizer, carabiner holder, rackhouse |
| Files | `files/` (the STL) and `LICENSE.txt` |
| Images | `images/` in numbered order. Image 01 becomes the thumbnail. The images are 3D renders: add a photo of your own print once you have one. |
| Print settings → Supports / Rafts | No / No |
| Print settings → Resolution | 0.2 mm |
| Print settings → Infill | 30% gyroid, 4 walls |
| Print settings → Filament | PLA+ or PETG |
| Print settings → Notes | Print flat, text up, as exported. |

**Description** (paste into the Summary/Description box; it's also in `DESCRIPTION.md`):

````markdown
# Double Ring: two-row gear ring for cams & draws

A two-row gear ring with 20 fully enclosed windows: 13 around the outside for cams and 7 on the inner row for quickdraws, nuts and a nut tool.

- **Every opening is fully enclosed.** Once a carabiner's gate closes through it, it can't slide off in any direction: on a wall, in a car, in a pack or at the crag.
- **20 clip openings**, each at least 14 mm wide, with a 6-7.9 mm strip a carabiner gate closes around.
- **Hangs from:** top eye: hook, carabiner or sling.
- **RACKHOUSE / NOT FOR CLIMBING** debossed into the face.

Size: 180 x 207 mm, 9 mm thick. About 122 g.

## Printing
Prints **flat, text up**, exactly as exported, **no supports**. Fits a 210 mm bed (Ender 3, Prusa MK3/MK4, Bambu A1/P1/X1).
0.2 mm layers, **4 walls, 30% gyroid**. PLA+ indoors, PETG if it lives in a hot car.

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0). Print and remix it for yourself. Please don't sell prints or files. Commercial rights are reserved by Rackhouse Supply Co.; contact rackhousesupplyco@gmail.com for a commercial license.

**Not climbing equipment.** Never use this part in a climbing, rescue or fall-protection system.

Don't have a printer? Buy one printed to order in six colors at https://alkalman123.github.io/RackHouse/
````

## Sport Board - Quickdraw Wall Board (Rackhouse)

**Folder in the upload zip:** `rackhouse-sport-board-v1/`

| Field on Thingiverse | Enter this |
|---|---|
| Thing name | Sport Board - Quickdraw Wall Board (Rackhouse) |
| Category | Hobby > Sport & Outdoors |
| License | **Creative Commons - Attribution - Non-Commercial - Share Alike** |
| This is a remix | **Leave OFF** (original design) |
| Tags | climbing, quickdraw, sport climbing, gear board, gear organizer, carabiner holder, wall rack, rackhouse |
| Files | `files/` (the STL) and `LICENSE.txt` |
| Images | `images/` in numbered order. Image 01 becomes the thumbnail. The images are 3D renders: add a photo of your own print once you have one. |
| Print settings → Supports / Rafts | No / No |
| Print settings → Resolution | 0.2 mm |
| Print settings → Infill | 30% gyroid, 4 walls |
| Print settings → Filament | PLA+ or PETG |
| Print settings → Notes | Print flat, text up, as exported. |

**Description** (paste into the Summary/Description box; it's also in `DESCRIPTION.md`):

````markdown
# Sport Board: quickdraw wall board

A two-row board for a sport rack: 7 closed slots below and 6 above, whose quickdraws hang through a long window so the rows never tangle.

- **Every opening is fully enclosed.** Once a carabiner's gate closes through it, it can't slide off in any direction: on a wall, in a car, in a pack or at the crag.
- **13 clip openings**, each at least 14 mm wide, with a 6-9 mm strip a carabiner gate closes around.
- **Hangs from:** end slots: two hooks, two screws with washers, or a sling through both.
- **RACKHOUSE / NOT FOR CLIMBING** debossed into the face.

Size: 200 x 97 mm, 9 mm thick. About 100 g.

## Printing
Prints **flat, text up**, exactly as exported, **no supports**. Fits a 210 mm bed (Ender 3, Prusa MK3/MK4, Bambu A1/P1/X1).
0.2 mm layers, **4 walls, 30% gyroid**. PLA+ indoors, PETG if it lives in a hot car.

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0). Print and remix it for yourself. Please don't sell prints or files. Commercial rights are reserved by Rackhouse Supply Co.; contact rackhousesupplyco@gmail.com for a commercial license.

**Not climbing equipment.** Never use this part in a climbing, rescue or fall-protection system.

Don't have a printer? Buy one printed to order in six colors at https://alkalman123.github.io/RackHouse/
````

## Approach Bar - Ultralight Quickdraw Bar (Rackhouse)

**Folder in the upload zip:** `rackhouse-approach-bar-v1/`

| Field on Thingiverse | Enter this |
|---|---|
| Thing name | Approach Bar - Ultralight Quickdraw Bar (Rackhouse) |
| Category | Hobby > Sport & Outdoors |
| License | **Creative Commons - Attribution - Non-Commercial - Share Alike** |
| This is a remix | **Leave OFF** (original design) |
| Tags | climbing, quickdraw, ultralight, gear bar, gear organizer, carabiner holder, backpack, rackhouse |
| Files | `files/` (the STL) and `LICENSE.txt` |
| Images | `images/` in numbered order. Image 01 becomes the thumbnail. The images are 3D renders: add a photo of your own print once you have one. |
| Print settings → Supports / Rafts | No / No |
| Print settings → Resolution | 0.2 mm |
| Print settings → Infill | 30% gyroid, 4 walls |
| Print settings → Filament | PLA+ or PETG |
| Print settings → Notes | Print flat, text up, as exported. |

**Description** (paste into the Summary/Description box; it's also in `DESCRIPTION.md`):

````markdown
# Approach Bar: ultralight quickdraw bar

An ultralight 6 mm bar for 7 quickdraws, about 36 g: light enough to live in your pack.

- **Every opening is fully enclosed.** Once a carabiner's gate closes through it, it can't slide off in any direction: on a wall, in a car, in a pack or at the crag.
- **7 clip openings**, each at least 14 mm wide, with a 8-8 mm strip a carabiner gate closes around.
- **Hangs from:** end slots: two hooks, two screws with washers, or a sling through both.
- **RACKHOUSE / NOT FOR CLIMBING** debossed into the face.

Size: 200 x 40 mm, 6 mm thick. About 36 g.

## Printing
Prints **flat, text up**, exactly as exported, **no supports**. Fits a 210 mm bed (Ender 3, Prusa MK3/MK4, Bambu A1/P1/X1).
0.2 mm layers, **4 walls, 30% gyroid**. PLA+ indoors, PETG if it lives in a hot car.

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0). Print and remix it for yourself. Please don't sell prints or files. Commercial rights are reserved by Rackhouse Supply Co.; contact rackhousesupplyco@gmail.com for a commercial license.

**Not climbing equipment.** Never use this part in a climbing, rescue or fall-protection system.

Don't have a printer? Buy one printed to order in six colors at https://alkalman123.github.io/RackHouse/
````

## Pocket Bar - 4-Slot Carabiner Bar (Rackhouse)

**Folder in the upload zip:** `rackhouse-pocket-bar-v1/`

| Field on Thingiverse | Enter this |
|---|---|
| Thing name | Pocket Bar - 4-Slot Carabiner Bar (Rackhouse) |
| Category | Hobby > Sport & Outdoors |
| License | **Creative Commons - Attribution - Non-Commercial - Share Alike** |
| This is a remix | **Leave OFF** (original design) |
| Tags | climbing, carabiner holder, quickdraw, nut tool, gear organizer, glovebox, backpack, rackhouse |
| Files | `files/` (the STL) and `LICENSE.txt` |
| Images | `images/` in numbered order. Image 01 becomes the thumbnail. The images are 3D renders: add a photo of your own print once you have one. |
| Print settings → Supports / Rafts | No / No |
| Print settings → Resolution | 0.2 mm |
| Print settings → Infill | 30% gyroid, 4 walls |
| Print settings → Filament | PLA+ or PETG |
| Print settings → Notes | Print flat, text up, as exported. |

**Description** (paste into the Summary/Description box; it's also in `DESCRIPTION.md`):

````markdown
# Pocket Bar: 4-slot carabiner bar

A 130 mm bar with 4 enclosed slots for a pack lid, glovebox or crag bag: a nut tool, a couple of draws, a belay device and a locker.

- **Every opening is fully enclosed.** Once a carabiner's gate closes through it, it can't slide off in any direction: on a wall, in a car, in a pack or at the crag.
- **4 clip openings**, each at least 14 mm wide, with a 9-9 mm strip a carabiner gate closes around.
- **Hangs from:** end slots: two hooks, two screws with washers, or a sling through both.
- **RACKHOUSE / NOT FOR CLIMBING** debossed into the face.

Size: 130 x 44 mm, 9 mm thick. About 33 g.

## Printing
Prints **flat, text up**, exactly as exported, **no supports**. Fits a 210 mm bed (Ender 3, Prusa MK3/MK4, Bambu A1/P1/X1).
0.2 mm layers, **4 walls, 30% gyroid**. PLA+ indoors, PETG if it lives in a hot car.

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0). Print and remix it for yourself. Please don't sell prints or files. Commercial rights are reserved by Rackhouse Supply Co.; contact rackhousesupplyco@gmail.com for a commercial license.

**Not climbing equipment.** Never use this part in a climbing, rescue or fall-protection system.

Don't have a printer? Buy one printed to order in six colors at https://alkalman123.github.io/RackHouse/
````

---

<!-- organizers:end -->

## Gatekeeper V3 - Trad Rack & Helmet Wall Hanger (Rackhouse)

**Folder in the upload zip:** `rackhouse-gatekeeper-v3/`

| Field on Thingiverse | Enter this |
|---|---|
| Thing name | Gatekeeper V3 - Trad Rack & Helmet Wall Hanger (Rackhouse) |
| Category | Hobby > Sport & Outdoors |
| License | **Creative Commons - Attribution - Non-Commercial - Share Alike** |
| This is a remix | **Leave OFF** (original design) |
| Tags | climbing, trad, rack, gear organizer, helmet holder, cam, quickdraw, wall hanger, garage organization, van life, rackhouse |
| Files | `files/` (the STL) and `LICENSE.txt` |
| Images | `images/` in numbered order. Image 01 becomes the thumbnail. |
| Print settings → Supports / Rafts | No / No |
| Print settings → Resolution | 0.2 mm |
| Print settings → Infill | 30% gyroid, 4 walls |
| Print settings → Filament | PLA+ or PETG |
| Print settings → Notes | Print flat, text side up. Needs 210 mm of bed in one direction. |

**Description** (paste into the Summary/Description box; it's also in `DESCRIPTION.md`):

````markdown
# Gatekeeper V3: trad rack & helmet hanger

Hang your whole trad rack and your helmet off one hook in the garage, van or gear closet.

- **4 gear slots** (20 x 11 mm) sized for a carabiner gate: clip cams and quickdraws.
- **Big pear-shaped opening**: drape slings, cordelettes or a rope coil.
- **J-hook** at the bottom: drop your helmet's chin strap in without unbuckling it. The gate is angled so the strap stays put.
- **13 mm hang hole** in the top tab: one hook, peg or screw.
- **RACKHOUSE / NOT FOR CLIMBING** debossed into the rail.

Size: 209 x 104 x 10 mm. About 65-85 g.

## Printing
Prints flat exactly as exported, **no supports**. Needs a bed of at least 210 mm in one direction (Ender 3, Prusa MK3/MK4, Bambu A1/P1/X1).
0.2 mm layers, 4 walls, 30% gyroid. PLA+ indoors, PETG in a hot van.

Use a screw into a stud or a rated anchor once it's loaded with a full rack.

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0). Print and remix it for yourself. Please don't sell prints or files. Commercial rights are reserved by Rackhouse Supply Co.; contact rackhousesupplyco@gmail.com for a commercial license.

**Not climbing equipment.** Never use this part in a climbing, rescue or fall-protection system.

Don't have a printer? Buy one printed to order in six colors at https://alkalman123.github.io/RackHouse/
````

## Cup Cradle V2 - Wide-Mouth Nalgene Car Cupholder Adapter (Rackhouse)

**Folder in the upload zip:** `rackhouse-cup-cradle-v2/`

| Field on Thingiverse | Enter this |
|---|---|
| Thing name | Cup Cradle V2 - Wide-Mouth Nalgene Car Cupholder Adapter (Rackhouse) |
| Category | Hobby > Automotive |
| License | **Creative Commons - Attribution - Non-Commercial - Share Alike** |
| This is a remix | **Leave OFF** (original design) |
| Tags | nalgene, water bottle, cupholder, cup holder adapter, car, automotive, wide mouth, 32 oz, hiking, climbing, rackhouse |
| Files | `files/` (the STL) and `LICENSE.txt` |
| Images | `images/` in numbered order. Image 01 becomes the thumbnail. |
| Print settings → Supports / Rafts | No / No |
| Print settings → Resolution | 0.2 mm |
| Print settings → Infill | 15-20% gyroid, 3-4 walls |
| Print settings → Filament | PETG (recommended for cars) or PLA+ |
| Print settings → Notes | Print stem down, as exported. |

**Description** (paste into the Summary/Description box; it's also in `DESCRIPTION.md`):

````markdown
# Cup Cradle V2: wide-mouth bottle cupholder adapter

A 32 oz wide-mouth water bottle is too fat for a car cupholder. This holds it upright.

- **Tapered stem with 8 flex ribs** wedges into round cupholders from **69 to 79 mm** across.
- **45-degree flare** into a **94 mm** cup, 51 mm deep: fits 32 oz wide-mouth bottles (about 3.5 in / 89 mm across).
- **Windows** around the cup so you can pinch the bottle out, and a **drain hole** for condensation.
- 101 mm wide, 135 mm tall. About 140-180 g.

Measure your cupholder before printing. Shallow, square or stepped cupholders may not seat the same way.

## Printing
Prints **stem down** exactly as exported, **no supports** (every overhang is 45 degrees or steeper).
0.2 mm layers, 3 walls (4 for a tighter fit), 15-20% gyroid. **Use PETG** if it'll sit in a hot car: PLA softens around 55-60 C.

Nalgene is a trademark of its owner. This adapter is not affiliated with or endorsed by Nalgene.

**License:** Creative Commons Attribution-NonCommercial-ShareAlike 4.0 (CC BY-NC-SA 4.0). Print and remix it for yourself. Please don't sell prints or files. Commercial rights are reserved by Rackhouse Supply Co.; contact rackhousesupplyco@gmail.com for a commercial license.

**Not climbing equipment.** Never use this part in a climbing, rescue or fall-protection system.

Don't have a printer? Buy one printed to order in six colors at https://alkalman123.github.io/RackHouse/
````

---

## After you publish

| Design | Thingiverse URL | Printables URL | MakerWorld URL |
|---|---|---|---|
| Gear Board | | | |
| Crag Ring | | | |
| Rock Ring | | | |
| Double Ring | | | |
| Sport Board | | | |
| Approach Bar | | | |
| Pocket Bar | | | |
| Gatekeeper V3 | | | |
| Cup Cradle V2 | | | |

Once they're live, paste each link into `SHOP.openDesigns` in
`js/store-data.js`: the Kickstarter page's "Open designs" list picks them
up automatically.
Free files bring in people who later buy a printed one or back the
campaign.
