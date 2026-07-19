# ADR 0001 — Modular monolith, service-ready (not microservices yet)

**Status:** Accepted · **Date:** 2026-07

## Context
Ten services are specified. A pre-revenue team must ship a demo-quality MVP and keep it
maintainable, while not painting itself into a monolithic corner.

## Decision
Build one deployable app + one worker, with the ten services as packages behind `Protocol`
interfaces communicating in-process (sync) and over a versioned event bus (async). Enforce: no
cross-service table access; depend on interfaces, not implementations.

## Alternatives considered
- **Microservices from day one.** Rejected: 10 repos/pipelines/DBs is ops overhead that buys
  nothing at current scale and slows learning. Distributed failure modes before product-market fit.
- **Unstructured monolith.** Rejected: fast today, unmaintainable in six months; boundaries would
  erode and extraction would become a rewrite.

## Consequences
Microservice-grade boundaries with monolith-grade ops. Extraction later = swap an in-process client
for a network client; contracts (interfaces + events) are unchanged. Discipline (the "no shared
tables" rule) must be enforced in review and CI, since the language won't stop a violation.

## Validate with customers/scale
Split a service only when a real signal demands it (independent scaling, team ownership, blast
radius) — not on principle.
