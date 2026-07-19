"""Citation-preservation guard: a proposed change may not silently drop a citation the live page
depends on. This is the check that blocked the 'Message Recall' enrichment in the demo."""
import pytest

from brandbrain.platform.auth import Principal, Role
from brandbrain.services.mlr.schemas import CheckRequest
from brandbrain.services.mlr.service import MlrEngineImpl

pytestmark = pytest.mark.unit


async def test_dropped_citation_fails_check():
    eng = MlrEngineImpl()
    p = Principal(subject="u", email="e", display_name="R", roles={Role.MLR}, brand_ids={"b"})
    res = await eng.check(CheckRequest(
        brand_id="b", before_text="x", after_text="y",
        before_citations=["eu_msg_testing", "eu_tracker"],
        after_citations=["eu_tracker"],   # dropped eu_msg_testing
    ), p)
    assert res.passed is False
    assert any(r.name == "citation_preservation" and not r.passed for r in res.results)
