# app/api/websocket.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict, Set
import asyncio
import json
from datetime import datetime
from app.adapters.mock_generator import get_mock_market_snapshot

router = APIRouter()

# ── 연결된 클라이언트 관리 ────────────────────────
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


# ── 시세 브로드캐스트 루프 ────────────────────────
async def market_broadcast_loop():
    """
    1초마다 시세 데이터를 모든 연결 클라이언트에 브로드캐스트
    실제: krx_fetcher → 개발: mock_generator
    """
    while True:
        try:
            snapshot = get_mock_market_snapshot()
            await manager.broadcast({
                "type":      "market_snapshot",
                "data":      snapshot,
                "timestamp": datetime.now().isoformat(),
            })
        except Exception as e:
            print(f"[WS] broadcast error: {e}")
        await asyncio.sleep(1)


# ── WebSocket 엔드포인트 ──────────────────────────
@router.websocket("/ws/market")
async def market_websocket(ws: WebSocket):
    """
    실시간 시세 스트리밍
    → appFrontEnd, agenticAi 에이전트 공통 연결
    """
    await manager.connect(ws)
    try:
        while True:
            # 클라이언트로부터 ping 수신 대기
            data = await ws.receive_text()
            if data == "ping":
                await ws.send_json({"type": "pong"})
    except WebSocketDisconnect:
        manager.disconnect(ws)