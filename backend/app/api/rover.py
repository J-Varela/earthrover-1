from typing import Literal

from fastapi import APIRouter
from pydantic import BaseModel

from app.models import Mission
from app.simulation.rover import Rover

router = APIRouter(prefix="/rover", tags=["rover"])

rover = Rover()


class CommandRequest(BaseModel):
    command: Literal["forward", "backward", "left", "right", "stop"]


@router.get("/telemetry")
def get_telemetry():
    return rover.telemetry()


@router.post("/command")
def send_command(payload: CommandRequest):
    rover.command(payload.command)
    return rover.telemetry()


@router.post("/mission")
def set_mission(payload: Mission):
    rover.set_mission(payload.target_x, payload.target_y)
    return rover.telemetry()
