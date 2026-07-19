"""Structured logging + OpenTelemetry tracing. Observability is a trust feature: if we can't see
what the system did, we can't prove what it did.
"""
from __future__ import annotations

import logging

import structlog


def configure_telemetry(service_name: str, log_level: str = "INFO") -> None:
    logging.basicConfig(level=getattr(logging, log_level.upper(), logging.INFO), format="%(message)s")
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.dict_tracebacks,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(getattr(logging, log_level.upper(), logging.INFO)),
    )
    # In prod, also: OTel FastAPI instrumentation + OTLP exporter to the collector.


def logger(name: str) -> structlog.stdlib.BoundLogger:
    return structlog.get_logger(name)
