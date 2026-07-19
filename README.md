# BrandBrain

> Trust-first AI **decision intelligence** for pharmaceutical brand teams.
> *"Help Brand Directors make evidence-backed strategic decisions they can confidently put their
> name behind."* **Trust is the product.**

This is a monorepo: a demo-ready **frontend**, a **backend** scaffold, and the **strategy + design
docs**. Start with **[`HANDOFF.md`](HANDOFF.md)** for full status and next steps.

## Repository layout

| Path | What it is | Status |
|---|---|---|
| `BrandBrain Demo.html` | Interactive frontend prototype (React+Tailwind, CDN, zero-build) | ✅ demo-ready, runs on mock data |
| `web/` | The demo packaged for static hosting (Vercel / GitHub Pages) | ✅ deployable |
| `backend/` | FastAPI "modular monolith" — 10 services, contracts, TDD | 🟡 scaffold; service methods are stubs |
| `backend/docs/TECHNICAL_DESIGN.md` | The engineering design document | ✅ complete |
| `docs/` | Product Architecture & MVP thesis (Word) | ✅ complete |

## Quickstart

**Run the demo locally:** open `BrandBrain Demo.html` in any browser. No build, no backend.

**Backend (when implementing):**
```bash
cd backend
pip install -e ".[dev,llm]"
docker compose up -d          # postgres+pgvector, redis, minio
alembic upgrade head
uvicorn brandbrain.main:app --reload
```

## Deploy the demo

- **Vercel:** import the repo, set **Root Directory = `web`**, framework **Other**, no build. (Works
  with a private repo.)
- **GitHub Pages:** enable Pages → "GitHub Actions"; the workflow in `.github/workflows/pages.yml`
  publishes `web/`. (Requires a public repo, or GitHub Pro for private Pages.)

## ⚠️ Confidentiality

This repo contains product-strategy material intended to be **private**. Create the GitHub repo as
**Private**. If you want a public live demo, deploy `web/` via Vercel from the private repo, or copy
only `web/` into a separate public repo. All example data (brand, studies, quotes) is illustrative
and anonymized — no real brand is implied.
