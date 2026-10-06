"""Generates the product side of the website from one catalog, so prices,
specs and copy stay consistent everywhere.

    python3 designs/products.py          # geometry + products-report.json
    python3 designs/render/make_images.py
    python3 designs/make_product_drawings.py
    python3 designs/make_site.py

Writes: product pages for the carabiner organizers, the Full Kit bundle
page, the product blocks in js/store-data.js, the shop grid, the footer
Shop list on every page, and redirect stubs for retired products.
"""

import glob
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = "https://alkalman123.github.io/RackHouse/"
REPORT = json.load(open(os.path.join(HERE, "products-report.json")))

COLORS = [("rock", "Rock", "#63707c"), ("moss", "Moss", "#55805a"), ("ice", "Ice", "#4a90c2"),
          ("sand", "Sand", "#c9a86a"), ("ink", "Ink", "#202326"), ("ember", "Ember", "#d85c2a")]

# ----------------------------------------------------------------- catalog
# Every carabiner organizer: closed openings only, prints flat, no supports.
ORGANIZERS = {
    "gear-board": dict(
        name="The Gear Board", price=38.0, badge="Flagship", default="ember",
        tagline="18-slot board for a whole rack",
        card="Your whole rack on one board: 18 closed slots in three rows.",
        short="Your whole rack on one board. 18 closed slots in three rows of six: quickdraws on the bottom row, cams and nuts on the rows above, each hanging through its own window so nothing tangles. Every opening is fully enclosed, so nothing falls off in the closet, the car, your pack or at the crag.",
        desc=["Your whole rack on one board. Eighteen closed slots in three rows of six: clip quickdraws on the bottom row and cams, nuts and slings on the rows above. Each upper row hangs through its own long window, so nothing tangles with the row below.",
              "Every opening is fully enclosed, so a clipped carabiner can't fall off in any direction: in the gear closet, bouncing around in the car, stuffed in a pack or leaning against a boulder at the crag. Hang it on two hooks or screws through the top slots, or run a sling through both and hang it from anything."],
        holds="A double rack of cams, a set of nuts and six quickdraws",
        hang_how="Two top slots (24 × 12 mm): hang it on two hooks, two screws with washers, or run a sling through both slots and hang it from a single hook, a car grab handle or a tree at the crag.",
        gear_word="a full rack", use_h="A whole rack, in order, on one board.",
        use_p="Quickdraws along the bottom, cams in size order across the middle, big cams and slings up top. Rack up by unclipping a row at a time, and see at a glance what's missing before you leave.",
        related=["crag-ring", "sport-board", "full-kit"]),
    "crag-ring": dict(
        name="The Crag Ring", price=24.0, badge="Crag favorite", default="rock",
        tagline="Carry-handle gear ring for the crag",
        card="A light gear ring with a carry handle: grab your rack like a bag.",
        short="A light 7 mm gear ring with a hand-size carry handle. Rack your cams through 11 closed windows, grab the handle and walk to the crag, then clip the handle to a sling or a tree. Every window is fully enclosed, so nothing falls off on the approach.",
        desc=["A light gear ring with a hand-size carry handle on top. Clip your cams through its 11 closed windows, grab the handle and carry your whole rack like a bag: from the closet to the car, from the car to the crag.",
              "At the base of the route, clip the handle to a sling, a tree or your pack and rack straight off it. At home it hangs on any hook. Every window is fully enclosed, so nothing falls off on the walk in."],
        holds="A single rack of cams, or 11 pieces of gear",
        hang_how="The 76 × 26 mm carry handle fits a hand, a hook, a carabiner or a sling.",
        gear_word="a trad rack", use_h="Carry your rack like a bag.",
        use_p="Cams in size order around the ring, handle on top. Pick it up by the handle in the car, clip it to a tree at the crag, and hang it back on the hook when you're home.",
        related=["gear-board", "rock-ring", "full-kit"]),
    "rock-ring": dict(
        name="The Rock Ring", price=28.0, badge="Trad", default="sand",
        tagline="Flat gear ring for a trad rack",
        card="A flat ring with 13 closed windows for your cams.",
        short="A flat gear ring with 13 closed windows punched right through it. Rack your cams in size order around the ring and hang it from the top eye. Nothing sticks out, so it packs flat and never snags; every window is fully enclosed, so nothing falls off.",
        desc=["A flat gear ring for a trad rack: 13 closed windows punched right through a wide ring. Clip your cams in size order around it, and hang it from the top eye on a hook, a carabiner or a sling.",
              "Nothing sticks out, so it slides flat into a pack or a crate without snagging. Every window is fully enclosed, so a clipped carabiner can't fall off, whichever way the ring gets tossed."],
        holds="A single rack of cams plus nuts, 13 pieces",
        hang_how="24 mm top eye: a hook, a carabiner or a sling.",
        gear_word="a trad rack", use_h="Your cams, in size order, in a circle.",
        use_p="Smallest to biggest around the ring, so you can see the whole rack at a glance and rack up in order.",
        related=["double-ring", "crag-ring", "gear-board"]),
    "double-ring": dict(
        name="The Double Ring", price=34.0, badge="Trad + sport", default="ice",
        tagline="Two rows: cams outside, draws inside",
        card="Two rows of windows: cams on the outside, draws and nuts inside.",
        short="A two-row gear ring with 20 closed windows: 13 around the outside for cams and 7 on the inner row for quickdraws, nuts and a nut tool, which hang through the middle. Every window is fully enclosed.",
        desc=["Two rows of closed windows on one ring: 13 around the outside for cams, and 7 on the inner row for quickdraws, nuts and a nut tool, which hang through the big center opening.",
              "It's the whole trad kit (rack, draws and the small stuff) on one ring that hangs from the top eye. Every window is fully enclosed, so nothing falls off in the car or the pack."],
        holds="A rack of cams plus draws, nuts and a nut tool, 20 pieces",
        hang_how="24 mm top eye: a hook, a carabiner or a sling.",
        gear_word="a trad rack and draws", use_h="Cams outside, everything else inside.",
        use_p="Cams fan out around the outer row; draws and nuts hang through the middle from the inner row, so the two never tangle.",
        related=["rock-ring", "gear-board", "crag-ring"]),
    "sport-board": dict(
        name="The Sport Board", price=28.0, badge="Sport", default="moss",
        tagline="Two-row board for quickdraws",
        card="Two rows of closed slots for a full sport rack of quickdraws.",
        short="A two-row board for a sport rack: 7 closed slots below and 6 above, whose quickdraws hang down through a long window so the rows never tangle. Every slot is fully enclosed.",
        desc=["A full sport rack on one board: 7 closed slots on the bottom row and 6 on the top row. The top row's quickdraws hang down through a long window, so the two rows never tangle.",
              "Hang it in the closet, from a headrest in the car, or from a sling at the crag. Every slot is fully enclosed, so a draw can't fall off however it's carried."],
        holds="13 quickdraws, or draws plus slings and a belay device",
        hang_how="Two end slots (24 × 12 mm): two hooks, two screws with washers, or a sling through both.",
        gear_word="quickdraws", use_h="Thirteen draws, two rows, zero tangles.",
        use_p="Bottom row hangs below the board; top row hangs through the window in the middle. Grab a draw one-handed without disturbing the rest.",
        related=["approach-bar", "gear-board", "pocket-bar"]),
    "approach-bar": dict(
        name="The Approach Bar", price=16.0, badge="Ultralight", default="ink",
        tagline="Ultralight 6 mm quickdraw bar",
        card="Ultralight 6 mm bar for 7 quickdraws: about 36 g.",
        short="An ultralight 6 mm bar for 7 quickdraws: about 36 g, light enough to live in your pack. Every slot is fully enclosed, so nothing falls off on the approach.",
        desc=["Seven closed slots on an ultralight 6 mm bar that weighs about 36 g. Rack your draws on it at home and throw it straight in your pack: it's thin enough to slide down the back panel.",
              "At the crag, clip the end slots to a sling or your harness and hand draws out in order. Every slot is fully enclosed, so nothing falls off."],
        holds="7 quickdraws",
        hang_how="Two end slots: hooks, a sling, or a carabiner on your harness or pack.",
        gear_word="quickdraws", use_h="Seven draws, 36 grams.",
        use_p="Light enough to forget it's in the pack, stiff enough to keep seven draws in order.",
        related=["sport-board", "pocket-bar", "gear-board"]),
    "pocket-bar": dict(
        name="The Pocket Bar", price=12.0, badge="Pocket size", default="ember",
        tagline="4-slot bar for a pack lid or glovebox",
        card="A 130 mm bar with 4 slots: lives in a pack lid or glovebox.",
        short="A 130 mm bar with 4 closed slots that lives in a pack lid, a glovebox or a crag bag: for your nut tool, a couple of draws, a belay device and a locker. Every slot is fully enclosed.",
        desc=["Four closed slots on a 130 mm bar small enough for a pack lid, a glovebox or a crag bag. It's for the stuff that always goes missing: nut tool, belay device, a locker and a couple of draws.",
              "Clip it to your harness or pack, or hang it on a hook by its end slots. Every slot is fully enclosed, so nothing falls off."],
        holds="4 pieces: draws, a nut tool, a belay device or lockers",
        hang_how="Two end slots: a hook, a carabiner or a sling.",
        gear_word="quickdraws", use_h="The small stuff, in one place.",
        use_p="Nut tool, belay device and a couple of draws, clipped together so they're always in the pack when you need them.",
        related=["approach-bar", "sport-board", "crag-ring"]),
}
BUNDLE = dict(id="full-kit", name="The Full Kit", price=62.0, compare=70.0, badge="Bundle",
              tagline="Gear Board + Crag Ring + Sticker Pack",
              short="The Gear Board for home, the Crag Ring for the approach, and a sticker pack, in the colors you pick. Save $8.")
