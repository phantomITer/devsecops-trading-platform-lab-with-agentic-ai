# app/api/instruments.py

from typing import List, Optional
from fastapi import APIRouter, Query, HTTPException
import json
from pathlib import Path
from app.schemas.instruments import InstrumentOut

router = APIRouter(prefix="/instruments", tags=["instruments"])


# JSON 파일 경로 설정
DATA_FILE = Path(__file__).parent.parent.parent / "data" / "instruments.json"


def load_instruments():
    """JSON 파일에서 종목 데이터 로드"""
    with DATA_FILE.open(encoding="utf-8") as f:
        return json.load(f)


# 인메모리 데이터 (서버 시작 시 한 번 로드)
INSTRUMENTS_DATA = load_instruments()


@router.get("/", response_model=List[InstrumentOut])
def list_instruments(
    market: Optional[str] = Query(None, description="Market filter: KOSPI, KOSDAQ, US"),
    type: Optional[str] = Query(None, description="Type filter: STOCK, ETF"),
    q: Optional[str] = Query(None, description="Search keyword (symbol or name)"),
    offset: int = Query(0, ge=0, description="Page start index"),
    limit: int = Query(50, ge=1, le=200, description="Page size (max 200)"),
):
    """
    거래 가능한 종목 (주식/ETF) 목록을 조회합니다.

    - **market**: 시장 필터 (KOSPI, KOSDAQ, US)
    - **type**: 종목 유형 필터 (STOCK, ETF)
    - **q**: 검색 키워드 (종목명 또는 티커)
    - **offset**: 페이지 시작 인덱스 (default: 0)
    - **limit**: 페이지 크기 (default: 50, max: 200)
    """
    # 필터링
    items = INSTRUMENTS_DATA

    if market:
        items = [i for i in items if i["market"] == market]

    if type:
        items = [i for i in items if i["type"] == type]

    if q:
        q_lower = q.lower()
        items = [
            i
            for i in items
            if q_lower in i["symbol"].lower() or q_lower in i["name"].lower()
        ]

    # 페이징
    items = items[offset : offset + limit]

    return items

@router.get("/{symbol}")
def get_instrument(symbol: str):
    for item in INSTRUMENTS_DATA:
        if item["symbol"].upper() == symbol.upper():
            return item
    raise HTTPException(status_code=404, detail="Instrument not found")
