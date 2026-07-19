# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base
ENV PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app

# System deps kept minimal; add only what wheels need.
RUN apt-get update && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml README.md ./
COPY src ./src
RUN pip install -e ".[llm]"

# Non-root: security baseline.
RUN useradd -m app && chown -R app /app
USER app

EXPOSE 8000
# API image. The worker uses the same image with a different command (see docker-compose).
CMD ["uvicorn", "brandbrain.main:app", "--host", "0.0.0.0", "--port", "8000"]