ORDER = ["gear-board", "crag-ring", "sport-board", "rock-ring", "double-ring", "approach-bar", "pocket-bar", "full-kit",
         "gatekeeper", "cup-cradle", "tee", "stickers"]
RETIRED = {"product-draw-bar.html": "product-sport-board.html", "product-felt-pads.html": "shop.html",
           "product-gift-duo.html": "product-full-kit.html"}
FOOTER_SHOP = [("product-gear-board.html", "The Gear Board"), ("product-crag-ring.html", "The Crag Ring"),
               ("product-sport-board.html", "The Sport Board"), ("product-rock-ring.html", "The Rock Ring"),
               ("product-double-ring.html", "The Double Ring"), ("product-approach-bar.html", "The Approach Bar"),
               ("product-pocket-bar.html", "The Pocket Bar"), ("product-full-kit.html", "The Full Kit"),
               ("product-gatekeeper.html", "The Gatekeeper"), ("product-cup-cradle.html", "The Cup Cradle"),
               ("product-tee.html", "Rackhouse Tee"), ("product-stickers.html", "Sticker Pack"), ("shop.html", "All products")]

CHECK = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>'


def esc(s):
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def js_str(s):
    return "'" + s.replace("\\", "\\\\").replace("'", "\\'") + "'"


def img(pid, color, view):
    return f"img/products/{pid}-{color}-{view}.jpg"


