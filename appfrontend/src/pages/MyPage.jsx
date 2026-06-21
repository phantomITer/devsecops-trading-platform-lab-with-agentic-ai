import { useEffect, useMemo, useState } from "react";
import { getAccounts } from "../api/client";

const fallbackAccounts = [
  {
    id: 1,
    name: "기본 투자 계좌",
    currency: "KRW",
    initial_balance: 10000000,
    current_balance: 10425000,
  },
  {
    id: 2,
    name: "단기 매매 계좌",
    currency: "KRW",
    initial_balance: 5000000,
    current_balance: 4875000,
  },
];

export default function MyPage() {
  const [accounts, setAccounts] = useState([]);
  const [selectedAccountId, setSelectedAccountId] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const formatMoney = (value) => Number(value ?? 0).toLocaleString("ko-KR");

  useEffect(() => {
    const fetchAccounts = async () => {
      try {
        setLoading(true);
        setError("");

        const data = await getAccounts();
        const list = Array.isArray(data) && data.length > 0 ? data : fallbackAccounts;

        setAccounts(list);
        setSelectedAccountId(list[0]?.id ?? null);
      } catch (e) {
        console.error("accounts error:", e);
        setError("계좌 정보를 불러오지 못했습니다. 예시 데이터를 표시합니다.");
        setAccounts(fallbackAccounts);
        setSelectedAccountId(fallbackAccounts[0]?.id ?? null);
      } finally {
        setLoading(false);
      }
    };

    fetchAccounts();
  }, []);

  const selectedAccount = useMemo(() => {
    return accounts.find((account) => account.id === selectedAccountId) ?? null;
  }, [accounts, selectedAccountId]);

  const totalCurrentBalance = useMemo(() => {
    return accounts.reduce(
      (sum, account) => sum + Number(account.current_balance ?? 0),
      0
    );
  }, [accounts]);

  const totalInitialBalance = useMemo(() => {
    return accounts.reduce(
      (sum, account) => sum + Number(account.initial_balance ?? 0),
      0
    );
  }, [accounts]);

  const totalProfit = totalCurrentBalance - totalInitialBalance;
  const totalProfitRate =
    totalInitialBalance > 0 ? (totalProfit / totalInitialBalance) * 100 : 0;

  return (
    <div className="page-shell">
      <section className="hero-strip hero-strip-single">
        <div className="hero-card hero-card-main">
          <p className="eyebrow">내 자산</p>
          <h1>마이페이지</h1>
          <p className="muted">
            계좌 목록, 현재 잔액, 초기 자산 대비 손익을 확인합니다.
          </p>
        </div>
      </section>

      <section className="mypage-grid">
        <div className="home-main">
          <div className="section-bar">
            <strong>내 계좌 목록</strong>
            <span className="muted">
              {loading ? "불러오는 중..." : `${accounts.length}개 계좌`}
            </span>
          </div>

          {error && <p className="error-text page-error">{error}</p>}

          <div className="account-list-wrap">
            {accounts.length === 0 ? (
              <div className="empty-panel">표시할 계좌가 없습니다.</div>
            ) : (
              accounts.map((account) => {
                const profit =
                  Number(account.current_balance ?? 0) -
                  Number(account.initial_balance ?? 0);
                const profitRate =
                  Number(account.initial_balance ?? 0) > 0
                    ? (profit / Number(account.initial_balance ?? 0)) * 100
                    : 0;

                return (
                  <button
                    key={account.id}
                    type="button"
                    className={`account-card ${
                      selectedAccountId === account.id ? "active" : ""
                    }`}
                    onClick={() => setSelectedAccountId(account.id)}
                  >
                    <div className="account-card-top">
                      <div>
                        <p className="eyebrow">계좌 #{account.id}</p>
                        <h3>{account.name}</h3>
                      </div>
                      <span className="account-currency">
                        {account.currency ?? "KRW"}
                      </span>
                    </div>

                    <div className="account-balance">
                      <strong>{formatMoney(account.current_balance)}원</strong>
                      <span className={profit >= 0 ? "up" : "down"}>
                        {profit >= 0 ? "+" : ""}
                        {formatMoney(profit)}원 ({profitRate.toFixed(2)}%)
                      </span>
                    </div>

                    <div className="account-meta">
                      <span>초기 자산 {formatMoney(account.initial_balance)}원</span>
                    </div>
                  </button>
                );
              })
            )}
          </div>
        </div>

        <aside className="side-panel">
          <div className="stock-summary-card">
            <p className="eyebrow">자산 요약</p>
            <h2>{selectedAccount?.name ?? "계좌 선택"}</h2>
            <p className="muted">
              {selectedAccount
                ? `계좌 번호 ${selectedAccount.id} · ${selectedAccount.currency ?? "KRW"}`
                : "선택된 계좌가 없습니다."}
            </p>

            <div className="price-box">
              <strong>{formatMoney(selectedAccount?.current_balance)}원</strong>
              <span className={totalProfit >= 0 ? "up" : "down"}>
                {totalProfit >= 0 ? "+" : ""}
                {totalProfitRate.toFixed(2)}%
              </span>
            </div>

            <div className="summary-list">
              <div>
                <span>총 초기 자산</span>
                <strong>{formatMoney(totalInitialBalance)}원</strong>
              </div>
              <div>
                <span>총 현재 자산</span>
                <strong>{formatMoney(totalCurrentBalance)}원</strong>
              </div>
              <div>
                <span>총 손익</span>
                <strong className={totalProfit >= 0 ? "up" : "down"}>
                  {totalProfit >= 0 ? "+" : ""}
                  {formatMoney(totalProfit)}원
                </strong>
              </div>
              <div>
                <span>선택 계좌 초기 자산</span>
                <strong>
                  {formatMoney(selectedAccount?.initial_balance)}원
                </strong>
              </div>
            </div>
          </div>
        </aside>
      </section>
    </div>
  );
}