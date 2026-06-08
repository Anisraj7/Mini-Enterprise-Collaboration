// components/navigation/NavMenu.jsx

import { NavLink } from "react-router-dom";

export default function NavMenu({ user }) {
  const menuItems = [
    {
      label: "Dashboard",
      path: "/dashboard",
      roles: [
        "organization_admin",
        "workspace_admin",
        "manager",
        "employee",
      ],
    },

    {
      label: "Organizations",
      path: "/organizations",
      roles: ["super_admin"],
    },

    {
      label: "Organization",
      path: `/organizations/${user?.organization_id}`,
      roles: ["organization_admin"],
    },

    {
      label: "Users",
      path: "/organization-users",
      roles: [
        "super_admin",
        "organization_admin",
        "workspace_admin",
      ],
    },

    {
      label: "Workspaces",
      path: "/workspaces",
      roles: ["organization_admin"],
    },

    {
      label: "Activity",
      path: "/activity",
      roles: [
        "organization_admin",
        "workspace_admin",
        "manager",
        "employee",
      ],
    },

    {
      label: "Audit Logs",
      path: "/admin/audit-logs",
      roles: [
        "organization_admin",
        "workspace_admin",
        "manager",
      ],
    },

    {
      label: "SLA Dashboard",
      path: "/dashboard/sla",
      roles: [
        "organization_admin",
        "workspace_admin",
        "manager",
      ],
    },

    {
      label: "SLA Rules",
      path: "/admin/sla-rules",
      roles: [
        "organization_admin",
        "workspace_admin",
        "manager",
      ],
    },
  ];

  const visibleItems = menuItems.filter(
    (item) => user && item.roles.includes(user.role)
  );

  const canAccessTasks =
    user &&
    [
      "organization_admin",
      "workspace_admin",
      "manager",
      "employee",
    ].includes(user.role);

  const canAccessApprovals =
    user &&
    [
      "organization_admin",
      "workspace_admin",
      "manager",
      "employee",
    ].includes(user.role);

  return (
    <div className="flex items-center gap-5">
      {/* Dashboard */}
      {visibleItems
        .filter((item) => item.label === "Dashboard")
        .map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `text-sm font-medium transition-colors ${
                isActive
                  ? "text-cyan-400"
                  : "text-slate-300 hover:text-cyan-400"
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}

      {/* Tasks Dropdown */}
      {canAccessTasks && (
        <div className="relative group">
          <button className="text-sm font-medium text-slate-300 hover:text-cyan-400 transition-colors">
            Tasks
          </button>

          <div className="absolute left-0 top-full hidden group-hover:block bg-slate-900 border border-slate-700 rounded-lg shadow-lg min-w-[180px] z-50">
            <NavLink
              to="/create-task"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Create Task
            </NavLink>

            <NavLink
              to="/kanban"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Kanban Board
            </NavLink>
          </div>
        </div>
      )}

      {/* Approvals Dropdown */}
      {canAccessApprovals && (
        <div className="relative group">
          <button className="text-sm font-medium text-slate-300 hover:text-cyan-400 transition-colors">
            Approvals
          </button>

          <div className="absolute left-0 top-full hidden group-hover:block bg-slate-900 border border-slate-700 rounded-lg shadow-lg min-w-[240px] z-50">
            <NavLink
              to="/approvals"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Approval Requests
            </NavLink>

            <NavLink
              to="/approval-escalations"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Approval Escalations
            </NavLink>

            <NavLink
              to="/approval-delegations"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Approval Delegations
            </NavLink>

            <NavLink
              to="/notification-preferences"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Notification Preferences
            </NavLink>
          </div>
        </div>
      )}

      {/* Remaining Menu Items */}
      {visibleItems
        .filter((item) => item.label !== "Dashboard")
        .map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `text-sm font-medium transition-colors ${
                isActive
                  ? "text-cyan-400"
                  : "text-slate-300 hover:text-cyan-400"
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
    </div>
  );
}