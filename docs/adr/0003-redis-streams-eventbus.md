# ADR 0003 — Redis Streams as the event bus for the MVP (Kafka/NATS later)

**Status:** Accepted · **Date:** 2026-07

## Context
Async work (ingestion, synthesis, notifications) and an auditable event log both need a backbone.
We already run Redis for cache/queue.

## Decision
Use Redis Streams (durable, consumer groups, replay) behind `platform.eventbus.EventBus`. Provide an
in-memory bus for tests.

## Alternatives considered
- **Kafka/NATS JetStream now.** Rejected for the MVP: heavy to operate; scale we don't have yet.
- **Cloud queue (SQS/PubSub).** Rejected: weaker replay/ordering ergonomics for an audit substrate,
  and more cloud lock-in than we want this early.

## Consequences
One fewer system to run; durable + replayable log that doubles as audit substrate. The `EventBus`
interface makes a Kafka/NATS move a config+adapter change. Watch Redis memory/retention for the
stream log; set retention + offload to the audit table.
