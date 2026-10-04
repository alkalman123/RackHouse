# Rackhouse — business docs

Everything here supports one goal: take real orders with real payment,
funded by revenue rather than upfront investment, without printing
anything until an order is actually in hand.

**The site is already live**, deployed via GitHub Pages (not Render —
`RENDER-DEPLOYMENT.md` is kept as a documented alternative, not the
active path). If you don't have the live link, ask and it'll be given
to you directly.

## Start here — this week's checklist

1. **Decide on payment** → `PAYMENTS-SETUP.md` (Stripe Payment Links are
   already wired into the code — just paste in URLs — or launch with the
   built-in email-invoice flow and add Stripe later)
2. **Kickstarter** → `KICKSTARTER-CAMPAIGN.md`. The shareable page is
   already live at https://alkalman123.github.io/RackHouse/kickstarter.html ;
   create the Kickstarter project and paste its URL into `js/store-data.js`
3. **Post the free design files** → `THINGIVERSE-UPLOAD.md` (license and
   copy-paste text ready; upload zip in `designs/`)
4. **Print one of each 3D-printed product**, or get one printed, to
   (a) have a real photo/video and (b) get real cost numbers →
   `UNIT-ECONOMICS-AND-SCALING.md`
5. **Set up the print-on-demand tee/stickers** → `ORDER-INTAKE-AND-FULFILLMENT.md`
6. **Post the launch sequence** → `SOCIAL-MEDIA-KIT.md`
7. **Fulfill the first order fast** when it lands, and log the real
   numbers back into the cost model

## The documents

| Document | What's in it |
|---|---|
| `BUSINESS-PLAN.md` | The whole plan in one place — go-to-market using your existing audience, phased rollout, illustrative financials, risks and how the build already handles them |
| `UNIT-ECONOMICS-AND-SCALING.md` | Real weights computed from the current CAD designs, a cost-per-part framework, and how to scale printing without spending ahead of demand |
| `ORDER-INTAKE-AND-FULFILLMENT.md` | How orders actually reach you, what's automatic out of the box, and how to wire up hands-off order tracking, customer emails, and print-on-demand fulfillment for the tee/stickers |
| `LEGAL-AND-ENTITY-FORMATION.md` | Sole prop vs. LLC, when to actually form one, product-liability and trademark considerations, and **§4c: why the products were redesigned and who owns the designs** — general education, not legal advice |
| `KICKSTARTER-CAMPAIGN.md` | Goal and budget, reward tiers, paste-ready story/risks text, video plan, pre-launch plan, how to share in climbing communities without getting banned |
| `THINGIVERSE-UPLOAD.md` | Step-by-step upload of the three designs with license choice, titles, tags, print settings and descriptions |
| `PAYMENTS-SETUP.md` | Exact steps to accept credit cards via Stripe, and how it plugs into the code that's already built for it |
| `RENDER-DEPLOYMENT.md` | An alternative hosting path, documented but not the one currently live |
| `SOCIAL-MEDIA-KIT.md` | Ready-to-edit launch posts and an evergreen content list |

## What I could and couldn't do myself

I built, tested, and can edit anything in the codebase — the storefront,
the cart/checkout logic, the Stripe Payment Link hook, all of it. What I
can't do is act as you on services that need your own identity and
banking: creating your Render account, your Stripe account, your Kickstarter
project, your Thingiverse uploads, or an LLC all require your own sign-up, your own bank account, and in the LLC's
case your own state filing. Every doc above tells you exactly what to
click; none of it requires waiting on me again to move forward.

## If something in here turns out wrong

The cost estimates in `UNIT-ECONOMICS-AND-SCALING.md` are computed from
real geometry but assumed filament prices and print times — replace them
with your own numbers the moment you have a real print. Everything in
`LEGAL-AND-ENTITY-FORMATION.md` is general education, not advice for your
specific situation — a real lawyer or accountant beats this document
every time money or a dispute is actually on the line.
