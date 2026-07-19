# Event contracts (the asynchronous API)

These JSON-Schemas are the **source of truth** for what flows over the event bus. They are
versioned in the `type` string (`noun.verb.vN`); a breaking change means a **new version**, never
an edit to an existing schema. Producers and consumers are validated against these in CI
(`tests/contract/`), so a service can be extracted or replaced without silent contract drift.

Every event validates against `_envelope.schema.json`; the `payload` object then validates against
the schema named by its `type`. The synchronous API (REST) is generated from the code
(`make openapi` → `contracts/openapi/openapi.json`).
