import { useState } from "react";

export default function ProjectFormModal({
  open,
  onClose,
  onSubmit,
}) {
  const [formData, setFormData] =
    useState({
      workspace_id: "",
      owner_id: "",
      name: "",
      description: "",
      priority: "MEDIUM",
      start_date: "",
      end_date: "",
    });

  if (!open) return null;

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]:
        e.target.value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(formData);
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center">
      <div className="bg-white rounded-lg p-6 w-full max-w-xl">
        <h2 className="text-lg font-semibold mb-4">
          Project
        </h2>

        <form
          onSubmit={handleSubmit}
          className="space-y-3"
        >
          <input
            name="workspace_id"
            placeholder="Workspace ID"
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          />

          <input
            name="owner_id"
            placeholder="Owner ID"
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          />

          <input
            name="name"
            placeholder="Project Name"
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          />

          <textarea
            name="description"
            placeholder="Description"
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          />

          <select
            name="priority"
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          >
            <option value="LOW">
              LOW
            </option>
            <option value="MEDIUM">
              MEDIUM
            </option>
            <option value="HIGH">
              HIGH
            </option>
            <option value="CRITICAL">
              CRITICAL
            </option>
          </select>

          <input
            type="date"
            name="start_date"
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          />

          <input
            type="date"
            name="end_date"
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          />

          <div className="flex gap-2">
            <button
              className="bg-blue-600 text-white px-4 py-2 rounded"
            >
              Save
            </button>

            <button
              type="button"
              onClick={onClose}
              className="border px-4 py-2 rounded"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}