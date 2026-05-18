import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";

export default function EditTask() {
  const { id } = useParams();
  const navigate = useNavigate();

  const [loading, setLoading] = useState(true);
  const [updating, setUpdating] = useState(false);

  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

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
        setLoading(true);

        const response = await API.get(`/tasks/${id}`);
        const data = response.data;

        setTask({
          title: data.title || "",
          description: data.description || "",
          priority: data.priority || "medium",
          status: data.status || "todo",
          due_date: data.due_date
            ? data.due_date.slice(0, 16)
            : "",
        });
      } catch (err) {
        setError(
          err.response?.data?.detail ||
            "Unable to load task details."
        );
      } finally {
        setLoading(false);
      }
    };

    loadTask();
  }, [id]);

  const updateField = (key, value) => {
    setTask((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const handleUpdate = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    if (!task.title.trim()) {
      return setError("Task title is required.");
    }

    try {
      setUpdating(true);

      await API.put(`/tasks/${id}`, {
        ...task,
        due_date: task.due_date || null,
      });

      setSuccess("Task updated successfully.");

      setTimeout(() => {
        navigate("/dashboard");
      }, 1200);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to update task."
      );
    } finally {
      setUpdating(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-100">
        <Navbar />

        <div className="flex justify-center items-center h-[80vh]">
          <div className="bg-white px-6 py-4 rounded-xl shadow-md">
            <p className="text-gray-600 font-medium">
              Loading task details...
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />

      <div className="max-w-3xl mx-auto p-6">
        <div className="bg-white rounded-2xl shadow-xl overflow-hidden">
          
          {/* Header */}
          <div className="bg-emerald-600 px-6 py-5">
            <h1 className="text-2xl font-bold text-white">
              Edit Task
            </h1>

            <p className="text-emerald-100 text-sm mt-1">
              Update task details, priority, and status.
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleUpdate} className="p-6">

            {/* Error */}
            {error && (
              <div className="bg-red-100 border border-red-300 text-red-700 px-4 py-3 rounded-lg mb-5">
                {error}
              </div>
            )}

            {/* Success */}
            {success && (
              <div className="bg-green-100 border border-green-300 text-green-700 px-4 py-3 rounded-lg mb-5">
                {success}
              </div>
            )}

            {/* Title */}
            <div className="mb-5">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Task Title
              </label>

              <input
                type="text"
                placeholder="Enter task title"
                value={task.title}
                onChange={(e) =>
                  updateField("title", e.target.value)
                }
                className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            {/* Description */}
            <div className="mb-5">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Description
              </label>

              <textarea
                rows={5}
                placeholder="Update task description..."
                value={task.description}
                onChange={(e) =>
                  updateField("description", e.target.value)
                }
                className="w-full border border-gray-300 rounded-xl px-4 py-3 resize-none focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            {/* Priority + Status */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
              
              {/* Priority */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Priority
                </label>

                <select
                  value={task.priority}
                  onChange={(e) =>
                    updateField("priority", e.target.value)
                  }
                  className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                >
                  <option value="low">🟢 Low</option>
                  <option value="medium">🟡 Medium</option>
                  <option value="high">🔴 High</option>
                </select>
              </div>

              {/* Status */}
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Status
                </label>

                <select
                  value={task.status}
                  onChange={(e) =>
                    updateField("status", e.target.value)
                  }
                  className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500"
                >
                  <option value="todo">Todo</option>
                  <option value="in_progress">
                    In Progress
                  </option>
                  <option value="review">Review</option>
                  <option value="done">Done</option>
                </select>
              </div>
            </div>

            {/* Due Date */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Due Date
              </label>

              <input
                type="datetime-local"
                value={task.due_date}
                onChange={(e) =>
                  updateField("due_date", e.target.value)
                }
                className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:outline-none focus:ring-2 focus:ring-emerald-500"
              />
            </div>

            {/* Buttons */}
            <div className="flex gap-4">
              <button
                type="submit"
                disabled={updating}
                className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-3 rounded-xl transition disabled:opacity-70"
              >
                {updating ? "Updating Task..." : "Update Task"}
              </button>

              <button
                type="button"
                onClick={() => navigate("/dashboard")}
                className="px-6 py-3 border border-gray-300 rounded-xl hover:bg-gray-100 transition"
              >
                Cancel
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}