"""Ingestion PUBLISHES the document lifecycle; it CONSUMES nothing."""
from brandbrain.domain.events import EventType

PUBLISHES = [
    EventType.DOCUMENT_RECEIVED,
    EventType.DOCUMENT_METADATA_PROPOSED,
    EventType.DOCUMENT_APPROVED,
    EventType.DOCUMENT_INGESTED,
    EventType.DOCUMENT_INDEXED,
]
CONSUMES: list[str] = []
