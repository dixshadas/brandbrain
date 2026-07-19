from brandbrain.domain.events import EventType
PUBLISHES: list[str] = []
CONSUMES = [EventType.DOCUMENT_INDEXED]   # refresh lexical index on new content
