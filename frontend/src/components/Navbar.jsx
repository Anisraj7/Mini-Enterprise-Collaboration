// components/Navbar.jsx

import { useEffect, useState } from "react";

import { Bell } from "lucide-react";

import { useNavigate } from "react-router-dom";

import API from "../api/axios";

import NotificationPanel from "./NotificationPanel";

import NavMenu from "./navigation/NavMenu";

export default function Navbar() {
  const navigate = useNavigate();

  const [user, setUser] = useState(null);

  const [notificationsOpen, setNotificationsOpen] = useState(false);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const response = await API.get("/auth/me");

        setUser(response.data);
      } catch {
        navigate("/");
      }
    };

    loadUser();
  }, [navigate]);

  const logout = () => {
    localStorage.clear();

    navigate("/");
  };

  return (
    <nav
      className="
      sticky top-0 z-50
      bg-slate-700
      border-b border-white/10
    "
    >
      <div className="px-5 py-3">
        <div
          className="
          flex items-center
          justify-between
        "
        >
          <div
            className="cursor-pointer"
            onClick={() => {
              if (user?.role === "super_admin") {
                navigate("/organizations");
              } else {
                navigate("/dashboard");
              }
            }}
          >
            <div
              className="cursor-pointer"
              onClick={() => {
                if (user?.role === "super_admin") {
                  navigate("/organizations");
                } else {
                  navigate("/dashboard");
                }
              }}
            >
              <div className="flex flex-col">
                <h1
                  className="
        text-lg
        font-bold
        text-cyan-400
        leading-tight
      "
                >
                  {user?.organization_name ||
                    user?.organization?.name ||
                    (user?.role === "super_admin"
                      ? "Mini Enterprise Collaboration"
                      : "Organization")}
                </h1>

                <p
                  className="
        text-xs
        text-slate-300
      "
                >
                  {(user?.full_name || user?.name || user?.email || "").toUpperCase()}

                  {" • "}

                  {(user?.role || "").replaceAll("_", " ").toLowerCase()}
                </p>
              </div>
            </div>
          </div>

          <NavMenu user={user} />

          <div
            className="
            flex items-center
            gap-3
          "
          >
            <button onClick={() => setNotificationsOpen(!notificationsOpen)}>
              <Bell size={18} />
            </button>

            <button
              onClick={logout}
              className="
              px-3 py-2
              rounded-lg
              bg-red-500
              text-white
            "
            >
              Logout
            </button>
          </div>
        </div>
      </div>

      {notificationsOpen && <NotificationPanel />}
    </nav>
  );
}
