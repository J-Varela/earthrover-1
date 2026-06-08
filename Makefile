.PHONY: backend-install backend-dev backend-check frontend-install frontend-dev frontend-lint frontend-test frontend-build verify

backend-install:
	cd backend && uv sync

backend-dev:
	cd backend && uv run uvicorn app.main:app --reload

backend-check:
	cd backend && uv run python -m compileall app
	cd backend && uv run pytest -q

frontend-install:
	cd frontend && npm install

frontend-dev:
	cd frontend && npm run dev

frontend-lint:
	cd frontend && npm run lint

frontend-test:
	cd frontend && npm test

frontend-build:
	cd frontend && npm run build

verify: backend-check frontend-lint frontend-test frontend-build