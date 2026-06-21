import { useNavigate } from "react-router-dom";
import { useState } from "react";

export default function SignupPage() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    name: "",
    email: "",
    phone: "",
    broker: "mock-invest",
    password: "",
  });

  const handleChange = (e) => {
    setForm((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    alert("회원가입 API와 계좌 자동 생성 API 연결 예정");
    navigate("/login");
  };

  return (
    <div className="auth-page">
      <form className="auth-card" onSubmit={handleSubmit}>
        <p className="eyebrow">회원가입</p>
        <h1>기본 계좌를 바로 만드세요</h1>

        <label>이름</label>
        <input name="name" value={form.name} onChange={handleChange} />

        <label>이메일</label>
        <input name="email" value={form.email} onChange={handleChange} />

        <label>전화번호</label>
        <input name="phone" value={form.phone} onChange={handleChange} />

        <label>증권사</label>
        <select name="broker" value={form.broker} onChange={handleChange}>
          <option value="mock-invest">Mock Invest</option>
          <option value="blue-sec">Blue Securities</option>
          <option value="alpha-trade">Alpha Trade</option>
        </select>

        <label>비밀번호</label>
        <input
          type="password"
          name="password"
          value={form.password}
          onChange={handleChange}
        />

        <button className="primary-btn" type="submit">
          회원가입하고 계좌 만들기
        </button>
      </form>
    </div>
  );
}