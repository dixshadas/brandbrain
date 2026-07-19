# ADR 0002 — pgvector for the MVP, Qdrant later (behind a VectorStore interface)

**Status:** Accepted · **Date:** 2026-07

## Context
Retrieval needs vector similarity. We also value "one datastore to operate" early.

## Decision
Use pgvector inside the existing Postgres for the MVP. Hide it behind `platform.vectorstore.
VectorStore` so a Qdrant/Weaviate adapter is a drop-in later.

## Alternatives considered
- **Dedicated vector DB now (Qdrant/Weaviate/Pinecone).** Rejected for the MVP: another system to
  run, secure, and back up before we know our scale or filtering needs.
- **Pinecone (managed).** Rejected early: cost + data-residency questions in pharma; revisit if ops
  burden of self-hosting dominates.

## Consequences
Simplicity now; a known migration path. Risk: pgvector performance ceiling on large brands —
mitigated by the interface and by the fact that per-brand corpora are modest (thousands, not
billions, of units).

## Validate
Benchmark recall/latency on the largest design-partner estate before Y1 extraction.
