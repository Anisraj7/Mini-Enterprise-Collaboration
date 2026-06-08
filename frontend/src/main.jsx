import "./index.css";
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";

import { Toaster } from "react-hot-toast";

import {
  AuthProvider,
} from "./components/AuthContext";

ReactDOM.createRoot(
  document.getElementById("root")
).render(
  <React.StrictMode>

    <Toaster position="top-right" />

    <AuthProvider>
      <App />
    </AuthProvider>

  </React.StrictMode>
);


