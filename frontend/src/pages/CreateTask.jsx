import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";


export default function CreateTask() {
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");
  const [form, setForm] = useState({
    title: "",
    description: "",
    priority: "medium",
    status: "todo",
    due_date: "",
    assigned_to_id: "",
  });

  useEffect(() => {
    const loadUsers = async () => {
      try {
        const response = await API.get("/users/assignable");
        setUsers(response.data);
      } catch {
        setError("Unable to load users for assignment.");
      }
    };

    loadUsers();
  }, []);

  const updateForm = (key, value) => {
    setForm((current) => ({ ...current, [key]: value }));
  };

  const handleSubmit = async () => {
    setError("");
    try {
      await API.post("/tasks/", {
        title: form.title,
        description: form.description || null,
        priority: form.priority,
        status: form.status,
        due_date: form.due_date || null,
        assigned_to_id: form.assigned_to_id ? Number(form.assigned_to_id) : null,
      });
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Error creating task.");
    }
  };

  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar />

      <div className="p-6 max-w-xl mx-auto">
        <div className="bg-white p-6 rounded-xl shadow">
          <h2 className="text-xl font-bold mb-4 text-gray-700">Create Task</h2>

          <input
            placeholder="Task Title"
            className="border p-2 w-full mb-3 rounded"
            value={form.title}
            onChange={(e) => updateForm("title", e.target.value)}
          />

          <textarea
            placeholder="Description"
            className="border p-2 w-full mb-3 rounded"
            value={form.description}
            onChange={(e) => updateForm("description", e.target.value)}
          />

          <select
            className="border p-2 w-full mb-3 rounded"
            value={form.priority}
            onChange={(e) => updateForm("priority", e.target.value)}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>

          <select
            className="border p-2 w-full mb-3 rounded"
            value={form.status}
            onChange={(e) => updateForm("status", e.target.value)}
          >
            <option value="todo">Todo</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>

          <input
            type="datetime-local"
            className="border p-2 w-full mb-3 rounded"
            value={form.due_date}
            onChange={(e) => updateForm("due_date", e.target.value)}
          />

          <select
            className="border p-2 w-full mb-4 rounded"
            value={form.assigned_to_id}
            onChange={(e) => updateForm("assigned_to_id", e.target.value)}
          >
            <option value="">Assign to (optional)</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name} ({user.role})
              </option>
            ))}
          </select>

          {error && <p className="text-sm text-red-600 mb-3">{error}</p>}

          <button
            onClick={handleSubmit}
            className="w-full bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700 transition"
          >
            Create Task
          </button>
        </div>
      </div>
    </div>
  );
}
