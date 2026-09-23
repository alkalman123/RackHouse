# Deploying to Render (optional alternative)

**Not the active deployment.** The live site runs on GitHub Pages
directly from this repo's `main` branch — see the live link if you
don't already have it. Render is documented here only as an alternative
host, mainly useful if you want a custom domain without dealing with
GitHub Pages' own custom-domain setup.

## If you want to move to Render later

1. Go to **render.com**, sign up or log in (GitHub sign-in makes the
   next step easier).
2. **New +** → **Static Site** → connect this repo (`rackhouse`).
3. **Branch:** `main`. **Root Directory:** `.` (this repo's root — the
   site now lives at the top level, not in a subfolder). **Build
   Command:** leave blank. **Publish Directory:** `.`
4. Click **Create Static Site**. You'll get a free
   `https://rackhouse.onrender.com`-style URL, or add a custom domain
   under that service's **Settings → Custom Domains** once you own one.

## After you deploy anywhere: the checklist that actually matters

- [ ] Swap `SHOP.email` in `js/store-data.js` for a real inbox (see this
      repo's `README.md` launch checklist).
- [ ] Decide on payment (see `PAYMENTS-SETUP.md`).
- [ ] Place one real test order yourself, start to finish, on whichever
      URL is live.