def frame():
    """Head/header/drawer and footer of an existing product page, as a template."""
    s = open(os.path.join(ROOT, "product-gatekeeper.html")).read()
    head = s[:s.index('<main id="main">')]
    foot = s[s.index("</main>"):]
    foot = foot[:foot.index("<script src=\"js/store-data.js\"></script>")]
    return head, foot


def set_head(head, title, desc, image, url, price):
    head = re.sub(r"<title>.*?</title>", f"<title>{esc(title)} — Rackhouse</title>", head)
    for prop in ('name="description"', 'property="og:description"', 'name="twitter:description"'):
        head = re.sub(rf'(<meta {prop} content=")[^"]*', lambda m: m.group(1) + esc(desc), head)
    for prop in ('property="og:title"', 'name="twitter:title"'):
        head = re.sub(rf'(<meta {prop} content=")[^"]*', lambda m: m.group(1) + esc(title) + " — Rackhouse", head)
    for prop in ('property="og:image"', 'name="twitter:image"'):
        head = re.sub(rf'(<meta {prop} content=")[^"]*', lambda m: m.group(1) + SITE + image, head)
    head = re.sub(r'(<meta property="og:url" content=")[^"]*', lambda m: m.group(1) + SITE + url, head)
    head = re.sub(r'(<meta property="product:price:amount" content=")[^"]*', lambda m: m.group(1) + f"{price:.2f}", head)
    return head


def swatches(default, attr=""):
    return "".join(f'\n            <button type="button" class="swatch-btn{" selected" if k == default else ""}" data-color-key="{k}" style="background:{h};" aria-label="{n}"></button>'
                   for k, n, h in COLORS)


def card(pid, badge_cls="badge"):
    if pid == "full-kit":
        return (f'<a href="product-full-kit.html" class="product-card">\n        <div class="thumb"><div class="badges"><span class="badge badge-dark">Bundle</span></div>'
                f'<img loading="lazy" src="{img("gear-board", "ember", "gear")}" alt="The Full Kit bundle"></div>\n'
                f'        <div class="body"><div class="title-row"><h3>The Full Kit</h3><span class="price">${BUNDLE["price"]:.2f}</span></div><p class="desc">Gear Board + Crag Ring + stickers. Save $8.</p></div>\n      </a>')
    c = ORGANIZERS[pid]
    return (f'<a href="product-{pid}.html" class="product-card">\n        <div class="thumb"><div class="badges"><span class="badge badge-ember">{esc(c["badge"])}</span></div>'
            f'<img loading="lazy" src="{img(pid, c["default"], "gear")}" alt="{esc(c["name"])} loaded with {esc(c["gear_word"])}"></div>\n'
            f'        <div class="body"><div class="title-row"><h3>{esc(c["name"])}</h3><span class="price">${c["price"]:.2f}</span></div><p class="desc">{esc(c["card"])}</p></div>\n      </a>')


