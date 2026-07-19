# Tests — the test pyramid

Trust is the product, so the test strategy is weighted toward the guarantees users rely on.

| Layer | Marker | What it proves | Speed |
|---|---|---|---|
| unit | `unit` | Pure logic: confidence capping, claim-layer rules, citation guards, hash chaining | ms |
| contract | `contract` | Every event payload validates against its published JSON-Schema; OpenAPI matches routes | ms |
| integration | `integration` | Real Postgres/Redis/MinIO (testcontainers): brand isolation, review gate, audit append-only | s |
| eval | `eval` | AI quality: the synthesizer cites, preserves contradictions, refuses false certainty | slow / gated |

Run: `pytest -m "unit or contract"` (fast, every commit) · `pytest -m integration` (pre-merge) ·
`pytest -m eval` (nightly / gated — may call an LLM).

The `eval/` suite is the safety net specific to an AI product: a curated golden set of
(estate, question, expected-properties) cases scored on **grounding** (every claim cited),
**contradiction-preservation** (known mixed signals are NOT averaged away), **calibration**
(confidence tracks evidence), and **abstention** (says "we don't know" when it should). A
regression here blocks release even when unit tests are green.
