import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import ProtectedRoute from "./components/ProtectedRoute";
import MainLayout from "./layouts/MainLayout";

import Login from "./pages/Login";
import Register from "./pages/Register";
import OAuthCallback from "./pages/OAuthCallback";

import Dashboard from "./pages/Dashboard";
import CreateTask from "./pages/CreateTask";
import AssignTask from "./pages/AssignTask";
import EditTask from "./pages/EditTask";
import Users from "./pages/Users";
import KanbanBoard from "./pages/KanbanBoard";
import Approval from "./pages/Approval";
import Activity from "./pages/Activity";

import Billing from "./pages/Billing";
import PaymentSuccess from "./pages/PaymentSuccess";

import SLARules from "./pages/SLARules";
import SLADashboard from "./pages/SLADashboard";
import ApprovalEscalations from "./pages/ApprovalEscalations";
import ApprovalDelegations from "./pages/ApprovalDelegations";
import NotificationPreferences from "./pages/NotificationPreferences";
import AuditLogs from "./pages/AuditLogs";

import Workspaces from "./pages/collaboration/Workspaces";
import WorkspaceDetails from "./pages/collaboration/WorkspaceDetails";
import Channels from "./pages/collaboration/Channels";
import ChannelDetails from "./pages/collaboration/ChannelDetails";
import Members from "./pages/collaboration/Members";

import UsageDashboard from "./pages/collaboration/UsageDashboard";
import OrganizationSettings from "./pages/collaboration/OrganizationSettings";
import OrganizationOnboarding from "./pages/collaboration/OrganizationOnboarding";
import Organizations from "./pages/collaboration/Organizations";
import OrganizationDetails from "./pages/collaboration/OrganizationDetails";
import OrganizationUsers from "./pages/collaboration/OrganizationUsers";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        {/* Public Routes */}
        <Route path="/" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/oauth/callback" element={<OAuthCallback />} />
        <Route path="/payment-success" element={<PaymentSuccess />} />

        {/* Protected Routes */}
        <Route
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
          <Route path="/dashboard" element={<Dashboard />} />

          <Route path="/create-task" element={<CreateTask />} />
          <Route path="/tasks/:id/assign" element={<AssignTask />} />
          <Route path="/tasks/:id/edit" element={<EditTask />} />

          <Route path="/users" element={<Users />} />
          <Route path="/kanban" element={<KanbanBoard />} />
          <Route path="/approvals" element={<Approval />} />
          <Route path="/activity" element={<Activity />} />

          <Route path="/billing" element={<Billing />} />

          <Route path="/admin/sla-rules" element={<SLARules />} />
          <Route path="/dashboard/sla" element={<SLADashboard />} />

          <Route
            path="/approval-escalations"
            element={<ApprovalEscalations />}
          />

          <Route
            path="/approval-delegations"
            element={<ApprovalDelegations />}
          />

          <Route
            path="/notification-preferences"
            element={<NotificationPreferences />}
          />

          <Route path="/admin/audit-logs" element={<AuditLogs />} />

          {/* ========================================= */}
          {/* ORGANIZATION MANAGEMENT */}
          {/* ========================================= */}

          <Route path="/organizations" element={<Organizations />} />

          <Route
            path="/organizations/:organizationId"
            element={<OrganizationDetails />}
          />

          <Route
            path="/organizations/onboard"
            element={<OrganizationOnboarding />}
          />

          <Route
            path="/organizations/:organizationId/settings"
            element={<OrganizationSettings />}
          />

          <Route
            path="/organizations/:organizationId/usage"
            element={<UsageDashboard />}
          />

          {/* ========================================= */}
          {/* WORKSPACE & CHANNEL FOUNDATION */}
          {/* ========================================= */}

          <Route path="/workspaces" element={<Workspaces />} />

          <Route
            path="/workspaces/:workspaceId"
            element={<WorkspaceDetails />}
          />

          <Route
            path="/workspaces/:workspaceId/members"
            element={<Members />}
          />

          <Route
            path="/workspaces/:workspaceId/channels"
            element={<Channels />}
          />

          <Route path="/channels/:channelId" element={<ChannelDetails />} />

          <Route path="/organization-users" element={<OrganizationUsers />} />
        </Route>

        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