def product_page(pid):
    c = ORGANIZERS[pid]
    r = REPORT[pid]
    w, h, _ = r["size_mm"]
    head, foot = frame()
    desc_meta = f'{c["name"]}: {c["short"]} {w:g} x {h:g} mm, about {r["est_weight_g"]} g.'
    head = set_head(head, c["name"], desc_meta[:300], img(pid, c["default"], "gear"), f"product-{pid}.html", c["price"])
    d = c["default"]
    dname = dict((k, n) for k, n, _ in COLORS)[d]
    paras = "\n".join(f'        <p class="desc">{esc(p)}</p>' for p in c["desc"])
    main = f'''<main id="main">
<section class="section-tight">
  <div class="container">
    <div class="breadcrumbs">
      <a href="index.html">Home</a><span class="sep">/</span>
      <a href="shop.html">Shop</a><span class="sep">/</span>
      <span class="current">{esc(c["name"])}</span>
    </div>

    <div class="pdp">
      <div class="pdp-gallery">
        <div class="filter-row gallery-tabs" role="group" aria-label="Gallery view">
          <button type="button" class="filter-chip active" data-gallery-tab="photos">Photos</button>
          <button type="button" class="filter-chip" data-gallery-tab="3d">3D View</button>
        </div>
        <div class="main-frame" id="galleryPhotoFrame">
          <img id="pdpMainImg" src="{img(pid, d, "gear")}" alt="{esc(c["name"])} loaded with {esc(c["gear_word"])}">
        </div>
        <div class="main-frame" id="gallery3DFrame" style="display:none;">
          <div id="viewer3D" style="width:100%;height:100%;"></div>
          <span class="viewer-hint">Drag to rotate · Scroll to zoom</span>
        </div>
        <div class="pdp-thumbs">
          <button type="button" data-angle="gear" class="active"><img loading="lazy" src="{img(pid, d, "gear")}" alt="Loaded with gear"></button>
          <button type="button" data-angle="hero"><img loading="lazy" src="{img(pid, d, "hero")}" alt="Three-quarter view"></button>
          <button type="button" data-angle="front"><img loading="lazy" src="{img(pid, d, "front")}" alt="Front view"></button>
          <button type="button" data-angle="edge"><img loading="lazy" src="{img(pid, d, "edge")}" alt="Edge view"></button>
        </div>
        <p class="muted" style="font-size:12.5px;margin-top:10px;">Images are 3D renders of the actual product file, shown with typical climbing gear.</p>
      </div>

      <div class="pdp-info">
        <div class="badges-row">
          <span class="badge badge-ember">{esc(c["badge"])}</span>
          <span class="badge">{r["openings"]} closed openings</span>
        </div>
        <h1>{esc(c["name"])}</h1>
        <p class="muted" style="margin-top:6px;font-weight:650;">{esc(c["tagline"])}</p>
        <div class="price-row">
          <span class="price num">${c["price"]:.2f}</span>
        </div>
{paras}

        <div class="option-block">
          <div class="opt-title"><span>Color</span><span id="selectedColorName">{dname}</span></div>
          <div class="swatch-picker" id="swatchPicker">{swatches(d)}
          </div>
        </div>

        <div class="buy-row">
          <div class="qty-stepper" id="pdpQty">
            <button type="button" data-step="dec" aria-label="Decrease quantity">−</button>
            <input type="text" inputmode="numeric" value="1" readonly aria-label="Quantity">
            <button type="button" data-step="inc" aria-label="Increase quantity">+</button>
          </div>
          <button type="button" id="addToCartBtn" class="btn btn-primary">Add to cart</button>
          <button type="button" id="buyNowBtn" class="btn btn-ember">Buy now</button>
        </div>

        <ul class="pdp-trust">
          <li>{CHECK} Every opening fully enclosed: clipped gear can't fall off</li>
          <li>{CHECK} Made to order — ships in 2–4 business days</li>
          <li>{CHECK} Free standard shipping over $60</li>
        </ul>

        <div class="safety-note">
          <b>Not climbing protection</b>
          {esc(c["name"])} is a gear organizer, not an anchor, and it says NOT FOR CLIMBING right on it. Never clip it into a climbing system or hang body weight from it.
        </div>

        <div class="accordion" id="details">
          <details open>
            <summary>Details &amp; specs{CHEV}</summary>
            <div class="panel">
              <table class="spec-table">
                <tr><th>Size</th><td>{w:g} × {h:g} mm, {r["thickness_mm"]:g} mm thick ({w / 25.4:.1f} × {h / 25.4:.1f} in)</td></tr>
                <tr><th>Weight</th><td>About {r["est_weight_g"]} g</td></tr>
                <tr><th>Openings</th><td>{r["openings"]} fully enclosed openings, each at least 14 mm across</td></tr>
                <tr><th>Holds</th><td>{esc(c["holds"])}</td></tr>
                <tr><th>Clip strip</th><td>{r["clip_web_mm"][0]:g}–{r["clip_web_mm"][1]:g} mm: easy for any standard carabiner to close around</td></tr>
                <tr><th>Hangs from</th><td>{esc(c["hang_how"])}</td></tr>
                <tr><th>Material</th><td>PLA+ (PETG on request for hot cars), matte finish</td></tr>
                <tr><th>Text</th><td>"RACKHOUSE" and "NOT FOR CLIMBING" debossed in</td></tr>
                <tr><th>Design</th><td>Original Rackhouse design. Prints flat, no supports</td></tr>
                <tr><th>Colorways</th><td>Rock, Moss, Ice, Sand, Ink, Ember</td></tr>
              </table>
              <div class="spec-image"><img loading="lazy" src="img/products/{pid}-dimensions.jpg" alt="Dimension drawing of {esc(c["name"])}: {w:g} by {h:g} mm"></div>
            </div>
          </details>
          <details>
            <summary>Closet, car, pack, crag{CHEV}</summary>
            <div class="panel">
              <p><b>Closet:</b> {esc(c["hang_how"])}</p>
              <p><b>Car:</b> hang it from a grab handle or headrest with a carabiner. Gear stays clipped on bumpy roads because every opening is closed.</p>
              <p><b>Pack:</b> it's flat and rounded, so it slides in without snagging, and nothing comes unclipped in the pack.</p>
              <p><b>Crag:</b> clip it to a sling, a tree or your pack at the base and rack straight off it.</p>
            </div>
          </details>
          <details>
            <summary>Material &amp; care{CHEV}</summary>
            <div class="panel">
              <p>Printed in PLA+. Wipe clean with a damp cloth. PLA+ softens above about 55 °C (130 °F), so if it'll ride in a car parked in the sun, ask for PETG in the order notes and we'll print it in that instead, same price.</p>
            </div>
          </details>
          <details>
            <summary>Shipping &amp; returns{CHEV}</summary>
            <div class="panel">
              <p>Made to order, 2–4 business days before it ships. Full policy on the <a href="shipping-returns.html" style="color:var(--ember-dark);text-decoration:underline;">shipping &amp; returns page</a>.</p>
            </div>
          </details>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="grid grid-2" style="align-items:center; gap:56px;">
      <div class="reveal">
        <img loading="lazy" src="{img(pid, "ink" if d != "ink" else "rock", "gear")}" alt="{esc(c["name"])} in Ink, loaded with {esc(c["gear_word"])}" style="border-radius:var(--radius-lg); border:1px solid var(--line); width:100%; height:auto; display:block;">
      </div>
      <div class="reveal reveal-1">
        <span class="eyebrow">In use</span>
        <h2 style="margin-top:10px;">{esc(c["use_h"])}</h2>
        <p class="lede" style="margin-top:16px;">{esc(c["use_p"])}</p>
      </div>
    </div>
  </div>
</section>

<section class="section" style="background:var(--paper-dim);">
  <div class="container">
    <div class="section-head center">
      <span class="eyebrow">More from Rackhouse</span>
      <h2>Pairs well with</h2>
    </div>
    <div class="grid grid-3">
      {(chr(10) + "      ").join(card(x) for x in c["related"])}
    </div>
  </div>
</section>
'''
    script = f'''<script src="js/store-data.js"></script>
<script src="js/cart.js"></script>
<script src="js/ui.js"></script>
<script type="module">
  import {{ mountModelViewer }} from './js/model-viewer.js';
  window.mountModelViewer = mountModelViewer;
</script>
<script>
(function () {{
  const PID = '{pid}';
  const params = new URLSearchParams(location.search);
  const requested = params.get('color');
  let selected = COLORWAYS.some((c) => c.key === requested) ? requested : PRODUCTS[PID].defaultColor;
  let activeAngle = 'gear';
  const mainImg = document.getElementById('pdpMainImg');
  const thumbBtns = document.querySelectorAll('.pdp-thumbs button');
  const swatchBtns = document.querySelectorAll('.swatch-btn');
  const colorLabel = document.getElementById('selectedColorName');
  let viewer = null;
  const tabBtns = document.querySelectorAll('[data-gallery-tab]');
  const photoFrame = document.getElementById('galleryPhotoFrame');
  const frame3D = document.getElementById('gallery3DFrame');
  const viewerContainer = document.getElementById('viewer3D');

  function ensureViewer() {{
    if (viewer || !window.mountModelViewer) return;
    const loading = document.createElement('div');
    loading.className = 'viewer-loading';
    loading.textContent = 'Loading 3D model…';
    viewerContainer.appendChild(loading);
    viewer = window.mountModelViewer(viewerContainer, {{
      stlUrl: 'models/' + PID + '.stl',
      color: colorway(selected).hex,
      onReady: () => loading.remove(),
      onError: () => {{ loading.textContent = 'Could not load the 3D model.'; }},
    }});
  }}
  tabBtns.forEach((btn) => {{
    btn.addEventListener('click', () => {{
      tabBtns.forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const is3D = btn.getAttribute('data-gallery-tab') === '3d';
      photoFrame.style.display = is3D ? 'none' : '';
      frame3D.style.display = is3D ? '' : 'none';
      if (is3D) ensureViewer();
    }});
  }});
  function render() {{
    const set = productImages(PID, selected);
    const c = colorway(selected);
    mainImg.src = set[activeAngle];
    mainImg.alt = `${{PRODUCTS[PID].name}} in ${{c.name}}, ${{activeAngle === 'gear' ? 'loaded with gear' : activeAngle + ' view'}}`;
    if (viewer) viewer.setColor(c.hex);
    thumbBtns.forEach((b) => {{
      const angle = b.getAttribute('data-angle');
      b.querySelector('img').src = set[angle];
      b.classList.toggle('active', angle === activeAngle);
    }});
    swatchBtns.forEach((b) => b.classList.toggle('selected', b.getAttribute('data-color-key') === selected));
    colorLabel.textContent = c.name;
  }}
  swatchBtns.forEach((b) => b.addEventListener('click', () => {{ selected = b.getAttribute('data-color-key'); render(); }}));
  thumbBtns.forEach((b) => b.addEventListener('click', () => {{ activeAngle = b.getAttribute('data-angle'); render(); }}));
  render();
  const qty = initQtyStepper(document.getElementById('pdpQty'), {{ min: 1, max: 10 }});
  function currentItem() {{
    const c = colorway(selected);
    return {{
      key: `${{PID}}:${{selected}}`, productId: PID, name: PRODUCTS[PID].name, variant: c.name, variantHex: c.hex,
      price: PRODUCTS[PID].price, qty: qty.get(), image: productImages(PID, selected).gear,
    }};
  }}
  document.getElementById('addToCartBtn').addEventListener('click', () => addToCartAndNotify(currentItem()));
  document.getElementById('buyNowBtn').addEventListener('click', () => {{
    const stripeLink = getStripeLink(PID);
    if (stripeLink) {{ window.location.href = stripeLink; return; }}
    cartAdd(currentItem());
    window.location.href = 'checkout.html';
  }});
}})();
</script>
</body>
</html>
'''
    with open(os.path.join(ROOT, f"product-{pid}.html"), "w") as f:
        f.write(head + main + foot + script)


