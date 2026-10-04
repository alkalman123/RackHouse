# Legal & entity formation — general guidance, not legal advice

**Read this first:** I'm not a lawyer or accountant, this isn't legal or
tax advice, and nothing here is specific to your state or situation. It's
a map of the questions a real attorney or accountant would want you to
have already thought about, so that conversation (which is worth having
once real money is involved) is fast and cheap instead of starting from
zero. Budget for a one-time consult with a small-business attorney and/or
CPA once you clear the "$500 in real revenue" mark below — many offer a
flat-fee first session specifically for this kind of question.

## 1. Sole proprietor vs. LLC — the actual difference

**Sole proprietorship** is the default. If you sell something under your
own name (or a "doing business as" name) without registering an entity,
you're already one — no paperwork required, no separate step to "start."
Its defining feature: **there is no legal wall between your business and
you personally.** If the business is sued or owes money, your personal
assets (car, savings, etc.) are on the table.

**LLC (Limited Liability Company)** creates that wall, generally
shielding personal assets from business debts and lawsuits *as long as
you keep business and personal finances genuinely separate* (a separate
bank account, no mixing funds — courts will disregard the LLC's
protection, called "piercing the corporate veil," if you don't). It costs
money to form (state filing fee, often $50–500 depending on state) and
usually an annual fee or report to stay active, plus it adds a small
amount of paperwork (its own bank account, possibly its own tax filing
depending on how you elect to be taxed).

Neither is "more legitimate" than the other at this stage — plenty of
real, profitable small print shops run for years as a sole proprietorship
before ever forming an entity. The question is when the liability
protection becomes worth the cost and paperwork.

## 2. When to actually form the LLC — trigger conditions, not a date

Form one when **two or more** of these become true, not on a fixed
timeline:

- [ ] You've had **sustained real revenue** for a couple of months (a
      commonly cited rough threshold is a few hundred to low thousands
      of dollars a month — the point where a lawsuit or a bad debt could
      meaningfully hurt you, not just annoy you).
- [ ] You're **shipping products that could plausibly cause an injury**
      if something goes wrong — a printed part fails, a customer misuses
      it, etc. (see the product-liability section below — this applies
      to this business more than it might first appear).
- [ ] You're **signing contracts** in the business's name (a wholesale
      deal, a lease, a supplier agreement).
- [ ] You want to **open a business bank account or apply for business
      credit** — most banks want an LLC or at minimum an EIN and a DBA.
- [ ] You're bringing on **anyone else** — a co-founder, a contractor
      you pay regularly, an employee.

If none of those are true yet, an LLC mostly buys you paperwork you don't
need yet. If two or more are true, it's worth the ~$50–500 and the
afternoon of paperwork.

## 3. Product liability — why this matters more than "just a novelty item"

This is worth taking seriously specifically *because* the products are
climbing-adjacent, not despite it:

- **The site's disclaimers are a real risk-reduction measure, not just
  copy.** Every relevant product page and the FAQ state plainly that
  these are storage/novelty items, not rated climbing protection, and
  the Gatekeeper has "NOT FOR CLIMBING" printed into the physical part
  itself. Keep these. If you add products in the future, keep the same
  standard — clear, prominent, on the product page itself.
- **A disclaimer reduces risk, it doesn't eliminate it.** Someone
  misusing a product against clear instructions is a stronger legal
  position for you than no warning at all, but it isn't a guarantee. This
  is a real reason to consider **general liability insurance** once
  volume grows — policies aimed at small makers/Etsy-style sellers
  commonly run in the low hundreds of dollars per year, which is cheap
  relative to the protection.
- **An LLC doesn't protect you from your own negligence** — it protects
  your *personal* assets from the *business's* liabilities. If a product
  genuinely causes harm because of an actual defect, that's a real claim
  against the business either way; the entity structure just decides
  whose assets are exposed to it.

## 4. Trademark: the Cup Cradle mentions "Nalgene," specifically

