# BrandBrain — project handoff

**What this is:** BrandBrain — a trust-first AI decision-intelligence product for pharmaceutical
brand teams. *"Help Brand Directors make evidence-backed strategic decisions they can confidently
put their name behind."* Trust is the product.

This bundle is a **portable snapshot** meant to be uploaded into another workspace to keep
building. Everything needed to run the demo and continue development is here.

---

## What's in the box

```
BrandBrain Demo.html      ← the interactive frontend prototype (open this first)
web/                      ← the same demo, packaged to deploy to Vercel (index.html + vercel.json)
backend/                  ← FastAPI "modular monolith" scaffold (10 services) + the TDD
docs/                     ← Product Architecture & MVP thesis (Word doc)
backend/docs/TECHNICAL_DESIGN.md   ← the engineering design doc (read before touching backend)
```

## Current status (be precise about this)

| Piece | Status |
|---|---|
| **Frontend demo** (`BrandBrain Demo.html` / `web/`) | ✅ Complete, self-contained, runs on mock data. No backend required. This is the YC demo. |
| **Backend** (`backend/`) | 🟡 Scaffold only. Import-clean, all contracts/interfaces/models defined, but service methods are **stubs** (`NotImplementedError`). It is *not* a running API yet. |
| **Docs** | ✅ Product Architecture (docs/) + Technical Design (backend/docs/TECHNICAL_DESIGN.md) complete. |

> The frontend does **not** call the backend. The demo is intentionally front-end-only on mock
> data so it's bulletproof for a live demo. Wiring them together is future work.

---

## Deploy the frontend to Vercel (2 minutes, no backend needed)

**Drag & drop (no CLI):**
1. https://vercel.com/new
2. Drag the `web/` folder onto the page.
3. Framework preset **Other**, no build command, output dir `.` → **Deploy**.
4. You get a public URL, e.g. `https://brandbrain-demo.vercel.app` — shareable with anyone, no login.

**Or CLI:**
```bash
npm i -g vercel
cd web && vercel && vercel --prod
```

The production URL works across accounts and machines — paste it into any chat or open it on the
demo laptop. First load needs internet (React/Tailwind/Babel load from CDN).

---

## Continuing in the other (Fable) account

Upload this whole bundle into the new workspace, then hand the new Claude this orientation:

> "This is BrandBrain, a trust-first pharma decision-intelligence product. The frontend prototype
> (`BrandBrain Demo.html`) is complete and demo-ready on mock data. The backend (`backend/`) is a
> FastAPI modular-monolith scaffold whose service methods are stubs — read
> `backend/docs/TECHNICAL_DESIGN.md` first; it specifies every service's Purpose / Inputs /
> Outputs / Interface / Failure modes. Do not redesign the product or the architecture — implement
> them. Trust is the product: every AI output must stay cited, confidence-scored, contradiction-
> preserving, and human-gated."

### Highest-leverage next steps
1. **Implement one backend service end-to-end** as a reference — the Synthesizer is the hero:
   `retrieval → structured LLM output → Trust Engine scoring → MLR checks → persist`. The Trust
   Engine and the MLR citation-guard already have real logic to build on.
2. **Wire the frontend to the API** — replace the mock objects in the demo with `fetch` calls, or
   (cleaner) port the demo into a Vite + TypeScript + Tailwind app with `lucide-react` + Framer
   Motion (the demo currently uses CDN React + Babel + inline icons for zero-build portability).
3. **Stand up the backend** on a stateful host (Render / Railway / Fly) — the `Dockerfile` and
   `docker-compose.yml` are ready. Vercel is not a fit for the FastAPI worker + Postgres/Redis.

---

## Notes & honest caveats
- The frontend was verified by static analysis only in the originating session (no browser was
  available there). Open it once in a browser before presenting; if the console flags anything,
  it'll be a quick fix.
- Backend deps (FastAPI etc.) were never installed/run in the originating session — verification
  was `py_compile` + import-resolution + contract-schema validation. Expect to `pip install -e
  ".[dev,llm]"` and iterate.
- All data (YI Combo glaucoma brand, switching-drivers story, studies, quotes) is **illustrative
  and synthetic** — built from the uploaded IQVIA-style market sizing and HCP segmentation
  materials; no real prescriber or panel data is implied.