def bundle_page():
    b = BUNDLE
    head, foot = frame()
    head = set_head(head, b["name"], "The Full Kit: the Gear Board for home, the Crag Ring for the approach, and a Rackhouse sticker pack, in the colors you pick. Save $8.",
                    img("gear-board", "ember", "gear"), "product-full-kit.html", b["price"])
    head = head.replace('<script type="importmap">{"imports": {"three": "./js/vendor/three.module.min.js"}}</script>\n', "")
    main = f'''<main id="main">
<section class="section-tight">
  <div class="container">
    <div class="breadcrumbs">
      <a href="index.html">Home</a><span class="sep">/</span>
      <a href="shop.html">Shop</a><span class="sep">/</span>
      <span class="current">The Full Kit</span>
    </div>

    <div class="pdp">
      <div class="pdp-gallery">
        <div class="main-frame" style="display:grid; grid-template-columns:1fr 1fr; gap:2px;">
          <img id="kitImg1" src="{img("gear-board", "ember", "gear")}" alt="The Gear Board, Ember, loaded with gear" style="width:100%;height:100%;object-fit:cover;">
          <img id="kitImg2" src="{img("crag-ring", "rock", "gear")}" alt="The Crag Ring, Rock, loaded with cams" style="width:100%;height:100%;object-fit:cover;">
        </div>
        <p class="muted" style="font-size:12.5px;text-align:center;">Preview updates as you choose colors below. Images are 3D renders.</p>
      </div>

      <div class="pdp-info">
        <div class="badges-row">
          <span class="badge badge-dark">Bundle</span>
          <span class="badge">Save $8</span>
        </div>
        <h1>The Full Kit</h1>
        <p class="muted" style="margin-top:6px;font-weight:650;">{esc(b["tagline"])}</p>
        <div class="price-row">
          <span class="price num">${b["price"]:.2f}</span>
          <span class="was num">${b["compare"]:.2f}</span>
        </div>
        <p class="desc">Everything you need to get your gear organized, at home and on the move. The Gear Board holds your whole rack in the closet; the Crag Ring carries the cams you need to the crag; and a Rackhouse sticker pack goes in the box. Every opening on both pieces is fully enclosed, so nothing falls off.</p>

        <div class="option-block">
          <div class="opt-title"><span>Gear Board color</span><span id="kitColorName1">Ember</span></div>
          <div class="swatch-picker" data-picker="1">{swatches("ember")}
          </div>
        </div>
        <div class="option-block" style="margin-top:20px;padding-top:20px;">
          <div class="opt-title"><span>Crag Ring color</span><span id="kitColorName2">Rock</span></div>
          <div class="swatch-picker" data-picker="2">{swatches("rock")}
          </div>
        </div>

        <div class="buy-row">
          <div class="qty-stepper" id="pdpQty">
            <button type="button" data-step="dec" aria-label="Decrease quantity">−</button>
            <input type="text" inputmode="numeric" value="1" readonly aria-label="Quantity">
            <button type="button" data-step="inc" aria-label="Increase quantity">+</button>
          </div>
          <button type="button" id="addToCartBtn" class="btn btn-primary">Add to cart</button>
          <button type="button" id="buyNowBtn" class="btn btn-ember">Buy now</button>
        </div>

        <ul class="pdp-trust">
          <li>{CHECK} Gear Board ($38) + Crag Ring ($24) + Sticker Pack ($8)</li>
          <li>{CHECK} One box, one shipment, made to order in 2–4 business days</li>
          <li>{CHECK} Free standard shipping (it's over $60)</li>
        </ul>

        <div class="safety-note">
          <b>Not climbing protection</b>
          Both pieces are gear organizers, not anchors. They say NOT FOR CLIMBING right on them.
        </div>

        <div class="accordion">
          <details open>
            <summary>What's in the box{CHEV}</summary>
            <div class="panel">
              <table class="spec-table">
                <tr><th>The Gear Board</th><td>18 closed slots, {REPORT["gear-board"]["size_mm"][0]:g} × {REPORT["gear-board"]["size_mm"][1]:g} mm, about {REPORT["gear-board"]["est_weight_g"]} g. <a href="product-gear-board.html" style="color:var(--ember-dark);text-decoration:underline;">Details</a></td></tr>
                <tr><th>The Crag Ring</th><td>11 closed windows and a carry handle, {REPORT["crag-ring"]["size_mm"][0]:g} × {REPORT["crag-ring"]["size_mm"][1]:g} mm, about {REPORT["crag-ring"]["est_weight_g"]} g. <a href="product-crag-ring.html" style="color:var(--ember-dark);text-decoration:underline;">Details</a></td></tr>
                <tr><th>Sticker Pack</th><td>4 weatherproof vinyl stickers</td></tr>
              </table>
            </div>
          </details>
          <details>
            <summary>Shipping &amp; returns{CHEV}</summary>
            <div class="panel"><p>Made to order, 2–4 business days before it ships. Full policy on the <a href="shipping-returns.html" style="color:var(--ember-dark);text-decoration:underline;">shipping &amp; returns page</a>.</p></div>
          </details>
        </div>
      </div>
    </div>
  </div>
</section>
'''
    script = '''<script src="js/store-data.js"></script>
<script src="js/cart.js"></script>
<script src="js/ui.js"></script>
<script>
(function () {
  let color1 = 'ember';
  let color2 = 'rock';
  function render() {
    document.getElementById('kitImg1').src = productImages('gear-board', color1).gear;
    document.getElementById('kitImg2').src = productImages('crag-ring', color2).gear;
    document.getElementById('kitColorName1').textContent = colorway(color1).name;
    document.getElementById('kitColorName2').textContent = colorway(color2).name;
    document.querySelectorAll('[data-picker="1"] .swatch-btn').forEach((b) => b.classList.toggle('selected', b.getAttribute('data-color-key') === color1));
    document.querySelectorAll('[data-picker="2"] .swatch-btn').forEach((b) => b.classList.toggle('selected', b.getAttribute('data-color-key') === color2));
  }
  document.querySelectorAll('[data-picker="1"] .swatch-btn').forEach((b) => b.addEventListener('click', () => { color1 = b.getAttribute('data-color-key'); render(); }));
  document.querySelectorAll('[data-picker="2"] .swatch-btn').forEach((b) => b.addEventListener('click', () => { color2 = b.getAttribute('data-color-key'); render(); }));
  render();
  const qty = initQtyStepper(document.getElementById('pdpQty'), { min: 1, max: 10 });
  function currentItem() {
    const c1 = colorway(color1), c2 = colorway(color2);
    return {
      key: `full-kit:${color1}:${color2}`, productId: 'full-kit', name: 'The Full Kit',
      variant: `Gear Board ${c1.name} · Crag Ring ${c2.name}`,
      price: PRODUCTS['full-kit'].price, qty: qty.get(), image: productImages('gear-board', color1).gear,
    };
  }
  document.getElementById('addToCartBtn').addEventListener('click', () => addToCartAndNotify(currentItem()));
  document.getElementById('buyNowBtn').addEventListener('click', () => {
    const stripeLink = getStripeLink('full-kit');
    if (stripeLink) { window.location.href = stripeLink; return; }
    cartAdd(currentItem());
    window.location.href = 'checkout.html';
  });
})();
</script>
</body>
</html>
'''
    with open(os.path.join(ROOT, "product-full-kit.html"), "w") as f:
        f.write(head + main + foot + script)


