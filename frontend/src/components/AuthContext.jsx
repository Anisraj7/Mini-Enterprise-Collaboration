import {
  useEffect,
  useState,
} from "react";

import { AuthContext } from "./authContextValue";

import {
  getMe,
  login as loginService,
} from "../services/auth/authService";

export function AuthProvider({
  children,
}) {
  const [user, setUser] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const [isAuthenticated, setIsAuthenticated] =
    useState(false);

  const loadUser = async () => {
    try {
      const token =
        localStorage.getItem("token");

      if (!token) {
        setUser(null);
        setIsAuthenticated(false);
        return;
      }

      const currentUser =
        await getMe();

      localStorage.setItem(
        "user",
        JSON.stringify(currentUser)
      );

      localStorage.setItem(
        "role",
        currentUser.role
      );

      setUser(currentUser);
      setIsAuthenticated(true);
    } catch (error) {
      console.error(error);

      localStorage.removeItem("token");
      localStorage.removeItem("refresh_token");
      localStorage.removeItem("user");
      localStorage.removeItem("role");

      setUser(null);
      setIsAuthenticated(false);
    }
  };

  const login = async (
    email,
    password
  ) => {
    const data =
      await loginService(
        email,
        password
      );

    localStorage.setItem(
      "token",
      data.access_token
    );

    if (data.refresh_token) {
      localStorage.setItem(
        "refresh_token",
        data.refresh_token
      );
    }

    await loadUser();

    return data;
  };

  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    localStorage.removeItem("role");

    setUser(null);
    setIsAuthenticated(false);
  };

  useEffect(() => {
    const initialize = async () => {
      await loadUser();
      setLoading(false);
    };

    initialize();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        loading,
        isAuthenticated,
        login,
        logout,
        loadUser,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}
