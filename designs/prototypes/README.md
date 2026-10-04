# Carabiner-holder prototypes (R01–R10 rings, B01–B10 straight)

Twenty print-and-test candidates. **Nothing here is on the website yet.**
Print the ones you want to try, run the tests below, and say which to
continue with. The winner(s) then get the full treatment: final tuning,
product photos, product page, Thingiverse files.

`rings.jpg` and `bars.jpg` show all twenty side by side. Each prototype's
ID is debossed on the part, so prints don't get mixed up.

## Why the last Rock Ring wouldn't hold carabiners

Its band was 20 × 14 mm (14 × 14 at the notches), which is too fat for a
cam carabiner to close around. It also sat only 12 mm off the wall, so
there was no room for the carabiner to wrap behind it. Every prototype
here fixes both, and the build script checks it on every part:

- **every clip point is at most 12 × 12 mm** (most are 12 × 10, the hooks
  and loops 7–8 × 10);
- **every clip rail is 25 mm off the wall** (30 mm on R10 and B10);
- **screwed at 2–3 posts**, not hung from a single hook, so the part can't
  swing or tip when you clip or unclip.

## The prototypes

Clip section and clearance are in mm.

| ID | File | What it is | Clip section | Off wall | Screws | Print size (mm) | Weight (g) |
|---|---|---|---|---|---|---|---|
| **R01** | `R01-fin-ring.stl` | Thin 12 x 10 mm clip band with 12 positions split by fins on the inner edge; helmet hook at the top. | 12 × 10 | 25 | 2 | 182 × 205 × 35 | ~75 |
| **R02** | `R02-outer-fin-ring.stl` | Same thin band, dividers on the outside edge so the inside stays clear for the helmet. | 12 × 10 | 25 | 2 | 192 × 207 × 35 | ~74 |
| **R03** | `R03-notched-ring.stl` | Closest to the ring you liked: wider band with deep notches; the band is 11 x 10 mm at every notch. | 11 × 10 | 25 | 2 | 186 × 205 × 35 | ~81 |
| **R04** | `R04-hook-ring.stl` | Five open J-hooks hang from the bottom: drop a carabiner on, no gate to open. | 7 × 10 | 25 | 3 | 147 × 202.5 × 35 | ~81 |
| **R05** | `R05-gear-loop-ring.stl` | Seven closed gear loops around the bottom, like the loops on a harness: one piece per loop. | 8 × 10 | 25 | 2 | 205.8 × 208 × 35 | ~85 |
| **R06** | `R06-double-ring.stl` | Two rings: the outer one for cams (10 spots), the inner one for nuts and draws (6 spots). | 10 × 10 | 25 | 2 | 186 × 208 × 35 | ~103 |
| **R07** | `R07-hub-ring.stl` | Ring with a center hub screwed to the wall; the helmet hook comes off the hub, so it's the strongest helmet mount. | 12 × 10 | 25 | 3 | 182 × 205 × 35 | ~90 |
| **R08** | `R08-ring-helmet-below.stl` | Smaller ring with the helmet on a J-hook underneath, so the helmet never covers the rack; 10 positions on the sides. | 12 × 10 | 25 | 2 | 145.7 × 209 × 35 | ~64 |
| **R09** | `R09-racetrack-ring.stl` | Stretched ring with a flat bottom: four spots in a straight row plus four up each curved side. | 12 × 10 | 25 | 2 | 200 × 158 × 35 | ~74 |
| **R10** | `R10-heavy-ring.stl` | Heavy-duty: 12 x 12 mm band, 30 mm off the wall, six posts and three screws for a big double rack. | 12 × 12 | 30 | 3 | 184 × 208 × 42 | ~100 |
| **B01** | `B01-fin-rail.stl` | Straight 12 x 10 mm clip rail, 7 spots split by fins on top, 25 mm off the wall. | 12 × 10 | 25 | 2 | 200 × 32 × 35 | ~32 |
| **B02** | `B02-two-bay-rail.stl` | Same rail with a third screw in the middle: two bays of 4 spots, stiffer under a full load. | 12 × 10 | 25 | 3 | 200 × 32 × 35 | ~36 |
| **B03** | `B03-hook-bar.stl` | Five open J-hooks under a straight spine: drop carabiners on without opening the gate. | 8 × 10 | 25 | 2 | 200 × 62 × 35 | ~51 |
| **B04** | `B04-double-rail.stl` | Two rails: the bottom one for 7 quickdraws, the top one for 5 slings or bigger gear. | 10 × 10 | 25 | 2 | 200 × 72 × 35 | ~55 |
| **B05** | `B05-rail-helmet-hook.stl` | Five clip spots plus a big helmet hook at the end: a full mini gear wall in one bar. | 12 × 10 | 25 | 2 | 200 × 70 × 35 | ~38 |
| **B06** | `B06-slot-plate.stl` | The Draw Bar, fixed: bigger 15 x 24 mm slots, a 9 mm bottom rail and 25 mm of wall clearance. | 9 × 10 | 25 | 2 | 200 × 46 × 35 | ~57 |
| **B07** | `B07-dense-comb.stl` | Ten tightly spaced spots (17 mm apart) for a full set of quickdraws. | 12 × 10 | 25 | 2 | 200 × 32 × 35 | ~33 |
| **B08** | `B08-gear-loop-bar.stl` | Six closed gear loops hanging from a spine, like harness gear loops: nothing can slide. | 8 × 10 | 25 | 2 | 200 × 49 × 35 | ~47 |
| **B09** | `B09-compact-rail.stl` | Short 150 mm version with 5 spots for a small space, a van or a nut/tool rack. | 12 × 10 | 25 | 2 | 150 × 32 × 35 | ~27 |
| **B10** | `B10-heavy-rail.stl` | Heavy-duty 12 x 12 mm rail, 30 mm off the wall, three screws: 8 spots for heavy gear. | 12 × 12 | 30 | 3 | 200 × 32 × 42 | ~44 |

