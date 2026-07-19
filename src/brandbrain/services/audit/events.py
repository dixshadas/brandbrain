"""Audit CONSUMES everything — it is the universal subscriber. It publishes nothing."""
PUBLISHES: list[str] = []
CONSUMES = ["*"]   # wildcard: the worker routes every event to the Audit Engine
