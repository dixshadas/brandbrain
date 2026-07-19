"""Central, typed configuration. One settings object, read from env (BB_ prefix).

Kept boring on purpose: no dynamic config, no service discovery magic. A new engineer can
read this file and know every knob the system has.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="BB_", env_file=".env", extra="ignore")

    env: Literal["local", "dev", "staging", "prod"] = "local"
    log_level: str = "INFO"
    service_name: str = "brandbrain-api"

    # datastores
    database_url: str = "postgresql+asyncpg://brandbrain:brandbrain@localhost:5432/brandbrain"
    redis_url: str = "redis://localhost:6379/0"
    eventbus_backend: Literal["redis", "memory"] = "redis"

    # object storage
    s3_endpoint_url: str | None = None
    s3_bucket: str = "brandbrain-evidence"
    s3_access_key: str = ""
    s3_secret_key: str = ""
    s3_region: str = "us-east-1"

    # vector store
    vector_backend: Literal["pgvector", "qdrant"] = "pgvector"
    embedding_model: str = "text-embedding-3-large"
    embedding_dim: int = 1536

    # llm gateway
    llm_backend: str = "litellm"
    llm_synthesis_model: str = "anthropic/claude-3-7-sonnet"
    llm_classify_model: str = "anthropic/claude-3-5-haiku"
    llm_max_concurrency: int = 8

    # auth
    oidc_issuer: str = ""
    oidc_audience: str = "brandbrain-api"
    oidc_jwks_url: str = ""
    service_jwt_secret: str = "change-me-in-prod"

    # telemetry
    otel_exporter_otlp_endpoint: str | None = None
    sentry_dsn: str | None = None

    @property
    def is_prod(self) -> bool:
        return self.env == "prod"


@lru_cache
def get_settings() -> Settings:
    return Settings()
