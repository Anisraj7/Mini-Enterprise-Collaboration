import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import API from "../api/axios";

export default function CreateTask() {
  const navigate = useNavigate();

  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const [files, setFiles] = useState([]);

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

        setUsers(
          Array.isArray(response.data?.items)
            ? response.data.items.filter(
                (user) => user.role === "employee" || user.role === "manager",
              )
            : [],
        );
      } catch (err) {
        console.error(err);
        setUsers([]);
        setError("Unable to load users.");
      }
    };

    loadUsers();
  }, []);

  const updateForm = (key, value) => {
    setForm((prev) => ({
      ...prev,
      [key]: value,
    }));
  };

  const resetForm = () => {
    setForm({
      title: "",
      description: "",
      priority: "medium",
      status: "todo",
      due_date: "",
      assigned_to_id: "",
    });

    setFiles([]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");
    setSuccess("");

    if (!form.title.trim()) {
      return setError("Task title is required.");
    }

    try {
      setLoading(true);

      // Create task
      const response = await API.post("/tasks/", {
        title: form.title,
        description: form.description || null,
        priority: form.priority,
        status: form.status,
        due_date: form.due_date || null,
        assigned_to_id: form.assigned_to_id
          ? Number(form.assigned_to_id)
          : null,
      });

      const taskId = response.data.id;

      // Upload documents
      if (files.length > 0) {
        setUploading(true);

        await Promise.all(
          files.map(async (file) => {
            const formData = new FormData();
            formData.append("file", file);

            await API.post(`/documents/upload?task_id=${taskId}`, formData, {
              headers: {
                "Content-Type": "multipart/form-data",
              },
            });
          }),
        );
      }

      setSuccess("Task created successfully.");

      resetForm();

      setTimeout(() => {
        navigate("/dashboard");
      }, 1200);
    } catch (err) {
      setError(err.response?.data?.detail || "Failed to create task.");
    } finally {
      setLoading(false);
      setUploading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-3xl mx-auto p-6">
        <div className="bg-white shadow-xl rounded-2xl overflow-hidden">
          {/* Header */}
          <div className="bg-indigo-600 px-6 py-5">
            <h1 className="text-2xl font-bold text-white">Create New Task</h1>

            <p className="text-indigo-100 text-sm mt-1">
              Manage tasks, assign team members, and upload documents.
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="p-6">
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
                value={form.title}
                onChange={(e) => updateForm("title", e.target.value)}
                className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              />
            </div>

            {/* Description */}
            <div className="mb-5">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Description
              </label>

              <textarea
                rows={5}
                placeholder="Write task details..."
                value={form.description}
                onChange={(e) => updateForm("description", e.target.value)}
                className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:outline-none resize-none"
              />
            </div>

            {/* Priority & Status */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5 mb-5">
              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Priority
                </label>

                <select
                  value={form.priority}
                  onChange={(e) => updateForm("priority", e.target.value)}
                  className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                >
                  <option value="low">🟢 Low</option>
                  <option value="medium">🟡 Medium</option>
                  <option value="high">🔴 High</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-semibold text-gray-700 mb-2">
                  Status
                </label>

                <select
                  value={form.status}
                  onChange={(e) => updateForm("status", e.target.value)}
                  className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
                >
                  <option value="todo">Todo</option>
                  <option value="in_progress">In Progress</option>
                  <option value="review">Review</option>
                  <option value="done">Done</option>
                </select>
              </div>
            </div>

            {/* Due Date */}
            <div className="mb-5">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Due Date
              </label>

              <input
                type="datetime-local"
                value={form.due_date}
                onChange={(e) => updateForm("due_date", e.target.value)}
                className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              />
            </div>

            {/* Assign User */}
            <div className="mb-5">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Assign To
              </label>

              <select
                value={form.assigned_to_id}
                onChange={(e) => updateForm("assigned_to_id", e.target.value)}
                className="w-full border border-gray-300 rounded-xl px-4 py-3 focus:ring-2 focus:ring-indigo-500 focus:outline-none"
              >
                <option value="">Select User (Optional)</option>

                {Array.isArray(users) &&
                  users.map((user) => (
                    <option key={user.id} value={user.id}>
                      {user.name} ({user.role})
                    </option>
                  ))}
              </select>
            </div>

            {/* File Upload */}
            <div className="mb-6">
              <label className="block text-sm font-semibold text-gray-700 mb-2">
                Upload Documents
              </label>

              <input
                type="file"
                multiple
                onChange={(e) => setFiles(Array.from(e.target.files))}
                className="w-full border border-gray-300 rounded-xl px-4 py-3 bg-gray-50"
              />

              {/* File Preview */}
              {files.length > 0 && (
                <div className="mt-4 bg-gray-50 border rounded-xl p-4">
                  <p className="font-semibold text-sm text-gray-700 mb-2">
                    Selected Files
                  </p>

                  <ul className="space-y-2">
                    {files.map((file, index) => (
                      <li
                        key={index}
                        className="flex items-center justify-between bg-white px-3 py-2 rounded-lg border"
                      >
                        <span className="text-sm text-gray-700 truncate">
                          {file.name}
                        </span>

                        <span className="text-xs text-gray-500">
                          {(file.size / 1024).toFixed(1)} KB
                        </span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Buttons */}
            <div className="flex gap-4">
              <button
                type="submit"
                disabled={loading}
                className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold py-3 rounded-xl transition disabled:opacity-70"
              >
                {loading
                  ? uploading
                    ? "Uploading Files..."
                    : "Creating Task..."
                  : "Create Task"}
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
