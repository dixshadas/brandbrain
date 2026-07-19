from brandbrain.domain.events import EventType
PUBLISHES = [EventType.NOTIFICATION_SENT]
CONSUMES = [
    EventType.DOCUMENT_INDEXED,
    EventType.SYNTHESIS_COMPLETED,
    EventType.BRAIN_UPDATE_PROPOSED,
    EventType.MLR_CHECK_FAILED,
]
