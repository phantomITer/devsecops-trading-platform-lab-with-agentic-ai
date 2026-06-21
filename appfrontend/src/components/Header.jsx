import { Link, useNavigate } from "react-router-dom";

export default function Header({ isAuthed, onLogout }) {
  const navigate = useNavigate();

  return (
    <header className="site-header">
      <div className="header-left">
        <Link to="/" className="brand">
          DevSecOps Trading Platform With Agentic AI
        </Link>
      </div>

      <div className="header-right">
        <input
          className="search-input"
          placeholder="종목명 / 종목코드 검색"
        />

        {isAuthed ? (
          <>
            <button className="ghost-btn" onClick={() => navigate("/mypage")}>
              마이페이지
            </button>
            <button className="primary-btn small" onClick={onLogout}>
              로그아웃
            </button>
          </>
        ) : (
          <>
            <button className="ghost-btn" onClick={() => navigate("/signup")}>
              회원가입
            </button>
            <button
              className="primary-btn small"
              onClick={() => navigate("/login")}
            >
              로그인
            </button>
          </>
        )}
      </div>
    </header>
  );
}