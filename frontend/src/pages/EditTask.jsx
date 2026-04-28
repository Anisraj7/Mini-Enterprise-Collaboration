import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";


export default function EditTask() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [error, setError] = useState("");
  const [task, setTask] = useState({
    title: "",
    description: "",
    priority: "medium",
    status: "todo",
    due_date: "",
  });

  useEffect(() => {
    const loadTask = async () => {
      try {
        const response = await API.get(`/tasks/${id}`);
        const data = response.data;
        setTask({
          title: data.title || "",
          description: data.description || "",
          priority: data.priority || "medium",
          status: data.status || "todo",
          due_date: data.due_date ? data.due_date.slice(0, 16) : "",
        });
      } catch (err) {
        setError(err.response?.data?.detail || "Unable to load task.");
      }
    };

    loadTask();
  }, [id]);

  const handleUpdate = async () => {
    setError("");
    try {
      await API.put(`/tasks/${id}`, {
        ...task,
        due_date: task.due_date || null,
      });
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to update task.");
    }
  };

  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar />

      <div className="p-6 max-w-xl mx-auto">
        <div className="bg-white p-6 rounded-xl shadow">
          <h2 className="text-xl font-bold mb-4">Edit Task</h2>

          <input
            className="border p-2 w-full mb-3 rounded"
            value={task.title}
            onChange={(e) => setTask({ ...task, title: e.target.value })}
          />

          <textarea
            className="border p-2 w-full mb-3 rounded"
            value={task.description}
            onChange={(e) => setTask({ ...task, description: e.target.value })}
          />

          <select
            className="border p-2 w-full mb-3 rounded"
            value={task.priority}
            onChange={(e) => setTask({ ...task, priority: e.target.value })}
          >
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>

          <select
            className="border p-2 w-full mb-3 rounded"
            value={task.status}
            onChange={(e) => setTask({ ...task, status: e.target.value })}
          >
            <option value="todo">Todo</option>
            <option value="in_progress">In Progress</option>
            <option value="done">Done</option>
          </select>

          <input
            type="datetime-local"
            className="border p-2 w-full mb-3 rounded"
            value={task.due_date}
            onChange={(e) => setTask({ ...task, due_date: e.target.value })}
          />

          {error && <p className="text-sm text-red-600 mb-3">{error}</p>}

          <button
            onClick={handleUpdate}
            className="bg-emerald-500 text-white px-4 py-2 rounded"
          >
            Update
          </button>
        </div>
      </div>
    </div>
  );
}
