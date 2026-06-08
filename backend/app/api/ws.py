import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from app.api.rover import rover

router = APIRouter(prefix="/ws", tags=["websocket"])


@router.websocket("/telemetry")
async def telemetry_socket(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            await websocket.send_json(rover.telemetry())
            await asyncio.sleep(0.5)
    except WebSocketDisconnect:
        return
