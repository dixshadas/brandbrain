"""Authentication + authorization.

Users authenticate via the enterprise IdP (OIDC/OAuth2); we validate the JWT against the IdP's
JWKS. Internal service-to-service calls use short-lived signed tokens. Authorization is RBAC
*and* brand-scoped: a Principal carries the set of brands it may touch, and every brand-scoped
read/write must assert membership (BrandIsolationError otherwise). This is the code-level half of
the 'brand isolation' guarantee the product sells.
"""
from __future__ import annotations

from enum import StrEnum

from pydantic import BaseModel, Field

from brandbrain.platform.errors import BrandIsolationError


class Role(StrEnum):
    VIEWER = "viewer"                # read syntheses, brand brain (published)
    ANALYST = "analyst"              # run syntheses, propose brain updates
    REVIEWER = "reviewer"            # approve/publish in the review queue
    MLR = "mlr"                      # manage locked claims, sign off substantiation
    ADMIN = "admin"                  # connectors, users, settings


class Principal(BaseModel):
    """The authenticated subject on every request. Injected as a FastAPI dependency."""
    subject: str
    email: str
    display_name: str
    roles: set[Role] = Field(default_factory=set)
    brand_ids: set[str] = Field(default_factory=set)   # brands this principal may access
    is_service: bool = False

    def require_role(self, *roles: Role) -> None:
        if self.is_service:
            return
        if not set(roles) & self.roles:
            from brandbrain.platform.errors import AuthorizationError

            raise AuthorizationError(f"requires one of roles: {[r.value for r in roles]}")

    def assert_brand(self, brand_id: str) -> None:
        """Enforce brand isolation. Service principals may be granted cross-brand scopes explicitly."""
        if self.is_service:
            return
        if brand_id not in self.brand_ids:
            raise BrandIsolationError(f"principal not permitted for brand {brand_id}")


# --- FastAPI dependencies (thin; real JWKS validation lives in the OIDC verifier) ---
async def get_principal() -> Principal:  # pragma: no cover - overridden by real verifier
    """Placeholder dependency. In production this validates the bearer JWT against the IdP JWKS,
    maps IdP groups -> Role, and loads brand entitlements. Overridden in main.py via DI.
    """
    raise NotImplementedError("Bound to the OIDC verifier in main.create_app().")
