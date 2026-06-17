import os

def write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  [OK] {path}")

# ─────────────────────────────────────────────
# 1. app/core/security.py  (JWT)
# ─────────────────────────────────────────────
write("app/core/security.py", '''
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User

SECRET_KEY = "devsecops-secret-key-change-in-prod"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain: str, hashed: str) -> bool:
    return pwd_context.verify(plain, hashed)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
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

# ─────────────────────────────────────────────
# 2. app/models/user.py
# ─────────────────────────────────────────────
write("app/models/user.py", '''
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    accounts = relationship("Account", back_populates="owner")
''')

# ─────────────────────────────────────────────
# 3. app/models/account.py  (기존 수정)
# ─────────────────────────────────────────────
write("app/models/account.py", '''
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=False)
    currency = Column(String, default="KRW")
    initial_balance = Column(Float, default=0.0)
    current_balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    owner = relationship("User", back_populates="accounts")
    orders = relationship("Order", back_populates="account")
    positions = relationship("Position", back_populates="account")
''')

# ─────────────────────────────────────────────
# 4. app/models/order.py
# ─────────────────────────────────────────────
write("app/models/order.py", '''
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    symbol = Column(String, nullable=False)
    side = Column(String, nullable=False)       # BUY / SELL
    order_type = Column(String, nullable=False) # MARKET / LIMIT
    quantity = Column(Float, nullable=False)
    price = Column(Float, nullable=True)
    status = Column(String, default="NEW")
    created_at = Column(DateTime, default=datetime.utcnow)
    account = relationship("Account", back_populates="orders")
''')

# ─────────────────────────────────────────────
# 5. app/models/position.py
# ─────────────────────────────────────────────
write("app/models/position.py", '''
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    symbol = Column(String, nullable=False)
    quantity = Column(Float, default=0.0)
    avg_price = Column(Float, default=0.0)
    updated_at = Column(DateTime, default=datetime.utcnow)
    account = relationship("Account", back_populates="positions")
''')

# ─────────────────────────────────────────────
# 6. app/models/agent_log.py
# ─────────────────────────────────────────────
write("app/models/agent_log.py", '''
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base

class AgentLog(Base):
    __tablename__ = "agent_logs"
    id = Column(Integer, primary_key=True, index=True)
    agent_id = Column(String, nullable=False)
    agent_type = Column(String, nullable=False)  # red / blue / institutional / retail_a / retail_b
    action = Column(String, nullable=False)
    result = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
''')

# ─────────────────────────────────────────────
# 7. app/models/security_event.py
# ─────────────────────────────────────────────
write("app/models/security_event.py", '''
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
from app.database import Base

class SecurityEvent(Base):
    __tablename__ = "security_events"
    id = Column(Integer, primary_key=True, index=True)
    event_type = Column(String, nullable=False)   # ATTACK / DEFENSE / ANOMALY
    severity = Column(String, nullable=False)     # LOW / MEDIUM / HIGH / CRITICAL
    source = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
''')

# ─────────────────────────────────────────────
# 8. app/models/__init__.py
# ─────────────────────────────────────────────
write("app/models/__init__.py", '''
from app.models.user import User
from app.models.account import Account
from app.models.order import Order
from app.models.position import Position
from app.models.agent_log import AgentLog
from app.models.security_event import SecurityEvent
''')

# ─────────────────────────────────────────────
# 9. app/schemas/user.py
# ─────────────────────────────────────────────
write("app/schemas/user.py", '''
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    created_at: datetime
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    username: str
    password: str
''')

# ─────────────────────────────────────────────
# 10. app/schemas/account.py
# ─────────────────────────────────────────────
write("app/schemas/account.py", '''
from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

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
    id: int
    name: str
    currency: str
    initial_balance: float
    current_balance: float
    created_at: datetime
    class Config:
        from_attributes = True
''')

# ─────────────────────────────────────────────
# 11. app/schemas/order.py
# ─────────────────────────────────────────────
write("app/schemas/order.py", '''
from pydantic import BaseModel, field_validator
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
    id: int
    account_id: int
    symbol: str
    side: str
    order_type: str
    quantity: float
    price: Optional[float]
    status: str
    created_at: datetime
    class Config:
        from_attributes = True
