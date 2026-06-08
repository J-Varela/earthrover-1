# EarthRover-1 Frontend

React + Vite dashboard for the rover simulation.

## Run

```bash
npm install
npm run dev
```

## Environment

By default the frontend is built into static assets and served from `dist`.
The Docker Compose setup proxies `/api` and `/ws/telemetry` to the backend container.

Optional environment variables for non-container deployments:
- `VITE_API_BASE_URL` — public browser-facing API base URL if you are bypassing the proxy
- `VITE_WS_URL` — public browser-facing websocket URL if you are bypassing the proxy
