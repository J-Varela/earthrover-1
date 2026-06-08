# EarthRover-1 Backend

FastAPI backend for the rover simulation.

## Run

```bash
uv sync
uv run uvicorn app.main:app --reload
```

## Main endpoints

- `GET /rover/telemetry`
- `POST /rover/command`
- `POST /rover/mission`
- `GET /world`

## Behavior notes

- Manual rover commands cancel any active mission so direct operator input takes precedence.