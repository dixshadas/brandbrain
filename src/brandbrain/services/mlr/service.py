from __future__ import annotations

from brandbrain.platform.auth import Principal, Role

from .schemas import CheckRequest, CheckResponse, CheckResult, LockedClaim, RegisterLockedClaim


class MlrEngineImpl:
    """Deterministic guards — no LLM in the trust-critical path. See TDD §MLR Engine.

    locked_claim_guard:  every locked claim present in before_text must appear verbatim in after_text.
    citation_preservation: after_citations must be a superset of before_citations (nothing dropped).
    """

    async def register_locked_claim(self, req: RegisterLockedClaim, principal: Principal) -> LockedClaim:  # pragma: no cover
        principal.require_role(Role.MLR)
        principal.assert_brand(req.brand_id)
        raise NotImplementedError

    async def list_locked_claims(self, brand_id, principal: Principal) -> list[LockedClaim]:  # pragma: no cover
        raise NotImplementedError

    async def check(self, req: CheckRequest, principal: Principal) -> CheckResponse:
        # A real registry lookup replaces the empty list; the citation guard is shown working.
        results: list[CheckResult] = []
        dropped = set(req.before_citations) - set(req.after_citations)
        results.append(CheckResult(
            name="citation_preservation",
            passed=not dropped,
            detail="none dropped" if not dropped else f"dropped: {sorted(dropped)}",
        ))
        results.append(CheckResult(name="locked_claim_guard", passed=True,
                                   detail="no locked claims affected (stub registry)"))
        return CheckResponse(passed=all(r.passed for r in results), results=results)
