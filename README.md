# EarthRover-1

EarthRover-1 is a full-stack rover simulation project with a FastAPI backend and a React + Vite frontend.

## Overview

The project simulates a rover operating in a virtual world. The backend exposes telemetry, command, mission, and world APIs. The frontend provides a dashboard for telemetry, mission control, and rover commands.

## Repository structure

- `backend/` — FastAPI application, simulation engine, domain models, and API routes
- `frontend/` — React + Vite dashboard, telemetry display, and rover controls

## Requirements

- Python 3.11+
- `uv`
- Node.js + npm

## Getting started

Install dependencies for both apps:

```bash
make backend-install frontend-install
```

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

Default backend URL: `http://localhost:8000`

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Default frontend URL: `http://localhost:5173`

By default the frontend is built as static assets and served from `/dist`.
The frontend container also proxies `/api` and `/ws/telemetry` to the backend container in Docker Compose.

### Docker Compose

```bash
docker compose up --build
```

This starts:
- backend on `http://localhost:8000`
- frontend on `http://localhost:5173`

The frontend service builds the app into `dist` and serves it with nginx, while nginx proxies `/api` and `/ws/telemetry` to the backend container.

## Backend API

- `GET /rover/telemetry` — fetch current rover telemetry
- `POST /rover/command` — send a rover control command
- `POST /rover/mission` — create or update a mission
- `GET /world` — fetch world state and environment data

## Development

Common workspace commands:

```bash
make backend-dev
make frontend-dev
make verify
```

### Backend

```bash
cd backend
uv sync
uv run uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Verification

### Backend

```bash
cd backend
uv run python -m compileall app
uv run pytest -q
```

### Frontend

```bash
cd frontend
npm test
npm run lint
npm run build
```

## Notes

- Backend source: `backend/app/`
- Frontend source: `frontend/src/`
- Backend CORS origins default to `http://localhost:5173,http://127.0.0.1:5173`; override with `ALLOWED_ORIGINS`
- Sending a manual rover command cancels any active mission so direct controls always take precedence
- Use `VITE_API_BASE_URL` and `VITE_WS_URL` to point the frontend at a public backend without relying on the Vite proxy


## License

This repository does not include a license file. Add one if you want to share or reuse the project publicly.
