// components/navigation/NavMenu.jsx

import { NavLink } from "react-router-dom";

export default function NavMenu({ user }) {
  const menuItems = [
    {
      label: "Dashboard",
      path: "/dashboard",
      roles: ["organization_admin", "workspace_admin", "manager", "employee"],
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
      roles: ["super_admin", "organization_admin", "workspace_admin"],
    },

    {
      label: "Workspaces",
      path: "/workspaces",
      roles: ["organization_admin"],
    },
  ];

  const visibleItems = menuItems.filter(
    (item) => user && item.roles.includes(user.role),
  );

  const canAccessTasks =
    user &&
    ["organization_admin", "workspace_admin", "manager", "employee"].includes(
      user.role,
    );

  const canAccessApprovals =
    user &&
    ["organization_admin", "workspace_admin", "manager", "employee"].includes(
      user.role,
    );

  const canAccessLogs =
    user &&
    ["organization_admin", "workspace_admin", "manager"].includes(user.role);

  const canAccessSLA =
    user &&
    ["organization_admin", "workspace_admin", "manager"].includes(user.role);

  const canAccessCollaboration =
    user &&
    ["organization_admin", "workspace_admin", "manager", "employee"].includes(
      user.role,
    );

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

      {/* Logs Dropdown */}
      {canAccessLogs && (
        <div className="relative group">
          <button className="text-sm font-medium text-slate-300 hover:text-cyan-400 transition-colors">
            Logs
          </button>

          <div className="absolute left-0 top-full hidden group-hover:block bg-slate-900 border border-slate-700 rounded-lg shadow-lg min-w-[220px] z-50">
            <NavLink
              to="/activity"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Activity
            </NavLink>

            <NavLink
              to="/admin/audit-logs"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Audit Logs
            </NavLink>
          </div>
        </div>
      )}

      {/* SLA Dropdown */}
      {canAccessSLA && (
        <div className="relative group">
          <button className="text-sm font-medium text-slate-300 hover:text-cyan-400 transition-colors">
            SLA
          </button>

          <div className="absolute left-0 top-full hidden group-hover:block bg-slate-900 border border-slate-700 rounded-lg shadow-lg min-w-[220px] z-50">
            <NavLink
              to="/dashboard/sla"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              SLA Dashboard
            </NavLink>

            <NavLink
              to="/admin/sla-rules"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              SLA Rules
            </NavLink>
          </div>
        </div>
      )}

      {/* Collaboration Dropdown */}
      {canAccessCollaboration && (
        <div className="relative group">
          <button className="text-sm font-medium text-slate-300 hover:text-cyan-400 transition-colors">
            Collaboration
          </button>

          <div className="absolute left-0 top-full hidden group-hover:block bg-slate-900 border border-slate-700 rounded-lg shadow-lg min-w-[220px] z-50">
            <NavLink
              to="/teams"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Teams
            </NavLink>

            <NavLink
              to="/projects"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Projects
            </NavLink>

            <NavLink
              to="/meetings"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Meetings
            </NavLink>

            <NavLink
              to="/calendar"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Project Calendar
            </NavLink>

            <NavLink
              to="/workload"
              className="block px-4 py-3 text-sm text-slate-300 hover:bg-slate-800"
            >
              Workload Dashboard
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
