# app/api/v1/market_data.py

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.adapters.krx_fetcher import (
    get_current_price,
    get_ohlcv,
    get_market_snapshot,
    get_ticker_list,
)

router = APIRouter(prefix="/market-data", tags=["market-data"])


@router.get("/", summary="시장 스냅샷 조회")
def list_market_data(
    market: str = Query(default="KOSPI", description="KOSPI 또는 KOSDAQ"),
    top_n: int = Query(default=30, description="상위 N개 종목"),  # ← 30으로 수정
) -> list:
    """
    KOSPI/KOSDAQ 시가총액 상위 30개 종목 현재 시세 반환
    """
    result = get_market_snapshot(market=market, top_n=top_n)
    if not result:
        raise HTTPException(status_code=503, detail="KRX 시세 데이터를 가져올 수 없습니다.")
    return result


@router.get("/tickers", summary="전체 종목 코드 목록 조회")
def list_tickers(
    market: str = Query(default="KOSPI", description="KOSPI 또는 KOSDAQ"),
) -> list:
    """
    KOSPI/KOSDAQ 전체 종목 코드 + 이름 반환
    """
    result = get_ticker_list(market=market)
    if not result:
        raise HTTPException(status_code=503, detail="종목 목록을 가져올 수 없습니다.")
    return result


@router.get("/{symbol}", summary="단일 종목 현재가 조회")
def get_market_data(symbol: str) -> dict:
    """
    단일 종목 현재가 (당일 or 전일 종가)
    예: /api/v1/market-data/005930 → 삼성전자
    """
    result = get_current_price(symbol)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"종목 {symbol}의 시세 데이터를 찾을 수 없습니다."
        )
    return result


@router.get("/{symbol}/ohlcv", summary="단일 종목 OHLCV 조회")
def get_ohlcv_data(
    symbol: str,
    from_date: Optional[str] = Query(default=None, description="시작일 (YYYYMMDD)"),
    to_date: Optional[str] = Query(default=None, description="종료일 (YYYYMMDD)"),
) -> list:
    """
    단일 종목 OHLCV 데이터 (기본: 최근 30일)
    예: /api/v1/market-data/005930/ohlcv
    """
    result = get_ohlcv(ticker=symbol, from_date=from_date, to_date=to_date)
    if not result:
        raise HTTPException(
            status_code=404,
            detail=f"종목 {symbol}의 OHLCV 데이터를 찾을 수 없습니다."
        )
    return result