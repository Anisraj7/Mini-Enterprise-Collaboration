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
  ChevronDown,
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

  // =========================================
  // LOAD USER
  // =========================================

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

  // =========================================
  // LOAD NOTIFICATIONS
  // =========================================

  useEffect(() => {
    const loadNotifications = async () => {
      try {
        const response = await API.get("/notifications/");

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

  // =========================================
  // LOGOUT
  // =========================================

  const logout = () => {
    localStorage.removeItem("token");

    localStorage.removeItem("refresh_token");

    navigate("/");
  };

  // =========================================
  // NAVIGATION SECTIONS
  // =========================================

  const navSections = [
    {
      label: "Workspace",

      items: [
        {
          label: "Dashboard",
          path: "/dashboard",
          icon: LayoutDashboard,
          roles: ["admin", "manager", "employee", "auditor"],
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
          label: "Create",
          path: "/create-task",
          icon: PlusSquare,
          roles: ["admin", "manager"],
          color: "from-cyan-500 to-sky-500",
        },
      ],
    },

    // =========================================
    // SLA
    // =========================================

    {
      label: "SLA & Workflow",

      dropdown: true,

      icon: ShieldCheck,

      color: "from-blue-500 to-cyan-500",

      items: [
        {
          label: "SLA Dashboard",
          path: "/dashboard/sla",
          icon: LayoutDashboard,
          roles: ["admin", "manager", "auditor"],
        },

        {
          label: "SLA Rules",
          path: "/admin/sla-rules",
          icon: ShieldCheck,
          roles: ["admin"],
        },

        {
          label: "Escalations",
          path: "/approval-escalations",
          icon: Bell,
          roles: ["admin", "manager", "auditor"],
        },

        {
          label: "Delegations",
          path: "/approval-delegations",
          icon: Users,
          roles: ["admin", "manager"],
        },
      ],
    },

    // =========================================
    // MANAGEMENT
    // =========================================

    {
      label: "Management",

      dropdown: true,

      icon: Users,

      color: "from-orange-500 to-red-500",

      items: [
        {
          label: "Users",
          path: "/users",
          icon: Users,
          roles: ["admin"],
        },

        {
          label: "Register",
          path: "/register",
          icon: ShieldCheck,
          roles: ["admin"],
        },

        {
          label: "Billing",
          path: "/billing",
          icon: CreditCard,
          roles: ["admin", "manager"],
        },

        {
          label: "Activity",
          path: "/activity",
          icon: Activity,
          roles: ["admin", "manager"],
        },

        {
          label: "Audit Logs",
          path: "/admin/audit-logs",
          icon: Activity,
          roles: ["admin", "auditor"],
        },
      ],
    },

    // =========================================
    // NOTIFICATIONS
    // =========================================

    {
      label: "Notifications",

      dropdown: true,

      icon: Bell,

      color: "from-violet-500 to-indigo-500",

      items: [
        {
          label: "Preferences",
          path: "/settings/notification-preferences",
          icon: Bell,
          roles: ["admin", "manager", "employee", "auditor"],
        },
      ],
    },
  ];

  return (
    <nav
      className="
    sticky top-0 z-50
    bg-slate-950/90
    backdrop-blur-2xl
    border-b border-white/10
    shadow-[0_10px_40px_rgba(0,0,0,0.35)]
  "
    >
      {/* ========================================= */}
      {/* TOP BAR */}
      {/* ========================================= */}

      <div
        className="
      border-b border-white/10
      px-3 lg:px-5
      py-2
    "
      >
        <div
          className="
        max-w-[1800px]
        mx-auto
        flex items-center justify-between
        gap-4
      "
        >
          {/* ========================================= */}
          {/* LOGO */}
          {/* ========================================= */}

          <div
            className="cursor-pointer shrink-0"
            onClick={() => {
              setNotificationsOpen(false);

              navigate("/dashboard");
            }}
          >
            <h1
              className="
            text-xl xl:text-2xl
            font-black
            bg-gradient-to-r
            from-cyan-400
            via-indigo-300
            to-pink-400
            bg-clip-text
            text-transparent
            tracking-tight
          "
            >
              TaskFlow
            </h1>

            {user && (
              <p className="text-[10px] text-slate-400 mt-0.5">
                Organization :{" "}
                <span className="text-cyan-300 font-medium">
                  {user.organization?.name}
                </span>
              </p>
            )}
          </div>

          {/* ========================================= */}
          {/* RIGHT */}
          {/* ========================================= */}

          <div className="flex items-center gap-2">
            {/* NOTIFICATIONS */}

            <div className="relative">
              <button
                type="button"
                onClick={() => setNotificationsOpen((open) => !open)}
                className="
                relative
                bg-white/[0.08]
                hover:bg-white/[0.14]
                transition-all duration-200
                p-2
                rounded-xl
                border border-white/10
              "
              >
                <Bell size={16} className="text-white" />

                {notificationsCount > 0 && (
                  <span
                    className="
                  absolute -top-1 -right-1
                  bg-gradient-to-r
                  from-red-500 to-pink-500
                  text-white
                  text-[9px]
                  min-w-[16px]
                  h-4
                  px-1
                  flex items-center justify-center
                  rounded-full
                  font-bold
                "
                  >
                    {notificationsCount}
                  </span>
                )}
              </button>

              {notificationsOpen && (
                <div
                  className="
                absolute right-0 top-full
                mt-2
                w-[min(24rem,calc(100vw-2rem))]
                z-50
              "
                >
                  <NotificationPanel
                    onUnreadCountChange={setNotificationsCount}
                  />
                </div>
              )}
            </div>

            {/* PROFILE */}

            <div className="relative hidden md:block group">
              <button
                className="
              flex items-center gap-2
              bg-white/[0.08]
              hover:bg-white/[0.14]
              border border-white/10
              px-2.5 py-1.5
              rounded-xl
              transition-all duration-300
            "
              >
                <div
                  className="
                w-8 h-8 rounded-full
                bg-gradient-to-r
                from-cyan-400 to-indigo-500
                text-white
                flex items-center justify-center
                font-bold
                text-sm
              "
                >
                  {user?.name?.charAt(0)?.toUpperCase()}
                </div>

                <div className="text-left leading-tight">
                  <p className="text-xs font-semibold text-white capitalize">
                    {user?.name}
                  </p>

                  <p className="text-[10px] text-slate-400 capitalize">
                    {user?.role}
                  </p>
                </div>
              </button>

              {/* PROFILE DROPDOWN */}

              <div
                className="
              absolute right-0 top-full mt-2
              w-52
              bg-slate-900/95
              backdrop-blur-2xl
              border border-white/10
              rounded-2xl
              shadow-2xl
              opacity-0 invisible
              translate-y-2
              group-hover:opacity-100
              group-hover:visible
              group-hover:translate-y-0
              transition-all duration-300
              overflow-hidden
              p-2
              z-50
            "
              >
                <div className="px-3 py-2 border-b border-white/10">
                  <p className="text-white font-semibold text-xs">
                    {user?.name}
                  </p>

                  <p className="text-slate-400 text-[10px] capitalize mt-1">
                    {user?.role}
                  </p>
                </div>

                <button
                  onClick={logout}
                  className="
                mt-2
                w-full
                flex items-center gap-2
                px-3 py-2.5
                rounded-xl
                text-red-400
                hover:bg-red-500/10
                hover:text-red-300
                transition-all duration-200
                text-xs font-medium
              "
                >
                  <LogOut size={14} />
                  Logout
                </button>
              </div>
            </div>

            {/* MOBILE MENU */}

            <button
              onClick={() => setMobileMenu(!mobileMenu)}
              className="
            lg:hidden
            bg-white/[0.08]
            hover:bg-white/[0.14]
            text-white
            p-2
            rounded-xl
            border border-white/10
          "
            >
              {mobileMenu ? <X size={18} /> : <Menu size={18} />}
            </button>
          </div>
        </div>
      </div>

      {/* ========================================= */}
      {/* BOTTOM NAVIGATION */}
      {/* ========================================= */}

      <div className="px-3 lg:px-5 py-2.5">
        <div className="max-w-[1800px] mx-auto">
          {/* DESKTOP NAV */}

          <div
            className="
          hidden lg:flex
          items-center
          gap-2
          flex-wrap
        "
          >
            {navSections.map((section) => {
              // =====================================
              // NORMAL ITEMS
              // =====================================

              if (!section.dropdown) {
                return section.items
                  .filter((item) => item.roles.includes(user?.role))
                  .map((item) => {
                    const Icon = item.icon;

                    const isActive = location.pathname === item.path;

                    return (
                      <Link
                        key={item.path}
                        to={item.path}
                        className={`
                        flex items-center gap-2
                        px-3 py-2
                        rounded-xl
                        text-[13px]
                        font-medium
                        transition-all duration-300
                        border border-white/5

                        ${
                          isActive
                            ? `
                              bg-gradient-to-r
                              ${item.color}
                              text-white
                              shadow-lg
                            `
                            : `
                              bg-white/[0.06]
                              text-slate-200
                              hover:bg-white/[0.12]
                            `
                        }
                      `}
                      >
                        <Icon size={15} />

                        {item.label}
                      </Link>
                    );
                  });
              }

              // =====================================
              // DROPDOWNS
              // =====================================

              const SectionIcon = section.icon;

              return (
                <div key={section.label} className="relative group">
                  <button
                    className="
                    flex items-center gap-2
                    px-3 py-2
                    rounded-xl
                    text-[13px]
                    font-medium
                    transition-all duration-300
                    border border-white/5
                    bg-white/[0.06]
                    text-slate-200
                    hover:bg-white/[0.12]
                  "
                  >
                    <SectionIcon size={15} />

                    {section.label}

                    <ChevronDown size={14} />
                  </button>

                  {/* DROPDOWN */}

                  <div
                    className="
                    absolute top-full left-0 mt-2
                    w-64
                    bg-slate-900/95
                    backdrop-blur-2xl
                    border border-white/10
                    rounded-2xl
                    shadow-2xl
                    opacity-0 invisible
                    translate-y-2
                    group-hover:opacity-100
                    group-hover:visible
                    group-hover:translate-y-0
                    transition-all duration-300
                    p-2
                    z-50
                  "
                  >
                    <div className="space-y-1.5">
                      {section.items
                        .filter((item) => item.roles.includes(user?.role))
                        .map((item) => {
                          const Icon = item.icon;

                          const isActive = location.pathname === item.path;

                          return (
                            <Link
                              key={item.path}
                              to={item.path}
                              className={`
                              flex items-center gap-3
                              px-3 py-2.5
                              rounded-xl
                              text-sm font-medium
                              transition-all duration-300

                              ${
                                isActive
                                  ? `
                                    bg-gradient-to-r
                                    ${section.color}
                                    text-white
                                  `
                                  : `
                                    text-slate-200
                                    hover:bg-white/[0.08]
                                  `
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
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}
