# app/adapters/krx_fetcher.py

from pykrx import stock
from datetime import datetime, timedelta
from typing import Optional, List, Dict
import pandas as pd
import os
from app.core.config import settings


def _today() -> str:
    # 날짜만 필요할 때 (YYYYMMDD)
    return datetime.now().strftime("%Y%m%d")


def _now_ts() -> str:
    # 수집 시각 기록 용 (YYYY-MM-DDTHH:MM:SS)
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _prev_date(days: int = 1) -> str:
    return (datetime.now() - timedelta(days=days)).strftime("%Y%m%d")


def get_ticker_list(market: str = "KOSPI") -> List[Dict]:
    """
    KOSPI 또는 KOSDAQ 전체 종목 코드 + 이름 반환
    pykrx가 깨지는 날에는 빈 리스트 반환.
    """
    try:
        tickers = stock.get_market_ticker_list(market=market)
    except Exception as e:
        print(f"[WARN] get_market_ticker_list({market}) failed: {e}")
        return []

    result: List[Dict] = []
    for ticker in tickers:
        try:
            name = stock.get_market_ticker_name(ticker)
        except Exception as e:
            print(f"[WARN] get_market_ticker_name({ticker}) failed: {e}")
            name = None
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
) -> List[Dict]:
    """
    단일 종목 OHLCV 데이터 반환
    기본: 최근 30일
    """
    from_date = from_date or _prev_date(30)
    to_date   = to_date   or _today()

    try:
        df = stock.get_market_ohlcv(from_date, to_date, ticker)
    except Exception as e:
        print(f"[WARN] get_market_ohlcv({from_date}, {to_date}, {ticker}) failed: {e}")
        return []

    if df is None or df.empty:
        return []

    df = df.reset_index()
    df.columns = ["date", "open", "high", "low", "close", "volume", "turnover", "change"]
    df["ticker"] = ticker
    df["date"] = df["date"].astype(str)

    return df[["date", "ticker", "open", "high", "low", "close", "volume"]].to_dict("records")


def get_current_price(ticker: str) -> Optional[Dict]:
    """
    단일 종목 현재가 (당일 OHLCV 기준)
    updated_at: 우리가 시세를 조회한 시각 (YYYY-MM-DDTHH:MM:SS)
    """
    today = _today()
    try:
        df = stock.get_market_ohlcv(today, today, ticker)
    except Exception as e:
        print(f"[WARN] get_market_ohlcv({today}, {today}, {ticker}) failed: {e}")
        df = None

    if df is None or df.empty:
        # 장 마감 or 휴장이면 전일 데이터
        prev = _prev_date(1)
        try:
            df = stock.get_market_ohlcv(prev, prev, ticker)
        except Exception as e:
            print(f"[WARN] get_market_ohlcv({prev}, {prev}, {ticker}) failed: {e}")
            df = None

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
        "updated_at":  _now_ts(),  # ← 날짜+시간
    }


def get_market_snapshot(
    market: str = "KOSPI",
    top_n: int = 20,
) -> List[Dict]:
    """
    시가총액 상위 N개 종목 스냅샷 (pykrx 상태에 따라 실패 가능)
    실패 시 빈 리스트 반환.
    """
    today = _today()

    # 1) 오늘 날짜 시도
    try:
        df = stock.get_market_ohlcv_by_ticker(today, market=market)
    except Exception as e:
        print(f"[WARN] get_market_ohlcv_by_ticker({today}, {market}) failed: {e}")
        df = None

    # 2) 오늘 데이터가 없으면 전일로 fallback
    if df is None or df.empty:
        prev = _prev_date(1)
        try:
            df = stock.get_market_ohlcv_by_ticker(prev, market=market)
        except Exception as e:
            print(f"[WARN] get_market_ohlcv_by_ticker({prev}, {market}) failed: {e}")
            df = None

    if df is None or df.empty:
        print("[WARN] get_market_snapshot: empty dataframe for both today and previous day")
        return []

    # 3) 필요한 컬럼이 모두 있는지 검증
    required_cols = ["티커", "시가", "고가", "저가", "종가", "거래량"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"[WARN] get_market_snapshot: missing columns {missing}, columns={df.columns.tolist()}")
        return []

    # 4) 상위 N개 추출 (현재는 단순 head)
    df = df.head(top_n).reset_index(drop=True)

    result: List[Dict] = []
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