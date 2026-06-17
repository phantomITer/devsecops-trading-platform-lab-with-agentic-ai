import os

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] {path}")

# 1. database.py - declarative_base + utcnow 경고 수정
write("app/database.py", '''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from datetime import datetime, UTC

SQLALCHEMY_DATABASE_URL = "sqlite:///./trading.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    from app.models import User, Account, Order, Position, AgentLog, SecurityEvent
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
''')

# 2. 모든 모델 utcnow → datetime.now(UTC)
write("app/models/user.py", '''
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    accounts = relationship("Account", back_populates="owner")
''')

write("app/models/account.py", '''
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from app.database import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=False)
    currency = Column(String, default="KRW")
    initial_balance = Column(Float, default=0.0)
    current_balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    owner = relationship("User", back_populates="accounts")
    orders = relationship("Order", back_populates="account")
    positions = relationship("Position", back_populates="account")
''')

write("app/models/order.py", '''
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)
    order_type = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=True)
    status = Column(String, default="NEW")
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
    account = relationship("Account", back_populates="orders")
''')

write("app/models/position.py", '''
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, UTC
from app.database import Base

class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    symbol = Column(String, nullable=False)
    quantity = Column(Float, default=0.0)
    avg_price = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=lambda: datetime.now(UTC))
    account = relationship("Account", back_populates="positions")
''')

write("app/models/agent_log.py", '''
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, UTC
from app.database import Base

class AgentLog(Base):
    __tablename__ = "agent_logs"
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, nullable=False)
    agent_type = Column(String, nullable=False)
    action = Column(String, nullable=False)
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
''')

write("app/models/security_event.py", '''
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime, UTC
from app.database import Base

class SecurityEvent(Base):
    __tablename__ = "security_events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    source = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(UTC))
''')

# 3. security.py - utcnow 수정
write("app/core/security.py", '''
from datetime import datetime, timedelta, UTC
from typing import Optional
from jose import JWTError, jwt
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

SECRET_KEY = "devsecops-secret-key-change-in-prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

ph = PasswordHasher()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def hash_password(password: str) -> str:
    return ph.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return ph.verify(hashed, plain)
    except VerifyMismatchError:
        return False

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    return user
''')

# 4. 모든 스키마 ConfigDict로 수정
write("app/schemas/user.py", '''
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str
''')

write("app/schemas/account.py", '''
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime

class AccountCreate(BaseModel):
    name: str
    currency: str = "KRW"
    initial_balance: float = 0.0

    @field_validator("name")
    @classmethod
    def name_not_empty(cls, v):
        if not v.strip():
            raise ValueError("name must not be empty")
        return v

    @field_validator("initial_balance")
    @classmethod
    def balance_non_negative(cls, v):
        if v < 0:
            raise ValueError("initial_balance must be >= 0")
        return v

class AccountResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    name: str
    currency: str
    initial_balance: float
    current_balance: float
    created_at: datetime
''')

write("app/schemas/order.py", '''
from pydantic import BaseModel, ConfigDict, field_validator
from datetime import datetime
from typing import Optional
from enum import Enum

class OrderSide(str, Enum):
    BUY = "BUY"
    SELL = "SELL"

class OrderType(str, Enum):
    MARKET = "MARKET"
    LIMIT = "LIMIT"

class OrderCreate(BaseModel):
    account_id: int
    symbol: str
    side: OrderSide
    order_type: OrderType
    quantity: float
    price: Optional[float] = None

    @field_validator("quantity")
    @classmethod
    def quantity_positive(cls, v):
        if v <= 0:
            raise ValueError("quantity must be > 0")
        return v

class OrderResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    account_id: int
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float]
    status: str
    created_at: datetime
''')

write("app/schemas/position.py", '''
from pydantic import BaseModel, ConfigDict
from datetime import datetime

class PositionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    account_id: int
    symbol: str
    quantity: float
    avg_price: float
    updated_at: datetime
''')

write("app/schemas/agent_log.py", '''
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class AgentLogCreate(BaseModel):
    agent_id: str
    agent_type: str
    action: str
    result: Optional[str] = None

class AgentLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    agent_id: str
    agent_type: str
    action: str
    result: Optional[str]
    created_at: datetime
''')

write("app/schemas/security_event.py", '''
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

class SecurityEventCreate(BaseModel):
    event_type: str
    severity: str
    source: Optional[str] = None
    description: Optional[str] = None

class SecurityEventResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    event_type: str
    severity: str
    source: Optional[str]
    description: Optional[str]
    created_at: datetime
''')

# 5. main.py - on_event → lifespan
write("app/main.py", '''
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.api.v1 import auth, users, accounts, orders, positions, agent_logs, security_events, health

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
''')

print()
print("=" * 50)
print("✅ 경고 수정 완료!")
print("=" * 50)
print()
print("pytest tests/test_v1.py -v 로 재확인하세요.")