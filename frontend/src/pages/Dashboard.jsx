import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import { getUserWebSocketUrl } from "../api/websocket";
import { getPageItems } from "../api/pagination";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [summary, setSummary] = useState(null);
  const [user, setUser] = useState(null);

  const [notifications, setNotifications] = useState([]);
  const [activities, setActivities] = useState([]);

  const [error, setError] = useState("");

  const navigate = useNavigate();

  // Dashboard Loader
  const loadDashboard = async () => {
    try {
      const [
        userResponse,
        tasksResponse,
        summaryResponse,
        auditResponse,
        notificationResponse,
      ] = await Promise.all([
        API.get("/auth/me"),
        API.get("/tasks/"),
        API.get("/dashboard/summary"),
        API.get("/audit-logs/"),
        API.get("/notifications/"),
      ]);

      setUser(userResponse.data);

      // FIXED PAGINATION RESPONSE
      setTasks(getPageItems(tasksResponse.data));

      setSummary(summaryResponse.data);

      // FIXED PAGINATION RESPONSE
      setActivities(getPageItems(auditResponse.data));

      // FIXED PAGINATION RESPONSE
      setNotifications(getPageItems(notificationResponse.data));
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load dashboard.");
    }
  };

  // Initial Load
  useEffect(() => {
    const token = localStorage.getItem("token");

    if (!token) {
      navigate("/");
      return;
    }

    Promise.resolve().then(loadDashboard);
  }, [navigate]);

  // WebSocket Connection
  useEffect(() => {
    if (!user) return;

    const ws = new WebSocket(getUserWebSocketUrl(user.id));

    ws.onopen = () => {
      console.log("WebSocket Connected");
    };

    ws.onmessage = (event) => {
      let parsedMessage;

      try {
        parsedMessage = JSON.parse(event.data);
      } catch {
        parsedMessage = {
          message: event.data,
        };
      }

      // Add live notification
      setNotifications((prev) => [
        {
          id: Date.now(),
          message: parsedMessage.message || "New notification",
          created_at: new Date(),
          is_read: false,
        },
        ...prev,
      ]);

      // Reload dashboard
      loadDashboard();
    };

    ws.onclose = () => {
      console.log("WebSocket Disconnected");
    };

    return () => {
      ws.close();
    };
  }, [user]);

  // Delete Task
  const handleDelete = async (id) => {
    try {
      await API.delete(`/tasks/${id}`);

      await loadDashboard();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to delete task.");
    }
  };

  // Update Status
  const handleStatusChange = async (id, status) => {
    try {
      await API.patch(`/tasks/${id}/status`, { status });

      await loadDashboard();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to update task status.");
    }
  };

  // Mark Notification Read
  const markAsRead = async (id) => {
    try {
      await API.patch(`/notifications/${id}/read`);

      setNotifications((prev) =>
        prev.map((notif) =>
          notif.id === id ? { ...notif, is_read: true } : notif,
        ),
      );
    } catch (err) {
      console.log(err);
    }
  };

  const canManageTasks = [
    "organization_admin",
    "workspace_admin",
    "manager",
  ].includes(user?.role);

  const showAssignedToColumn = user?.role !== "employee";

  const statusCounts = summary?.tasks_by_status || {};

  const statusData = [
    {
      name: "TODO",
      value: statusCounts.todo || 0,
    },
    {
      name: "IN PROGRESS",
      value: statusCounts.in_progress || 0,
    },
    {
      name: "REVIEW",
      value: statusCounts.review || 0,
    },
    {
      name: "DONE",
      value: statusCounts.done || 0,
    },
  ];

  const COLORS = ["#facc15", "#3b82f6", "#a855f7", "#22c55e"];

  // SAFE FILTER
  const unreadCount = Array.isArray(notifications)
    ? notifications.filter((n) => !n.is_read).length
    : 0;

  return (
    <div className="bg-gray-50 min-h-screen">
      <div className="p-6 max-w-7xl mx-auto">
        {/* HEADER */}
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-700">
              Enterprise Dashboard
            </h1>

            {user && (
              <p className="text-sm text-gray-500">
                Signed in as {user.name} ({user.role})
              </p>
            )}
          </div>

          {canManageTasks && (
            <button
              onClick={() => navigate("/create-task")}
              className="bg-gradient-to-r from-indigo-600 to-cyan-600 text-white px-5 py-2 rounded-lg shadow hover:scale-105 transition"
            >
              Create Task
            </button>
          )}
        </div>

        {/* ERROR */}
        {error && <p className="text-sm text-red-600 mb-4">{error}</p>}

        {/* AI SUMMARY */}
        <div className="grid md:grid-cols-3 gap-4 mb-6">
          <div className="bg-red-500 text-white p-5 rounded-xl shadow">
            <h2 className="text-lg font-semibold">High Priority Tasks</h2>

            <p className="text-3xl font-bold mt-2">
              {summary?.high_priority_tasks || 0}
            </p>
          </div>

          <div className="bg-yellow-500 text-white p-5 rounded-xl shadow">
            <h2 className="text-lg font-semibold">Delayed Tasks</h2>

            <p className="text-3xl font-bold mt-2">
              {summary?.delayed_tasks || 0}
            </p>
          </div>

          <div className="bg-indigo-600 text-white p-5 rounded-xl shadow">
            <h2 className="text-lg font-semibold">AI Insight</h2>

            <p className="mt-3 text-sm">
              {summary?.ai_summary || "No insights available"}
            </p>
          </div>
        </div>

        {/* STATS */}
        <div className="grid md:grid-cols-4 gap-4 mb-6">
          <div className="bg-indigo-600 text-white p-4 rounded-xl shadow">
            <p>Total Tasks</p>

            <h2 className="text-2xl font-bold">
              {summary?.total_tasks ?? tasks.length}
            </h2>
          </div>

          <div className="bg-emerald-500 text-white p-4 rounded-xl shadow">
            <p>Completed</p>

            <h2 className="text-2xl font-bold">
              {summary?.completed_tasks || 0}
            </h2>
          </div>

          <div className="bg-amber-500 text-white p-4 rounded-xl shadow">
            <p>Pending Approvals</p>

            <h2 className="text-2xl font-bold">
              {summary?.pending_approvals || 0}
            </h2>
          </div>

          <div className="bg-sky-500 text-white p-4 rounded-xl shadow">
            <p>Unread Notifications</p>

            <h2 className="text-2xl font-bold">{unreadCount}</h2>
          </div>
        </div>

        {/* NOTIFICATIONS + ACTIVITY */}
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          {/* Notifications */}
          <div className="bg-white p-5 rounded-xl shadow">
            <div className="flex justify-between items-center mb-4">
              <h2 className="font-semibold text-lg">Live Notifications</h2>

              <span className="bg-red-500 text-white px-2 py-1 rounded-full text-xs">
                {unreadCount}
              </span>
            </div>

            <div className="space-y-3 max-h-80 overflow-y-auto">
              {notifications.length === 0 ? (
                <p className="text-gray-500 text-sm">No notifications</p>
              ) : (
                notifications.map((notif, index) => (
                  <div
                    key={index}
                    className={`p-3 rounded-lg border ${
                      notif.is_read
                        ? "bg-gray-100"
                        : "bg-blue-50 border-blue-300"
                    }`}
                  >
                    <div className="flex justify-between items-center">
                      <div>
                        <p className="text-sm font-medium">{notif.message}</p>

                        {notif.created_at && (
                          <p className="text-xs text-gray-500 mt-1">
                            {new Date(notif.created_at).toLocaleString()}
                          </p>
                        )}
                      </div>

                      {!notif.is_read && notif.id && (
                        <button
                          onClick={() => markAsRead(notif.id)}
                          className="text-xs bg-blue-500 text-white px-2 py-1 rounded"
                        >
                          Read
                        </button>
                      )}
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Activity Feed */}
          {/* <div className="bg-white p-5 rounded-xl shadow">
            <h2 className="font-semibold text-lg mb-4">Activity Feed</h2>

            <div className="space-y-3 max-h-80 overflow-y-auto">
              {activities.length === 0 ? (
                <p className="text-gray-500 text-sm">No activities found</p>
              ) : (
                activities.map((activity) => (
                  <div key={activity.id} className="border-b pb-2">
                    <p className="text-sm font-medium">{activity.action}</p>

                    <p className="text-xs text-gray-500">
                      {new Date(
                        activity.timestamp || activity.created_at,
                      ).toLocaleString()}
                    </p>
                  </div>
                ))
              )}
            </div> */}
          {/* </div> */}
        </div>

        {/* CHARTS */}
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          {/* Bar Chart */}
          <div className="bg-white p-5 rounded-xl shadow">
            <h2 className="font-semibold mb-3">Task Distribution</h2>

            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={statusData}>
                <XAxis dataKey="name" />

                <YAxis allowDecimals={false} />

                <Tooltip />

                <Bar dataKey="value" fill="#6366f1" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* Pie Chart */}
          <div className="bg-white p-5 rounded-xl shadow">
            <h2 className="font-semibold mb-3">Task Status</h2>

            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={statusData} dataKey="value" outerRadius={80}>
                  {statusData.map((entry, index) => (
                    <Cell key={entry.name} fill={COLORS[index]} />
                  ))}
                </Pie>

                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* TASK TABLE */}
        <div className="bg-white rounded-xl shadow overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-100 text-gray-600 uppercase text-xs">
              <tr>
                <th className="p-4 text-left">Title</th>

                <th>Status</th>

                <th>Priority</th>

                {showAssignedToColumn && <th>Assigned To</th>}

                <th>Due Date</th>

                <th>Actions</th>
              </tr>
            </thead>

            <tbody>
              {tasks.map((task) => (
                <tr key={task.id} className="border-t hover:bg-gray-50">
                  <td className="p-4">{task.title}</td>

                  <td>
                    <select
                      value={task.status}
                      onChange={(e) =>
                        handleStatusChange(task.id, e.target.value)
                      }
                      className="border px-2 py-1 rounded"
                    >
                      <option value="todo">Todo</option>

                      <option value="in_progress">In Progress</option>

                      <option value="review">Review</option>

                      <option value="done">Done</option>
                    </select>
                  </td>

                  <td>{task.priority}</td>

                  {showAssignedToColumn && (
                    <td>{task.assigned_to_name || "Unassigned"}</td>
                  )}

                  <td>
                    {task.due_date
                      ? new Date(task.due_date).toLocaleString()
                      : "No deadline"}
                  </td>

                  <td className="flex gap-2 p-2">
                    {canManageTasks && (
                      <button
                        onClick={() => navigate(`/tasks/${task.id}/assign`)}
                        className="bg-sky-500 px-2 py-1 text-white rounded"
                      >
                        Assign
                      </button>
                    )}

                    {canManageTasks && (
                      <button
                        onClick={() => navigate(`/tasks/${task.id}/edit`)}
                        className="bg-amber-500 px-2 py-1 text-white rounded"
                      >
                        Edit
                      </button>
                    )}

                    {user?.role === "admin" && (
                      <button
                        onClick={() => handleDelete(task.id)}
                        className="bg-red-500 px-2 py-1 text-white rounded"
                      >
                        Delete
                      </button>
                    )}
                  </td>
                </tr>
              ))}

              {tasks.length === 0 && (
                <tr>
                  <td colSpan="6" className="text-center p-4">
                    No tasks available
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
