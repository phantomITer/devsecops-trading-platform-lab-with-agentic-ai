import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";
import { useState } from "react";
import Header from "./components/Header";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import TradePage from "./pages/TradePage";
import MyPage from "./pages/MyPage";
import "./styles.css";
import { clearToken, getToken } from "./api/client";

function PrivateRoute({ isAuthed, children }) {
  if (!isAuthed) {
    return <Navigate to="/login" replace />;
  }
  return children;
}

export default function App() {
  const [auth, setAuth] = useState(() => {
    const token = getToken();
    return token ? { access_token: token } : null;
  });

  const handleLogin = (payload) => {
    setAuth(payload);
  };

  const handleLogout = () => {
    clearToken();
    setAuth(null);
  };

  return (
    <BrowserRouter>
      <div className="app-root">
        <Header isAuthed={!!auth} onLogout={handleLogout} />

        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/login" element={<LoginPage onLogin={handleLogin} />} />
          <Route
            path="/trade"
            element={
              <PrivateRoute isAuthed={!!auth}>
                <TradePage />
              </PrivateRoute>
            }
          />
          <Route
            path="/mypage"
            element={
              <PrivateRoute isAuthed={!!auth}>
                <MyPage />
              </PrivateRoute>
            }
          />
        </Routes>
      </div>
    </BrowserRouter>
  );
}