''')

# ─────────────────────────────────────────────
# 12. app/schemas/position.py
# ─────────────────────────────────────────────
write("app/schemas/position.py", '''
from pydantic import BaseModel
from datetime import datetime

class PositionResponse(BaseModel):
    id: int
    account_id: int
    symbol: str
    quantity: float
    avg_price: float
    updated_at: datetime
    class Config:
        from_attributes = True
''')

# ─────────────────────────────────────────────
# 13. app/schemas/agent_log.py
# ─────────────────────────────────────────────
write("app/schemas/agent_log.py", '''
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AgentLogCreate(BaseModel):
    agent_id: str
    agent_type: str
    action: str
    result: Optional[str] = None

class AgentLogResponse(BaseModel):
    id: int
    agent_id: str
    agent_type: str
    action: str
    result: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True
''')

# ─────────────────────────────────────────────
# 14. app/schemas/security_event.py
# ─────────────────────────────────────────────
write("app/schemas/security_event.py", '''
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class SecurityEventCreate(BaseModel):
    event_type: str
    severity: str
    source: Optional[str] = None
    description: Optional[str] = None

class SecurityEventResponse(BaseModel):
    id: int
    event_type: str
    severity: str
    source: Optional[str]
    description: Optional[str]
    created_at: datetime
    class Config:
        from_attributes = True
''')

# ─────────────────────────────────────────────
# 15. app/services/user_service.py
# ─────────────────────────────────────────────
write("app/services/user_service.py", '''
from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token

def create_user(db: Session, data: UserCreate) -> User:
    if db.query(User).filter(User.username == data.username).first():
        raise HTTPException(status_code=400, detail="Username already exists")
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status_code=400, detail="Email already exists")
    user = User(
        username=data.username,
        email=data.email,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(User).filter(User.username == username).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}

def get_users(db: Session):
    return db.query(User).all()

def get_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def delete_user(db: Session, user_id: int):
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
''')

# ─────────────────────────────────────────────
# 16. app/services/accounts_service.py
# ─────────────────────────────────────────────
write("app/services/accounts_service.py", '''
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.account import Account
from app.schemas.account import AccountCreate

