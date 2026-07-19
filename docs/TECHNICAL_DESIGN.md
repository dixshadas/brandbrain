# BrandBrain — Technical Design Document (TDD)

**Status:** Draft v0.1 · **Owner:** Founding Staff Engineer / AI Architect
**Scope:** The production intelligence system that implements the approved Product Architecture.
**Audience:** Engineering, Security/Compliance, and technical reviewers (incl. YC).

> This document does **not** re-open product decisions. It translates them into services,
> contracts, and a rollout. The guiding constraint is the product's one promise — **trust is the
> product** — so every choice below is judged on transparency, auditability, explainability,
> governance, developer simplicity, and future extensibility, in that spirit. We optimize for
> maintainability, never cleverness.

---

## 1. Design goals & non-goals

**Goals.** (1) Every user-visible claim is traceable to an atomic source. (2) Contradictions are
preserved, never averaged. (3) The system never fabricates certainty. (4) Nothing publishes to the
Brand Brain without a human and passing machine checks. (5) Every run, review, and decision is on
an immutable audit trail. (6) A new engineer can read one service package and understand it.

**Non-goals (now).** Autonomous agents that act without human review; a horizontal
document-search product; predictive/forecasting analytics; multi-region active-active. These are
explicitly deferred (see the Product Architecture) and the design leaves room for them without
demanding them.

---

## 2. Architecture: a modular monolith that is service-ready

One deployable application (`brandbrain.main:app`) plus one worker (`brandbrain.worker`). Inside
it, ten services live as independent Python packages with **strict boundaries**:

- A service exposes an **interface** (a `Protocol`); callers depend on the interface, never the
  implementation.
- Services talk **synchronously** through those interfaces (in-process function calls) and
  **asynchronously** through a **versioned event bus**.
- **No service touches another's tables.** Cross-service state changes happen via events.

This is the deliberate middle path between a big ball of mud and premature microservices. It gives
us microservice-grade *boundaries* with monolith-grade *operational simplicity* — the right trade
for an MVP-stage team. Extraction later is mechanical: replace a service's in-process client with a
network client; the interface and event contracts don't change. (See `docs/adr/0001`.)

```
                       ┌───────────────────────── API process (FastAPI) ─────────────────────────┐
  Browser / SPA  ─────►│  main.create_app(): mounts 10 routers · OIDC auth · problem+json errors  │
                       └───────────┬──────────────────────────────────────────────────────────────┘
                                   │ in-process calls via service Interfaces (sync)
   ┌───────────────────────────────┼───────────────────────────────────────────────────────────┐
   │  ingestion  evidence_store  retrieval  synthesizer  brand_brain  mlr  trust  audit  reco  … │
   └───────────────────────────────┼───────────────────────────────────────────────────────────┘
                                   │ publish/subscribe (async, versioned)
                       ┌───────────▼───────────┐         ┌───────────────── Worker process (arq) ─┐
                       │      Event Bus         │◄───────►│ ingestion pipeline · synth.execute ·   │
                       │  (Redis Streams)       │         │ notification fan-out · audit (all evts)│
                       └───────────┬───────────┘         └────────────────────────────────────────┘
                                   ▼
   Postgres + pgvector  ·  Redis (streams + cache)  ·  S3/MinIO (originals)  ·  OIDC IdP  ·  OTel
```

**Request vs. run.** Anything slow or cross-service (ingestion parsing, a synthesis run,
notification fan-out) happens in the worker off the request path. The API stays fast and stateless;
the worker is where at-least-once, idempotent processing lives.

---

## 3. Technology choices (and why)