## Printing

- Every file is already laid out **face down**: the front sits on the
  bed and the standoff posts point up. **No supports.**
- 0.2 mm layers, **4 walls, 30–40% gyroid** (40% for R10/B10). PLA+ or
  PETG.
- Rings need a bed of at least 210 mm in one direction (Ender 3,
  Prusa MK3/MK4, Bambu A1/P1/X1). Bars need 200 mm.
- At ~30–100 g each, printing all twenty uses about 1.3 kg of filament.
  If that's too much, print the shortlist first.

## Mounting

Each screw goes through a countersunk hole in the front and down through
a post into the wall. Use **#8 flat-head wood screws, 2½" (64 mm)** long
(**3" / 76 mm** for R10 and B10). Drive them into a stud, or use rated
drywall anchors. Drill a 3 mm pilot hole first.

## How to test each one

Score 1–5, write notes. It takes about 10 minutes per part.

1. **Clip**: clip on your own cam carabiners, a wiregate quickdraw and a
   locking carabiner. Does each one close fully, with one hand?
2. **Stays put**: rack a full set of cams. Does every piece stay in its
   own spot, or do they slide together?
3. **Grab**: take a cam off one-handed, without looking. Easy?
4. **Helmet**: hang your helmet. Does it stay on, and can you still reach
   the gear?
5. **Load**: hang roughly twice your rack weight (a 10–12 kg bag) for 24
   hours. Any bending, cracking, or posts pulling loose?
6. **Looks**: would you hang it in your living room?

| ID | Clip | Stays put | Grab | Helmet | Load | Looks |
|---|---|---|---|---|---|---|
| R01 | | | | | | |
| R02 | | | | | | |
| R03 | | | | | | |
| R04 | | | | | | |
| R05 | | | | | | |
| R06 | | | | | | |
| R07 | | | | | | |
| R08 | | | | | | |
| R09 | | | | | | |
| R10 | | | | | | |
| B01 | | | | | | |
| B02 | | | | | | |
| B03 | | | | | | |
| B04 | | | | | | |
| B05 | | | | | | |
| B06 | | | | | | |
| B07 | | | | | | |
| B08 | | | | | | |
| B09 | | | | | | |
| B10 | | | | | | |

## Rebuild or tweak

```
python3 designs/prototypes.py
```

Every dimension is a parameter in `designs/prototypes.py`: band size,
standoff, positions, hook throat and so on. Tell me what to change after
testing and I'll update the chosen design.

**Not climbing equipment.** These are organizers. Never use them to hold
a person.
