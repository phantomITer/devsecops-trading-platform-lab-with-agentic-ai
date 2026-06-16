# app/adapters/mock_generator.py

import random
import json
from datetime import datetime, timedelta
from pathlib import Path


MOCK_TICKERS = [
    {"ticker": "005930", "name": "삼성전자",   "base_price": 75000},
    {"ticker": "000660", "name": "SK하이닉스", "base_price": 180000},
    {"ticker": "035420", "name": "NAVER",      "base_price": 220000},
    {"ticker": "051910", "name": "LG화학",     "base_price": 350000},
    {"ticker": "006400", "name": "삼성SDI",    "base_price": 400000},
]


def _random_walk(base: float, volatility: float = 0.02) -> float:
    """랜덤 워크 가격 생성"""
    change = random.gauss(0, volatility)
    return round(base * (1 + change), 0)


def get_mock_ticker_list() -> list[dict]:
    return [
        {"ticker": t["ticker"], "name": t["name"], "market": "KOSPI"}
        for t in MOCK_TICKERS
    ]


def get_mock_current_price(ticker: str) -> dict:
    """Mock 현재가 생성"""
    target = next(
        (t for t in MOCK_TICKERS if t["ticker"] == ticker),
        MOCK_TICKERS[0]
    )
    base  = target["base_price"]
    close = _random_walk(base)
    high  = close * random.uniform(1.0, 1.03)
    low   = close * random.uniform(0.97, 1.0)
    open_ = _random_walk(base)

    return {
        "ticker":      ticker,
        "open_price":  round(open_, 0),
        "high_price":  round(high, 0),
        "low_price":   round(low, 0),
        "close_price": round(close, 0),
        "volume":      random.randint(100_000, 10_000_000),
        "updated_at":  datetime.now().isoformat(),
    }


def get_mock_market_snapshot() -> list[dict]:
    """Mock 전체 종목 스냅샷"""
    return [
        get_mock_current_price(t["ticker"])
        for t in MOCK_TICKERS
    ]


def get_mock_ohlcv(ticker: str, days: int = 30) -> list[dict]:
    """Mock OHLCV 히스토리 생성"""
    target = next(
        (t for t in MOCK_TICKERS if t["ticker"] == ticker),
        MOCK_TICKERS[0]
    )
    base   = target["base_price"]
    result = []

    for i in range(days, 0, -1):
        date  = (datetime.now() - timedelta(days=i)).strftime("%Y%m%d")
        close = _random_walk(base, 0.015)
        high  = close * random.uniform(1.0, 1.02)
        low   = close * random.uniform(0.98, 1.0)
        open_ = _random_walk(close, 0.01)
        base  = close  # 다음 날 기준가

        result.append({
            "date":        date,
            "ticker":      ticker,
            "open":        round(open_, 0),
            "high":        round(high, 0),
            "low":         round(low, 0),
            "close":       round(close, 0),
            "volume":      random.randint(100_000, 10_000_000),
        })
    return result