"""The confidence contract: explainable and *capped*. A single source may never read as HIGH."""
import pytest

from brandbrain.domain.common import ConfidenceBand, Method
from brandbrain.services.trust.schemas import EvidenceSignal, ScoreRequest
from brandbrain.services.trust.service import TrustEngineImpl

pytestmark = pytest.mark.unit


async def test_single_source_never_high():
    eng = TrustEngineImpl()
    conf = await eng.score(ScoreRequest(
        statement="Switching intent is rising.",
        signals=[EvidenceSignal(evidence_unit_id="eu1", supports=True, method=Method.QUANT,
                                source_quality=1.0, recency_score=1.0)],
    ))
    assert conf.band != ConfidenceBand.HIGH
    assert conf.rationale.evidence_count == 1
    assert conf.score <= 0.5   # honesty cap


async def test_triangulated_multi_source_can_be_high():
    eng = TrustEngineImpl()
    signals = [
        EvidenceSignal(evidence_unit_id=f"eu{i}", supports=True,
                       method=Method.QUANT if i % 2 else Method.QUAL,
                       source_quality=0.9, recency_score=0.9)
        for i in range(5)
    ]
    conf = await eng.score(ScoreRequest(statement="Resistance concern is a consistent brake.", signals=signals))
    assert conf.rationale.method_triangulation is True
    assert conf.band in (ConfidenceBand.MODERATE, ConfidenceBand.HIGH)


async def test_contradictions_lower_consistency():
    eng = TrustEngineImpl()
    signals = [
        EvidenceSignal(evidence_unit_id="a", supports=True, method=Method.QUANT, source_quality=0.8, recency_score=0.8),
        EvidenceSignal(evidence_unit_id="b", supports=False, method=Method.QUAL, source_quality=0.8, recency_score=0.8),
    ]
    conf = await eng.score(ScoreRequest(statement="Weight is the top driver.", signals=signals))
    assert conf.rationale.consistency < 1.0