| Concern | Choice | Why this, not the alternative |
|---|---|---|
| Language / runtime | **Python 3.12** | Team + AI ecosystem; async maturity. |
| Web framework | **FastAPI** | Pydantic-native, async, **auto-generated OpenAPI** (docs = contract for free). Alt: Django (heavier, sync-first), Flask (no typing/async story). |
| Domain/validation | **Pydantic v2** | The type system *is* the trust layer — illegal states (a FACT with no citation) can't be constructed. |
| Relational DB | **PostgreSQL 16** + SQLAlchemy 2.0 (async) + Alembic | One dependable datastore: relational + JSONB + `pgvector`. Boring on purpose. |
| Vector search | **pgvector now**, Qdrant later (behind `VectorStore`) | One datastore to run for the MVP = developer simplicity; the interface makes the swap config, not rewrite. (ADR 0002) |
| Event bus / queue | **Redis Streams now**, Kafka/NATS later (behind `EventBus`) | Durable, replayable, consumer groups — an *auditable* log, not just delivery. We already run Redis. (ADR 0003) |
| Background work | **arq** (async Redis queue) | Async-native, tiny surface. Alt: Celery (heavier, sync-oriented). |
| Auth | **OIDC/OAuth2** to the enterprise IdP (Okta/Entra/Auth0); JWT via JWKS | SSO is table stakes in pharma; we validate, we don't store passwords. RBAC + brand-scope in `Principal`. |
| Object storage | **S3-compatible** (AWS S3 / MinIO local) | Content-addressed, write-once originals so citations stay re-verifiable. |
| LLM access | **Provider-abstracted gateway** (litellm) + **structured outputs** (instructor) | No vendor SDK in core; every call is typed + traced + costed. Swap models by config. |
| Caching | **Redis** | Same instance as streams: response cache, rate limits, idempotency keys. |
| Observability | **OpenTelemetry** (traces/metrics/logs) + **structlog** (JSON) + Sentry | "If we can't see what it did, we can't prove what it did." Every LLM call is a span. |
| Deployment | **Docker** → **ECS Fargate or K8s**, **Terraform** IaC, **GitHub Actions** CI/CD | Two images (api, worker) from one Dockerfile; scale independently. |

Full rationale for the three consequential swaps (vector, bus, monolith) lives in `docs/adr/`.

---

## 4. Cross-cutting concerns

**Brand isolation.** Every brand-scoped row carries an immutable `brand_id` (`TenantMixin`), every
repository filters by it, and `Principal.assert_brand()` is called on every brand-scoped read/write
(`BrandIsolationError` otherwise). Agents read only a brand's *published* Brain layer. This is the
code-level half of the isolation guarantee the product sells.

**Identity of everything.** Prefixed ULIDs (`doc_…`, `syn_…`, `bp_…`, `evt_…`) — sortable and
self-describing, which matters most when reading an audit trail.

**Errors.** Typed `BrandBrainError` subclasses map to RFC-9457 `problem+json`, so the UI can
explain *why* (e.g. `citation_preservation_failed`) rather than showing a bare 500.

**Idempotency.** Event handlers key on `event.id`; ingestion dedupes on document `sha256`; unsafe
POSTs accept an `Idempotency-Key`. At-least-once delivery is safe because handlers are idempotent.

---

## 5. Service specifications

Each service is specified as **Purpose · Inputs · Outputs · Dependencies · Interface · Future
evolution · Failure modes**. Code lives in `src/brandbrain/services/<name>/`.

### 5.1 Research Ingestion
- **Purpose.** The front door and the governance gate. Accept documents from every source, parse
  them into atomic evidence units, propose metadata, and hold everything behind a human review gate
  so nothing enters the estate unreviewed.
- **Inputs.** Uploaded bytes (multipart) or a connector `object_key`; source type; filename/MIME.
- **Outputs.** An `IngestJob` (state machine: `received → parsing → needs_review → indexing →
  ready`); events `document.received/metadata_proposed/approved/ingested/indexed`.
- **Dependencies.** ObjectStore (write-once originals), EventBus, Evidence Store (writes units on
  approval), LLM gateway (metadata detection), parsers (PDF/PPTX/DOCX/XLSX + ASR for audio).
- **Interface.** `start(req) · get_job(id) · confirm_metadata(id, req)` (the gate; REVIEWER/ANALYST).
- **Future evolution.** Pluggable connector framework (SharePoint/SFTP/email → Veeva, Snowflake…);
  auto-classification improving the *proposal* while the human confirm stays mandatory.
- **Failure modes.** Unparseable/corrupt file → job `failed` with reason, original retained.
  Duplicate `sha256` → dedupe, link to existing doc. ASR low-confidence → flag units, don't drop.
  Metadata detector down → job parks in `needs_review` (never auto-advances). Partial parse →
  quarantine; never index a partial document silently.

### 5.2 Evidence Store
- **Purpose.** The canonical, immutable system of record: documents + **evidence units** (the
  atom — a slide, page, transcript turn, or table cell) with full provenance. Everything downstream
  cites a unit by id, so a citation is always re-verifiable.
