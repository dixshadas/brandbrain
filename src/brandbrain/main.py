"""API composition root.

The modular monolith is assembled here: every service router is mounted onto one FastAPI app,
error handlers map typed errors to RFC-9457 problem responses, and telemetry is configured.
Because each router is self-contained and depends only on its service *interface*, moving a
service to its own process later means pointing its router at a remote client — nothing else.
"""
from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from brandbrain import __version__
from brandbrain.config import get_settings
from brandbrain.platform.errors import BrandBrainError
from brandbrain.platform.telemetry import configure_telemetry, logger

# Service routers
from brandbrain.services.audit.api import router as audit_router
from brandbrain.services.brand_brain.api import router as brain_router
from brandbrain.services.evidence_store.api import router as evidence_router
from brandbrain.services.ingestion.api import router as ingestion_router
from brandbrain.services.mlr.api import router as mlr_router
from brandbrain.services.notification.api import router as notification_router
from brandbrain.services.recommendation.api import router as recommendation_router
from brandbrain.services.retrieval.api import router as retrieval_router
from brandbrain.services.synthesizer.api import router as synthesizer_router
from brandbrain.services.trust.api import router as trust_router

log = logger(__name__)

ROUTERS = [
    ingestion_router, evidence_router, retrieval_router, synthesizer_router,
    brain_router, mlr_router, trust_router, audit_router,
    recommendation_router, notification_router,
]


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    s = get_settings()
    configure_telemetry(s.service_name, s.log_level)
    log.info("startup", env=s.env, version=__version__)
    yield
    log.info("shutdown")


def create_app() -> FastAPI:
    s = get_settings()
    app = FastAPI(
        title="BrandBrain API",
        version=__version__,
        description="Trust-first evidence intelligence for pharmaceutical brand teams.",
        lifespan=lifespan,
    )

    @app.exception_handler(BrandBrainError)
    async def _domain_error(_: Request, exc: BrandBrainError) -> JSONResponse:
        # RFC-9457 problem+json — machine-readable, so the UI can explain *why* something failed.
        return JSONResponse(
            status_code=exc.http_status,
            content={"type": f"about:blank#{exc.code}", "title": exc.code, "detail": str(exc)},
            media_type="application/problem+json",
        )

    @app.get("/healthz", tags=["ops"], summary="Liveness")
    async def healthz() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    for r in ROUTERS:
        app.include_router(r)

    return app


app = create_app()
