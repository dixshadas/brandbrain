.PHONY: install up down migrate api worker test lint typecheck contracts tree
install:      ; pip install -e ".[dev,llm]"
up:           ; docker compose up -d
down:         ; docker compose down
migrate:      ; alembic upgrade head
api:          ; uvicorn brandbrain.main:app --reload
worker:       ; arq brandbrain.worker.WorkerSettings
test:         ; pytest -m "unit or contract"
test-all:     ; pytest
lint:         ; ruff check src tests && ruff format --check src tests
typecheck:    ; mypy src
contracts:    ; python -m tests.contract.validate_all
openapi:      ; python -c "import json,brandbrain.main as m; print(json.dumps(m.app.openapi()))" > contracts/openapi/openapi.json
