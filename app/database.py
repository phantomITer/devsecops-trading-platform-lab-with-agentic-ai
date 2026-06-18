# app/database.py

from datetime import datetime, UTC
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# 1) 환경변수에서 DB 설정 읽기
# 기본은 sqlite, .env에서 DB_TYPE=mysql 로 바꾸면 MySQL 사용
DB_TYPE = os.getenv("DB_TYPE", "mysql")  # "sqlite" or "mysql"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "trading_platform")
DB_USER = os.getenv("DB_USER", "trading_user")
DB_PASS = os.getenv("DB_PASS", "trading_pass")

# 2) DB_TYPE에 따라 SQLAlchemy URL 구성
if DB_TYPE == "mysql":
    # Rocky01 Docker MySQL 용
    # requirements에 pymysql 추가 필요
    SQLALCHEMY_DATABASE_URL = (
        f"mysql+pymysql://{DB_USER}:{DB_PASS}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        pool_pre_ping=True,
    )
else:
    # 기본값: 로컬 SQLite (기존과 동일)
    # 파일 위치는 프로젝트 루트의 trading.db
    SQLALCHEMY_DATABASE_URL = "sqlite:///./trading.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    # 순환 참조 방지를 위해 함수 안에서 import
    from app.models import User, Account, Order, Position, AgentLog, SecurityEvent

    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()