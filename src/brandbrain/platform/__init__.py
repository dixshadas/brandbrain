"""Shared infrastructure, every piece behind an interface so it can be swapped or mocked.

The application code depends on these *protocols*, never on a concrete vendor. That is what
makes 'pgvector now, Qdrant later' or 'Redis Streams now, Kafka later' a config change, not a
rewrite.
"""
