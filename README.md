# BrandBrain — trust-first evidence intelligence for pharma brand teams

> The implementation of the [Product Architecture](docs/PRODUCT_ARCHITECTURE.md).
> The design that governs this code lives in **[docs/TECHNICAL_DESIGN.md](docs/TECHNICAL_DESIGN.md)** — read it first.

BrandBrain turns a brand's fragmented research estate into **defensible strategic answers**.
Every output is cited to an atomic source, preserves contradictions instead of averaging them,
states its confidence honestly, and is governed by a human review gate. **Trust is the product**,
so the architecture optimizes for transparency, auditability, explainability, and governance —
never for cleverness.

## Architecture at a glance

A **modular monolith that is service-ready**: one deployable FastAPI app whose ten internal
services have strict boundaries and talk over an event bus, so any service can be extracted into
its own deployment later without changing its contract.

```
API (FastAPI)  ─┐
                ├─►  10 services (ingestion · evidence_store · retrieval · synthesizer ·
Worker (arq)   ─┘        brand_brain · mlr · trust · audit · recommendation · notification)
                              │  in-process calls (sync)  +  event bus (async)
                              ▼
                platform/  (db · eventbus · objectstore · vectorstore · llm · auth · telemetry)
                              ▼
        Postgres+pgvector · Redis(streams+cache) · S3/MinIO · OIDC IdP · OTel collector
```

Read the service specs, stack rationale, data/event contracts, trust & audit design, and rollout
plan in [`docs/TECHNICAL_DESIGN.md`](docs/TECHNICAL_DESIGN.md).

## Repository layout

```
contracts/          Versioned event JSON-Schemas (the async API); OpenAPI is generated from code
docs/               TECHNICAL_DESIGN.md (the TDD) + Architecture Decision Records (adr/)
src/brandbrain/
  platform/         Shared infra behind interfaces (db, eventbus, objectstore, vectorstore, llm, auth)
  domain/           Cross-cutting value objects + the canonical Event envelope
  services/<svc>/   Per service: schemas · interface · service · models · repository · api · events
  main.py           App factory — mounts every router, wires OpenAPI + telemetry
  worker.py         Event consumer entrypoint (ingestion pipeline, synthesis runs, notifications)
tests/              unit · integration · contract · eval (the AI/trust eval harness)
```

## Quickstart (local)

```bash
cp .env.example .env
docker compose up -d            # postgres+pgvector, redis, minio, otel-collector
uv pip install -e ".[dev,llm]"  # or: pip install -e ".[dev,llm]"
alembic upgrade head
uvicorn brandbrain.main:app --reload      # API  -> http://localhost:8000/docs
arq brandbrain.worker.WorkerSettings      # background worker
pytest -m "unit"                          # fast tests
```

## The ten services

| Service | One-line responsibility |
|---|---|
| `ingestion` | Accept documents from every source, parse to atomic evidence, gate metadata by a human |
| `evidence_store` | Canonical, immutable store of documents + atomic evidence units + provenance |
| `retrieval` | Hybrid (vector + lexical) search returning citation-stamped evidence spans |
| `synthesizer` | Cross-study reasoning that preserves contradictions and names gaps |
| `brand_brain` | Curated, versioned, review-gated, brand-isolated knowledge pages |
| `mlr` | Locked-claim registry, verbatim guard, citation-preservation, substantiation checks |
| `trust` | Confidence scoring + FACT/INSIGHT/INTERPRETATION/RECOMMENDATION classification |
| `audit` | Append-only, hash-chained record of every run, review, and decision |
| `recommendation` | Human-reviewed recommended actions derived from a synthesis (never autonomous) |
| `notification` | Brand Pulse, alerts, and review-queue notifications with deep links |

Nothing publishes without a reviewer. Every run is logged. See the TDD for the why.
