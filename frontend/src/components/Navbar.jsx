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
  X,
} from "lucide-react";

import {
  Link,
  useLocation,
  useNavigate,
} from "react-router-dom";

import API from "../api/axios";

export default function Navbar() {

  const navigate = useNavigate();

  const location = useLocation();

  const [user, setUser] =
    useState(null);

  const [mobileMenu, setMobileMenu] =
    useState(false);

  const [notificationsCount, setNotificationsCount] =
    useState(0);

  // LOAD USER
  useEffect(() => {

    const loadUser = async () => {

      try {

        const response = await API.get(
          "/auth/me"
        );

        setUser(response.data);

      } catch {

        localStorage.removeItem("token");

        navigate("/");
      }
    };

    loadUser();

  }, [navigate]);

  // LOAD NOTIFICATIONS
  useEffect(() => {

    const loadNotifications = async () => {

      try {

        const response = await API.get(
          "/notifications/"
        );

        const unread =
          response.data.filter(
            (n) => !n.is_read
          ).length;

        setNotificationsCount(unread);

      } catch (err) {

        console.log(err);
      }
    };

    loadNotifications();

  }, []);

  // LOGOUT
  const logout = () => {

    localStorage.removeItem("token");

    navigate("/");
  };

  // NAV ITEMS
  const navItems = [

    {
      label: "Dashboard",
      path: "/dashboard",
      icon: LayoutDashboard,
      roles: ["admin", "manager", "employee"],
      color:
        "from-indigo-500 to-blue-500",
    },

    {
      label: "Kanban",
      path: "/kanban",
      icon: Workflow,
      roles: ["admin", "manager", "employee"],
      color:
        "from-purple-500 to-pink-500",
    },

    {
      label: "Approvals",
      path: "/approvals",
      icon: ClipboardCheck,
      roles: ["admin", "manager"],
      color:
        "from-emerald-500 to-green-500",
    },

    {
      label: "Activity",
      path: "/activity",
      icon: Activity,
      roles: ["admin", "manager"],
      color:
        "from-orange-500 to-amber-500",
    },

    {
      label: "Create",
      path: "/create-task",
      icon: PlusSquare,
      roles: ["admin", "manager"],
      color:
        "from-cyan-500 to-sky-500",
    },

    {
      label: "Users",
      path: "/users",
      icon: Users,
      roles: ["admin"],
      color:
        "from-rose-500 to-red-500",
    },

    {
      label: "Register",
      path: "/register",
      icon: ShieldCheck,
      roles: ["admin"],
      color:
        "from-yellow-500 to-orange-500",
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
            onClick={() =>
              navigate("/dashboard")
            }
          >

            <h1 className="text-3xl font-extrabold bg-gradient-to-r from-cyan-400 via-indigo-300 to-pink-400 bg-clip-text text-transparent tracking-wide">
              TaskFlow
            </h1>

            {user && (

              <p className="text-xs text-indigo-200 mt-1">

                {user.name}
                {" • "}

                <span className="capitalize font-medium">
                  {user.role}
                </span>

              </p>

            )}

          </div>

          {/* DESKTOP NAV */}
          <div className="hidden lg:flex items-center gap-3">

            {navItems
              .filter((item) =>
                item.roles.includes(
                  user?.role
                )
              )
              .map((item) => {

                const Icon =
                  item.icon;

                const isActive =
                  location.pathname ===
                  item.path;

                return (

                  <Link
                    key={item.path}
                    to={item.path}
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
          <button
            className="relative bg-white/10 hover:bg-white/20 transition p-2.5 rounded-xl backdrop-blur-sm"
          >

            <Bell
              size={18}
              className="text-white"
            />

            {notificationsCount > 0 && (

              <span className="absolute -top-1 -right-1 bg-gradient-to-r from-red-500 to-pink-500 text-white text-[10px] w-5 h-5 flex items-center justify-center rounded-full font-bold shadow">

                {notificationsCount}

              </span>

            )}

          </button>

          {/* USER CARD */}
          <div className="hidden md:flex items-center gap-3 bg-white/10 backdrop-blur-sm border border-white/10 px-3 py-2 rounded-2xl">

            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-cyan-400 to-indigo-500 text-white flex items-center justify-center font-bold shadow-lg">

              {user?.name?.charAt(0)}

            </div>

            <div>

              <p className="text-sm font-semibold text-white">
                {user?.name}
              </p>

              <p className="text-xs text-indigo-200 capitalize">
                {user?.role}
              </p>

            </div>

          </div>

          {/* LOGOUT */}
          <button
            onClick={logout}
            className="hidden md:flex items-center gap-2 bg-gradient-to-r from-red-500 to-pink-500 hover:scale-105 text-white px-4 py-2 rounded-xl text-sm font-semibold transition-all shadow-lg"
          >

            <LogOut size={16} />

            Logout

          </button>

          {/* MOBILE BUTTON */}
          <button
            onClick={() =>
              setMobileMenu(
                !mobileMenu
              )
            }
            className="lg:hidden bg-white/10 text-white p-2 rounded-xl"
          >

            {mobileMenu ? (
              <X size={20} />
            ) : (
              <Menu size={20} />
            )}

          </button>

        </div>

      </div>

      {/* MOBILE MENU */}
      {mobileMenu && (

        <div className="lg:hidden border-t border-indigo-800 bg-slate-900 px-4 py-4 space-y-3">

          {navItems
            .filter((item) =>
              item.roles.includes(
                user?.role
              )
            )
            .map((item) => {

              const Icon =
                item.icon;

              const isActive =
                location.pathname ===
                item.path;

              return (

                <Link
                  key={item.path}
                  to={item.path}
                  onClick={() =>
                    setMobileMenu(false)
                  }
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

            Logout

          </button>

        </div>

      )}

    </nav>
  );
}