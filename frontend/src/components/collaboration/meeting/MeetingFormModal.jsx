import { useState } from "react";

export default function MeetingFormModal({
  open,
  onClose,
  onSubmit,
}) {
  const [formData, setFormData] =
    useState({
      project_id: "",
      title: "",
      description: "",
      start_time: "",
      end_time: "",
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
          Meeting
        </h2>

        <form
          onSubmit={handleSubmit}
          className="space-y-3"
        >
          <input
            name="project_id"
            placeholder="Project ID"
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          />

          <input
            name="title"
            placeholder="Meeting Title"
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          />

          <textarea
            name="description"
            placeholder="Description"
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          />

          <input
            type="datetime-local"
            name="start_time"
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          />

          <input
            type="datetime-local"
            name="end_time"
            onChange={handleChange}
            className="w-full border rounded px-3 py-2"
          />

          <div className="flex gap-2">
            <button className="bg-blue-600 text-white px-4 py-2 rounded">
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