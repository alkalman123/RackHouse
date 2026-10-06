# Prototype photo kit: from renders to real photos

Everything on the site today is a **3D render**, labelled that way on
every image. That's fine for the shop, but Kickstarter needs the real
thing: product projects must show a working prototype in its current
state, and renders that could pass for photos aren't allowed to stand in
for one. This kit gets you from zero to real photos on the site and the
campaign in one weekend.

## 1. Print these first

Two lead products, in the colors that photograph best:

| Print | Color | Why | Est. filament |
|---|---|---|---|
| Gear Board | Ember | Flagship, hero shot, Kickstarter lead image | ~171 g |
| Crag Ring | Rock | Second lead, the "carry it to the crag" story | ~72 g |

Then one of each of the others in any color (Rock Ring, Double Ring,
Sport Board, Approach Bar, Pocket Bar: about 380 g together). Print
files: `designs/print-ready/` in your private archive.

**Settings:** PLA+ (PETG for anything that will live in a car), 0.2 mm
layers, 4 walls, 30% gyroid, flat with the text up, no supports, brim
optional. Every part fits a 210 mm bed.

**Load test while you shoot.** Hang the full gear each product page lists
(Gear Board: a double rack, nuts and six quickdraws) for a week. Look for
whitening or sag in the strips the carabiners clip around. The site's
capacities come from the CAD, so this test is what makes them true.

**Double Ring:** clip a full-size carabiner through each **inner** window
and photograph it. The render pipeline couldn't fit one there, so this
is the shot that proves (or disproves) the "draws on the inner row"
claim. If they don't fit, tell Claude and the copy gets changed.

## 2. Gear and setup

- Your real rack: cams, quickdraws, a few slings, a helmet.
- Two screws with washers in a wall stud (or two hooks), or a sling.
- **Light:** a big window with indirect daylight, to one side. No direct
  sun, no ceiling light, no flash. Overcast days are perfect.
- **Backdrop:** a plain wall (white, light grey, wood or garage
  plywood). For the clean shop shots, a sheet of white foam board.
- **Phone:** main (1x) or 2x lens, never ultra-wide (it bends straight
  edges). Tap to focus on the product, lower exposure a touch. Use a
  tripod or lean on something; shoot several of each.
- Wipe the print and trim any stringing; take off brim marks with a
  deburring tool or a knife.

## 3. Shot list (per lead product; 6-10 photos each)

| # | Shot | What it proves |
|---|---|---|
| 1 | Loaded on the wall, three-quarter angle, like the site's "gear" render | It holds a real rack |
| 2 | Same, straight on | Every slot, the layout |
| 3 | Close-up: a carabiner gate closed through one window | "Fully enclosed" is real |
| 4 | Board in your hands, flipped upside down, nothing falling (photo + 10 s video) | Nothing falls off |
| 5 | Crag Ring carried by the handle; clipped to a sling or tree at the crag | Carry use |
| 6 | In the trunk / in a pack lid (Pocket Bar, Approach Bar) | Car and pack use |
| 7 | Empty, on the foam board, flat light | Clean product shot |
| 8 | Edge on, with a ruler | Real thickness and size |
| 9 | On the printer bed or coming off it | Printed in-house |
| 10 | Two colors side by side | Colorways are real |

Real gear carries other brands' logos. That's fine in the background;
just don't make a brand the subject of the shot, and never suggest
Rackhouse is affiliated with one.

## 4. Put the photos on the site

1. Copy the photos to your computer.
2. Run, once per product:
   ```
   pip install pillow pillow-heif
   python3 tools/prep_photos.py gear-board IMG_2041.HEIC IMG_2042.HEIC --caption "Gear Board in Ember, loaded"
   ```
   It crops to a square, strips all phone metadata **including GPS
   location**, saves `img/photos/gear-board-1.jpg` and up, and prints
   the lines to paste.
3. Paste the lines into `SHOP.photos['gear-board']` in
   `js/store-data.js`, then commit and push.

What happens automatically: photos show first in that product's gallery
with an orange **"Photo · printed prototype"** tag; renders keep the
**"3D render"** tag; the caption under the gallery updates; and the
Kickstarter page's hidden **"From the print bed"** section appears with
your photos. (Or send the photos to Claude in a session and ask to add
them.)

## 5. Kickstarter

- Lead image: photo 1 or 4 of the Gear Board.
- Use photos for every product image in the campaign. If you show a
  render at all (for example a colorway you haven't printed), caption it
  "3D render" right on the image.
- Video: the plan in `KICKSTARTER-CAMPAIGN.md` §2; shots 1, 3, 4 and 9
  above are the core of it.
- Keep the raw, unedited originals: they're also dated evidence of your
  own work on the designs (see `DESIGN-OWNERSHIP-RECORD.md`).
