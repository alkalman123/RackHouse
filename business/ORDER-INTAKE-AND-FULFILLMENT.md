# Order intake, fulfillment, and automation

The honest bottom line first, then the exact setup steps.

## What's automatic today vs. what needs you

| Step | 3D-printed items, printed by you | 3D-printed items, routed to a drop-ship print farm | Merch (Tee, Stickers) |
|---|---|---|---|
| Take payment | **Automatic** — Stripe Payment Link or built-in checkout | **Automatic** — same | **Automatic** — same |
| Customer gets a receipt email | **Automatic** — Stripe's built-in receipt (one checkbox, see below) | **Automatic** — same | **Automatic** — same |
| You get notified of the order | **Automatic** — Stripe app/email push | **Automatic** — same | **Automatic** — same |
| "What happens next" branded email | Automatic once you do the 15-minute Zapier/Make setup below | Automatic — same setup | Same |
| Production | **You** — slice, print, pack (a human has to run the printer) | **Automatic** — the farm prints, you never touch it | **Automatic** once linked to a print-on-demand partner |
| Shipping | **You** — box it, buy a label, ship it | **Automatic** — the farm ships directly to the customer (if it drop-ships — see Part 3b) | **Automatic** — the POD partner ships and emails tracking |
| Shipping notification email | Automatic once you do the tracker setup below | Automatic (farm sends its own, if it drop-ships) | Automatic (POD partner sends its own) |

