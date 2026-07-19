"""Cross-cutting domain vocabulary shared by every service.

`common` holds the value objects that make trust concrete — Citation, Confidence, ClaimLayer,
Contradiction, EvidenceGap. `events` holds the canonical Event envelope and payloads. Services
own their *own* aggregates; only genuinely shared concepts live here.
"""
