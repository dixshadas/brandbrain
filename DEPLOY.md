# Deploying Brainlee to Vercel

This repo contains **two independent, zero-build static apps**, deployed as **two separate
Vercel projects** from the same GitHub repository:

| App | Folder | Domain | Audience | Indexable |
|---|---|---|---|---|
| **Marketing site** | [`web/`](./web) | `brainlee.tech` | Public | Yes |
| **Interactive prototype** | [`prototype/`](./prototype) | `demo.brainlee.tech` | YC / investors / enterprise demos only | No (`noindex, nofollow`) |

Both are self-contained React + Tailwind + Babel pages (no build step, no backend). They
share the same branding, logo, typography and design tokens, but are otherwise fully
independent — **updating one never requires touching the other**, and neither links to
the other. `web/` does not contain the prototype's code at all; it was never shipped
there, not merely hidden.

The old combined `web/index.html` (marketing + prototype in one file, gated behind a
`?preview=` key) has been retired in favor of this split — that gate was only obscurity
(the prototype code still shipped in the public bundle); this split means the prototype
code is **not present** in the public deploy at all.

---

## 1. Marketing site → `brainlee.tech`

Root [`vercel.json`](./vercel.json) already configures this project:
`outputDirectory: "web"`, no build command, clean URLs, security headers, SPA rewrite.
[`.vercelignore`](./.vercelignore) keeps the Python backend, docs, tests, and the
`prototype/` folder out of this deploy.

1. Go to <https://vercel.com/new> and **Import** `dixshadas/brandbrain`.
2. Framework Preset **Other**, Root Directory `./` (leave as repo root — `outputDirectory`
   in `vercel.json` already points to `web`), Build Command *(none)*.
3. **Deploy.** You'll get a URL like `https://brandbrain.vercel.app`.
4. **Settings → Domains** → add `brainlee.tech` (and `www.brainlee.tech` if desired) →
   follow Vercel's DNS instructions with your domain registrar.

Every push to `main` redeploys this project automatically.

## 2. Interactive prototype → `demo.brainlee.tech`

This is a **second, separate Vercel project** importing the **same repository**, scoped to
the `prototype/` folder.

1. Go to <https://vercel.com/new> and **Import** `dixshadas/brandbrain` again (Vercel
   allows importing the same repo into multiple projects).
2. Framework Preset **Other**, **Root Directory: `prototype`** (this is the key
   difference — Vercel then only ever sees files inside `prototype/`, so nothing from the
   marketing site, backend, or docs can leak into this deploy).
3. Build Command *(none)*, Output Directory *(default — `prototype/vercel.json` handles
   rewrites and headers, including `X-Robots-Tag: noindex, nofollow`)*.
4. **Deploy.**
5. **Settings → Domains** → add `demo.brainlee.tech` → follow the DNS instructions
   (typically a `CNAME` record for the `demo` subdomain pointing at Vercel).
6. Give this project a distinct, private name in the Vercel dashboard (e.g.
   `brainlee-prototype`) so it's not confused with the public site.

Give this project's URL only to YC partners, investors, and enterprise prospects during
live demos. **Never link it from the marketing site** — there is no nav item, footer
link, button, or CTA anywhere in `web/` that references it, by design.

### SEO isolation
`prototype/index.html` ships `<meta name="robots" content="noindex, nofollow">` and
`prototype/vercel.json` sends an `X-Robots-Tag: noindex, nofollow` header on every route;
`prototype/robots.txt` disallows all crawling. The marketing site's `robots` meta stays
`index,follow` and is fully indexable.

## Local CLI (either app)

```bash
npm i -g vercel
cd web/         # or cd prototype/
vercel          # first run: log in + link the project (interactive)
vercel --prod   # promote to the public production URL for that project
```

## Post-deploy verification checklist

**Marketing site (`brainlee.tech`)**
- [ ] Loads past the loading splash with no console errors (React/Tailwind/Babel load from CDN).
- [ ] Nav: Product, How it works, Request a Demo only — no prototype link anywhere.
- [ ] View source / inspect: no `App()`, `Sidebar`, or prototype screen code present.
- [ ] `curl -I https://brainlee.tech` → no `X-Robots-Tag: noindex`.

**Prototype (`demo.brainlee.tech`)**
- [ ] Loads the full interactive experience directly — no marketing page in between.
- [ ] `curl -I https://demo.brainlee.tech` → `X-Robots-Tag: noindex, nofollow` present.
- [ ] Not discoverable from `brainlee.tech` by any click path.

> Note: both pages load React/Tailwind/Babel from public CDNs at runtime, so the first
> load needs internet. This works on Vercel's network; it cannot be verified inside a
> sandbox whose egress blocks those CDNs.
