import { useEffect, useMemo, useState } from "react";
import {
  createOrder,
  getMarketData,
  getOrders,
  getPositions,
} from "../api/client";

const DEFAULT_SYMBOL = "005930";

const fallbackMarket = {
  symbol: "005930",
  name: "삼성전자",
  price: 81200,
  change: 1200,
  change_rate: 1.5,
  volume: 15432021,
};

const fallbackOrders = [
  {
    id: 101,
    account_id: 1,
    symbol: "005930",
    side: "BUY",
    order_type: "LIMIT",
    price: 80500,
    quantity: 10,
    status: "FILLED",
  },
  {
    id: 102,
    account_id: 1,
    symbol: "000660",
    side: "SELL",
    order_type: "MARKET",
    price: 0,
    quantity: 3,
    status: "PENDING",
  },
];

const fallbackPositions = [
  {
    id: 1,
    account_id: 1,
    symbol: "005930",
    quantity: 12,
    avg_price: 79800,
    updated_at: "2026-06-21T15:39:35.394Z",
  },
  {
    id: 2,
    account_id: 1,
    symbol: "000660",
    quantity: 3,
    avg_price: 221000,
    updated_at: "2026-06-21T15:39:35.394Z",
  },
];

export default function TradePage() {
  const [symbol, setSymbol] = useState(DEFAULT_SYMBOL);
  const [market, setMarket] = useState(null);
  const [orders, setOrders] = useState([]);
  const [positions, setPositions] = useState([]);

  const [marketLoading, setMarketLoading] = useState(true);
  const [ordersLoading, setOrdersLoading] = useState(true);
  const [positionLoading, setPositionLoading] = useState(true);

  const [marketError, setMarketError] = useState("");
  const [orderError, setOrderError] = useState("");
  const [positionError, setPositionError] = useState("");
  const [submitMessage, setSubmitMessage] = useState("");

  const [form, setForm] = useState({
    account_id: 1,
    symbol: DEFAULT_SYMBOL,
    side: "BUY",
    order_type: "LIMIT",
    price: 0,
    quantity: 1,
  });

  const formatMoney = (value) => Number(value ?? 0).toLocaleString("ko-KR");
  const formatNumber = (value) => Number(value ?? 0).toLocaleString("ko-KR");

  const formatDateTime = (value) => {
    if (!value) return "-";
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return value;
    return date.toLocaleString("ko-KR");
  };

  const loadMarket = async (targetSymbol) => {
    try {
      setMarketLoading(true);
      setMarketError("");
      const data = await getMarketData(targetSymbol);
      setMarket(data || fallbackMarket);
    } catch (e) {
      console.error("market error:", e);
      setMarketError("시세 정보를 불러오지 못했습니다. 예시 데이터를 표시합니다.");
      setMarket({
        ...fallbackMarket,
        symbol: targetSymbol || fallbackMarket.symbol,
      });
    } finally {
      setMarketLoading(false);
    }
  };

  const loadOrders = async () => {
    try {
      setOrdersLoading(true);
      setOrderError("");
      const data = await getOrders();
      setOrders(Array.isArray(data) && data.length > 0 ? data : fallbackOrders);
    } catch (e) {
      console.error("orders error:", e);
      setOrderError("주문 내역을 불러오지 못했습니다. 예시 데이터를 표시합니다.");
      setOrders(fallbackOrders);
    } finally {
      setOrdersLoading(false);
    }
  };

  const loadPositions = async () => {
    try {
      setPositionLoading(true);
      setPositionError("");
      const data = await getPositions();
      setPositions(Array.isArray(data) ? data : []);
    } catch (e) {
      console.error("positions error:", e);
      setPositionError("보유 포지션을 불러오지 못했습니다. 예시 데이터를 표시합니다.");
      setPositions(fallbackPositions);
    } finally {
      setPositionLoading(false);
    }
  };

  useEffect(() => {
    loadMarket(DEFAULT_SYMBOL);
    loadOrders();
    loadPositions();
  }, []);

  const handleSearch = (e) => {
    e.preventDefault();
    const nextSymbol = form.symbol.trim();
    if (!nextSymbol) return;
    setSymbol(nextSymbol);
    loadMarket(nextSymbol);
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    setForm((prev) => ({
      ...prev,
      [name]:
        name === "account_id" || name === "price" || name === "quantity"
          ? Number(value)
          : value,
    }));
  };

  const handleOrderSubmit = async (e) => {
    e.preventDefault();

    if (!form.symbol.trim()) {
      setSubmitMessage("종목 코드를 입력해주세요.");
      return;
    }

    if (form.quantity <= 0) {
      setSubmitMessage("수량은 1 이상이어야 합니다.");
      return;
    }

    if (form.order_type === "LIMIT" && Number(form.price) <= 0) {
      setSubmitMessage("지정가 주문은 가격을 입력해야 합니다.");
      return;
    }

    try {
      setSubmitMessage("");

      const payload = {
        account_id: Number(form.account_id),
        symbol: form.symbol.trim(),
        side: form.side,
        order_type: form.order_type,
        price: form.order_type === "MARKET" ? 0 : Number(form.price),
        quantity: Number(form.quantity),
      };

      await createOrder(payload);
      setSubmitMessage("주문이 접수되었습니다.");
      await loadOrders();
      await loadPositions();
    } catch (e) {
      console.error("create order error:", e);
      setSubmitMessage(
        e?.response?.data?.detail || "주문 요청에 실패했습니다."
      );
    }
  };

  const estimatedAmount = useMemo(() => {
    const basePrice =
      form.order_type === "MARKET"
        ? Number(market?.price ?? 0)
        : Number(form.price ?? 0);

    return basePrice * Number(form.quantity ?? 0);
  }, [form.order_type, form.price, form.quantity, market]);

  const filteredPositions = useMemo(() => {
    return positions.filter(
      (item) => Number(item.account_id) === Number(form.account_id)
    );
  }, [positions, form.account_id]);

  return (
    <div className="page-shell">
      <section className="trade-layout">
        <div className="trade-main">
          <div className="market-panel">
            <div className="section-bar">
              <strong>시세 조회</strong>
              <span className="muted">{symbol}</span>
            </div>

            <form className="symbol-search" onSubmit={handleSearch}>
              <input
                name="symbol"
                value={form.symbol}
                onChange={handleChange}
                placeholder="예: 005930"
              />
              <button className="primary-btn" type="submit">
                조회
              </button>
            </form>

            {marketError && <p className="error-text page-error">{marketError}</p>}

            <div className="market-summary-card">
              <p className="eyebrow">현재 종목</p>
              <h1>{market?.name || "종목 정보"}</h1>
              <p className="muted">{market?.symbol || symbol}</p>

              <div className="price-box">
                <strong>
                  {marketLoading ? "불러오는 중..." : `${formatMoney(market?.price)}원`}
                </strong>
                <span
                  className={Number(market?.change ?? 0) >= 0 ? "up" : "down"}
                >
                  {Number(market?.change ?? 0) >= 0 ? "+" : ""}
                  {formatMoney(market?.change)}원 (
                  {Number(market?.change_rate ?? 0).toFixed(2)}%)
                </span>
              </div>

              <div className="summary-list">
                <div>
                  <span>거래량</span>
                  <strong>{formatNumber(market?.volume)}</strong>
                </div>
                <div>
                  <span>주문 기준 종목</span>
                  <strong>{form.symbol}</strong>
                </div>
              </div>
            </div>

            <div className="chart-placeholder-card">
              <div className="section-bar">
                <strong>차트 영역</strong>
                <span className="muted">다음 단계</span>
              </div>
              <div className="chart-placeholder-box">
                캔들 차트와 호가창을 여기에 연결합니다.
              </div>
            </div>
          </div>

          <div className="orders-panel">
            <div className="section-bar">
              <strong>주문 내역</strong>
              <span className="muted">
                {ordersLoading ? "불러오는 중..." : `${orders.length}건`}
              </span>
            </div>

            {orderError && <p className="error-text page-error">{orderError}</p>}

            <div className="orders-table-wrap">
              <table className="orders-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>종목</th>
                    <th>구분</th>
                    <th>유형</th>
                    <th>가격</th>
                    <th>수량</th>
                    <th>상태</th>
                  </tr>
                </thead>
                <tbody>
                  {orders.length === 0 ? (
                    <tr>
                      <td colSpan="7" className="empty-row">
                        주문 내역이 없습니다.
                      </td>
                    </tr>
                  ) : (
                    orders.map((order) => (
                      <tr key={order.id}>
                        <td>{order.id}</td>
                        <td>{order.symbol}</td>
                        <td className={order.side === "BUY" ? "up" : "down"}>
                          {order.side}
                        </td>
                        <td>{order.order_type}</td>
                        <td>
                          {Number(order.price) > 0
                            ? `${formatMoney(order.price)}원`
                            : "시장가"}
                        </td>
                        <td>{formatNumber(order.quantity)}</td>
                        <td>{order.status ?? "PENDING"}</td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        <aside className="trade-side">
          <div className="order-form-card">
            <div className="section-bar">
              <strong>주문 입력</strong>
              <span className="muted">활성 계좌 1개 기준</span>
            </div>

            <form className="order-form" onSubmit={handleOrderSubmit}>
              <label>계좌 ID</label>
              <input
                type="number"
                name="account_id"
                value={form.account_id}
                onChange={handleChange}
              />

              <label>종목 코드</label>
              <input
                name="symbol"
                value={form.symbol}
                onChange={handleChange}
              />

              <label>매수 / 매도</label>
              <select name="side" value={form.side} onChange={handleChange}>
                <option value="BUY">BUY</option>
                <option value="SELL">SELL</option>
              </select>

              <label>주문 유형</label>
              <select
                name="order_type"
                value={form.order_type}
                onChange={handleChange}
              >
                <option value="LIMIT">LIMIT</option>
                <option value="MARKET">MARKET</option>
              </select>

              <label>가격</label>
              <input
                type="number"
                name="price"
                value={form.price}
                onChange={handleChange}
                disabled={form.order_type === "MARKET"}
              />

              <label>수량</label>
              <input
                type="number"
                name="quantity"
                value={form.quantity}
                min="1"
                onChange={handleChange}
              />

              <div className="estimate-box">
                <span>예상 주문 금액</span>
                <strong>{formatMoney(estimatedAmount)}원</strong>
              </div>

              {submitMessage && <p className="error-text inline">{submitMessage}</p>}

              <button className="primary-btn" type="submit">
                주문 실행
              </button>
            </form>
          </div>

          <div className="position-card">
            <div className="section-bar">
              <strong>보유 포지션</strong>
              <span className="muted">
                {positionLoading ? "불러오는 중..." : `계좌 ${form.account_id}`}
              </span>
            </div>

            {positionError && (
              <p className="error-text page-error">{positionError}</p>
            )}

            <div className="position-body">
              {positionLoading ? (
                <p className="muted">불러오는 중...</p>
              ) : filteredPositions.length === 0 ? (
                <p className="muted">현재 계좌에 보유 포지션이 없습니다.</p>
              ) : (
                <div className="position-list">
                  {filteredPositions.map((item, idx) => (
                    <div
                      className="position-item"
                      key={item.id ?? `${item.account_id}-${item.symbol}-${idx}`}
                    >
                      <div className="position-head">
                        <strong>{item.symbol}</strong>
                        <span>{formatNumber(item.quantity)}주</span>
                      </div>

                      <div className="summary-list">
                        <div>
                          <span>계좌</span>
                          <strong>{item.account_id}</strong>
                        </div>
                        <div>
                          <span>평균 단가</span>
                          <strong>{formatMoney(item.avg_price)}원</strong>
                        </div>
                        <div>
                          <span>최종 갱신</span>
                          <strong>{formatDateTime(item.updated_at)}</strong>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </aside>
      </section>
    </div>
  );
}