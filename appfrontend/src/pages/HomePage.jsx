import { useEffect, useState } from "react";
import { getTopStocks } from "../api/client";
import MarketTable from "../components/MarketTable";

const fallbackStocks = Array.from({ length: 30 }).map((_, idx) => ({
  rank: idx + 1,
  symbol: ["005930", "000660", "035420", "051910", "005380"][idx % 5] + idx,
  name: ["삼성전자", "SK하이닉스", "NAVER", "LG화학", "현대차"][idx % 5],
  price: 70000 + idx * 1300,
  change_rate: idx % 2 === 0 ? 1.2 + idx * 0.1 : -0.8 - idx * 0.05,
  trading_value: 1000000000 + idx * 100000000,
  market_cap: 50000000000 + idx * 2000000000,
}));

export default function HomePage() {
  const [stocks, setStocks] = useState([]);
  const [selectedStock, setSelectedStock] = useState(null);
  const [loading, setLoading] = useState(true);

  const formatPrice = (value) => Number(value ?? 0).toLocaleString("ko-KR");
  const formatRate = (value) => {
    const num = Number(value ?? 0);
    return `${num > 0 ? "+" : ""}${num.toFixed(2)}%`;
  };

  useEffect(() => {
    const fetchStocks = async () => {
      try {
        setLoading(true);
        const data = await getTopStocks();
        const list = Array.isArray(data) && data.length > 0 ? data : fallbackStocks;
        setStocks(list);
        setSelectedStock(list[0]);
      } catch (e) {
        console.error("top30 error:", e);
        setStocks(fallbackStocks);
        setSelectedStock(fallbackStocks[0]);
      } finally {
        setLoading(false);
      }
    };

    fetchStocks();
  }, []);

  return (
    <div className="page-shell">
      <section className="hero-strip hero-strip-single">
        <div className="hero-card hero-card-main">
          <p className="eyebrow">국내 시장</p>
          <h1>실시간 인기 종목 30</h1>
          <p className="muted">
            상위 30개 종목의 가격, 등락률, 거래대금, 시가총액을 확인합니다.
          </p>
        </div>
      </section>

      <section className="home-grid">
        <div className="home-main">
          <div className="section-bar">
            <div className="filter-tabs">
              <button className="active" type="button">전체</button>
              <button type="button">국내</button>
              <button type="button">해외</button>
              <button type="button">거래대금</button>
              <button type="button">등락률</button>
            </div>
            <span className="muted">
              {loading ? "불러오는 중..." : "30개 종목 표시"}
            </span>
          </div>

          <MarketTable stocks={stocks} onSelect={setSelectedStock} />
        </div>

        <aside className="side-panel">
          <div className="stock-summary-card">
            <p className="eyebrow">선택 종목</p>
            <h2>{selectedStock?.name ?? "-"}</h2>
            <p className="muted">{selectedStock?.symbol ?? "-"}</p>

            <div className="price-box">
              <strong>{formatPrice(selectedStock?.price)}원</strong>
              <span className={(selectedStock?.change_rate ?? 0) >= 0 ? "up" : "down"}>
                {formatRate(selectedStock?.change_rate)}
              </span>
            </div>

            <div className="mini-chart">미니 차트 영역</div>

            <div className="summary-list">
              <div>
                <span>거래대금</span>
                <strong>{formatPrice(selectedStock?.trading_value)}</strong>
              </div>
              <div>
                <span>시가총액</span>
                <strong>{formatPrice(selectedStock?.market_cap)}</strong>
              </div>
            </div>
          </div>
        </aside>
      </section>
    </div>
  );
}