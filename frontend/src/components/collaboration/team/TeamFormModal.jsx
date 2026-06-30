import { useState, useEffect } from "react";

export default function TeamFormModal({
  open,
  onClose,
  onSubmit,
  initialData = null,
}) {
  const [formData, setFormData] =
    useState({
      workspace_id: "",
      name: "",
      description: "",
    });

  useEffect(() => {
    if (initialData) {
      setFormData({
        workspace_id:
          initialData.workspace_id || "",
        name:
          initialData.name || "",
        description:
          initialData.description || "",
      });
    }
  }, [initialData]);

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
      <div className="bg-white rounded-lg p-6 w-full max-w-lg">
        <h2 className="text-lg font-semibold mb-4">
          Team
        </h2>

        <form
          onSubmit={handleSubmit}
          className="space-y-3"
        >
          <input
            name="workspace_id"
            value={
              formData.workspace_id
            }
            onChange={handleChange}
            placeholder="Workspace ID"
            className="w-full border rounded px-3 py-2"
          />

          <input
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Team Name"
            className="w-full border rounded px-3 py-2"
          />

          <textarea
            name="description"
            value={
              formData.description
            }
            onChange={handleChange}
            placeholder="Description"
            className="w-full border rounded px-3 py-2"
          />

          <div className="flex gap-2">
            <button
              type="submit"
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