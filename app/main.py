
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.api.v1 import auth, users, accounts, orders, positions, agent_logs, security_events, health, market_data

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    print("[APP] DevSecOps Trading Platform v1.0.0 started")
    yield

app = FastAPI(
    title="DevSecOps Trading Platform",
    version="1.0.0",
    description="DevSecOps Trading Platform Lab with Agentic AI",
    redirect_slashes=False,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,           prefix="/api/v1")
app.include_router(auth.router,             prefix="/api/v1")
app.include_router(users.router,            prefix="/api/v1")
app.include_router(accounts.router,         prefix="/api/v1")
app.include_router(orders.router,           prefix="/api/v1")
app.include_router(positions.router,        prefix="/api/v1")
app.include_router(agent_logs.router,       prefix="/api/v1")
app.include_router(security_events.router,  prefix="/api/v1")
app.include_router(market_data.router,      prefix="/api/v1")
