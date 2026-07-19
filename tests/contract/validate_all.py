"""Standalone contract validator (also invoked by the contract test).

Validates representative event payloads against the published JSON-Schemas in /contracts/events.
Runnable without the app: `python -m tests.contract.validate_all`.
"""
from __future__ import annotations

import json
import pathlib
import sys

import jsonschema

ROOT = pathlib.Path(__file__).resolve().parents[2]
SCHEMA_DIR = ROOT / "contracts" / "events"

# (schema filename, example payload) — examples double as living documentation.
CASES: list[tuple[str, dict]] = [
    ("document.ingested.v1.json",
     {"document_id": "doc_1", "study_type": "atu", "evidence_unit_count": 48}),
    ("synthesis.completed.v1.json",
     {"run_id": "syn_1", "workflow": "brand_study_lens", "finding_count": 6,
      "contradiction_count": 1, "gap_count": 2, "overall_confidence": "high"}),
    ("brain.update_published.v1.json",
     {"proposal_id": "prop_1", "page_id": "bp-swd", "version": 2, "reviewer": "Andrew Smith"}),
    ("mlr.check_failed.v1.json",
     {"proposal_id": "prop_1", "check": "citation_preservation", "detail": "dropped: [eu_msg]"}),
]

ENVELOPE_EXAMPLE = {
    "id": "evt_01J9ZK8Q7T3M4N5P6R7S8T9V0W", "type": "synthesis.completed.v1",
    "occurred_at": "2026-07-18T12:00:00Z", "brand_id": "brand_demo",
    "actor": {"subject": "svc", "display_name": "Synthesizer", "kind": "service"}, "payload": {},
}


def _load(name: str) -> dict:
    return json.loads((SCHEMA_DIR / name).read_text())


def run() -> int:
    failures = 0
    # 1) every schema is itself a valid schema (validator chosen by its own $schema; version-agnostic)
    for path in sorted(SCHEMA_DIR.glob("*.json")):
        try:
            schema = _load(path.name)
            jsonschema.validators.validator_for(schema).check_schema(schema)
        except Exception as e:  # noqa: BLE001
            print(f"  X schema invalid: {path.name}: {e}"); failures += 1
    # 2) the envelope example validates
    try:
        jsonschema.validate(ENVELOPE_EXAMPLE, _load("_envelope.schema.json"))
    except Exception as e:  # noqa: BLE001
        print(f"  X envelope example failed: {e}"); failures += 1
    # 3) each payload example validates against its schema
    for name, payload in CASES:
        try:
            jsonschema.validate(payload, _load(name))
            print(f"  ok {name}")
        except Exception as e:  # noqa: BLE001
            print(f"  X {name}: {e}"); failures += 1
    print(f"\ncontract validation: {'PASS' if not failures else f'{failures} FAILURE(S)'}")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(run())
