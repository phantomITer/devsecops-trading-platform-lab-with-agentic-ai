import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login } from "../api/client";

export default function LoginPage({ onLogin }) {
  const navigate = useNavigate();
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const handleChange = (e) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!form.username.trim() || !form.password.trim()) {
      setError("아이디와 비밀번호를 입력해주세요.");
      return;
    }

    try {
      setSubmitting(true);
      setError("");

      const result = await login({
        username: form.username.trim(),
        password: form.password,
      });

      onLogin(result);
      navigate("/trade");
    } catch (e) {
      console.error(e);
      setError(
        e?.response?.data?.detail || "로그인에 실패했습니다."
      );
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <p className="eyebrow">로그인</p>
        <h1>거래를 시작하세요</h1>

        <label htmlFor="username">아이디</label>
        <input
          id="username"
          name="username"
          value={form.username}
          onChange={handleChange}
          autoComplete="username"
        />

        <label htmlFor="password">비밀번호</label>
        <input
          id="password"
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
          autoComplete="current-password"
        />

        {error && <p className="error-text inline">{error}</p>}

        <button className="primary-btn" type="submit" disabled={submitting}>
          {submitting ? "로그인 중..." : "로그인"}
        </button>
      </form>
    </div>
  );
}