export default function MarketTable({ stocks = [], onSelect }) {
  const formatPrice = (value) => Number(value ?? 0).toLocaleString("ko-KR");

  const formatRate = (value) => {
    const num = Number(value ?? 0);
    return `${num > 0 ? "+" : ""}${num.toFixed(2)}%`;
  };

  return (
    <div className="market-table-wrap">
      <div className="market-table-head">
        <span>순위</span>
        <span>종목명</span>
        <span>현재가</span>
        <span>등락률</span>
        <span>거래대금</span>
        <span>시가총액</span>
      </div>

      {stocks.length === 0 ? (
        <div className="empty-panel">종목 데이터를 불러오지 못했습니다.</div>
      ) : (
        stocks.map((stock, index) => (
          <button
            key={stock.symbol ?? index}
            className="market-row"
            onClick={() => onSelect(stock)}
          >
            <span>{stock.rank ?? index + 1}</span>
            <span className="stock-name-cell">
              <strong>{stock.name}</strong>
              <small>{stock.symbol}</small>
            </span>
            <span>{formatPrice(stock.price)}</span>
            <span className={(stock.change_rate ?? 0) >= 0 ? "up" : "down"}>
              {formatRate(stock.change_rate)}
            </span>
            <span>{formatPrice(stock.trading_value)}</span>
            <span>{formatPrice(stock.market_cap)}</span>
          </button>
        ))
      )}
    </div>
  );
}