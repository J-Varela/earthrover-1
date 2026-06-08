# Root-context Dockerfile for the backend service.
# This lets `docker build .` work from the repo root while the app itself lives in backend/.

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir uv

# Copy dependency metadata first so dependency install layers can be cached.
COPY backend/pyproject.toml backend/uv.lock ./

RUN uv sync --frozen --no-dev

# Copy backend sources after dependency installation.
COPY backend/app ./app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
