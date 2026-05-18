import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { FcGoogle } from "react-icons/fc";
import {
  FiMail,
  FiLock,
  FiEye,
  FiEyeOff,
} from "react-icons/fi";

import API from "../api/axios";

export default function Login() {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const [showPassword, setShowPassword] =
    useState(false);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const login = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    if (!email.trim()) {
      return setError("Email is required.");
    }

    if (!password.trim()) {
      return setError("Password is required.");
    }

    try {
      setLoading(true);

      const params = new URLSearchParams();

      params.append("username", email);
      params.append("password", password);

      const response = await API.post(
        "/auth/login",
        params,
        {
          headers: {
            "Content-Type":
              "application/x-www-form-urlencoded",
          },
        }
      );

      // Save tokens
      localStorage.setItem(
        "token",
        response.data.access_token
      );

      if (response.data.refresh_token) {
        localStorage.setItem(
          "refresh_token",
          response.data.refresh_token
        );
      }

      setSuccess("Login successful.");

      setTimeout(() => {
        navigate("/dashboard");
      }, 1000);
    } catch (err) {
      const detail = err.response?.data?.detail;

      let message = "Login failed.";

      if (typeof detail === "string") {
        message = detail;
      } else if (Array.isArray(detail)) {
        message = detail
          .map((item) => item?.msg || JSON.stringify(item))
          .join(". ");
      } else if (
        detail &&
        typeof detail === "object"
      ) {
        message =
          detail.msg || JSON.stringify(detail);
      }

      setError(message);
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = () => {
    const apiBaseUrl =
      import.meta.env.VITE_API_BASE_URL ||
      "http://127.0.0.1:8000";

    window.location.href = `${apiBaseUrl}/auth/google`;
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-700 via-blue-600 to-cyan-500 px-4 py-10 overflow-hidden relative">
      
      {/* Background Blur */}
      <div className="absolute w-96 h-96 bg-white/10 rounded-full blur-3xl top-[-80px] left-[-80px]" />

      <div className="absolute w-96 h-96 bg-cyan-300/20 rounded-full blur-3xl bottom-[-100px] right-[-100px]" />

      {/* Card */}
      <div className="relative z-10 w-full max-w-md">
        
        <div className="backdrop-blur-xl bg-white/90 border border-white/20 shadow-2xl rounded-3xl overflow-hidden">
          
          {/* Header */}
          <div className="px-8 pt-10 pb-6 text-center">
            
            <div className="w-20 h-20 mx-auto rounded-2xl bg-gradient-to-r from-indigo-600 to-cyan-500 flex items-center justify-center shadow-lg mb-5">
              <span className="text-white text-3xl font-bold">
                T
              </span>
            </div>

            <h1 className="text-3xl font-bold text-gray-800">
              Welcome Back
            </h1>

            <p className="text-gray-500 mt-2 text-sm">
              Login to access your workspace and tasks
            </p>
          </div>

          {/* Form */}
          <form
            onSubmit={login}
            className="px-8 pb-8"
          >
            
            {/* Error */}
            {error && (
              <div className="bg-red-100 border border-red-300 text-red-700 text-sm px-4 py-3 rounded-xl mb-5">
                {error}
              </div>
            )}

            {/* Success */}
            {success && (
              <div className="bg-green-100 border border-green-300 text-green-700 text-sm px-4 py-3 rounded-xl mb-5">
                {success}
              </div>
            )}

            {/* Email */}
            <div className="mb-5">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Email Address
              </label>

              <div className="relative">
                <FiMail className="absolute left-4 top-4 text-gray-400" />

                <input
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) =>
                    setEmail(e.target.value)
                  }
                  className="w-full border border-gray-300 rounded-xl py-3 pl-12 pr-4 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />
              </div>
            </div>

            {/* Password */}
            <div className="mb-3">
              <div className="flex items-center justify-between mb-2">
                <label className="text-sm font-semibold text-gray-700">
                  Password
                </label>

                <Link
                  to="/forgot-password"
                  className="text-xs text-indigo-600 hover:underline"
                >
                  Forgot Password?
                </Link>
              </div>

              <div className="relative">
                <FiLock className="absolute left-4 top-4 text-gray-400" />

                <input
                  type={
                    showPassword
                      ? "text"
                      : "password"
                  }
                  placeholder="Enter your password"
                  value={password}
                  onChange={(e) =>
                    setPassword(e.target.value)
                  }
                  className="w-full border border-gray-300 rounded-xl py-3 pl-12 pr-14 focus:outline-none focus:ring-2 focus:ring-indigo-500"
                />

                <button
                  type="button"
                  onClick={() =>
                    setShowPassword(!showPassword)
                  }
                  className="absolute right-4 top-3.5 text-gray-500 hover:text-indigo-600"
                >
                  {showPassword ? (
                    <FiEyeOff size={20} />
                  ) : (
                    <FiEye size={20} />
                  )}
                </button>
              </div>
            </div>

            {/* Remember */}
            <div className="flex items-center justify-between mb-6 mt-4">
              
              <label className="flex items-center gap-2 text-sm text-gray-600">
                <input
                  type="checkbox"
                  className="rounded border-gray-300"
                />

                Remember me
              </label>

              <span className="text-xs text-gray-400">
                Secure Login
              </span>
            </div>

            {/* Login Button */}
            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-indigo-600 to-cyan-500 hover:opacity-90 text-white py-3 rounded-xl font-semibold shadow-lg transition duration-300 disabled:opacity-70"
            >
              {loading
                ? "Signing In..."
                : "Sign In"}
            </button>

            {/* Divider */}
            <div className="flex items-center my-6">
              <div className="flex-1 h-px bg-gray-300"></div>

              <p className="px-4 text-sm text-gray-500">
                OR
              </p>

              <div className="flex-1 h-px bg-gray-300"></div>
            </div>

            {/* Google Login */}
            <button
              type="button"
              onClick={handleGoogleLogin}
              className="w-full flex items-center justify-center gap-3 border border-gray-300 bg-white py-3 rounded-xl hover:bg-gray-50 transition duration-300 shadow-sm"
            >
              <FcGoogle size={24} />

              <span className="font-medium text-gray-700">
                Continue with Google
              </span>
            </button>

            {/* Register */}
            <p className="text-center text-sm text-gray-600 mt-7">
              Don&apos;t have an account?{" "}

              <Link
                to="/register"
                className="text-indigo-600 font-semibold hover:underline"
              >
                Create Account
              </Link>
            </p>
          </form>
        </div>

        {/* Footer */}
        <p className="text-center text-white/80 text-xs mt-6">
          © 2026 TaskFlow. All rights reserved.
        </p>
      </div>
    </div>
  );
}