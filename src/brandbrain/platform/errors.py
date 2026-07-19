"""Typed application errors. Handlers in main.py map these to RFC-9457 problem responses."""
from __future__ import annotations


class BrandBrainError(Exception):
    """Base for all domain/application errors."""
    code = "brandbrain_error"
    http_status = 500


class NotFoundError(BrandBrainError):
    code = "not_found"
    http_status = 404


class ValidationError(BrandBrainError):
    code = "validation_error"
    http_status = 422


class AuthorizationError(BrandBrainError):
    code = "forbidden"
    http_status = 403


class BrandIsolationError(AuthorizationError):
    """Raised when a principal or agent attempts to read across a brand boundary."""
    code = "brand_isolation_violation"


class GovernanceError(BrandBrainError):
    """A write attempted to bypass the review gate, or a locked-claim guard tripped."""
    code = "governance_violation"
    http_status = 409


class LockedClaimViolation(GovernanceError):
    code = "locked_claim_violation"


class CitationDroppedError(GovernanceError):
    code = "citation_preservation_failed"


class ConflictError(BrandBrainError):
    code = "conflict"
    http_status = 409
