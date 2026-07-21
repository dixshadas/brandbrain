# Deploying the BrandBrain frontend to Vercel

The demo (`web/index.html`) is a self-contained React + Tailwind + Babel page that
runs entirely in the browser on mock data. No build step and no backend are needed.

This repo is configured so a **default repository import serves `web/` correctly**:
- Root [`vercel.json`](./vercel.json) sets `outputDirectory: "web"`, no build command,
  clean URLs, security headers, and an SPA rewrite to `/index.html`.
- [`.vercelignore`](./.vercelignore) keeps the Python backend, docs, and tests out of
  the static deploy.

## Option A — Connect the repo (recommended: auto-deploys on every merge to `main`)

1. Go to <https://vercel.com/new>.
2. **Import** the `dixshadas/brandbrain` GitHub repository.
   (If the repo isn't listed, click *Adjust GitHub App Permissions* and grant access.)
3. Vercel reads the root `vercel.json` automatically:
   - **Framework Preset:** Other
   - **Root Directory:** `./` (leave as the repo root — `outputDirectory` points to `web`)
   - **Build Command:** *(none)*
   - **Output Directory:** `web` (already set by `vercel.json`)
4. Click **Deploy**. You'll get a production URL like `https://brandbrain.vercel.app`.

Every future push/merge to `main` then redeploys automatically.

### Custom domain (if you have one)
Project → **Settings → Domains** → add your domain and follow the DNS instructions.
Vercel serves the production deployment on that domain once DNS verifies.

## Option B — Vercel CLI

```bash
npm i -g vercel
cd /path/to/brandbrain
vercel            # first run: log in + link the project (interactive)
vercel --prod     # promote to the public production URL
```

## Post-deploy verification checklist
- [ ] Production URL loads and the app renders past the "Preparing your brand's memory…" splash.
- [ ] No console errors (React, Tailwind, and Babel load from CDN on first paint).
- [ ] Deep links / refreshes resolve (SPA rewrite to `/index.html`).
- [ ] Security headers present (`X-Content-Type-Options`, `Referrer-Policy`).

> Note: the page loads React/Tailwind/Babel from public CDNs at runtime, so the first
> load needs internet. This works on Vercel's network; it cannot be verified inside a
> sandbox whose egress blocks those CDNs.
