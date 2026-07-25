# Brainlee — interactive prototype (private)

The full interactive product experience — Knowledge Hub, HCP Simulation, Decision
Studio, Brand Pulse, MLR Governance, Brand Brain, Audit Trail — as a single
self-contained page (`index.html`): React + Babel + Tailwind loaded from CDN, no build
step, no backend, running entirely on mock data.

**This is not the public site.** It is meant to be deployed to its own private domain
(`demo.brainlee.tech`) and shared only with YC partners, investors, and enterprise
prospects during live demos. See [`../DEPLOY.md`](../DEPLOY.md) for the deployment
setup, and [`../web/`](../web) for the public marketing site — the two are independent,
zero-build apps deployed as separate Vercel projects from this same repo.

`robots.txt` and the page's own `<meta name="robots">` tag both set `noindex, nofollow`;
`vercel.json` also sends an `X-Robots-Tag: noindex, nofollow` header. Nothing here should
ever be indexed or linked from the public site.
