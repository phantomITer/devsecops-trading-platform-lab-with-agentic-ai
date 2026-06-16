# setup_files.py
import os

files = {
"app/core/security.py": '''
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_access_token(token: str) -> Optional[dict]:
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
    except JWTError:
        return None

def verify_api_key(api_key: str) -> Optional[str]:
    return settings.VALID_API_KEYS.get(api_key)
'''.strip(),

"app/core/dependencies.py": '''
from fastapi import Header, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.core.security import verify_api_key, decode_access_token
from app.database import SessionLocal
from typing import Optional

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def verify_agent_api_key(x_api_key: Optional[str] = Header(None)) -> str:
    if not x_api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="X-API-Key header missing")
    agent_id = verify_api_key(x_api_key)
    if not agent_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid API Key")
    return agent_id

bearer_scheme = HTTPBearer(auto_error=False)

async def verify_jwt_token(credentials: Optional[HTTPAuthorizationCredentials] = Depends(bearer_scheme)) -> dict:
    if not credentials:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authorization header missing")
    payload = decode_access_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")
    return payload

AgentDep = Depends(verify_agent_api_key)
UserDep  = Depends(verify_jwt_token)
DBDep    = Depends(get_db)
'''.strip(),

"app/database.py": '''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

connect_args = {"check_same_thread": False} if settings.DB_URL.startswith("sqlite") else {}
engine = create_engine(settings.DB_URL, connect_args=connect_args, echo=settings.DEBUG)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from app.models import accounts, orders, instruments  # noqa
    Base.metadata.create_all(bind=engine)
'''.strip(),

"app/models/__init__.py": '''
from app.models.accounts import Account
from app.models.orders import Order, OrderSide, OrderStatus
from app.models.instruments import Instrument

__all__ = ["Account", "Order", "OrderSide", "OrderStatus", "Instrument"]
'''.strip(),

"app/models/accounts.py": '''
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from sqlalchemy.sql import func
from app.database import Base

class Account(Base):
    __tablename__ = "accounts"
    id             = Column(Integer, primary_key=True, index=True)
    agent_id       = Column(String, unique=True, index=True, nullable=False)
    balance        = Column(Float, default=10_000_000.0)
    equity         = Column(Float, default=10_000_000.0)
    unrealized_pnl = Column(Float, default=0.0)
    realized_pnl   = Column(Float, default=0.0)
    is_active      = Column(Boolean, default=True)
    created_at     = Column(DateTime, server_default=func.now())
    updated_at     = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<Account agent={self.agent_id} balance={self.balance}>"
'''.strip(),

"app/models/orders.py": '''
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
from sqlalchemy.sql import func
import enum
from app.database import Base

class OrderSide(str, enum.Enum):
    LONG  = "long"
    SHORT = "short"

class OrderStatus(str, enum.Enum):
    PENDING   = "pending"
    FILLED    = "filled"
    CANCELLED = "cancelled"
    REJECTED  = "rejected"

class Order(Base):
    __tablename__ = "orders"
    id           = Column(Integer, primary_key=True, index=True)
    agent_id     = Column(String, index=True, nullable=False)
    ticker       = Column(String, nullable=False)
    side         = Column(Enum(OrderSide), nullable=False)
    quantity     = Column(Integer, nullable=False)
    price        = Column(Float, nullable=True)
    filled_price = Column(Float, nullable=True)
    status       = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    reason       = Column(String, nullable=True)
    created_at   = Column(DateTime, server_default=func.now())
    filled_at    = Column(DateTime, nullable=True)

    def __repr__(self):
        return f"<Order {self.agent_id} {self.side} {self.ticker} x{self.quantity}>"
'''.strip(),

"app/models/instruments.py": '''
from sqlalchemy import Column, Integer, String, Float, DateTime, BigInteger
from sqlalchemy.sql import func
from app.database import Base

class Instrument(Base):
    __tablename__ = "instruments"
    id          = Column(Integer, primary_key=True, index=True)
    ticker      = Column(String, unique=True, index=True, nullable=False)
    name        = Column(String, nullable=False)
    market      = Column(String, default="KOSPI")
    open_price  = Column(Float, nullable=True)
    high_price  = Column(Float, nullable=True)
    low_price   = Column(Float, nullable=True)
    close_price = Column(Float, nullable=True)
    volume      = Column(BigInteger, nullable=True)
    updated_at  = Column(DateTime, onupdate=func.now())

    def __repr__(self):
        return f"<Instrument {self.ticker} {self.name}>"
'''.strip(),

"app/services/accountsservice.py": '''
from sqlalchemy.orm import Session
from app.models.accounts import Account
from typing import Optional

def get_account(db: Session, agent_id: str) -> Optional[Account]:
    return db.query(Account).filter(Account.agent_id == agent_id).first()

def get_all_accounts(db: Session) -> list:
    return db.query(Account).all()

def create_account(db: Session, agent_id: str) -> Account:
    account = Account(agent_id=agent_id)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def update_balance(db: Session, agent_id: str, delta: float) -> Optional[Account]:
    account = get_account(db, agent_id)
    if not account:
        return None
    account.balance += delta
    db.commit()
    db.refresh(account)
    return account

def init_all_accounts(db: Session):
    for agent_id in ["red", "blue", "institutional", "retail_a", "retail_b"]:
        if not get_account(db, agent_id):
            create_account(db, agent_id)
'''.strip(),

"app/services/ordersservice.py": '''
from sqlalchemy.orm import Session
from app.models.orders import Order, OrderSide, OrderStatus
from typing import Optional
from datetime import datetime

def create_order(db: Session, agent_id: str, ticker: str, side: OrderSide,
                 quantity: int, price: Optional[float] = None, reason: Optional[str] = None) -> Order:
    order = Order(agent_id=agent_id, ticker=ticker, side=side,
                  quantity=quantity, price=price, reason=reason, status=OrderStatus.PENDING)
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def fill_order(db: Session, order_id: int, filled_price: float) -> Optional[Order]:
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    order.status       = OrderStatus.FILLED
    order.filled_price = filled_price
    order.filled_at    = datetime.utcnow()
    db.commit()
    db.refresh(order)
    return order

def get_orders_by_agent(db: Session, agent_id: str, limit: int = 50) -> list:
    return (db.query(Order).filter(Order.agent_id == agent_id)
            .order_by(Order.created_at.desc()).limit(limit).all())
'''.strip(),

"app/api/websocket.py": '''
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
'''.strip(),

"app/api/health.py": '''
from fastapi import APIRouter
from datetime import datetime

router = APIRouter()

_agent_heartbeats: dict = {}

@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "app": "DevSecOps Trading Platform",
        "timestamp": datetime.now().isoformat(),
    }

@router.post("/health/agents/{agent_id}/heartbeat")
def agent_heartbeat(agent_id: str):
    _agent_heartbeats[agent_id] = datetime.now().isoformat()
    return {"status": "ok", "agent_id": agent_id}

@router.get("/health/agents")
def get_agents_status():
    agent_ids = ["red", "blue", "institutional", "retail_a", "retail_b"]
    result = {}
    for agent_id in agent_ids:
        last = _agent_heartbeats.get(agent_id)
        result[agent_id] = {"online": last is not None, "last_seen": last or "never"}
    return {"agents": result}
'''.strip(),

"app/main.py": '''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import asyncio

from app.core.config import settings
from app.database import init_db, SessionLocal
from app.services.accountsservice import init_all_accounts
from app.api import health, accounts, orders, instruments
from app.api.websocket import router as ws_router, market_broadcast_loop

app = FastAPI(title=settings.APP_NAME, version=settings.APP_VERSION, debug=settings.DEBUG)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router,              tags=["health"])
app.include_router(accounts.router,   prefix="/accounts",    tags=["accounts"])
app.include_router(orders.router,     prefix="/orders",      tags=["orders"])
app.include_router(instruments.router,prefix="/instruments", tags=["instruments"])
app.include_router(ws_router,                                tags=["websocket"])

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
'''.strip(),
}

for filepath, content in files.items():
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✅ {filepath}")

print("\n--- 모든 파일 생성 완료 ---")