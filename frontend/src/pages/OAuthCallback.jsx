import { useEffect } from "react";
import { Link, useNavigate, useSearchParams } from "react-router-dom";

export default function OAuthCallback() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const accessToken = searchParams.get("access_token");
  const refreshToken = searchParams.get("refresh_token");
  const error = accessToken ? "" : "Google login did not return an access token.";

  useEffect(() => {
    if (!accessToken) {
      return;
    }

    localStorage.setItem("token", accessToken);
    if (refreshToken) {
      localStorage.setItem("refresh_token", refreshToken);
    }
    navigate("/dashboard", { replace: true });
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
          <p className="text-sm text-gray-500">Redirecting to your dashboard...</p>
        )}
      </div>
    </div>
  );
}
