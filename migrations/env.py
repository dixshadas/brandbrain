"""Alembic environment. Autogenerate reads every service's models via the shared Base metadata.

Importing the service `models` modules registers their tables on `Base.metadata`, so a single
`alembic revision --autogenerate` covers all ten services.
"""
from __future__ import annotations

from alembic import context

from brandbrain.config import get_settings
from brandbrain.platform.base import Base

# Import model modules for their side effect of registering tables on Base.metadata.
from brandbrain.services.audit import models as _audit          # noqa: F401
from brandbrain.services.brand_brain import models as _brain    # noqa: F401
from brandbrain.services.evidence_store import models as _ev    # noqa: F401
from brandbrain.services.ingestion import models as _ing        # noqa: F401
from brandbrain.services.mlr import models as _mlr              # noqa: F401
from brandbrain.services.notification import models as _notif   # noqa: F401
from brandbrain.services.recommendation import models as _rec   # noqa: F401
from brandbrain.services.synthesizer import models as _syn      # noqa: F401

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(url=get_settings().database_url, target_metadata=target_metadata, literal_binds=True)
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    # Real impl builds an async engine and runs within a connection; omitted in the scaffold.
    run_migrations_offline()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
