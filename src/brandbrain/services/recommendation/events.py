from brandbrain.domain.events import EventType
PUBLISHES = [EventType.RECOMMENDATION_DRAFTED]
CONSUMES = [EventType.SYNTHESIS_COMPLETED]
