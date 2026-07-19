from brandbrain.domain.events import EventType
PUBLISHES = [EventType.MLR_CHECK_FAILED, EventType.LOCKED_CLAIM_REGISTERED]
CONSUMES: list[str] = []
