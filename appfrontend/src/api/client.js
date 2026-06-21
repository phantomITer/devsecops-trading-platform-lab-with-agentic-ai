import axios from "axios";

const api = axios.create({
  baseURL: "http://localhost:8000/api/v1",
});

const TOKEN_KEY = "trading_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  if (token) {
    localStorage.setItem(TOKEN_KEY, token);
  }
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

api.interceptors.request.use((config) => {
  const token = getToken();

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error?.response?.status === 401) {
      clearToken();
    }
    return Promise.reject(error);
  }
);

export async function login(payload) {
  const res = await api.post("/auth/login", payload);

  const token =
    res.data?.access_token ||
    res.data?.token ||
    res.data?.accessToken ||
    null;

  if (token) {
    setToken(token);
  }

  return res.data;
}

export async function getAccounts() {
  const res = await api.get("/accounts");
  return res.data;
}

export async function getOrders() {
  const res = await api.get("/orders");
  return res.data;
}

export async function createOrder(payload) {
  const res = await api.post("/orders", payload);
  return res.data;
}

export async function getMarketData(symbol) {
  const res = await api.get(`/market-data/${symbol}`);
  return res.data;
}


export async function getPositions() {
  const res = await api.get("/positions/");
  return res.data;
}

export async function getTopStocks() {
  const res = await api.get("/market-data/top30");
  return res.data;
}
