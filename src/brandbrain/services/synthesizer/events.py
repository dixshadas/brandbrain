from brandbrain.domain.events import EventType
PUBLISHES = [EventType.SYNTHESIS_REQUESTED, EventType.SYNTHESIS_COMPLETED, EventType.SYNTHESIS_FAILED]
CONSUMES: list[str] = []   # runs are triggered by the API; the worker calls execute()
