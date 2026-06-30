// components/navigation/navConfig.js

export const navSections = [
  {
    label: "Platform",
    dropdown: true,
    items: [
      {
        label: "Organizations",
        path: "/organizations",
        roles: ["SUPER_ADMIN"],
      },
      {
        label: "Tenant Onboarding",
        path: "/tenant-onboarding",
        roles: ["SUPER_ADMIN"],
      },
      {
        label: "Usage Dashboard",
        path: "/usage-dashboard",
        roles: ["SUPER_ADMIN"],
      },
    ],
  },

  {
    label: "Collaboration",
    dropdown: true,
    items: [
      {
        label: "Workspaces",
        path: "/workspaces",
        roles: [
          "ORGANIZATION_ADMIN",
          "WORKSPACE_ADMIN",
          "MANAGER",
          "EMPLOYEE",
        ],
      },
    ],
  },

  {
    label: "Tasks",
    dropdown: true,
    items: [
      {
        label: "Dashboard",
        path: "/dashboard",
        roles: [
          "ORGANIZATION_ADMIN",
          "WORKSPACE_ADMIN",
          "MANAGER",
          "EMPLOYEE",
        ],
      },
      {
        label: "Create Task",
        path: "/tasks/create",
        roles: [
          "ORGANIZATION_ADMIN",
          "WORKSPACE_ADMIN",
          "MANAGER",
        ],
      },
      {
        label: "Kanban Board",
        path: "/kanban",
        roles: [
          "ORGANIZATION_ADMIN",
          "WORKSPACE_ADMIN",
          "MANAGER",
          "EMPLOYEE",
        ],
      },
    ],
  },

  {
    label: "Approvals",
    dropdown: true,
    items: [
      {
        label: "Approval Requests",
        path: "/approvals",
        roles: [
          "ORGANIZATION_ADMIN",
          "WORKSPACE_ADMIN",
          "MANAGER",
          "EMPLOYEE",
        ],
      },
      {
        label: "Approval Delegations",
        path: "/approval-delegations",
        roles: [
          "ORGANIZATION_ADMIN",
          "WORKSPACE_ADMIN",
          "MANAGER",
        ],
      },
      {
        label: "Approval Escalations",
        path: "/approval-escalations",
        roles: [
          "ORGANIZATION_ADMIN",
          "WORKSPACE_ADMIN",
          "MANAGER",
        ],
      },
      {
        label: "Notification Preferences",
        path: "/notification-preferences",
        roles: [
          "ORGANIZATION_ADMIN",
          "WORKSPACE_ADMIN",
          "MANAGER",
          "EMPLOYEE",
        ],
      },
    ],
  },

  {
    label: "Activity",
    dropdown: true,
    items: [
      {
        label: "Activity Feed",
        path: "/activity",
        roles: [
          "ORGANIZATION_ADMIN",
          "WORKSPACE_ADMIN",
          "MANAGER",
          "EMPLOYEE",
        ],
      },
      {
        label: "Audit Logs",
        path: "/admin/audit-logs",
        roles: [
          "ORGANIZATION_ADMIN",
          "WORKSPACE_ADMIN",
          "MANAGER",
        ],
      },
    ],
  },

  {
    label: "SLA",
    dropdown: true,
    items: [
      {
        label: "SLA Dashboard",
        path: "/dashboard/sla",
        roles: [
          "ORGANIZATION_ADMIN",
          "WORKSPACE_ADMIN",
          "MANAGER",
        ],
      },
      {
        label: "SLA Rules",
        path: "/admin/sla-rules",
        roles: [
          "ORGANIZATION_ADMIN",
          "WORKSPACE_ADMIN",
          "MANAGER",
        ],
      },
    ],
  },

      {
      label: "Projects",
      children: [
        {
          label: "Teams",
          path: "/teams",
        },
        {
          label: "Projects",
          path: "/projects",
        },
        {
          label: "Meetings",
          path: "/meetings",
        },
        {
          label: "Workload",
          path: "/projects",
        },
      ],
    }
];