from brandbrain.domain.events import EventType
PUBLISHES = [EventType.BRAIN_UPDATE_PROPOSED, EventType.BRAIN_UPDATE_PUBLISHED, EventType.BRAIN_UPDATE_REJECTED]
CONSUMES = [EventType.SYNTHESIS_COMPLETED]   # a completed run may auto-draft a proposal (still gated)
