# app/adapters/krx_fetcher.py

from pykrx import stock
from datetime import datetime, timedelta
from typing import Optional
import pandas as pd
import os
from app.core.config import settings


def _today() -> str:
    return datetime.now().strftime("%Y%m%d")


def _prev_date(days: int = 1) -> str:
    return (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")


def get_ticker_list(market: str = "KOSPI") -> list[dict]:
    """
    KOSPI 또는 KOSDAQ 전체 종목 코드 + 이름 반환
    """
    tickers = stock.get_market_ticker_list(market=market)
    result = []
    for ticker in tickers:
        name = stock.get_market_ticker_name(ticker)
        result.append({
            "ticker": ticker,
            "name": name,
            "market": market,
        })
    return result


def get_ohlcv(
    ticker: str,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> list[dict]:
    """
    단일 종목 OHLCV 데이터 반환
    기본: 최근 30일
    """
    from_date = from_date or _prev_date(30)
    to_date   = to_date   or _today()

    df = stock.get_market_ohlcv(from_date, to_date, ticker)
    if df is None or df.empty:
        return []

    df = df.reset_index()
    df.columns = ["date", "open", "high", "low", "close", "volume", "turnover", "change"]
    df["ticker"] = ticker
    df["date"] = df["date"].astype(str)

    return df[["date", "ticker", "open", "high", "low", "close", "volume"]].to_dict("records")


def get_current_price(ticker: str) -> Optional[dict]:
    """
    단일 종목 현재가 (당일 OHLCV)
    """
    today = _today()
    df = stock.get_market_ohlcv(today, today, ticker)
    if df is None or df.empty:
        # 장 마감 or 휴장이면 전일 데이터
        df = stock.get_market_ohlcv(_prev_date(1), _prev_date(1), ticker)
    if df is None or df.empty:
        return None

    row = df.iloc[-1]
    return {
        "ticker":      ticker,
        "open_price":  float(row["시가"]),
        "high_price":  float(row["고가"]),
        "low_price":   float(row["저가"]),
        "close_price": float(row["종가"]),
        "volume":      int(row["거래량"]),
        "updated_at":  _today(),
    }


def get_market_snapshot(
    market: str = "KOSPI",
    top_n: int = 20
) -> list[dict]:
    """
    시가총액 상위 N개 종목 스냅샷
    대시보드 및 에이전트 시장 데이터용
    """
    today = _today()
    df = stock.get_market_ohlcv_by_ticker(today, market=market)
    if df is None or df.empty:
        df = stock.get_market_ohlcv_by_ticker(
            _prev_date(1), market=market
        )
    if df is None or df.empty:
        return []

    df = df.head(top_n).reset_index()
    result = []
    for _, row in df.iterrows():
        result.append({
            "ticker":      row["티커"],
            "open_price":  float(row["시가"]),
            "high_price":  float(row["고가"]),
            "low_price":   float(row["저가"]),
            "close_price": float(row["종가"]),
            "volume":      int(row["거래량"]),
        })
    return result