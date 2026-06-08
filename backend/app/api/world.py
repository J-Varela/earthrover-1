from fastapi import APIRouter

from app.simulation.world import OBSTACLES

router = APIRouter(prefix="/world", tags=["world"])


@router.get("")
def get_world():
    return {"obstacles": OBSTACLES}