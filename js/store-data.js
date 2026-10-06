/* =============================================================================
   RACKHOUSE — store configuration & product catalog
   Single source of truth for pricing, shipping and product data.

   LAUNCH CHECKLIST — one item left before taking real orders:
   1. SHOP.payment.productLinks → paste a Stripe Payment Link URL per product
                      (see business/PAYMENTS-SETUP.md) once you have a Stripe
                      account, and every "Buy now" button on that product
                      instantly starts taking real cards — no other code
                      changes needed. Left blank, "Buy now" falls back to the
                      built-in cart + email-invoice checkout, which needs no
                      account at all. Multi-item carts ("Add to cart") always
                      use the built-in checkout, since one Payment Link can't
                      represent an arbitrary mixed cart without a backend.
   2. Swap SHOP.social if/when real social accounts exist (none are linked yet).
   ========================================================================== */

const SHOP = {
  name: 'Rackhouse',
  legalName: 'Rackhouse Supply Co.',
  tagline: 'Small-batch 3D-printed gear storage for climbers.',
  email: 'rackhousesupplyco@gmail.com',
  phone: '',
  address: 'Chicago, IL · ships from a home studio, not a storefront',
  currency: '$',
  freeShippingThreshold: 60,
  shipping: {
    standard: { label: 'Standard', price: 5.95, eta: '3–6 business days' },
    expedited: { label: 'Expedited', price: 14.95, eta: '2 business days' },
  },
  promoCodes: {
    'FIRSTSEND10': { percentOff: 10, label: '10% off your first send' },
  },
  payment: {
    // One Stripe Payment Link per product (optional). When a product's
    // link is set, its "Buy now" button skips the internal checkout and
    // sends the customer straight to Stripe's own hosted, card-accepting
    // checkout page for that item. Leave a value blank/'' to keep using
    // the built-in email-invoice checkout for that product. See
    // business/PAYMENTS-SETUP.md for exactly how to create these.
    productLinks: {
      'gear-board': '',
      'crag-ring': '',
      'sport-board': '',
      'rock-ring': '',
      'double-ring': '',
      'approach-bar': '',
      'pocket-bar': '',
      'full-kit': '',
      'gatekeeper': '',
      'cup-cradle': '',
      'tee': '',
      'stickers': '',
    },
  },
  social: {
    instagram: '',
  },
  // Kickstarter campaign (see business/KICKSTARTER-CAMPAIGN.md).
  // 1. Once your Kickstarter draft exists, turn on its pre-launch page and
  //    paste that URL into `url`; leave status 'prelaunch'. Every
  //    "Back us" button then sends people to Kickstarter's "Notify me on
  //    launch" button.
  // 2. On launch day set status to 'live' (buttons become "Back us on
  //    Kickstarter"). After it ends, set 'funded' or 'ended'.
  // While url is blank, the page collects "notify me" emails instead.
  kickstarter: {
    url: '',
    status: 'prelaunch',   // 'prelaunch' | 'live' | 'funded' | 'ended'
    goal: 1200,
    launchDate: '',        // e.g. 'November 12' — shown on the page when set
  },
};

const COLORWAYS = [
  { key: 'rock',  name: 'Rock',  hex: '#63707c', note: 'cool slate grey' },
  { key: 'moss',  name: 'Moss',  hex: '#55805a', note: 'forest green' },
  { key: 'ice',   name: 'Ice',   hex: '#4a90c2', note: 'glacier blue' },
  { key: 'sand',  name: 'Sand',  hex: '#c9a86a', note: 'warm tan' },
  { key: 'ink',   name: 'Ink',   hex: '#202326', note: 'matte black' },
  { key: 'ember', name: 'Ember', hex: '#d85c2a', note: 'signature orange' },
];

function colorway(key) {
  return COLORWAYS.find((c) => c.key === key) || COLORWAYS[0];
}

// Product renders for the carabiner organizers (designs/render/make_images.py)
function productImages(id, colorKey) {
  const base = `img/products/${id}-${colorKey}`;
  return { gear: `${base}-gear.jpg`, hero: `${base}-hero.jpg`, front: `${base}-front.jpg`, edge: `${base}-edge.jpg` };
}

