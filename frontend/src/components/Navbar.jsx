import { useEffect, useState } from "react";

import {
  Bell,
  ClipboardCheck,
  LayoutDashboard,
  LogOut,
  Menu,
  ShieldCheck,
  Users,
  Workflow,
  Activity,
  PlusSquare,
  CreditCard,
  X,
} from "lucide-react";

import { Link, useLocation, useNavigate } from "react-router-dom";

import API from "../api/axios";
import { getPageItems } from "../api/pagination";
import NotificationPanel from "./NotificationPanel";

export default function Navbar() {
  const navigate = useNavigate();

  const location = useLocation();

  const [user, setUser] = useState(null);

  const [mobileMenu, setMobileMenu] = useState(false);

  const [notificationsCount, setNotificationsCount] = useState(0);

  const [notificationsOpen, setNotificationsOpen] = useState(false);

  // LOAD USER
  useEffect(() => {
    const loadUser = async () => {
      try {
        const response = await API.get("/auth/me");

        setUser(response.data);
      } catch {
        localStorage.removeItem("token");
        localStorage.removeItem("refresh_token");
        navigate("/");
      }
    };

    loadUser();
  }, [navigate]);

  // LOAD NOTIFICATIONS
  useEffect(() => {
    const loadNotifications = async () => {
      try {
        const response = await API.get("/notifications/");

        console.log("Notifications API Response:", response.data);

        // SAFE ARRAY EXTRACTION
        const notifications = getPageItems(response.data);

        const unread = notifications.filter((n) => !n.is_read).length;

        setNotificationsCount(unread);
      } catch (err) {
        console.log(err);

        setNotificationsCount(0);
      }
    };

    loadNotifications();
  }, []);

  // LOGOUT
  const logout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");

    navigate("/");
  };

  // NAV ITEMS
  const navItems = [
    {
      label: "Dashboard",
      path: "/dashboard",
      icon: LayoutDashboard,
      roles: ["admin", "manager", "employee"],
      color: "from-indigo-500 to-blue-500",
    },

    {
      label: "Kanban",
      path: "/kanban",
      icon: Workflow,
      roles: ["admin", "manager", "employee"],
      color: "from-purple-500 to-pink-500",
    },

    {
      label: "Approvals",
      path: "/approvals",
      icon: ClipboardCheck,
      roles: ["admin", "manager", "employee"],
      color: "from-emerald-500 to-green-500",
    },

    {
      label: "Activity",
      path: "/activity",
      icon: Activity,
      roles: ["admin", "manager"],
      color: "from-orange-500 to-amber-500",
    },

    {
      label: "Billing",
      path: "/billing",
      icon: CreditCard,
      roles: ["admin", "manager"],
      color: "from-violet-500 to-fuchsia-500",
    },

    {
      label: "Create",
      path: "/create-task",
      icon: PlusSquare,
      roles: ["admin", "manager"],
      color: "from-cyan-500 to-sky-500",
    },

    {
      label: "Users",
      path: "/users",
      icon: Users,
      roles: ["admin"],
      color: "from-rose-500 to-red-500",
    },

    {
      label: "Register",
      path: "/register",
      icon: ShieldCheck,
      roles: ["admin"],
      color: "from-yellow-500 to-orange-500",
    },
  ];

  return (
    <nav className="sticky top-0 z-50 bg-gradient-to-r from-slate-900 via-indigo-950 to-slate-900 border-b border-indigo-800 shadow-xl">
      <div className="max-w-[1800px] mx-auto px-5 py-3 flex justify-between items-center">
        {/* LEFT */}
        <div className="flex items-center gap-10">
          {/* LOGO */}
          <div
            className="cursor-pointer"
            onClick={() => {
              setNotificationsOpen(false);

              navigate("/dashboard");
            }}
          >
            <h1 className="text-3xl font-extrabold bg-gradient-to-r from-cyan-400 via-indigo-300 to-pink-400 bg-clip-text text-transparent tracking-wide">
              TaskFlow
            </h1>

            {user && (
              <p className="text-xs text-indigo-200 mt-1">
                Organization ?{" "}
                <span className="font-medium text-cyan-300">
                  {user.organization?.name}
                </span>
              </p>
            )}
          </div>

          {/* DESKTOP NAV */}
          <div className="hidden lg:flex items-center gap-3">
            {navItems
              .filter((item) => item.roles.includes(user?.role))
              .map((item) => {
                const Icon = item.icon;

                const isActive = location.pathname === item.path;

                return (
                  <Link
                    key={item.path}
                    to={item.path}
                    onClick={() => setNotificationsOpen(false)}
                    className={`
                      flex items-center gap-2 px-4 py-2 rounded-xl text-sm font-semibold transition-all duration-200
                      ${
                        isActive
                          ? `bg-gradient-to-r ${item.color} text-white shadow-lg scale-105`
                          : "bg-white/10 text-indigo-100 hover:bg-white/20 hover:text-white"
                      }
                    `}
                  >
                    <Icon size={16} />

                    {item.label}
                  </Link>
                );
              })}
          </div>
        </div>

        {/* RIGHT */}
        <div className="flex items-center gap-3">
          {/* NOTIFICATION */}
          <div className="relative">
            <button
              type="button"
              aria-label="Open notifications"
              aria-expanded={notificationsOpen}
              onClick={() => setNotificationsOpen((open) => !open)}
              className="relative bg-white/10 hover:bg-white/20 transition p-2.5 rounded-xl backdrop-blur-sm"
            >
              <Bell size={18} className="text-white" />

              {notificationsCount > 0 && (
                <span className="absolute -top-1 -right-1 bg-gradient-to-r from-red-500 to-pink-500 text-white text-[10px] w-5 h-5 flex items-center justify-center rounded-full font-bold shadow">
                  {notificationsCount}
                </span>
              )}
            </button>

            {notificationsOpen && (
              <div className="absolute right-0 top-full mt-3 w-[min(24rem,calc(100vw-2rem))] z-50">
                <NotificationPanel
                  onUnreadCountChange={setNotificationsCount}
                />
              </div>
            )}
          </div>

          {/* USER CARD */}
          <div className="relative hidden md:block group">
            <button
              className="
              flex items-center gap-3
              bg-white/10 hover:bg-white/20
              backdrop-blur-sm
              border border-white/10
              px-3 py-2
              rounded-2xl
              transition-all duration-200
    "
            >
              {/* AVATAR */}
              <div
                className="
                w-10 h-10 rounded-full
                bg-gradient-to-r from-cyan-400 to-indigo-500
                text-white flex items-center justify-center
                font-bold shadow-lg
              "
              >
                {user?.name?.charAt(0).toUpperCase()}
              </div>

              {/* USER INFO */}
              <div className="text-left">
                <p className="text-sm font-semibold capitalize text-white">
                  {user?.name}
                </p>

                <p className="text-xs text-indigo-200 capitalize">
                  {user?.role}
                </p>
              </div>
            </button>

            {/* DROPDOWN */}

            <div
              className="
            absolute  top-full 
            w-15
            bg-slate-900/95
            backdrop-blur-xl
            border border-white/10
            rounded-3xl
            shadow-2xl
            opacity-0 invisible
            translate-y-2
            group-hover:opacity-100
            group-hover:visible
            group-hover:translate-y-0
            transition-all duration-300
            overflow-hidden
            p-2
          "
            >
              {/* USER INFO */}
              {/* <div className="px-4 py-3 border-b border-white/10">

            <p className="text-white font-semibold text-sm">
              {user?.name}
            </p>

            <p className="text-indigo-300 text-xs capitalize mt-1">
              {user?.role}
            </p>

          </div> */}

              {/* LOGOUT */}
              <button
                onClick={logout}
                className="
              mt-2 ml-2
              w-[90%]
              flex items-center gap-2
              px-3 py-2
              rounded-xl
              text-red-400
              hover:bg-red-500/10
              hover:text-red-300
              transition-all duration-200
              text-sm font-medium
            "
              >
                <div
                  className="
              w-5 h-5 rounded-lg
              bg-red-500/20
              flex items-center justify-center
            "
                >
                  <LogOut size={15} />
                </div>

                <span>Logout</span>
              </button>
            </div>
          </div>

          {/* MOBILE BUTTON */}
          <button
            onClick={() => setMobileMenu(!mobileMenu)}
            className="lg:hidden bg-white/10 text-white p-2 rounded-xl"
          >
            {mobileMenu ? <X size={20} /> : <Menu size={20} />}
          </button>
        </div>
      </div>

      {/* MOBILE MENU */}
      {mobileMenu && (
        <div className="lg:hidden border-t border-indigo-800 bg-slate-900 px-4 py-4 space-y-3">
          {navItems
            .filter((item) => item.roles.includes(user?.role))
            .map((item) => {
              const Icon = item.icon;

              const isActive = location.pathname === item.path;

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() => setMobileMenu(false)}
                  className={`
                    flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-semibold transition-all
                    ${
                      isActive
                        ? `bg-gradient-to-r ${item.color} text-white`
                        : "bg-white/10 text-indigo-100 hover:bg-white/20"
                    }
                  `}
                >
                  <Icon size={18} />

                  {item.label}
                </Link>
              );
            })}

          <button
            onClick={logout}
            className="w-full mt-2 flex items-center justify-center gap-2 bg-gradient-to-r from-red-500 to-pink-500 text-white px-4 py-3 rounded-xl text-sm font-semibold shadow-lg"
          >
            <LogOut size={16} />
          </button>
        </div>
      )}
    </nav>
  );
}
