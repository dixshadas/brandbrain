"""Prefixed, sortable identifiers (ULID-style) so every ID is self-describing in logs & audits.

e.g. doc_01J9Z...  syn_01J9Z...  bp_01J9Z...  — you can tell an ID's type by eye, which matters
when reading an audit trail.
"""
from __future__ import annotations

import os
import time

_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"  # Crockford base32


def _ulid() -> str:
    ms = int(time.time() * 1000)
    ts = "".join(_ALPHABET[(ms >> (i * 5)) & 31] for i in range(9, -1, -1))
    rnd = os.urandom(10)
    body = "".join(_ALPHABET[b & 31] for b in rnd) + "".join(_ALPHABET[(b >> 5) & 31] for b in rnd[:6])
    return (ts + body)[:26]


def new_id(prefix: str) -> str:
    """Return e.g. 'doc_01J9ZK8Q...'. Prefix names the entity type."""
    return f"{prefix}_{_ulid()}"
