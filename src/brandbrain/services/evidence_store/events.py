from brandbrain.domain.events import EventType
PUBLISHES: list[str] = []
CONSUMES = [EventType.DOCUMENT_APPROVED]   # writes units when a doc passes the gate