function gatekeeperImages(colorKey) {
  return {
    hero: `img/gatekeeper-${colorKey}-hero.jpg`,
    front: `img/gatekeeper-${colorKey}-front.jpg`,
    detail: `img/gatekeeper-${colorKey}-detail.jpg`,
  };
}

function cupCradleImages(colorKey) {
  return {
    hero: `img/cupcradle-${colorKey}-hero.jpg`,
    top: `img/cupcradle-${colorKey}-top.jpg`,
    profile: `img/cupcradle-${colorKey}-profile.jpg`,
  };
}

const TEE_COLORWAYS = [
  { key: 'ink',  name: 'Ink',  hex: '#20232a' },
  { key: 'sand', name: 'Sand', hex: '#d9c49a' },
  { key: 'rock', name: 'Rock', hex: '#6b7680' },
];

const SIZES = ['S', 'M', 'L', 'XL', 'XXL'];

function teeImage(colorKey) {
  return `img/tee-${colorKey}.svg`;
}

const PRODUCTS = {
  'gear-board': {
    id: 'gear-board',
    name: 'The Gear Board',
    tagline: '18-slot board for a whole rack',
    price: 38.0,
    slug: 'product-gear-board.html',
    badge: 'Flagship',
    hasColor: true,
    defaultColor: 'ember',
    image: productImages('gear-board', 'ember').gear,
    short: 'Your whole rack on one board. 18 closed slots in three rows of six: quickdraws on the bottom row, cams and nuts on the rows above, each hanging through its own window so nothing tangles. Every opening is fully enclosed, so nothing falls off in the closet, the car, your pack or at the crag.',
  },
  'crag-ring': {
    id: 'crag-ring',
    name: 'The Crag Ring',
    tagline: 'Carry-handle gear ring for the crag',
    price: 24.0,
    slug: 'product-crag-ring.html',
    badge: 'Crag favorite',
    hasColor: true,
    defaultColor: 'rock',
    image: productImages('crag-ring', 'rock').gear,
    short: 'A light 7 mm gear ring with a hand-size carry handle. Rack your cams through 11 closed windows, grab the handle and walk to the crag, then clip the handle to a sling or a tree. Every window is fully enclosed, so nothing falls off on the approach.',
  },
  'rock-ring': {
    id: 'rock-ring',
    name: 'The Rock Ring',
    tagline: 'Flat gear ring for a trad rack',
    price: 28.0,
    slug: 'product-rock-ring.html',
    badge: 'Trad',
    hasColor: true,
    defaultColor: 'sand',
    image: productImages('rock-ring', 'sand').gear,
    short: 'A flat gear ring with 13 closed windows punched right through it. Rack your cams in size order around the ring and hang it from the top eye. Nothing sticks out, so it packs flat and never snags; every window is fully enclosed, so nothing falls off.',
  },
  'double-ring': {
    id: 'double-ring',
    name: 'The Double Ring',
    tagline: 'Two rows: cams outside, draws inside',
    price: 34.0,
    slug: 'product-double-ring.html',
    badge: 'Trad + sport',
    hasColor: true,
    defaultColor: 'ice',
    image: productImages('double-ring', 'ice').gear,
    short: 'A two-row gear ring with 20 closed windows: 13 around the outside for cams and 7 on the inner row for quickdraws, nuts and a nut tool, which hang through the middle. Every window is fully enclosed.',
  },
  'sport-board': {
    id: 'sport-board',
    name: 'The Sport Board',
    tagline: 'Two-row board for quickdraws',
    price: 28.0,
    slug: 'product-sport-board.html',
    badge: 'Sport',
    hasColor: true,
    defaultColor: 'moss',
    image: productImages('sport-board', 'moss').gear,
    short: 'A two-row board for a sport rack: 7 closed slots below and 6 above, whose quickdraws hang down through a long window so the rows never tangle. Every slot is fully enclosed.',
  },
  'approach-bar': {
    id: 'approach-bar',
    name: 'The Approach Bar',
    tagline: 'Ultralight 6 mm quickdraw bar',
    price: 16.0,
    slug: 'product-approach-bar.html',
    badge: 'Ultralight',
    hasColor: true,
    defaultColor: 'ink',
    image: productImages('approach-bar', 'ink').gear,
    short: 'An ultralight 6 mm bar for 7 quickdraws: about 36 g, light enough to live in your pack. Every slot is fully enclosed, so nothing falls off on the approach.',
  },
  'pocket-bar': {
    id: 'pocket-bar',
    name: 'The Pocket Bar',
    tagline: '4-slot bar for a pack lid or glovebox',
    price: 12.0,
    slug: 'product-pocket-bar.html',
    badge: 'Pocket size',
    hasColor: true,
    defaultColor: 'ember',
    image: productImages('pocket-bar', 'ember').gear,
    short: 'A 130 mm bar with 4 closed slots that lives in a pack lid, a glovebox or a crag bag: for your nut tool, a couple of draws, a belay device and a locker. Every slot is fully enclosed.',
  },
  'full-kit': {
    id: 'full-kit',
    name: 'The Full Kit',
    tagline: 'Gear Board + Crag Ring + Sticker Pack',
    price: 62.0,
    compareAt: 70.0,
    slug: 'product-full-kit.html',
    badge: 'Bundle',
    hasColor: false,
    image: productImages('gear-board', 'ember').gear,
    short: 'The Gear Board for home, the Crag Ring for the approach, and a sticker pack, in the colors you pick. Save $8.',
  },
  'gatekeeper': {
    id: 'gatekeeper',
    name: 'The Gatekeeper',
    tagline: 'Gear organizer & helmet hook — V3',
    price: 20.0,
    slug: 'product-gatekeeper.html',
    badge: 'Helmet hook',
    hasColor: true,
    defaultColor: 'rock',
    short: 'A pear-shaped wall hanger, 21 cm tall, that keeps a whole trad rack and your helmet off one hook. Clip cams and draws through the four gear slots, drape slings over the frame, and hang your helmet from the J-hook by its chin strap. "NOT FOR CLIMBING" is debossed right into the rail, because it is genuinely not a rated carabiner.',
  },
  'cup-cradle': {
    id: 'cup-cradle',
    name: 'The Cup Cradle',
    tagline: 'Nalgene-to-cupholder adapter — V2',
    price: 16.0,
    slug: 'product-cup-cradle.html',
    badge: 'New',
    hasColor: true,
    defaultColor: 'ice',
    short: 'A ribbed, tapered stem wedges into 69–79 mm car cupholders and flares at 45° into a 94 mm cup that holds a 32 oz wide-mouth Nalgene upright. Arch windows let you grab the bottle, and a drain hole keeps spills from pooling.',
  },
  'tee': {
    id: 'tee',
    name: 'Rackhouse Tee',
    tagline: 'Logo tee, S–XXL',
    price: 26.0,
    slug: 'product-tee.html',
    badge: 'Merch',
    hasColor: true,
    defaultColor: 'ink',
    image: teeImage('ink'),
    short: 'A soft, midweight cotton tee with the carabiner mark and Rackhouse wordmark printed on the chest. Print-on-demand — made and shipped separately from the 3D-printed gear.',
  },
  'stickers': {
    id: 'stickers',
    name: 'Sticker Pack',
    tagline: 'Set of 4, vinyl, weatherproof',
    price: 8.0,
    slug: 'product-stickers.html',
    badge: 'Merch',
    hasColor: false,
    image: 'img/stickers-pack.svg',
    short: 'Four die-cut vinyl stickers: the carabiner mark, the wordmark, a mountain icon, and a "NOT FOR CLIMBING" tag just like the one debossed on the Gatekeeper. Waterproof, for a bottle, a bumper or a bin.',
  },
};

const CATALOG_ORDER = ['gear-board', 'crag-ring', 'sport-board', 'rock-ring', 'double-ring', 'approach-bar', 'pocket-bar', 'full-kit', 'gatekeeper', 'cup-cradle', 'tee', 'stickers'];

const COMING_SOON = [
  { name: 'Crimp Tray', note: 'A shallow dish for rings, coins and hold-shaped clutter.' },
  { name: 'Chalk Bucket Base', note: 'A weighted foot so your bucket stops tipping at the boulders.' },
];
