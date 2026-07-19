"""Shared fixtures. In-memory adapters keep unit tests fast and hermetic."""
from __future__ import annotations

import pytest


@pytest.fixture
def event_bus():
    from brandbrain.platform.eventbus import InMemoryEventBus
    return InMemoryEventBus()


@pytest.fixture
def object_store():
    from brandbrain.platform.objectstore import InMemoryObjectStore
    return InMemoryObjectStore()


@pytest.fixture
def vector_store():
    from brandbrain.platform.vectorstore import InMemoryVectorStore
    return InMemoryVectorStore()


@pytest.fixture
def analyst_principal():
    from brandbrain.platform.auth import Principal, Role
    return Principal(subject="u1", email="a@x.com", display_name="Analyst",
                     roles={Role.ANALYST}, brand_ids={"brand_demo"})
