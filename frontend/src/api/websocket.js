import API from "./axios";

export function getUserWebSocketUrl(userId) {
  const apiUrl = new URL(API.defaults.baseURL);

  apiUrl.protocol = apiUrl.protocol === "https:" ? "wss:" : "ws:";
  apiUrl.pathname = `/ws/${userId}`;
  apiUrl.search = "";
  apiUrl.hash = "";

  return apiUrl.toString();
}