def store_data():
    p = os.path.join(ROOT, "js", "store-data.js")
    s = open(p).read()
    links = "\n".join(f"      '{k}': ''," for k in ORDER)
    s = re.sub(r"    productLinks: \{\n.*?\n    \},", "    productLinks: {\n" + links + "\n    },", s, flags=re.S)
    a = s.find("function rockRingImages(colorKey) {")
    if a < 0:
        a = s.index("// Product renders for the carabiner organizers")
    b = s.index("function gatekeeperImages(colorKey) {")
    s = s[:a] + '''// Product renders for the carabiner organizers (designs/render/make_images.py)
function productImages(id, colorKey) {
  const base = `img/products/${id}-${colorKey}`;
  return { gear: `${base}-gear.jpg`, hero: `${base}-hero.jpg`, front: `${base}-front.jpg`, edge: `${base}-edge.jpg` };
}

''' + s[b:]
    entries = []
    for pid, c in ORGANIZERS.items():
        entries.append(f"""  '{pid}': {{
    id: '{pid}',
    name: {js_str(c["name"])},
    tagline: {js_str(c["tagline"])},
    price: {c["price"]:.1f},
    slug: 'product-{pid}.html',
    badge: {js_str(c["badge"])},
    hasColor: true,
    defaultColor: '{c["default"]}',
    image: productImages('{pid}', '{c["default"]}').gear,
    short: {js_str(c["short"])},
  }},""")
    entries.append(f"""  'full-kit': {{
    id: 'full-kit',
    name: 'The Full Kit',
    tagline: {js_str(BUNDLE["tagline"])},
    price: {BUNDLE["price"]:.1f},
    compareAt: {BUNDLE["compare"]:.1f},
    slug: 'product-full-kit.html',
    badge: 'Bundle',
    hasColor: false,
    image: productImages('gear-board', 'ember').gear,
    short: {js_str(BUNDLE["short"])},
  }},""")
    a = s.index("const PRODUCTS = {\n") + len("const PRODUCTS = {\n")
    keep = {}
    for key in ("gatekeeper", "cup-cradle", "tee", "stickers"):
        m = re.search(rf"  '{key}': \{{\n.*?\n  \}},\n", s, flags=re.S)
        keep[key] = m.group(0)
    b = s.index("\n};\n", a)
    body = "\n".join(entries) + "\n" + "".join(keep[k] for k in ("gatekeeper", "cup-cradle", "tee", "stickers")).rstrip("\n")
    s = s[:a] + body + s[b:]
    s = re.sub(r"const CATALOG_ORDER = \[.*?\];", "const CATALOG_ORDER = [" + ", ".join(f"'{k}'" for k in ORDER) + "];", s)
    s = s.replace("    badge: 'Flagship',\n    hasColor: true,\n    defaultColor: 'rock',\n    short: 'A pear-shaped",
                  "    badge: 'Helmet hook',\n    hasColor: true,\n    defaultColor: 'rock',\n    short: 'A pear-shaped")
    open(p, "w").write(s)


