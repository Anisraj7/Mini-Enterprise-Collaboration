import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";

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
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const loadDashboard = async () => {
    const [userResponse, tasksResponse, summaryResponse] = await Promise.all([
      API.get("/auth/me"),
      API.get("/tasks/"),
      API.get("/dashboard/summary"),
    ]);
    setUser(userResponse.data);
    setTasks(tasksResponse.data);
    setSummary(summaryResponse.data);
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/");
      return;
    }

    const loadInitialDashboard = async () => {
      try {
        const [userResponse, tasksResponse, summaryResponse] = await Promise.all([
          API.get("/auth/me"),
          API.get("/tasks/"),
          API.get("/dashboard/summary"),
        ]);
        setUser(userResponse.data);
        setTasks(tasksResponse.data);
        setSummary(summaryResponse.data);
      } catch (err) {
        setError(err.response?.data?.detail || "Unable to load dashboard.");
      }
    };

    loadInitialDashboard();
  }, [navigate]);

  const handleDelete = async (id) => {
    try {
      await API.delete(`/tasks/${id}`);
      await loadDashboard();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to delete task.");
    }
  };

  const handleStatusChange = async (id, status) => {
    try {
      await API.patch(`/tasks/${id}/status`, { status });
      await loadDashboard();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to update task status.");
    }
  };

  const canManageTasks = user?.role === "admin" || user?.role === "manager";
  const showAssignedToColumn = user?.role !== "employee";
  const statusCounts = summary?.tasks_by_status || {};

  const statusData = [
    { name: "TODO", value: statusCounts.todo || 0 },
    { name: "IN PROGRESS", value: statusCounts.in_progress || 0 },
    { name: "REVIEW", value: statusCounts.review || 0 },
    { name: "DONE", value: statusCounts.done || 0 },
  ];

  const COLORS = ["#facc15", "#3b82f6", "#a855f7", "#22c55e"];

  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar />
      <div className="p-6 max-w-7xl mx-auto">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className="text-3xl font-bold text-gray-700">Dashboard</h1>
            {user && <p className="text-sm text-gray-500">Signed in as {user.name} ({user.role})</p>}
          </div>
          {canManageTasks && (
            <button onClick={() => navigate("/create-task")} className="bg-gradient-to-r from-indigo-600 to-cyan-600 text-white px-5 py-2 rounded-lg shadow hover:scale-105 transition">
              Create Task
            </button>
          )}
        </div>

        {error && <p className="text-sm text-red-600 mb-4">{error}</p>}

        <div className="grid md:grid-cols-4 gap-4 mb-6">
          <div className="bg-indigo-600 text-white p-4 rounded-xl shadow"><p>Total Tasks</p><h2 className="text-2xl font-bold">{summary?.total_tasks ?? tasks.length}</h2></div>
          <div className="bg-emerald-500 text-white p-4 rounded-xl shadow"><p>Completed</p><h2 className="text-2xl font-bold">{summary?.completed_tasks ?? 0}</h2></div>
          <div className="bg-amber-500 text-white p-4 rounded-xl shadow"><p>Pending Approvals</p><h2 className="text-2xl font-bold">{summary?.pending_approvals ?? 0}</h2></div>
          <div className="bg-sky-500 text-white p-4 rounded-xl shadow"><p>In Review</p><h2 className="text-2xl font-bold">{statusCounts.review || 0}</h2></div>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <div className="bg-white p-5 rounded-xl shadow">
            <h2 className="font-semibold mb-3">Task Distribution</h2>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={statusData}><XAxis dataKey="name" /><YAxis allowDecimals={false} /><Tooltip /><Bar dataKey="value" fill="#6366f1" /></BarChart>
            </ResponsiveContainer>
          </div>
          <div className="bg-white p-5 rounded-xl shadow">
            <h2 className="font-semibold mb-3">Task Status</h2>
            <ResponsiveContainer width="100%" height={250}>
              <PieChart><Pie data={statusData} dataKey="value" outerRadius={80}>{statusData.map((entry, index) => <Cell key={entry.name} fill={COLORS[index]} />)}</Pie><Tooltip /></PieChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow overflow-hidden">
          <table className="w-full text-sm">
            <thead className="bg-gray-100 text-gray-600 uppercase text-xs">
              <tr><th className="p-4 text-left">Title</th><th>Status</th><th>Priority</th>{showAssignedToColumn && <th>Assigned To</th>}<th>Due Date</th><th>Actions</th></tr>
            </thead>
            <tbody>
              {tasks.map((task) => (
                <tr key={task.id} className="border-t hover:bg-gray-50">
                  <td className="p-4">{task.title}</td>
                  <td>
                    <select value={task.status} onChange={(e) => handleStatusChange(task.id, e.target.value)} className="border px-2 py-1">
                      <option value="todo">Todo</option><option value="in_progress">In Progress</option><option value="review">Review</option><option value="done">Done</option>
                    </select>
                  </td>
                  <td>{task.priority}</td>
                  {showAssignedToColumn && <td>{task.assigned_to_name || "Unassigned"}</td>}
                  <td>{task.due_date ? new Date(task.due_date).toLocaleString() : "No deadline"}</td>
                  <td className="flex gap-2 p-2">
                    {canManageTasks && <button onClick={() => navigate(`/tasks/${task.id}/edit`)} className="bg-amber-500 px-2 py-1 text-white rounded">Edit</button>}
                    {user?.role === "admin" && <button onClick={() => handleDelete(task.id)} className="bg-red-500 px-2 py-1 text-white rounded">Delete</button>}
                  </td>
                </tr>
              ))}
              {tasks.length === 0 && <tr><td colSpan="6" className="text-center p-4">No tasks available</td></tr>}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
