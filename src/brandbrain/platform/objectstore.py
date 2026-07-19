"""Binary storage for source documents and extracted assets (slide images, audio).

Interface + S3/MinIO adapter. Originals are write-once (content-addressed by SHA-256) so a
citation can always be re-verified against the exact bytes that were ingested.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class StoredObject:
    key: str
    sha256: str
    size: int
    content_type: str


class ObjectStore(Protocol):
    async def put(self, key: str, data: bytes, content_type: str) -> StoredObject: ...
    async def get(self, key: str) -> bytes: ...
    async def presign_get(self, key: str, ttl_seconds: int = 900) -> str: ...
    async def exists(self, key: str) -> bool: ...


class InMemoryObjectStore:
    def __init__(self) -> None:
        self._data: dict[str, tuple[bytes, str]] = {}

    async def put(self, key: str, data: bytes, content_type: str) -> StoredObject:
        self._data[key] = (data, content_type)
        return StoredObject(key, hashlib.sha256(data).hexdigest(), len(data), content_type)

    async def get(self, key: str) -> bytes:
        return self._data[key][0]

    async def presign_get(self, key: str, ttl_seconds: int = 900) -> str:
        return f"memory://{key}?ttl={ttl_seconds}"

    async def exists(self, key: str) -> bool:
        return key in self._data


class S3ObjectStore:  # pragma: no cover - needs boto3 + network
    """boto3 adapter (works against AWS S3 or MinIO). Stubbed for the scaffold."""

    def __init__(self, bucket: str, endpoint_url: str | None, region: str) -> None:
        self._bucket = bucket
        self._endpoint = endpoint_url
        self._region = region

    async def put(self, key: str, data: bytes, content_type: str) -> StoredObject:
        raise NotImplementedError("Use aioboto3 put_object; content-address by sha256.")

    async def get(self, key: str) -> bytes:
        raise NotImplementedError

    async def presign_get(self, key: str, ttl_seconds: int = 900) -> str:
        raise NotImplementedError

    async def exists(self, key: str) -> bool:
        raise NotImplementedError