So: **payment collection and customer emails can be 100% automatic today, on every item, regardless of who prints it.** Printing it yourself is the one path that always needs a human — a printer has to be run by someone. But routing a SKU to a drop-ship print farm makes it just as hands-off as the merch line, at the cost of a real margin hit (see `UNIT-ECONOMICS-AND-SCALING.md`'s "DIY printing vs. a print farm" section — worth doing for the Gatekeeper and Cup Cradle specifically, where the margin math already favors it once your own time is priced in).

## Part 1 — Order intake (works today, zero extra setup)

Every order arrives one of two ways, both already wired into the site:

1. **Single-item orders with a Stripe Payment Link set** (see `PAYMENTS-SETUP.md`) — the customer pays Stripe directly. You'll see it in your Stripe Dashboard and get Stripe's own instant email/push notification. Nothing to build; this is automatic the moment you paste in a Payment Link.
2. **Mixed-cart or no-Payment-Link orders** — the built-in checkout collects the order and opens a pre-filled email to you (see `js/checkout.js`) instead of charging a card. You reply with a Stripe Invoice or a one-off Payment Link to actually collect payment (also covered in `PAYMENTS-SETUP.md`).

**Turn on Stripe's automatic receipt email** (path 1, zero code, does most of the "email the customer" job by itself):
Stripe Dashboard → Settings → Emails → turn on "Email customers for successful payments." Done — every card payment now auto-sends the customer a receipt with your business name on it.

## Part 2 — The order tracker (the hub everything else hangs off)

Make one Google Sheet called **Rackhouse Orders** with these columns:

```
Date | Order ID | Customer | Email | Product | Variant | Qty | Total | Status | Tracking # | Notes
```

`Status` is a dropdown: `New → Printing → Packed → Shipped`. This sheet is the single place you look to know what's owed and what's done — and it's the trigger point for the automations below.

**Automatically add a row on every Stripe payment** (one-time setup, ~15 minutes):
1. Free account at [zapier.com](https://zapier.com) or [make.com](https://www.make.com) (Make's free tier is more generous for multi-step automations if you outgrow Zapier's single-step free plan — check current limits at signup, they change).
2. Trigger: **Stripe → New Payment** (or "Checkout Session Completed").
3. Action: **Google Sheets → Create Spreadsheet Row** in your Orders sheet, mapping Stripe's customer name/email/amount/line-item description into the columns above, `Status` defaulted to `New`.
4. Turn the Zap/scenario on. Every future payment now lands in your tracker with zero typing.

## Part 3 — Fulfilling a 3D-printed order (Gatekeeper, Rock Ring, Cup Cradle, Gift Duo, Felt Pads)

This is the one step that stays manual, because a real printer has to run:

1. New row shows up in the tracker with `Status = New`.
2. Slice and print (see `UNIT-ECONOMICS-AND-SCALING.md` for time/cost math). Set `Status = Printing`.
3. Pack it, weigh the box, buy a shipping label (USPS/UPS/Shippo — any of them show you the real rate before you pay). Set `Status = Packed`, paste the tracking number into the sheet.
4. Set `Status = Shipped`. This status change is the trigger for the automatic shipping-notification email below — you don't send anything by hand.

**Automatic "it shipped" email** (one-time setup):
1. Zapier/Make trigger: **Google Sheets → Updated Row** (watch the Orders sheet, filter to `Status = Shipped`).
2. Action: **Gmail/Outlook → Send Email** using a template pulling in the customer's name, product, and the tracking number column.
3. Write the template once (see the sample below); every future "Shipped" status change sends it automatically.

Sample template:

```
Subject: Your Rackhouse order is on its way

Hey {{Customer}},

Your {{Product}} shipped today. Tracking: {{Tracking #}}

Questions? Just reply to this email.

— Rackhouse
```

## Part 3b — Routing a 3D-printed SKU to a drop-ship print farm instead

Per the margin math in `UNIT-ECONOMICS-AND-SCALING.md`, this is worth
doing for the Gatekeeper and Cup Cradle from early on, not just as a
late-stage scaling move — those two lose money to your own labor when
printed one at a time, before you have enough volume to batch.

**The one requirement that makes this actually hands-off:** the farm
must ship directly to your customer, not back to you. If it ships to
you, you're back to manual packing and shipping — no better than
printing it yourself, and worse on margin. Confirm drop-ship support
before committing to a farm.

**A concrete lead:** [Slant 3D](https://www.slant3d.com) is an FDM
print farm built specifically for API-driven, drop-ship order
fulfillment — aimed at exactly this use case (e-commerce/Kickstarter
sellers who don't want to run their own printers). Get a current quote
directly; I don't have verified pricing to give you and per-unit costs
change over time.

**Wiring it up**, once you've picked a farm and confirmed drop-ship:

1. Upload the STL for the SKU you're routing (Gatekeeper, Cup Cradle,
   or both) to the farm, matching colorway options to what the site
   offers.
2. If the farm has an API and a Zapier/Make integration (check their
   docs — this varies by vendor and changes over time): **Trigger:
   Stripe → New Payment**, filtered to that SKU. **Action:** create an
   order with the farm, mapping the Stripe shipping address and
   colorway straight through. This is the same pattern as the Printful
   automation in Part 4 below.
3. If the farm doesn't have a no-code integration yet, fall back to the
   same semi-automated pattern as Printful's "day one" option: the new
   row in your order tracker (Part 2) tells you to submit that order on
   the farm's dashboard by hand — a couple minutes of clicking, not
   printing or packing.
4. Either way, the farm's own shipping confirmation to the customer
   replaces the tracker-triggered "it shipped" email from Part 3 for
   that order — nothing further needed from you.

You can run a mixed model: print the Rock Ring yourself (it wins DIY
even unbatched per the margin math) while routing the Gatekeeper and
Cup Cradle to the farm. Nothing about the site's code needs to change
either way — `SHOP.payment.productLinks` and the cart already treat
every product identically; only your own fulfillment process differs
per SKU.

## Part 4 — Fulfilling a merch order (Tee, Stickers) — fully automatic once linked

The tee and stickers are print-on-demand by design specifically so this line needs **zero manual production or packing from you**, ever. Two ways to wire it, pick based on how much you want to spend:

**Day one (free, ~90 seconds of your time per order):**
1. Create a free [Printful](https://www.printful.com) account, upload a clean vector of the carabiner logo (the site's mockups at `img/tee-*.svg` and `stickers-pack.svg` show the intended layout — recreate the art as a print-ready file, since those are web mockups, not print-resolution source files), and set up the tee (3 colors, S–XXL) and sticker pack as products there.
2. When a tee/sticker order lands in your tracker, open Printful, click **Create order**, paste in the customer's shipping address and item from the tracker row. Submit.
3. Printful prints, packs, ships, and **automatically emails the customer their own tracking number** — you never touch a box. Total manual work: pasting an address once.

**Once volume justifies it (fully hands-off, ~$20–30/month in automation tooling):**
1. Zapier and Make.com both have official **Stripe** and **Printful** integrations.
2. Trigger: **Stripe → New Payment**, filtered to line items matching the tee/sticker SKU.
3. Action: **Printful → Create Order**, mapping the Stripe shipping address and variant (size/color) straight through.
4. Now even the 90-second paste-in step disappears — a merch order goes from "customer pays" to "Printful is printing it" with nobody touching anything.

Printify is a direct alternative to Printful with the same shape of integration — compare pricing per unit for a tee and sticker pack before committing, since per-unit costs (which set your merch margin) vary between the two and change over time.

## Part 5 — The weekly 10-minute check

Even with everything above running, look at the tracker once a week:

- Anything stuck in `New` more than 2 days? Print it or push the Printful order through.
- Anything in `Printing` more than your normal print time? Something's stuck on the bed — go look.
- Any Stripe payment that *didn't* create a tracker row? The Zap/scenario silently failed — check Zapier/Make's run history for the error (a bad field mapping is the usual cause).

That's the whole system: Stripe collects money and emails receipts automatically today with no setup; a Google Sheet plus two small automations turn on hands-off order tracking and shipping emails; and the merch line can run completely on autopilot once it's pointed at a print-on-demand partner. The only irreducible manual step in the entire business is running the 3D printer — which is exactly the step you said you're not going to touch until real orders prove it's worth it.
