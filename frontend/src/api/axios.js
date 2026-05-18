import axios from "axios";

const API = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000"
});

function normalizeErrorDetail(error) {
  const detail = error.response?.data?.detail;

  if (typeof detail === "string") {
    return detail;
  }

  if (Array.isArray(detail)) {
    return detail
      .map((item) => {
        if (typeof item === "string") {
          return item;
        }
        if (item && typeof item === "object") {
          return item.msg || JSON.stringify(item);
        }
        return JSON.stringify(item);
      })
      .join(". ");
  }

  if (detail && typeof detail === "object") {
    return detail.msg || JSON.stringify(detail);
  }

  return undefined;
}

// Attach token automatically
API.interceptors.request.use((req) => {
  const token = localStorage.getItem("token");
  if (token) {
    req.headers.Authorization = `Bearer ${token}`;
  }
  return req;
});

API.interceptors.response.use(
  (response) => response,
  async (error) => {
    const normalizedDetail = normalizeErrorDetail(error);
    if (normalizedDetail) {
      if (!error.response) {
        error.response = { data: {} };
      }
      if (!error.response.data) {
        error.response.data = {};
      }
      error.response.data.detail = normalizedDetail;
    }

    const originalRequest = error.config;
    const refreshToken = localStorage.getItem("refresh_token");

    if (
      error.response?.status === 401 &&
      refreshToken &&
      !originalRequest._retry
    ) {
      originalRequest._retry = true;
      try {
        const response = await axios.post(
          `${API.defaults.baseURL}/auth/refresh`,
          {
            refresh_token: refreshToken,
          }
        );
        localStorage.setItem("token", response.data.access_token);
        originalRequest.headers.Authorization =
          `Bearer ${response.data.access_token}`;
        return API(originalRequest);
      } catch {
        localStorage.removeItem("token");
        localStorage.removeItem("refresh_token");
      }
    }

    return Promise.reject(error);
  }
);

export default API;
