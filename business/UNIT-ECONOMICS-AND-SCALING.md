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

Not guessed — computed from the actual STL geometry (mesh volume via the
divergence theorem, scaled by PLA's density of 1.24 g/cm³):

| Product | Solid volume | Weight at 100% infill | Weight at ~20–35% infill (typical) |
|---|---|---|---|
| Rock Ring | 644.6 cm³ | 799 g | **~160–210 g** |
| Gatekeeper | 87.1 cm³ | 108 g | **~70–100 g** |
| Cup Cradle | 129.9 cm³ | 161 g | **~90–130 g** |
| Gift Duo (2× Rock Ring) | — | — | **~320–420 g** |
| Felt Base Pads | — (not printed; a bought-in commodity item) | — | — |
| Tee, Sticker Pack | — (not printed here; print-on-demand — see `ORDER-INTAKE-AND-FULFILLMENT.md`) | — | — |

Print time is the one number I can't compute from geometry alone — it
depends on your printer's speed, nozzle, layer height, and slicer
settings. Don't trust a number here you haven't measured; the framework
below is built so you can drop your real number in once you have it.

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
| Rock Ring | $34.00 | $3.74 (170g) | $1.50 | $1.29 | $6.53 | **$27.47 (81%)** |
| Gatekeeper | $20.00 | $1.87 (85g) | $2.00 (larger flat box) | $0.88 | $4.75 | **$15.25 (76%)** |
| Cup Cradle | $16.00 | $2.42 (110g) | $1.30 | $0.76 | $4.48 | **$11.52 (72%)** |
| Gift Duo | $62.00 | $7.48 (340g) | $2.50 | $2.10 | $12.08 | **$49.92 (81%)** |
| Felt Base Pads | $5.00 | ~$0.75 (bought-in) | $0.75 | $0.45 | $1.95 | **$3.06 (61%)** |

Merch (print-on-demand, not filament — see `ORDER-INTAKE-AND-FULFILLMENT.md`):

| Product | Price | Est. POD base cost | Processing fee | Est. COGS | Est. gross margin |
|---|---|---|---|---|---|
| Rackhouse Tee | $26.00 | ~$13.00 (verify with Printful/Printify) | $1.05 | $14.05 | **~$11.95 (46%)** |
| Sticker Pack | $8.00 | ~$4.50 (verify with Printful/Printify) | $0.53 | $5.03 | **~$2.97 (37%)** |

The merch margins run lower than the 3D-printed line — that's the trade for zero labor, zero inventory risk, and zero print-queue time. Get an exact quote from whichever POD vendor you pick before trusting these two rows; base costs vary by garment brand, print area, and vendor, and change over time.

Two things the first table deliberately leaves out, on purpose:

- **Shipping.** The site charges $5.95 standard (free over $60) — verify
  that actually covers a real USPS/UPS/regional-carrier rate for your
  package's real weight and dimensions before you rely on it. A Rock Ring
  in a small box is light but bulky; get an actual quote.
- **Your time.** Materials margin looks great (65–83%) because it ignores
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

Rough per-unit cost from a third-party FDM print farm (a wide range,
since farms price on material + machine-time + their margin — get 2–3
real quotes before trusting this):

| Product | DIY filament-only cost | Ballpark print-farm cost |
|---|---|---|
| Rock Ring (~170g) | $3.74 | $8–14 |
| Gatekeeper (~85g) | $1.87 | $5–9 |
| Cup Cradle (~110g) | $2.42 | $6–10 |

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
| Gatekeeper | $20.00 | $10.12 (51%) |
| Rock Ring | $34.00 | $20.21 (59%) |
| Cup Cradle | $16.00 | $5.94 (37%) |

### Now price in your own hands-on time for the DIY column

DIY printing is mostly unattended machine time, but there's real
hands-on work per unit: slicing/setup, starting the print and checking
the first layers, post-processing, packing, and a shipping run. At a
placeholder **$25/hr** (swap in your real number), two scenarios:

- **One order at a time:** ~35–40 min hands-on ≈ $15–17/unit in labor
- **Batched** (several units per plate/session — scaling step 1 below): ~15–20 min/unit ≈ $6–8/unit in labor

| Product | DIY margin (materials only) | Minus labor, one-at-a-time | Minus labor, batched |
|---|---|---|---|
| Gatekeeper | $15.25 | **-$1.42** | $7.75 |
| Rock Ring | $27.47 | $10.80 | $19.97 |
| Cup Cradle | $11.52 | **-$5.15** | $4.02 |

The takeaway: **once your time is priced in, printing the Gatekeeper or
Cup Cradle one order at a time can lose money.** Only the Rock Ring
clearly wins DIY even unbatched, because its price is high enough to
absorb the labor. Batching (filling a plate with several units before
you print) fixes this for all three — but batching only works once
you have enough simultaneous orders to fill a plate, which isn't true
in the first weeks when orders trickle in one at a time.

Compare the time-adjusted DIY numbers above to the hands-off print-farm
margins: **the farm route wins on Gatekeeper and Cup Cradle, and comes
close on Rock Ring**, whenever DIY would otherwise be done one order at
a time. This is a genuine case for routing at least some of the catalog
through a farm from day one, not just as a stopgap before you own a
printer.

### The catch: this only works if the farm is actually hands-off

Most farms ship the finished part **back to you**, and you repack and
ship to the customer — which reintroduces labor and erases the
advantage above. For the "hands-free" case to hold, you need a farm
that drop-ships directly to your customer. See
`ORDER-INTAKE-AND-FULFILLMENT.md` for how to wire that up and a
concrete service to look at (Slant 3D, built specifically for
API-driven, drop-ship FDM fulfillment).

## The real bottleneck is printer-hours, not materials

A print that costs $3.74 in filament but ties up your printer for 8–10
hours caps how many you can sell per week far more than materials cost
ever will. Before pricing decisions, figure out (from your benchmark
print) roughly how many hours each product takes, then:

```
Max units/week on one printer ≈ (printer-hours available per week) ÷ (hours per print)
```

Example: if a Rock Ring takes ~8 hours and you can run the printer
~12 hours/day (waking hours plus one overnight run), that's roughly
1.5 prints/day, or **~10 Rock Rings/week** from a single machine — call
it $340/week gross on that SKU alone, materials-only margin ~$275/week,
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
