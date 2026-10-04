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
      'gatekeeper': '',
      'rock-ring': '',
      'cup-cradle': '',
      'gift-duo': '',
      'felt-pads': '',
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
  // Free design files (business/THINGIVERSE-UPLOAD.md). Paste each
  // Thingiverse / Printables URL once published; blank = "coming soon".
  openDesigns: {
    'gatekeeper': '',
    'rock-ring': '',
    'cup-cradle': '',
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

function rockRingImages(colorKey) {
  return {
    hero: `img/rockring-${colorKey}-hero.jpg`,
    front: `img/rockring-${colorKey}-front.jpg`,
    profile: `img/rockring-${colorKey}-profile.jpg`,
    detail: `img/rockring-${colorKey}-detail.jpg`,
  };
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
  'gatekeeper': {
    id: 'gatekeeper',
    name: 'The Gatekeeper',
    tagline: 'Gear organizer & helmet hook — V3',
    price: 20.0,
    slug: 'product-gatekeeper.html',
    badge: 'Flagship',
    hasColor: true,
    defaultColor: 'rock',
    short: 'A pear-shaped wall hanger, 21 cm tall, that keeps a whole trad rack and your helmet off one hook. Clip cams and draws through the four gear slots, drape slings over the frame, and hang your helmet from the J-hook by its chin strap. "NOT FOR CLIMBING" is debossed right into the rail, because it is genuinely not a rated carabiner.',
  },
  'rock-ring': {
    id: 'rock-ring',
    name: 'The Rock Ring',
    tagline: 'Portable edge lift block — V2',
    price: 34.0,
    slug: 'product-rock-ring.html',
    badge: 'Original',
    hasColor: true,
    defaultColor: 'rock',
    short: 'A 10 cm T-profile block with a 19 mm edge on one side and an 11 mm edge on the other. Run a cord or loading pin through the countersunk channel, hang a weight, and pinch-lift it for finger strength anywhere: garage, hotel room, crag parking lot.',
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
  'gift-duo': {
    id: 'gift-duo',
    name: 'Rock Ring — Gift Duo',
    tagline: 'Two Rock Rings, any two colors',
    price: 62.0,
    compareAt: 68.0,
    slug: 'product-gift-duo.html',
    badge: 'Bundle',
    hasColor: false,
    image: rockRingImages('rock').hero,
    short: 'Two Rock Ring edge blocks in the colorways of your choice, boxed together. Load both hands at once, or give one to your climbing partner.',
  },
  'felt-pads': {
    id: 'felt-pads',
    name: 'Felt Pad Set',
    tagline: 'Self-adhesive felt, 4-pack',
    price: 5.0,
    slug: 'product-felt-pads.html',
    badge: 'Add-on',
    hasColor: false,
    image: gatekeeperImages('sand').front,
    short: 'Four self-adhesive felt strips cut for the Rock Ring’s stem foot and the Cup Cradle’s base, so they sit quietly on a desk, shelf or console without rattling or scuffing.',
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

const CATALOG_ORDER = ['gatekeeper', 'rock-ring', 'cup-cradle', 'gift-duo', 'felt-pads', 'tee', 'stickers'];

const COMING_SOON = [
  { name: 'Crimp Tray', note: 'A shallow dish for rings, coins and hold-shaped clutter.' },
  { name: 'Chalk Bucket Base', note: 'A weighted foot so your bucket stops tipping at the boulders.' },
];