def create_account(db: Session, data: AccountCreate) -> Account:
    account = Account(
        name=data.name,
        currency=data.currency,
        initial_balance=data.initial_balance,
        current_balance=data.initial_balance,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def get_accounts(db: Session):
    return db.query(Account).all()

def get_account(db: Session, account_id: int):
    account = db.query(Account).filter(Account.id == account_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account
''')

# ─────────────────────────────────────────────
# 17. app/services/orders_service.py
# ─────────────────────────────────────────────
write("app/services/orders_service.py", '''
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.order import Order
from app.models.account import Account
from app.schemas.order import OrderCreate

def create_order(db: Session, data: OrderCreate) -> Order:
    account = db.query(Account).filter(Account.id == data.account_id).first()
    if not account:
        raise HTTPException(status_code=400, detail=f"Account {data.account_id} does not exist")
    if data.order_type == "LIMIT" and (data.price is None or data.price <= 0):
        raise HTTPException(status_code=400, detail="Limit orders require a positive price")
    order = Order(
        account_id=data.account_id,
        symbol=data.symbol,
        side=data.side,
        order_type=data.order_type,
        quantity=data.quantity,
        price=data.price,
        status="NEW",
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def get_orders(db: Session):
    return db.query(Order).all()

def get_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order
''')

# ─────────────────────────────────────────────
# 18. app/services/positions_service.py
# ─────────────────────────────────────────────
write("app/services/positions_service.py", '''
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.position import Position

def get_positions(db: Session):
    return db.query(Position).all()

def get_position(db: Session, position_id: int):
    position = db.query(Position).filter(Position.id == position_id).first()
    if not position:
        raise HTTPException(status_code=404, detail="Position not found")
    return position
''')

# ─────────────────────────────────────────────
# 19. app/services/agent_log_service.py
# ─────────────────────────────────────────────
write("app/services/agent_log_service.py", '''
from sqlalchemy.orm import Session
from app.models.agent_log import AgentLog
from app.schemas.agent_log import AgentLogCreate

def create_agent_log(db: Session, data: AgentLogCreate) -> AgentLog:
    log = AgentLog(
        agent_id=data.agent_id,
        agent_type=data.agent_type,
        action=data.action,
        result=data.result,
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_agent_logs(db: Session):
    return db.query(AgentLog).all()
''')

# ─────────────────────────────────────────────
# 20. app/services/security_event_service.py
# ─────────────────────────────────────────────
write("app/services/security_event_service.py", '''
from sqlalchemy.orm import Session
from app.models.security_event import SecurityEvent
from app.schemas.security_event import SecurityEventCreate

def create_security_event(db: Session, data: SecurityEventCreate) -> SecurityEvent:
    event = SecurityEvent(
        event_type=data.event_type,
        severity=data.severity,
        source=data.source,
        description=data.description,
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

def get_security_events(db: Session):
    return db.query(SecurityEvent).all()
''')

# ─────────────────────────────────────────────
# 21. app/api/v1/__init__.py
# ─────────────────────────────────────────────
write("app/api/v1/__init__.py", "")

# ─────────────────────────────────────────────
# 22. app/api/v1/auth.py
# ─────────────────────────────────────────────
write("app/api/v1/auth.py", '''
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, Token, LoginRequest
from app.services.user_service import create_user, authenticate_user

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserResponse, status_code=201)
def register(data: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, data)

@router.post("/login", response_model=Token)
def login(data: LoginRequest, db: Session = Depends(get_db)):
    return authenticate_user(db, data.username, data.password)
''')

# ─────────────────────────────────────────────
# 23. app/api/v1/users.py
# ─────────────────────────────────────────────
write("app/api/v1/users.py", '''
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.user import UserResponse
from app.services.user_service import get_users, get_user, delete_user
from app.core.security import get_current_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=List[UserResponse])
def list_users(db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_users(db)

@router.get("/{user_id}", response_model=UserResponse)
def read_user(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    return get_user(db, user_id)

@router.delete("/{user_id}", status_code=204)
def remove_user(user_id: int, db: Session = Depends(get_db), _=Depends(get_current_user)):
    delete_user(db, user_id)
''')

# ─────────────────────────────────────────────
# 24. app/api/v1/accounts.py
# ─────────────────────────────────────────────
write("app/api/v1/accounts.py", '''
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.account import AccountCreate, AccountResponse
from app.services.accounts_service import create_account, get_accounts, get_account

router = APIRouter(prefix="/accounts", tags=["accounts"])

@router.get("/", response_model=List[AccountResponse])
def list_accounts(db: Session = Depends(get_db)):
    return get_accounts(db)

@router.post("/", response_model=AccountResponse, status_code=201)
def new_account(data: AccountCreate, db: Session = Depends(get_db)):
    return create_account(db, data)

@router.get("/{account_id}", response_model=AccountResponse)
def read_account(account_id: int, db: Session = Depends(get_db)):
    return get_account(db, account_id)
''')

# ─────────────────────────────────────────────
# 25. app/api/v1/orders.py
# ─────────────────────────────────────────────
write("app/api/v1/orders.py", '''
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.order import OrderCreate, OrderResponse
from app.services.orders_service import create_order, get_orders, get_order

router = APIRouter(prefix="/orders", tags=["orders"])

@router.get("/", response_model=List[OrderResponse])
def list_orders(db: Session = Depends(get_db)):
    return get_orders(db)

@router.post("/", response_model=OrderResponse, status_code=201)
def new_order(data: OrderCreate, db: Session = Depends(get_db)):
    return create_order(db, data)

@router.get("/{order_id}", response_model=OrderResponse)
def read_order(order_id: int, db: Session = Depends(get_db)):
    return get_order(db, order_id)
''')

# ─────────────────────────────────────────────
# 26. app/api/v1/positions.py
# ─────────────────────────────────────────────
write("app/api/v1/positions.py", '''
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.position import PositionResponse
from app.services.positions_service import get_positions, get_position

router = APIRouter(prefix="/positions", tags=["positions"])

@router.get("/", response_model=List[PositionResponse])
def list_positions(db: Session = Depends(get_db)):
    return get_positions(db)

@router.get("/{position_id}", response_model=PositionResponse)
def read_position(position_id: int, db: Session = Depends(get_db)):
    return get_position(db, position_id)
''')

# ─────────────────────────────────────────────
# 27. app/api/v1/agent_logs.py
# ─────────────────────────────────────────────
write("app/api/v1/agent_logs.py", '''
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.agent_log import AgentLogCreate, AgentLogResponse
from app.services.agent_log_service import create_agent_log, get_agent_logs

router = APIRouter(prefix="/agent-logs", tags=["agent-logs"])

@router.get("/", response_model=List[AgentLogResponse])
def list_logs(db: Session = Depends(get_db)):
    return get_agent_logs(db)

@router.post("/", response_model=AgentLogResponse, status_code=201)
def new_log(data: AgentLogCreate, db: Session = Depends(get_db)):
    return create_agent_log(db, data)
''')

# ─────────────────────────────────────────────
# 28. app/api/v1/security_events.py
# ─────────────────────────────────────────────
write("app/api/v1/security_events.py", '''
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.security_event import SecurityEventCreate, SecurityEventResponse
from app.services.security_event_service import create_security_event, get_security_events

router = APIRouter(prefix="/security-events", tags=["security-events"])

@router.get("/", response_model=List[SecurityEventResponse])
def list_events(db: Session = Depends(get_db)):
    return get_security_events(db)

@router.post("/", response_model=SecurityEventResponse, status_code=201)
def new_event(data: SecurityEventCreate, db: Session = Depends(get_db)):
    return create_security_event(db, data)
''')

# ─────────────────────────────────────────────
# 29. app/api/v1/health.py
# ─────────────────────────────────────────────
write("app/api/v1/health.py", '''
from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["health"])

@router.get("/")
def health_check():
    return {"status": "ok", "version": "1.0.0"}
''')

# ─────────────────────────────────────────────
# 30. app/database.py  (get_db 추가)
# ─────────────────────────────────────────────
write("app/database.py", '''
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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

# ─────────────────────────────────────────────
# 31. app/main.py  (완전 재구성)
# ─────────────────────────────────────────────
write("app/main.py", '''
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from app.api.v1 import auth, users, accounts, orders, positions, agent_logs, security_events, health

app = FastAPI(
    title="DevSecOps Trading Platform",
    version="1.0.0",
    description="DevSecOps Trading Platform Lab with Agentic AI",
    redirect_slashes=False,
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

@app.on_event("startup")
async def startup():
    init_db()
    print("[APP] DevSecOps Trading Platform v1.0.0 started")
''')

# ─────────────────────────────────────────────
# 32. requirements.txt 업데이트
# ─────────────────────────────────────────────
with open("requirements.txt", "w", encoding="utf-8") as f:
    f.write("""fastapi>=0.110.0
uvicorn>=0.29.0
sqlalchemy>=2.0.0
pydantic>=2.0.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
pykrx>=1.0.45
httpx>=0.27.0
pytest>=8.0.0
pytest-asyncio>=0.23.0
""")
print("  [OK] requirements.txt")
# ─────────────────────────────────────────────
# 33. tests/test_v1.py
# ─────────────────────────────────────────────
write("tests/test_v1.py", '''
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_health():
    r = client.get("/api/v1/health/")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_register():
    r = client.post("/api/v1/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "password123"
    })
    assert r.status_code == 201

def test_register_duplicate():
    client.post("/api/v1/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "password123"
    })
    r = client.post("/api/v1/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "password123"
    })
    assert r.status_code == 400

def test_login():
    client.post("/api/v1/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "password123"
    })
    r = client.post("/api/v1/auth/login", json={
        "username": "testuser", "password": "password123"
    })
    assert r.status_code == 200
    assert "access_token" in r.json()

def test_login_wrong_password():
    client.post("/api/v1/auth/register", json={
        "username": "testuser", "email": "test@test.com", "password": "password123"
    })
    r = client.post("/api/v1/auth/login", json={
        "username": "testuser", "password": "wrongpass"
    })
    assert r.status_code == 401

def test_create_account():
    r = client.post("/api/v1/accounts/", json={
        "name": "Test Account", "currency": "KRW", "initial_balance": 1000000
    })
    assert r.status_code == 201

def test_create_account_negative_balance():
    r = client.post("/api/v1/accounts/", json={
        "name": "Test", "currency": "KRW", "initial_balance": -1000
    })
    assert r.status_code == 422

def test_create_account_empty_name():
    r = client.post("/api/v1/accounts/", json={
        "name": "", "currency": "KRW", "initial_balance": 1000
    })
    assert r.status_code == 422

def test_list_accounts():
    client.post("/api/v1/accounts/", json={
        "name": "Account A", "currency": "KRW", "initial_balance": 500000
    })
    r = client.get("/api/v1/accounts/")
    assert r.status_code == 200
    assert len(r.json()) >= 1

def test_get_account_not_found():
    r = client.get("/api/v1/accounts/9999")
    assert r.status_code == 404

def test_create_order():
    acc = client.post("/api/v1/accounts/", json={
        "name": "Acc", "currency": "KRW", "initial_balance": 1000000
    }).json()
    r = client.post("/api/v1/orders/", json={
        "account_id": acc["id"],
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 10,
        "price": 75000
    })
    assert r.status_code == 201

def test_create_order_invalid_account():
    r = client.post("/api/v1/orders/", json={
        "account_id": 9999,
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 10,
        "price": 75000
    })
    assert r.status_code == 400

def test_create_order_limit_no_price():
    acc = client.post("/api/v1/accounts/", json={
        "name": "Acc", "currency": "KRW", "initial_balance": 1000000
    }).json()
    r = client.post("/api/v1/orders/", json={
        "account_id": acc["id"],
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 10
    })
    assert r.status_code == 400

def test_create_order_zero_quantity():
    acc = client.post("/api/v1/accounts/", json={
        "name": "Acc", "currency": "KRW", "initial_balance": 1000000
    }).json()
    r = client.post("/api/v1/orders/", json={
        "account_id": acc["id"],
        "symbol": "005930",
        "side": "BUY",
        "order_type": "MARKET",
        "quantity": 0
    })
    assert r.status_code == 422

def test_create_order_invalid_side():
    acc = client.post("/api/v1/accounts/", json={
        "name": "Acc", "currency": "KRW", "initial_balance": 1000000
    }).json()
    r = client.post("/api/v1/orders/", json={
        "account_id": acc["id"],
        "symbol": "005930",
        "side": "HOLD",
        "order_type": "MARKET",
        "quantity": 10
    })
    assert r.status_code == 422

def test_list_orders():
    r = client.get("/api/v1/orders/")
    assert r.status_code == 200

def test_get_order_not_found():
    r = client.get("/api/v1/orders/9999")
    assert r.status_code == 404

def test_list_positions():
    r = client.get("/api/v1/positions/")
    assert r.status_code == 200

def test_get_position_not_found():
    r = client.get("/api/v1/positions/9999")
    assert r.status_code == 404

def test_create_agent_log():
    r = client.post("/api/v1/agent-logs/", json={
        "agent_id": "red-001",
        "agent_type": "red",
        "action": "A03_SQL_INJECTION",
        "result": "success"
    })
    assert r.status_code == 201

def test_list_agent_logs():
    r = client.get("/api/v1/agent-logs/")
    assert r.status_code == 200

def test_create_security_event():
    r = client.post("/api/v1/security-events/", json={
        "event_type": "ATTACK",
        "severity": "HIGH",
        "source": "red-agent",
        "description": "SQL Injection detected"
    })
    assert r.status_code == 201

def test_list_security_events():
    r = client.get("/api/v1/security-events/")
    assert r.status_code == 200

def test_e2e_full_flow():
    reg = client.post("/api/v1/auth/register", json={
        "username": "e2euser", "email": "e2e@test.com", "password": "e2epass123"
    })
    assert reg.status_code == 201

    login = client.post("/api/v1/auth/login", json={
        "username": "e2euser", "password": "e2epass123"
    })
    assert login.status_code == 200

    acc = client.post("/api/v1/accounts/", json={
        "name": "E2E Account", "currency": "KRW", "initial_balance": 5000000
    })
    assert acc.status_code == 201

    order = client.post("/api/v1/orders/", json={
        "account_id": acc.json()["id"],
        "symbol": "005930",
        "side": "BUY",
        "order_type": "LIMIT",
        "quantity": 5,
        "price": 75000
    })
    assert order.status_code == 201
    assert order.json()["status"] == "NEW"
''')

print()
print("=" * 50)
print("✅ 전체 파일 생성 완료!")
print("=" * 50)
print()
print("다음 명령어를 순서대로 실행하세요:")
print("1. pip install -r requirements.txt")
print("2. pytest tests/test_v1.py -v")
print("3. uvicorn app.main:app --reload")
