# Unit economics & print scaling

Everything here is a **framework with placeholder numbers**, not a guarantee.
The weights are computed from the actual STL files (see the math below);
the filament price, print times, and packaging costs are reasonable
market assumptions you should replace with your own once you've run a
real print. Where I'm confident, I say so. Where I'm estimating, I say
that too — don't take a number in this file as more precise than it is.

## Step zero: you don't need to buy anything yet

You said you're not printing until the first orders land — that's the
right call, and the site is built for it (checkout collects orders now,
production happens after). The only two things worth doing *before* an
order arrives:

1. **One benchmark print per product**, if you have access to any FDM
   printer (yours, a friend's, a local library makerspace, a maker space
   membership). This turns every estimate below into a real number —
   actual grams used and actual print time from your slicer. Twenty
   minutes of setup now saves you from pricing blind later.
2. **If you don't own a printer at all**, you don't need to buy one to
   take the first order. A local maker/print-farm operator, a campus or
   library makerspace, or a print-on-demand service (see "Scaling past
   one printer" below) can fulfill your first handful of orders for
   roughly the same per-part cost modeled here, with zero equipment
   spend. Buy a printer once you have proof the orders keep coming —
   that's the whole point of the make-to-order model you already have.

## Where the weights come from

Not guessed — computed from the actual CAD geometry. The seven carabiner
organizers come from `designs/products.py` in the private design archive (estimated printed weight at
4 walls, about 1.6 mm, plus 30% gyroid infill, PLA+ at 1.24 g/cm³; see
`designs/products-report.json`). The Gatekeeper and Cup Cradle come from
`designs/rackhouse_designs.py` and `designs/build-report.json`. Rebuild
the reports after any design change to refresh these:

| Product | Size (mm) | Openings | Est. printed weight |
|---|---|---|---|
| Gear Board (flagship) | 200 × 169 × 9 | 18 | **~171 g** |
| Crag Ring | 152 × 190 × 7 | 11 + handle | **~72 g** |
| Rock Ring | 176 × 203 × 9 | 13 | **~91 g** |
| Double Ring | 180 × 207 × 9 | 20 | **~122 g** |
| Sport Board | 200 × 97 × 9 | 13 | **~100 g** |
| Approach Bar | 200 × 40 × 6 | 7 | **~36 g** |
| Pocket Bar | 130 × 44 × 9 | 4 | **~33 g** |
| Gatekeeper V3 | 209 × 104 × 10 | 4 + helmet hook | **~65–85 g** |
| Cup Cradle V2 | — | — | **~140–180 g** |
| Full Kit (Gear Board + Crag Ring + stickers) | — | — | **~243 g** printed |
| Tee, Sticker Pack | — (print-on-demand — see `ORDER-INTAKE-AND-FULFILLMENT.md`) | — | — |

Print time is the one number I can't compute from geometry alone — it
depends on your printer's speed, nozzle, layer height, and slicer
settings. Don't trust a number here you haven't measured; the framework
below is built so you can drop your real number in once you have it.
All seven organizers are flat plates 6–9 mm thick, so they print fast
for their size and need no supports.

## Cost-per-part framework

Fill in your own values for the bracketed placeholders. The formula:

```
Cost per part = (grams × $/gram filament)
              + packaging
              + payment processing fee
              + (optional) your hourly rate × print/pack hours
```

Illustrative numbers at **$22/kg filament** (a reasonable PLA+ street
price — check your actual supplier) and **Stripe's standard 2.9% + $0.30**
processing fee:

| Product | Price | Filament cost | Packaging (est.) | Processing fee | Materials-only COGS | Gross margin |
|---|---|---|---|---|---|---|
| Gear Board | $38.00 | $3.76 (171 g) | $2.00 (flat box) | $1.40 | $7.16 | **$30.84 (81%)** |
| Crag Ring | $24.00 | $1.58 (72 g) | $1.75 | $1.00 | $4.33 | **$19.67 (82%)** |
| Rock Ring | $28.00 | $2.00 (91 g) | $2.00 | $1.11 | $5.11 | **$22.89 (82%)** |
| Double Ring | $34.00 | $2.68 (122 g) | $2.00 | $1.29 | $5.97 | **$28.03 (82%)** |
| Sport Board | $28.00 | $2.20 (100 g) | $1.75 | $1.11 | $5.06 | **$22.94 (82%)** |
| Approach Bar | $16.00 | $0.79 (36 g) | $1.25 (mailer) | $0.76 | $2.81 | **$13.19 (82%)** |
| Pocket Bar | $12.00 | $0.73 (33 g) | $1.00 (mailer) | $0.65 | $2.37 | **$9.63 (80%)** |
| Gatekeeper | $20.00 | $1.76 (80 g) | $2.00 | $0.88 | $4.64 | **$15.36 (77%)** |
| Cup Cradle | $16.00 | $3.52 (160 g) | $1.30 | $0.76 | $5.58 | **$10.42 (65%)** |
| Full Kit | $62.00 | $5.35 (243 g) | $3.40 (box + card) | $2.10 | $15.35 incl. ~$4.50 stickers | **$46.65 (75%)** |

Merch (print-on-demand, not filament — see `ORDER-INTAKE-AND-FULFILLMENT.md`):

| Product | Price | Est. POD base cost | Processing fee | Est. COGS | Est. gross margin |
|---|---|---|---|---|---|
| Rackhouse Tee | $26.00 | ~$13.00 (verify with Printful/Printify) | $1.05 | $14.05 | **~$11.95 (46%)** |
| Sticker Pack | $8.00 | ~$4.50 (verify with Printful/Printify) | $0.53 | $5.03 | **~$2.97 (37%)** |

The merch margins run lower than the 3D-printed line — that's the trade for zero labor, zero inventory risk, and zero print-queue time. Get an exact quote from whichever POD vendor you pick before trusting these two rows; base costs vary by garment brand, print area, and vendor, and change over time.

Two things the first table deliberately leaves out, on purpose:

- **Shipping.** The site charges $5.95 standard (free over $60) — verify
  that actually covers a real USPS/UPS/regional-carrier rate for your
  package's real weight and dimensions before you rely on it. The Gear
  Board ships in a roughly 22 × 19 cm flat box; the bars fit a padded
  mailer. Get an actual quote.
- **Your time.** Materials margin looks great (65–82%) because it ignores
  the thing that's actually scarce in a one-printer operation: print
  hours and your own pack/ship time. That's the real constraint — see
  below.

## DIY printing vs. a print farm — pricing in your own time

Materials-only margins (above) look great, but they hide the thing that
actually costs you: your own hands-on time. A print farm — a third-party
FDM shop that prints and ships parts on your behalf — trades margin for
zero equipment, zero print-queue time, and (if it's the right kind of
farm) zero of your own labor per order. Whether that trade is worth it
depends entirely on whether you price your time into the DIY column.

### Print-farm cost, ballpark

Rough per-unit cost from a third-party FDM print farm (modeled as about
$2.50 setup + $0.035/g; farms price on material + machine-time + their
margin, so get 2–3 real quotes before trusting this):

| Product | DIY filament-only cost | Ballpark print-farm cost |
|---|---|---|
| Gear Board (~171 g) | $3.76 | $6–10 |
| Crag Ring (~72 g) | $1.58 | $4–6 |
| Rock Ring (~91 g) | $2.00 | $5–7 |
| Double Ring (~122 g) | $2.68 | $6–8 |
| Sport Board (~100 g) | $2.20 | $5–7 |
| Approach Bar (~36 g) | $0.79 | $3–5 |
| Pocket Bar (~33 g) | $0.73 | $3–5 |
| Gatekeeper (~80 g) | $1.76 | $5–9 |
| Cup Cradle (~160 g) | $3.52 | $8–12 |

A print farm roughly **doubles to triples** your per-unit cost versus
printing it yourself — but it also removes the one-printer-at-a-time
ceiling entirely (see "the real bottleneck," below) and, if the farm
drop-ships, removes your labor too.

### Margin after farm cost + your own packaging/shipping

If the farm ships the part **to you** and you still pack/ship it to the
customer yourself (most consumer-facing farms work this way), the
margin at the midpoint of the ranges above:

| Product | Price | Print-farm margin |
|---|---|---|
| Gear Board | $38.00 | $26.11 (69%) |
| Crag Ring | $24.00 | $16.23 (68%) |
| Rock Ring | $28.00 | $19.20 (69%) |
| Double Ring | $34.00 | $23.94 (70%) |
| Sport Board | $28.00 | $19.14 (68%) |
| Approach Bar | $16.00 | $10.23 (64%) |
| Pocket Bar | $12.00 | $6.70 (56%) |
| Gatekeeper | $20.00 | $11.82 (59%) |
| Cup Cradle | $16.00 | $5.84 (36%) |

### Now price in your own hands-on time for the DIY column

DIY printing is mostly unattended machine time, but there's real
hands-on work per unit: slicing/setup, starting the print and checking
the first layers, post-processing, packing, and a shipping run. At a
placeholder **$25/hr** (swap in your real number), two scenarios:

- **One order at a time:** ~35–40 min hands-on ≈ $16/unit in labor
- **Batched** (several units per plate/session — scaling step 1 below): ~15–20 min/unit ≈ $7/unit in labor

| Product | DIY margin (materials only) | Minus labor, one-at-a-time | Minus labor, batched |
|---|---|---|---|
| Gear Board | $30.84 | $14.84 | $23.84 |
| Crag Ring | $19.67 | $3.67 | $12.67 |
| Rock Ring | $22.89 | $6.89 | $15.89 |
| Double Ring | $28.03 | $12.03 | $21.03 |
| Sport Board | $22.94 | $6.94 | $15.94 |
| Approach Bar | $13.19 | **-$2.81** | $6.19 |
| Pocket Bar | $9.63 | **-$6.37** | $2.63 |
| Gatekeeper | $15.36 | **-$0.64** | $8.36 |
| Cup Cradle | $10.42 | **-$5.58** | $3.42 |

The takeaway: **the Gear Board and Double Ring carry the business.**
They clear their labor even one at a time. The Approach Bar, Pocket Bar,
Gatekeeper and Cup Cradle lose money as single, one-off orders; they
earn their keep as add-ons in a bigger order (one box, one shipping run)
or batched several to a plate. The bars are small enough that 4–6 fit on
one plate next to a board, so batch them alongside Gear Board orders.

**Watch the Cup Cradle.** At ~160 g and $16 its farm margin is thin
(~$6, 36%). Raise it to **$18**, or sell it mainly as an add-on that
rides along in a bigger order, where the packaging and shipping are
already paid for.

### The catch: this only works if the farm is actually hands-off

Most farms ship the finished part **back to you**, and you repack and
ship to the customer — which reintroduces labor and erases the
advantage above. For the "hands-free" case to hold, you need a farm
that drop-ships directly to your customer. See
`ORDER-INTAKE-AND-FULFILLMENT.md` for how to wire that up and a
concrete service to look at (Slant 3D, built specifically for
API-driven, drop-ship FDM fulfillment).

## The real bottleneck is printer-hours, not materials

A print that costs $2–4 in filament but ties up your printer for 5–7
hours caps how many you can sell per week far more than materials cost
ever will. Before pricing decisions, figure out (from your benchmark
print) roughly how many hours each product takes, then:

```
Max units/week on one printer ≈ (printer-hours available per week) ÷ (hours per print)
```

Example: if a Gear Board takes ~5 hours and you can run the printer
~15 hours/day (waking hours plus one overnight run), that's roughly
3 prints/day, or **~21 Gear Boards/week** from a single machine — call
it $798/week gross on that SKU alone, materials-only margin ~$650/week,
before your labor. That's a real, useful ceiling to know going in.

## Scaling past one printer (only once demand proves it)

Do this in order — each step should be paid for by revenue you've
already seen, not upfront investment:

1. **Batch the plate.** Most slicers can nest multiple copies (or
   multiple different products) on one build plate per print job —
   cuts changeover time, not total print time, but reduces your active
   labor per unit.
2. **Print overnight / unattended.** If your printer and filament setup
   are reliable, running it 16–20 hrs/day instead of 8 roughly doubles
   throughput for zero equipment cost.
3. **Add a second printer** once weekly demand consistently exceeds one
   printer's ceiling for two to three weeks running — not before. A
   second entry-to-mid FDM printer is commonly $200–$500, a real but
   modest step, and only makes sense once orders are already paying for
   it.
4. **Recruit a "print partner."** Some makerspaces and hobbyist 3D
   printer owners will run prints for a per-part fee (a cut of margin,
   or a flat $/hour) — lets you scale capacity without buying hardware.
5. **Outsource to a print-on-demand manufacturing service** — see the
   "DIY vs. print farm" section above for the actual margin math, and
   `ORDER-INTAKE-AND-FULFILLMENT.md` for how to automate order intake
   to one. Worth doing earlier than step 3–4 for lower-priced SKUs
   specifically (see that section), not only as a late-stage scaling
   move.

Don't skip ahead in this list — every step past #2 costs real money or
margin, and the whole point of your make-to-order model is that you only
spend once you've already been paid.

## Sanity-check before you commit to these prices

- Print one of each on your own (or a borrowed) printer and log actual
  grams and hours.
- Get one real shipping quote for a packed box at the actual weight
  from USPS.com or your carrier of choice.
- Re-run the table above with your real numbers before your first sale.
