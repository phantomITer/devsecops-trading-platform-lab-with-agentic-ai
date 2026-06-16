from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from app.core.config import settings
from app.database import init_db, SessionLocal
from app.services.accounts_service import init_all_accounts
from app.api import health, accounts, orders, instruments
from app.api.websocket import router as ws_router, market_broadcast_loop

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,      prefix="/api",  tags=["health"])
app.include_router(accounts.router,    prefix="/api",  tags=["accounts"])
app.include_router(orders.router,      prefix="/api",  tags=["orders"])
app.include_router(instruments.router, prefix="/api",  tags=["instruments"])
app.include_router(ws_router,                          tags=["websocket"])

@app.on_event("startup")
async def startup():
    init_db()
    db = SessionLocal()
    try:
        init_all_accounts(db)
    finally:
        db.close()
    asyncio.create_task(market_broadcast_loop())
    print(f"[APP] {settings.APP_NAME} v{settings.APP_VERSION} started")