- **Inputs.** `RegisterDocument`, `AddEvidenceUnits` (from ingestion on approval).
- **Outputs.** `Document`, `EvidenceUnit`, document lists; resolves a citation → exact span.
- **Dependencies.** Postgres (documents, units), ObjectStore (original bytes), VectorStore
  (embeddings for units, MVP via pgvector column).
- **Interface.** `register_document · get_document · add_evidence_units · get_evidence_unit ·
  list_documents`.
- **Future evolution.** Versioned corrections (append, never mutate); cross-document entity linking;
  a document-level knowledge graph feeding retrieval.
- **Failure modes.** Vector upsert fails after row commit → outbox + retry (unit exists but flagged
  `unindexed`; retrieval excludes it until healed). Object bytes missing on citation resolve →
  hard error surfaced to the user ("source unavailable"), never a fabricated quote.

### 5.3 Evidence Retrieval
- **Purpose.** Hybrid (vector + lexical) search over evidence units, returning **citation-stamped**
  spans — never a bare snippet. The substrate the Synthesizer and Knowledge Navigator stand on.
- **Inputs.** `SearchRequest` (brand, query, filters, `top_k`, `alpha` = vector/lexical blend).
- **Outputs.** `SearchResponse` — ranked `SearchHit`s, each with a `Citation`, text, and the
  component scores (so ranking is inspectable).
- **Dependencies.** VectorStore, a lexical index (BM25), Evidence Store (hydrate citations),
  LLM gateway (embed the query).
- **Interface.** `search(req)`.
- **Future evolution.** Reranker model; query decomposition; per-brand learned weighting; a Qdrant
  adapter at scale (interface already isolates it).
- **Failure modes.** Vector backend timeout → degrade to lexical-only, mark results `degraded` so
  the caller knows. Empty result → honest empty state, never a hallucinated hit. Embedding drift on
  model change → re-embed job; never mix embedding spaces in one index.

### 5.4 Cross-Study Synthesizer
- **Purpose.** The core value. Reason across many studies/waves/methods to produce the output
  anatomy: story summary, agreements, **preserved contradictions**, gaps, changed metrics, and a
  labeled recommendation — all cited, all with honest confidence.
- **Inputs.** `RunRequest` (brand, workflow, confirmed `source_ids`, optional question). Scope is
  validated (`Brand Study Lens` needs ≥2 sources) — *confirmation-before-execution is enforced in
  the service, not just the UI.*
- **Outputs.** A `SynthesisRun` with a typed `SynthesisOutput`; events `synthesis.requested/
  completed/failed`; recorded `llm_call_ids` for reproducibility.
- **Dependencies.** Retrieval, LLM gateway (structured output = `SynthesisOutput`), **Trust Engine**
  (confidence + claim-layer), **MLR Engine** (locked-claim + citation guards), EventBus.
- **Interface.** `request_run` (async, returns QUEUED) · `get_run` · `execute` (worker).
- **Future evolution.** More named workflows; multi-step agentic retrieval with a human-visible
  plan; caching of sub-syntheses keyed on source-set hash.
- **Failure modes.** LLM emits an unciteable claim → **schema rejects it** (a FACT/INSIGHT without a
  citation cannot be constructed); the run fails closed rather than shipping an unsupported claim.
  LLM timeout/rate-limit → bounded retries (tenacity), then `failed` with reason. Partial output →
  never persisted as `completed`. It **never** writes to the Brain directly — output is a proposal.

### 5.5 Brand Brain
- **Purpose.** The compounding asset: curated, cited, **versioned**, **review-gated**,
  **brand-isolated** knowledge pages. Draft-first — AI proposes, a human publishes. Agents read only
  the published layer.
- **Inputs.** `ProposeUpdate` (diff + source tags + origin), `PublishDecision` (approve/reject).
- **Outputs.** `BrainPage` (published), `UpdateProposal` (with machine-check results), review queue;
  events `brain.update_proposed/published/rejected`.
- **Dependencies.** MLR Engine (machine checks before publish), Audit Engine, EventBus, Postgres
  (pages + append-only version history).
- **Interface.** `get_page · list_pages · propose_update · list_review_queue · decide`.
- **Future evolution.** Knowledge graph across pages; scheduled freshness re-checks (thin/stale
  flags); "Bootstrap" onboarding for a new brain; suggested reviewers.
- **Failure modes.** Publish attempted with a failed machine check → `GovernanceError`, blocked.
  Concurrent edits to one page → optimistic version check, second writer rebased/rejected. A
  proposal that would edit a locked claim → refused with a red-flag diff. Reject keeps the draft for
  audit — never deletes.

