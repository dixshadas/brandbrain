"""The type system is the first line of the trust architecture: illegal states must not compile
into existence. A FACT without a citation is unrepresentable; HIGH confidence from one source is
rejected at construction."""
import pytest
from pydantic import ValidationError

from brandbrain.domain.common import (
    ClaimLayer, Confidence, ConfidenceBand, ConfidenceRationale, Finding,
)

pytestmark = pytest.mark.unit


def test_fact_requires_citation():
    with pytest.raises(ValidationError):
        Finding(layer=ClaimLayer.FACT, statement="54% cite non-daily preference.", citations=[])


def test_high_confidence_requires_multiple_sources():
    with pytest.raises(ValidationError):
        Confidence(band=ConfidenceBand.HIGH, score=0.9,
                   rationale=ConfidenceRationale(evidence_count=1, source_quality=1.0, recency_score=1.0,
                                                 method_triangulation=False, consistency=1.0))