The Cup Cradle's description references one real brand ("Nalgene")
because that's the honest, useful way to tell a customer what it fits —
this is generally covered under **nominative fair use** (using a
trademark to truthfully describe compatibility, not to imply
sponsorship), and the product page already carries an explicit
disclaimer: *"not licensed, endorsed by, or affiliated with the
brand."* That's a reasonable, common practice for compatibility
accessories.

That said, it's not zero-risk, and it's worth knowing your levers if it
ever becomes a real concern:

- **Keep the disclaimer visible** (already done) — don't remove it.
- **Never imply sponsorship or an official partnership** in your own
  marketing/social posts, even casually ("official Nalgene adapter"
  would cross a line the current copy doesn't).
- **If this product becomes a meaningful share of revenue**, it's worth
  a cheap trademark-focused consult, or simply renaming it something
  descriptive-but-not-brand-forward (e.g. "Wide-Mouth Bottle Cupholder
  Adapter," with the brand compatibility mentioned in the body copy
  instead of the title) — an easy, low-cost way to reduce exposure
  further if you want to be conservative, entirely your call.
- If you ever receive a cease-and-desist or any legal letter from the
  company, don't respond yourself — that's the moment to get a lawyer,
  not negotiate solo.

## 4b. Trademark: your own "Rackhouse" name, and the merch line

Two things worth doing before this takes off, not required to launch:

- **A basic knockout search on your own name.** Before it's worth
  defending, check the USPTO's free TESS database
  (uspto.gov/trademarks/search) and a plain web/social search for
  "Rackhouse" in the outdoor/apparel space — this is a common enough
  word that a name collision is plausible. Not a blocker to launching;
  worth doing before you sink real marketing spend into the name.
- **The tee and stickers only carry your own logo** — no third-party
  marks involved, so there's no nominative-fair-use question there the
  way there is with the Cup Cradle. The only trademark question for
  merch is protecting *your own* mark (above), not clearing someone
  else's.

## 4c. Who owns the product designs, and why they were redrawn

**What changed.** The first versions of the Gatekeeper, Rock Ring and Cup
Cradle were STL files made by someone else and published under a
*non-commercial* license (Creative Commons BY-NC style). That license
lets you print them for yourself. It does **not** let you sell prints,
and editing an NC file doesn't fix that: an edited copy is a "derivative"
and inherits the NC restriction.

**What replaced them.** All three products were redesigned from scratch
as new, original parts, and the Draw Bar was added as a new original
design. Nothing was traced, imported or remixed from the old files.
They're defined from functional requirements (bottle and cupholder
diameters, carabiner gate openings and clearances, rack sizes, a 210 mm
print bed) in `designs/rackhouse_designs.py`:

| Product | Old file (not yours) | New Rackhouse design (yours) |
|---|---|---|
| Gatekeeper | Oversized carabiner-outline panel with a ring of holes | **V3:** pear frame, 4 stadium gear slots, cross rail with debossed text, helmet J-hook, top hang tab |
| Rock Ring | Dome-topped block with two open ports | **V3:** 184 mm clip-on gear ring, 15 numbered inner-edge notches, central helmet hook, keyhole hanger, 3 standoff feet |
| Cup Cradle | Stem flaring to a scalloped basket | **V2:** tapered stem with 8 wedge ribs, 45° flare, 94 mm cup with arch/gate windows, drain |
| Draw Bar | (none: new product) | Straight 200 mm rail, 7 carabiner slots, debossed text, 2 keyholes in standoff ends |

Copyright protects a design's specific *expression*, not the idea or
function ("hang gear on a wall," "adapt a bottle to a cupholder"). So an
independently created part that serves the same function is not an
infringement. These new parts don't share the old parts' shapes.

