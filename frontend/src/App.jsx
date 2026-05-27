import { BrowserRouter, Route, Routes } from "react-router-dom";
import Activity from "./pages/Activity";
import Approval from "./pages/Approval";
import AssignTask from "./pages/AssignTask";
import CreateTask from "./pages/CreateTask";
import Dashboard from "./pages/Dashboard";
import EditTask from "./pages/EditTask";
import KanbanBoard from "./pages/KanbanBoard";
import Login from "./pages/Login";
import OAuthCallback from "./pages/OAuthCallback";
import Register from "./pages/Register";
import Users from "./pages/Users";
import ProtectedRoute from "./components/ProtectedRoute";
import Billing from "./pages/Billing";
import PaymentSuccess from "./pages/PaymentSuccess";

import SLARules from "./pages/SLARules";
import SLADashboard from "./pages/SLADashboard";
import ApprovalEscalations from "./pages/ApprovalEscalations";
import ApprovalDelegations from "./pages/ApprovalDelegations";
import NotificationPreferences from "./pages/NotificationPreferences";
import AuditLogs from "./pages/AuditLogs";


function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/oauth/callback" element={<OAuthCallback />} />
        <Route path="/register" element={<Register />} />
        <Route
          path="/dashboard"
          element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/create-task"
          element={
            <ProtectedRoute>
              <CreateTask />
            </ProtectedRoute>
          }
        />
        <Route
          path="/tasks/:id/assign"
          element={
            <ProtectedRoute>
              <AssignTask />
            </ProtectedRoute>
          }
        />
        <Route
          path="/tasks/:id/edit"
          element={
            <ProtectedRoute>
              <EditTask />
            </ProtectedRoute>
          }
        />
        <Route
          path="/users"
          element={
            <ProtectedRoute>
              <Users />
            </ProtectedRoute>
          }
        />
        <Route
          path="/kanban"
          element={
            <ProtectedRoute>
              <KanbanBoard />
            </ProtectedRoute>
          }
        />
        <Route
          path="/approvals"
          element={
            <ProtectedRoute>
              <Approval />
            </ProtectedRoute>
          }
        />
        <Route
          path="/activity"
          element={
            <ProtectedRoute>
              <Activity />
            </ProtectedRoute>
          }
        />
        <Route
          path="/billing"
          element={
            <ProtectedRoute>
              <Billing />
            </ProtectedRoute>
          }
        />

        <Route path="/payment-success" element={<PaymentSuccess />} />

        <Route path="/admin/sla-rules" element={<ProtectedRoute><SLARules /></ProtectedRoute>} />
        <Route path="/dashboard/sla" element={<ProtectedRoute><SLADashboard /></ProtectedRoute>} />
        <Route
          path="/approval-escalations"
          element={<ProtectedRoute><ApprovalEscalations /></ProtectedRoute>}
        />
        <Route
          path="/approval-delegations"
          element={<ProtectedRoute><ApprovalDelegations /></ProtectedRoute>}
        />
        <Route
          path="/settings/notification-preferences"
          element={<ProtectedRoute><NotificationPreferences /></ProtectedRoute>}
        />
        <Route path="/admin/audit-logs" element={<ProtectedRoute><AuditLogs /></ProtectedRoute>} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
