from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Set
import asyncio
from datetime import datetime
from app.adapters.mock_generator import get_mock_market_snapshot

router = APIRouter()

class ConnectionManager:
    def __init__(self):
        self.active: Set[WebSocket] = set()

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active.add(ws)

    def disconnect(self, ws: WebSocket):
        self.active.discard(ws)

    async def broadcast(self, message: dict):
        disconnected = set()
        for ws in self.active:
            try:
                await ws.send_json(message)
            except Exception:
                disconnected.add(ws)
        self.active -= disconnected

manager = ConnectionManager()

async def market_broadcast_loop():
    while True:
        try:
            snapshot = get_mock_market_snapshot()
            await manager.broadcast({
                "type": "market_snapshot",
                "data": snapshot,
                "timestamp": datetime.now().isoformat(),
            })
        except Exception as e:
            print(f"[WS] broadcast error: {e}")
        await asyncio.sleep(1)

@router.websocket("/ws/market")
async def market_websocket(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            data = await ws.receive_text()
            if data == "ping":
                await ws.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(ws)