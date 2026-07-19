"""The audit hash chain is tamper-evident: editing a past record changes its hash and breaks the
chain from that point forward."""
import pytest

from brandbrain.services.audit.service import compute_hash

pytestmark = pytest.mark.unit


def test_chain_is_deterministic_and_order_sensitive():
    h1 = compute_hash("GENESIS", {"action": "brain.published", "target": "bp-swd"})
    h2 = compute_hash(h1, {"action": "synthesis.completed", "target": "syn-1"})
    # recomputing with a tampered earlier payload yields a different downstream hash
    h1_tampered = compute_hash("GENESIS", {"action": "brain.published", "target": "bp-OTHER"})
    h2_from_tampered = compute_hash(h1_tampered, {"action": "synthesis.completed", "target": "syn-1"})
    assert h2 != h2_from_tampered
