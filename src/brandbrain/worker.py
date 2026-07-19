"""Background worker: the async half of the modular monolith.

One process consumes the event bus and drives the long / cross-service work:
  - the ingestion pipeline (parse -> evidence units -> embeddings -> indexed)
  - synthesis execution (Synthesizer.execute) off the request path
  - fan-out to the Notification Engine
  - the universal Audit subscriber (every event is journaled)
Runs on arq (async Redis queue). At scale, split these into per-service consumer groups without
changing the handlers — they already depend only on service interfaces.
"""
from __future__ import annotations

from brandbrain.config import get_settings
from brandbrain.domain.events import Event
from brandbrain.platform.telemetry import configure_telemetry, logger

log = logger("worker")


async def route_event(ctx: dict, event_dict: dict) -> None:
    """arq task: deserialize an event and dispatch to interested handlers.

    Ordering guarantees come from the bus (per-key streams); handlers must be idempotent
    (keyed on event.id) because at-least-once delivery can replay.
    """
    event = Event.model_validate(event_dict)
    log.info("event", type=event.type, id=event.id, brand=event.brand_id)
    # Dispatch table wired at startup:
    #   audit.append(event)                     # always (universal subscriber)
    #   if DOCUMENT_APPROVED -> evidence_store ingest units -> emit DOCUMENT_INGESTED
    #   if SYNTHESIS_REQUESTED -> synthesizer.execute(run_id)
    #   if *_PROPOSED / *_INDEXED -> notification.fan_out(event)
    # (handlers omitted in the scaffold; see TDD §Worker & Eventing.)


async def startup(ctx: dict) -> None:
    s = get_settings()
    configure_telemetry("brandbrain-worker", s.log_level)
    log.info("worker.startup", env=s.env)


class WorkerSettings:
    """arq entrypoint: `arq brandbrain.worker.WorkerSettings`."""
    functions = [route_event]
    on_startup = startup
    # redis_settings derived from BB_REDIS_URL at boot in the real wiring.
