import { useEffect } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";
import API from "../api/axios";

export default function OAuthCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const accessToken = searchParams.get("access_token");
  const refreshToken = searchParams.get("refresh_token");
  const error = accessToken
    ? ""
    : "Google login did not return an access token.";

  useEffect(() => {
    if (!accessToken) {
      return;
    }

    localStorage.setItem("token", accessToken);
    if (refreshToken) {
      localStorage.setItem("refresh_token", refreshToken);
    }

    // Fetch user info to get role and organization_id
    const fetchUserAndRedirect = async () => {
      try {
        const response = await API.get("/auth/me");
        const user = response.data;

        localStorage.setItem("user", JSON.stringify(user));
        localStorage.setItem("role", user.role);

        if (user.role === "super_admin") {
          navigate("/organizations", { replace: true });
        } else if (user.role === "organization_admin") {
          navigate(`/organizations/${user.organization_id}`, { replace: true });
        } else {
          navigate("/dashboard", { replace: true });
        }
      } catch (err) {
        console.error("Failed to fetch user info:", err);
        navigate("/dashboard", { replace: true });
      }
    };

    fetchUserAndRedirect();
  }, [accessToken, refreshToken, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 px-4">
      <div className="bg-white p-6 rounded-xl shadow max-w-md w-full text-center">
        <h1 className="text-xl font-semibold text-gray-800 mb-2">
          Completing Google login
        </h1>
        {error ? (
          <>
            <p className="text-sm text-red-600 mb-4">{error}</p>
            <Link to="/" className="text-indigo-600 font-semibold">
              Back to login
            </Link>
          </>
        ) : (
          <p className="text-sm text-gray-500">
            Redirecting to your dashboard...
          </p>
        )}
      </div>
    </div>
  );
}