def footers():
    lis = "\n".join(f'          <li><a href="{h}">{esc(t)}</a></li>' for h, t in FOOTER_SHOP)
    for p in glob.glob(os.path.join(ROOT, "*.html")):
        s = open(p).read()
        s2 = re.sub(r"(<h4>Shop</h4>\n        <ul>\n).*?(\n        </ul>)", lambda m: m.group(1) + lis + m.group(2), s, flags=re.S)
        if s2 != s:
            open(p, "w").write(s2)


def redirects():
    for old, new in RETIRED.items():
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Moved — Rackhouse</title>
<meta name="robots" content="noindex">
<link rel="canonical" href="{SITE}{new}">
<meta http-equiv="refresh" content="0; url={new}">
<script>location.replace('{new}');</script>
<link rel="stylesheet" href="css/style.css">
</head>
<body>
<main class="section"><div class="container"><h1>This product has moved.</h1><p class="lede">It's been replaced by a better design. <a href="{new}" style="color:var(--ember-dark);text-decoration:underline;">Continue</a></p></div></main>
</body>
</html>
'''
        open(os.path.join(ROOT, old), "w").write(html)


def shop_grid():
    p = os.path.join(ROOT, "shop.html")
    s = open(p).read()
    cards = []
    for pid in ORDER:
        if pid in ORGANIZERS:
            c = ORGANIZERS[pid]
            dots = "".join(f'\n            <span class="swatch-dot" style="background:{h};"></span>' for _, _, h in COLORS)
            cards.append(f'''      <a href="product-{pid}.html" class="product-card" data-pid="{pid}">
        <div class="thumb">
          <div class="badges"><span class="badge badge-ember">{esc(c["badge"])}</span></div>
          <img loading="lazy" data-shop-img="{pid}" src="{img(pid, c["default"], "gear")}" alt="{esc(c["name"])} loaded with {esc(c["gear_word"])}">
        </div>
        <div class="body">
          <div class="title-row"><h3>{esc(c["name"])}</h3><span class="price">${c["price"]:.2f}</span></div>
          <p class="desc">{esc(c["card"])}</p>
          <div class="swatches">{dots}
          </div>
        </div>
      </a>''')
        elif pid == "full-kit":
            cards.append(f'''      <a href="product-full-kit.html" class="product-card">
        <div class="thumb">
          <div class="badges"><span class="badge badge-dark">Bundle</span><span class="badge">Save $8</span></div>
          <img loading="lazy" src="{img("gear-board", "ember", "gear")}" alt="The Full Kit bundle">
        </div>
        <div class="body">
          <div class="title-row"><h3>The Full Kit</h3><span class="price">${BUNDLE["price"]:.2f} <s class="muted" style="font-weight:500;font-size:.85em;">${BUNDLE["compare"]:.2f}</s></span></div>
          <p class="desc">Gear Board + Crag Ring + Sticker Pack, in the colors you pick.</p>
        </div>
      </a>''')
    start = s.index("<!-- product-grid:start -->")
    end = s.index("<!-- product-grid:end -->")
    s = s[:start] + "<!-- product-grid:start -->\n" + "\n\n".join(cards) + "\n      " + s[end:]
    open(p, "w").write(s)


GK_CARD = ('<a href="product-gatekeeper.html" class="product-card">\n        <div class="thumb"><div class="badges"><span class="badge">Helmet hook</span></div>'
           '<img loading="lazy" src="img/gatekeeper-rock-hero.jpg" alt="The Gatekeeper"></div>\n'
           '        <div class="body"><div class="title-row"><h3>The Gatekeeper</h3><span class="price">$20.00</span></div><p class="desc">Helmet hook and four-slot gear hanger.</p></div>\n      </a>')


def cross_sells():
    """'Pairs well with' on the pages make_site doesn't generate."""
    import re
    picks = {"product-gatekeeper.html": [card("gear-board"), card("crag-ring"), card("full-kit")],
             "product-cup-cradle.html": [card("gear-board"), card("crag-ring"), GK_CARD]}
    for name, cards in picks.items():
        p = os.path.join(ROOT, name)
        s = open(p).read()
        s, n = re.subn(r'(<h2>Pairs well with</h2>\s*</div>\s*<div class="grid grid-3">\n).*?(\n    </div>\n  </div>\n</section>)',
                       lambda m: m.group(1) + "      " + "\n      ".join(cards) + m.group(2), s, count=1, flags=re.S)
        if n != 1:
            raise SystemExit(f"cross-sell grid not found in {name}")
        s = s.replace('<span class="badge badge-ember">Flagship</span>\n          <span class="badge">V3</span>',
                      '<span class="badge">Helmet hook</span>\n          <span class="badge">V3</span>')
        open(p, "w").write(s)


def main():
    for pid in ORGANIZERS:
        product_page(pid)
    bundle_page()
    store_data()
    redirects()
    footers()
    cross_sells()
    if "<!-- product-grid:start -->" in open(os.path.join(ROOT, "shop.html")).read():
        shop_grid()
    print("site generated:", ", ".join(ORGANIZERS), "+ full-kit")


if __name__ == "__main__":
    main()