### 5.6 MLR Engine
- **Purpose.** Make Medical-Legal-Regulatory an ally. Hold the **locked-claim registry** (approved
  text reproduced verbatim) and run the **deterministic** governance guards that gate publishing.
- **Inputs.** `RegisterLockedClaim` (MLR role); `CheckRequest` (before/after text + citation sets).
- **Outputs.** `LockedClaim`; `CheckResponse` (per-check pass/fail + detail); `mlr.check_failed`.
- **Dependencies.** Postgres (registry), Audit Engine. **No LLM in the trust-critical path** — guards
  are deterministic so they're reproducible and defensible.
- **Interface.** `register_locked_claim · list_locked_claims · check`.
- **Future evolution.** Claim-to-evidence substantiation graph; expiry/renewal workflows; off-label
  language detection as an *advisory* signal (never an auto-block without human sign-off).
- **Failure modes.** Registry unavailable → checks **fail closed** (block publish), never open.
  Ambiguous verbatim match (whitespace/formatting) → normalized comparison; on doubt, flag for human.

### 5.7 Trust Engine
- **Purpose.** Turn evidence into an **explainable, capped** confidence, and classify every
  statement as FACT / INSIGHT / INTERPRETATION / RECOMMENDATION — the "what research says vs. what
  the AI concludes" separation, in code.
- **Inputs.** `ScoreRequest` (statement + `EvidenceSignal`s: support/contradict, method, quality,
  recency); `ClassifyRequest`.
- **Outputs.** `Confidence` (band + score + full rationale); `ClassifyResponse` (layer + reason).
- **Dependencies.** None hard — pure, deterministic functions (unit-tested). May consult the LLM
  gateway for *classification hints* only, never for the score.
- **Interface.** `score · classify`.
- **Future evolution.** Per-brand calibration against outcomes; learned source-quality priors;
  disagreement-aware scoring across suppliers.
- **Failure modes.** Single source → **hard cap below HIGH** (enforced in `Confidence` and in
  scoring). No signals → LOW with an explicit "insufficient evidence" note, never a default-high.

### 5.8 Audit Engine
- **Purpose.** The immutable, **hash-chained** record of every run, review, and decision. Tamper-
  evident: altering any past record breaks the chain from that point on.
- **Inputs.** `AppendRecord` (explicit) **and** every domain event (universal subscriber).
- **Outputs.** `AuditRecord`s (chained by `prev_hash`/`hash`); `verify_chain` result.
- **Dependencies.** Postgres (INSERT-only table — no update/delete path exists in the repository),
  EventBus (consumes `*`).
- **Interface.** `append · list_for_target · verify_chain`.
- **Future evolution.** Periodic anchoring of the chain head to external notarization; export for
  regulatory inspection; per-brand retention policies.
- **Failure modes.** Append fails mid-run → the triggering action's transaction rolls back (audit is
  part of the unit of work for governance-critical writes). Chain verify finds a break → surfaced to
  admins with the exact `seq`; the system treats the log as compromised until reconciled.

### 5.9 Recommendation Engine
- **Purpose.** Draft a **clearly-labeled, human-reviewed** recommended action from a completed
  synthesis. Deliberately **not** an agent — the product advises; a person decides and acts.
- **Inputs.** `synthesis.completed` events; `DecideRequest` (accept/dismiss + note).
- **Outputs.** `RecommendedAction` (action, rationale, supporting citations, confidence, status);
  `recommendation.drafted`.
- **Dependencies.** Synthesizer output, Trust Engine (confidence), Audit Engine, EventBus.
- **Interface.** `list_for_run · decide`.
- **Future evolution.** Playbook templates per situation; tracking accepted→outcome to calibrate
  future confidence; suggested owner/next step.
- **Failure modes.** No defensible action from the evidence → emit **nothing** (silence beats a weak
  recommendation). It never transitions state on its own; the only transitions are human decisions.

### 5.10 Notification Engine
- **Purpose.** The habit loop and the deep-link layer: the weekly **Brand Pulse**, review-queue
  alerts, indexing/ signal notifications — each routing into the exact flow.
- **Inputs.** Domain events (`document.indexed`, `synthesis.completed`, `brain.update_proposed`,
  `mlr.check_failed`); `build_pulse` request.
