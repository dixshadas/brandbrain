"""The asynchronous backbone. Services publish domain events; the worker consumes them.

Interface first (EventBus protocol), then two adapters: an in-memory bus for tests and a Redis
Streams bus for local/prod. Redis Streams gives us a *durable, replayable* log with consumer
groups — which matters because 'what happened and in what order' is an auditability requirement,
not just a delivery mechanism. Swap for Kafka/NATS at scale without touching callers.
"""
from __future__ import annotations

import asyncio
from collections import defaultdict
from collections.abc import Awaitable, Callable
from typing import Protocol

from brandbrain.domain.events import Event

Handler = Callable[[Event], Awaitable[None]]


class EventBus(Protocol):
    async def publish(self, event: Event) -> None: ...
    def subscribe(self, event_type: str, handler: Handler) -> None: ...
    async def start(self) -> None: ...
    async def stop(self) -> None: ...


class InMemoryEventBus:
    """Synchronous, deterministic bus for unit/integration tests."""

    def __init__(self) -> None:
        self._handlers: dict[str, list[Handler]] = defaultdict(list)
        self.published: list[Event] = []

    async def publish(self, event: Event) -> None:
        self.published.append(event)
        for h in self._handlers.get(event.type, []):
            await h(event)

    def subscribe(self, event_type: str, handler: Handler) -> None:
        self._handlers[event_type].append(handler)

    async def start(self) -> None:  # noqa: D401
        return None

    async def stop(self) -> None:
        return None


class RedisStreamEventBus:
    """Production adapter over Redis Streams (one stream per event type, one consumer group).

    Stubbed here to keep the scaffold import-clean without a live Redis; the real implementation
    uses XADD / XREADGROUP / XACK and a dead-letter stream for poison messages.
    """

    def __init__(self, redis_url: str, group: str = "brandbrain") -> None:
        self._url = redis_url
        self._group = group
        self._handlers: dict[str, list[Handler]] = defaultdict(list)
        self._tasks: list[asyncio.Task[None]] = []

    async def publish(self, event: Event) -> None:  # pragma: no cover - needs redis
        raise NotImplementedError("Wire redis.asyncio XADD here; see TDD §EventBus.")

    def subscribe(self, event_type: str, handler: Handler) -> None:
        self._handlers[event_type].append(handler)

    async def start(self) -> None:  # pragma: no cover
        raise NotImplementedError

    async def stop(self) -> None:  # pragma: no cover
        for t in self._tasks:
            t.cancel()


def build_event_bus() -> EventBus:
    from brandbrain.config import get_settings

    s = get_settings()
    if s.eventbus_backend == "memory":
        return InMemoryEventBus()
    return RedisStreamEventBus(s.redis_url)
