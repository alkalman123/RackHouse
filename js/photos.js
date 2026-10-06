/* Real prototype photos.
 *
 * Add photos to SHOP.photos in js/store-data.js (tools/prep_photos.py
 * prints the lines to paste). On a product page they appear first in the
 * gallery, and every image carries a corner tag saying whether it is a
 * photo of a printed prototype or a 3D render. On kickstarter.html they
 * fill the "From the print bed" strip, which stays hidden until there is
 * at least one photo.
 */
(function () {
  const all = (typeof SHOP !== 'undefined' && SHOP.photos) || {};
  const PHOTO_TAG = 'Photo · printed prototype';
  const RENDER_TAG = '3D render';

  function tag(frame) {
    let t = frame.querySelector('.media-tag');
    if (!t) {
      t = document.createElement('span');
      t.className = 'media-tag';
      frame.appendChild(t);
    }
    return t;
  }

  function productPage() {
    const m = location.pathname.match(/product-([a-z0-9-]+)\.html$/);
    const frame = document.getElementById('galleryPhotoFrame');
    const mainImg = document.getElementById('pdpMainImg');
    const thumbs = document.querySelector('.pdp-thumbs');
    if (!m || !frame || !mainImg) return;
    const photos = all[m[1]] || [];
    const label = tag(frame);
    const renderBtns = thumbs ? Array.from(thumbs.querySelectorAll('button')) : [];
    let showingPhoto = -1;

    function setLabel() {
      const isPhoto = showingPhoto >= 0;
      label.textContent = isPhoto ? PHOTO_TAG : RENDER_TAG;
      label.classList.toggle('is-photo', isPhoto);
    }

    const photoBtns = photos.map((p, i) => {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'photo-thumb';
      b.setAttribute('aria-label', 'Photo ' + (i + 1) + ': ' + (p.alt || 'printed prototype'));
      b.innerHTML = '<img loading="lazy" alt=""><span class="thumb-flag">Photo</span>';
      b.querySelector('img').src = p.src;
      b.addEventListener('click', () => show(i));
      thumbs.insertBefore(b, renderBtns[0] || null);
      return b;
    });

    function show(i) {
      showingPhoto = i;
      mainImg.src = photos[i].src;
      mainImg.alt = photos[i].alt || 'Photo of a printed prototype';
      photoBtns.forEach((b, k) => b.classList.toggle('active', k === i));
      renderBtns.forEach((b) => b.classList.remove('active'));
      setLabel();
    }

    // any render thumbnail or colour swatch goes back to the renders
    renderBtns.forEach((b) => b.addEventListener('click', () => {
      showingPhoto = -1;
      photoBtns.forEach((p) => p.classList.remove('active'));
      setLabel();
    }));
    document.querySelectorAll('.swatch-btn').forEach((b) => b.addEventListener('click', () => {
      if (showingPhoto >= 0) { showingPhoto = -1; photoBtns.forEach((p) => p.classList.remove('active')); }
      setLabel();
    }));

    const note = document.querySelector('.pdp-gallery > p.muted');
    if (photos.length) {
      show(0);
      if (note) note.textContent = 'Images tagged “Photo” are of a printed prototype; the rest are 3D renders of the product file.';
    } else {
      setLabel();
    }
  }

  function kickstarterStrip() {
    const sec = document.getElementById('ksPhotos');
    if (!sec) return;
    const grid = sec.querySelector('.ks-photo-grid');
    const list = [];
    Object.keys(all).forEach((pid) => (all[pid] || []).forEach((p) => list.push(Object.assign({ pid }, p))));
    if (!list.length) return;
    list.slice(0, 8).forEach((p) => {
      const fig = document.createElement('figure');
      fig.innerHTML = '<img loading="lazy"><figcaption></figcaption>';
      fig.querySelector('img').src = p.src;
      fig.querySelector('img').alt = p.alt || 'Printed prototype';
      fig.querySelector('figcaption').textContent = p.alt || '';
      grid.appendChild(fig);
    });
    sec.hidden = false;
  }

  productPage();
  kickstarterStrip();
})();
