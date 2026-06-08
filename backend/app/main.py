import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.rover import router as rover_router, rover
from app.api.ws import router as ws_router
from app.api.world import router as world_router
from app.simulation.engine import SimulationEngine

engine = SimulationEngine(rover)


def _allowed_origins() -> list[str]:
    raw_origins = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    )
    return [origin.strip() for origin in raw_origins.split(",") if origin.strip()]


@asynccontextmanager
async def lifespan(_: FastAPI):
    engine.start()
    try:
        yield
    finally:
        engine.stop()


app = FastAPI(title="EarthRover-1 API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rover_router)
app.include_router(world_router)
app.include_router(ws_router)