- **Outputs.** `Notification`s (with `deep_link`), `PulseDigest`; `notification.sent` receipts.
- **Dependencies.** EventBus (fan-out consumer), Postgres (inbox), channel adapters (in-app, email,
  Slack/Teams).
- **Interface.** `list_inbox · mark_read · build_pulse`.
- **Future evolution.** Per-user digest preferences; smart batching/quiet hours; a scheduled Pulse
  job; escalation for stale high-severity reviews.
- **Failure modes.** Channel down (email/Slack) → in-app always succeeds; external delivery retried
  with backoff, then dead-lettered. Duplicate events → idempotent on `(event_id, recipient)` so a
  replay never double-notifies.

---

## 6. Data model (core tables)

All brand-scoped tables carry `brand_id`, `created_at`, `updated_at`. Full definitions in each
service's `models.py`.

| Table | Owner | Key columns | Notes |
|---|---|---|---|
| `document` | evidence_store | id, brand_id, study_type, supplier, sha256, object_key | Source docs; `sha256` dedupes. |
| `evidence_unit` | evidence_store | id, document_id, locator_type/value, text, embedding_ref | **The citable atom.** pgvector column holds the embedding. |
| `ingest_job` | ingestion | id, document_id, source, status, proposed_json | Metadata-gate state machine. |
| `synthesis_run` | synthesizer | id, workflow, status, source_ids, output_json, llm_call_ids | Output stored as validated JSON; call ids for reproducibility. |
| `brain_page` | brand_brain | id, section, title, version, facts_json, thin, status | Only `status='published'` is agent-readable. |
| `brain_page_version` | brand_brain | id, page_id, version, facts_json, reviewer | Append-only history; publishing bumps version. |
| `brain_update_proposal` | brand_brain | id, page_id, origin, diff_json, status, machine_checks_json | The review queue. |
| `locked_claim` | mlr | id, mlr_ref, text, source_document_id | Verbatim MLR-approved text. |
| `audit_record` | audit | seq, id, action, actor_json, target_id, prev_hash, hash | **INSERT-only**, hash-chained. |
| `recommended_action` | recommendation | id, run_id, action, rationale, citations_json, status | Human accept/dismiss only. |
| `notification` | notification | id, kind, title, deep_link, read | Inbox; feeds the Pulse digest. |

**Storage split.** Postgres = relational truth + JSONB. pgvector = embeddings (MVP; Qdrant later).
S3/MinIO = original bytes (write-once, content-addressed). Redis = streams + cache + idempotency.

## 7. Eventing & the worker

Events are `noun.verb.vN`; a breaking change is a **new version**, never an edit to a live schema
(schemas in `/contracts/events`, enforced by `tests/contract`). The envelope carries
`brand_id + actor + trace_id + idempotency_key`, so the event log *is* an audit substrate.

Delivery is at-least-once with per-key ordering (Redis Streams consumer groups). The worker routes
each event: the **Audit Engine** consumes `*` (universal journal); `document.approved` drives
Evidence-Store unit-writes then `document.ingested/indexed`; `synthesis.requested` triggers
`Synthesizer.execute`; proposal/indexed/failure events fan out to **Notification**. Poison messages
dead-letter after bounded retries and raise an alert — they are never silently dropped.

## 8. Trust & audit design (the part that must not be wrong)

1. **Grounding by construction.** `Finding` refuses to exist as a FACT/INSIGHT without a `Citation`;
   `Confidence` refuses HIGH from a single source. The LLM returns a typed `SynthesisOutput`, so an
   unsupported claim fails validation and the **run fails closed** — we never ship an uncited claim.
2. **Layer separation.** Every statement is tagged FACT / INSIGHT / INTERPRETATION / RECOMMENDATION
   by the Trust Engine. "What the research says" and "what the AI concludes" are different types on
   the screen and in the API.
3. **Contradictions preserved.** A mixed signal is a `Contradiction` object with both sides + their
   sources + why-it-matters — structurally impossible to average into one number.
4. **Honest confidence.** Deterministic, explainable, **capped**; a bare number is never shown
   without its `ConfidenceRationale`.
5. **Missing info is a feature.** Gaps become `EvidenceGap`s with a drafted next-study question.
6. **Governance gate.** Brain publishing requires REVIEWER role **and** all MLR machine checks
   passing (locked-claim guard, citation-preservation). Fail → blocked, logged, kept for audit.