**Keep the evidence.** Your best protection is a clear record that the
new designs were created independently. That record already exists:
`designs/rackhouse_designs.py` is the full source and git history
timestamps it. Don't delete it, and don't add the old STLs back to any
repo or listing. When you post the designs on Thingiverse, **don't mark
them as a remix** of the old things. They aren't remixes, and marking
them as one would pull the old NC license onto them.

**Three honest caveats (take these to a lawyer if money is on the line):**

1. **Selling is fine; exclusivity is the open question.** Nothing
   prevents *you* from selling these designs commercially. You don't
   need anyone's permission to sell your own independent designs.
   Whether you can stop *others* from copying them depends on copyright
   ownership. The US Copyright Office currently requires meaningful
   *human* authorship, and these designs were generated with an AI
   assistant at your direction. Strengthen your claim by making and
   recording your own creative decisions: change the parameters
   (dimensions, slot pattern, text, rib count) to your taste, print and
   revise them, and keep notes and photos of that process. Your
   **trademark** ("Rackhouse," the logo, the debossed wordmark) protects
   the brand regardless.
2. **Patents are a separate system.** Copyright clearance says nothing
   about patents. Gear hangers, gear rails and cupholder adapters are
   old, crowded product categories. A quick search on Google Patents for
   each product (for example "cup holder adapter bottle", "climbing gear
   organizer rack hanger") before you scale up is cheap insurance.
3. **The old files still exist in git history.** The original STLs and
   renders were removed from the current versions of both repos, but
   they remain in past commits of the public repos. Purging them requires
   rewriting history (a force-push). That's optional, and you have to
   approve it explicitly. Your exposure is low because you're not
   selling them, but purging removes any doubt.

**Licensing your designs.** Post them publicly under **CC BY-NC-SA 4.0**
(set up in `designs/LICENSE` and `business/THINGIVERSE-UPLOAD.md`).
As the owner, you keep every right, including the exclusive right to sell
prints. Everyone else can print for personal use and remix
non-commercially, with credit, and their remixes must carry the same
non-commercial terms. That's the same arrangement the original designer
used on you, now working in your favor. If you'd rather nobody can post
modified versions at all, pick CC BY-NC-ND 4.0 instead.

## 5. Sales tax — the honest current state

The site does not currently collect sales tax (see `checkout.js` — no
tax line is computed). That's a deliberate, honest choice for a brand
new shop that likely doesn't have sales tax nexus (a legal obligation to
collect) anywhere yet. You'll generally owe sales tax collection once you
have "nexus" in a state — almost always true in your home state once you
have any sales there, and potentially in other states once your sales
into them cross that state's economic nexus threshold (commonly $100k or
200 transactions/year, but this varies by state and changes over time).
At real volume, look into a service like TaxJar or Avalara, or ask your
accountant — manually tracking this across states gets error-prone fast.

## 6. A few other small things worth doing early, cheaply

- **A simple Terms of Service and Privacy Policy page** for the site.
  Not currently on the site — worth adding once you're taking real
  payment info (even Stripe-hosted checkout benefits from a basic privacy
  policy describing what data you collect and how). Many free generators
  exist for a first pass; a lawyer review is worth it once revenue
  justifies it.
- **An EIN (Employer Identification Number)** is free and quick from the
  IRS directly (irs.gov — never pay a third-party site for this), and
  useful even as a sole proprietor if you want to avoid putting your own
  Social Security Number on business paperwork.
- **Keep a separate record of business income/expenses from day one** —
  even a simple spreadsheet. It's the single easiest thing to do now
  that saves real pain at tax time, LLC or not.

## 7. The one-paragraph version

Start as a sole proprietor (you already are one). Keep the safety
disclaimers exactly as strong as they are now. Track income and expenses
separately from the start. Revisit LLC formation once you hit real,
sustained revenue or start signing contracts — not before. Get a real
lawyer or accountant for anything that involves an actual dispute, a
cease-and-desist, or a formation decision with money on the line; this
document exists so that conversation is fast, not so you can skip it.
