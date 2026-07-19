"""AI quality evals — the release gate specific to an AI product.

These run against a curated golden set: (estate fixture, question, expected properties). They are
scored by deterministic assertions plus an LLM-as-judge rubric, and are `@pytest.mark.eval` so CI
can gate them separately (they may call a model). A regression here blocks release even if unit
tests pass — because the product's promise is trust, not merely working code.
"""
import pytest

pytestmark = [pytest.mark.eval, pytest.mark.skip(reason="requires LLM + golden fixtures; run nightly")]


GOLDEN = [
    # question, must-hold properties
    ("What are the switching drivers?", {"has_contradiction", "every_claim_cited", "names_payer_gap"}),
    ("How is brand health trending?", {"reads_from_source_table", "flags_significance"}),
    ("What don't we know about access?", {"abstains", "drafts_next_study_question"}),
]


@pytest.mark.parametrize("question,properties", GOLDEN)
async def test_synthesis_holds_trust_properties(question, properties):
    """Grounding: every FACT/INSIGHT carries a citation.
    Contradiction-preservation: known mixed signals appear as Contradictions, not an average.
    Calibration: confidence tracks evidence volume + triangulation.
    Abstention: thin areas produce an EvidenceGap + drafted question, never invented certainty.
    """
    ...  # harness wiring omitted in scaffold