7. **Tamper-evident audit.** Hash-chained, INSERT-only; `verify_chain` proves integrity on demand.
8. **Reproducibility.** Every LLM call records model + prompt hash + tokens + cost; any AI output
   can be re-explained months later.

## 9. Security & compliance

OIDC/OAuth2 SSO against the customer IdP; JWTs validated via JWKS; **no passwords stored**. RBAC
(`viewer/analyst/reviewer/mlr/admin`) plus **brand-scoping** on the `Principal`. Service-to-service
calls use short-lived signed tokens (mTLS at the mesh later). Data encrypted at rest (Postgres/S3
KMS) and in transit (TLS). PII/PHI minimized — the estate is market research, not patient data; any
incidental PII in transcripts is flagged at ingestion. Tenancy is row-level today with a documented
path to schema- or database-per-brand for customers who require physical isolation.

## 10. Deployment & observability

Two images from one Dockerfile (`api`, `worker`), scaled independently on ECS Fargate or K8s;
Postgres + Redis are managed services in prod (RDS + ElastiCache), S3 for objects. Terraform IaC;
GitHub Actions runs lint → type-check → unit+contract → build → deploy (integration on ephemeral
envs, evals nightly/gated). OpenTelemetry traces every request and **every LLM span**; structlog
emits JSON logs correlated by `trace_id`; Sentry for errors; dashboards for run latency, LLM cost
per brand, review-queue depth, and audit-chain health.

## 11. Test strategy (see `tests/`)

Weighted toward the trust guarantees. **unit** — confidence capping, claim-layer rules, citation
guard, hash chaining (pure, ms). **contract** — every event payload validates against its published
schema (`make contracts`). **integration** — Postgres/Redis/MinIO via testcontainers: brand
isolation, the publish gate, audit append-only. **eval** — the AI release gate: a golden set scored
on grounding, contradiction-preservation, calibration, and abstention; a regression blocks release
even when unit tests are green. This is TDD in practice: the invariant is written as a failing test
first (e.g. "single source ≠ HIGH"), then the code makes it pass.

## 12. Rollout plan (maps to the product roadmap)

- **M1 — one design-partner brand.** Ingestion + Evidence Store + Retrieval + Synthesizer + Trust +
  atomic citations. Modular monolith, single env. Goal: one undeniable synthesis.
- **M3 — habit + memory.** Brand Brain (review gate) + Audit + Notification/Brand Pulse; 3–5 brands.
- **M6 — trust to production.** Connected Sources (auto-ingest) + MLR Engine hardening +
  Recommendation drafts; first paid contracts; SSO with customer IdPs.
- **Y1 — extract under load.** Split the two hottest services (Retrieval, Synthesizer worker) into
  their own deployments using the existing interfaces + events; Qdrant if pgvector is the bottleneck;
  Kafka/NATS if Redis Streams is. Nothing about the contracts changes.

## 13. Synchronous API (generated)

The REST surface is generated from the code — `make openapi` emits `contracts/openapi/openapi.json`
and FastAPI serves interactive docs at `/docs`. Endpoint summary:

| Area | Method + path |
|---|---|
| Ingestion | `POST /v1/ingestion/jobs` · `GET /v1/ingestion/jobs/{id}` · `POST /v1/ingestion/jobs/{id}/confirm` |
| Evidence | `GET /v1/evidence/documents` · `GET /v1/evidence/documents/{id}` · `GET /v1/evidence/units/{id}` |
| Retrieval | `POST /v1/search` |
| Synthesizer | `POST /v1/synthesis/runs` · `GET /v1/synthesis/runs/{id}` |
| Brand Brain | `GET /v1/brain/pages` · `GET /v1/brain/pages/{id}` · `POST /v1/brain/proposals` · `GET /v1/brain/review-queue` · `POST /v1/brain/proposals/{id}/decision` |
| MLR | `GET/POST /v1/mlr/locked-claims` · `POST /v1/mlr/check` |
| Trust | `POST /v1/trust/score` · `POST /v1/trust/classify` |
| Audit | `GET /v1/audit/targets/{id}` · `GET /v1/audit/verify` |
| Recommendation | `GET /v1/recommendations/runs/{id}` · `POST /v1/recommendations/{id}/decision` |
| Notification | `GET /v1/notifications` · `POST /v1/notifications/{id}/read` · `GET /v1/notifications/pulse` |

---

*End of TDD v0.1. Companion ADRs in `docs/adr/`. This document and the scaffold are the contract
between product intent and implementation; change them together.*
