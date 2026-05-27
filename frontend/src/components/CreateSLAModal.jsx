import { useState } from "react";

import API from "../api/axios";

export default function CreateSLAModal({
  isOpen,
  onClose,
  onSuccess,
}) {
  const [formData, setFormData] =
    useState({
      module_name: "Task",
      priority: "Low",
      allowed_hours: "",
      escalation_enabled: false,
      escalation_after_hours: "",
      is_active: true,
    });

  const [loading, setLoading] =
    useState(false);

  if (!isOpen) return null;

  const handleChange = (e) => {
    const { name, value, type, checked } =
      e.target;

    setFormData({
      ...formData,
      [name]:
        type === "checkbox"
          ? checked
          : value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setLoading(true);

      await API.post("/sla-rules", {
        ...formData,
        allowed_hours: Number(formData.allowed_hours),
        escalation_after_hours: formData.escalation_enabled
          ? Number(formData.escalation_after_hours)
          : null,
      });

      onSuccess();
      onClose();
    } catch (error) {
      console.error(error);
      alert("Failed to create SLA rule");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl shadow-lg p-6 w-full max-w-lg">
        <div className="flex justify-between items-center mb-5">
          <h2 className="text-2xl font-bold">
            Create SLA Rule
          </h2>

          <button
            onClick={onClose}
            className="text-gray-500 text-xl"
          >
            ×
          </button>
        </div>

        <form
          onSubmit={handleSubmit}
          className="space-y-4"
        >
          {/* Module */}
          <div>
            <label className="block mb-1 font-medium">
              Module
            </label>

            <select
              name="module_name"
              value={
                formData.module_name
              }
              onChange={handleChange}
              className="w-full border rounded-lg px-3 py-2"
            >
              <option value="Task">
                Task
              </option>
              <option value="Approval">
                Approval
              </option>
            </select>
          </div>

          {/* Priority */}
          <div>
            <label className="block mb-1 font-medium">
              Priority
            </label>

            <select
              name="priority"
              value={formData.priority}
              onChange={handleChange}
              className="w-full border rounded-lg px-3 py-2"
            >
              <option value="Low">
                Low
              </option>
              <option value="Medium">
                Medium
              </option>
              <option value="High">
                High
              </option>
            </select>
          </div>

          {/* Allowed Hours */}
          <div>
            <label className="block mb-1 font-medium">
              Allowed Hours
            </label>

            <input
              type="number"
              name="allowed_hours"
              value={
                formData.allowed_hours
              }
              onChange={handleChange}
              required
              min="1"
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>

          {/* Escalation Enabled */}
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              name="escalation_enabled"
              checked={
                formData.escalation_enabled
              }
              onChange={handleChange}
            />

            <label>
              Escalation Enabled
            </label>
          </div>

          {/* Escalation Hours */}
          {formData.escalation_enabled && (
            <div>
              <label className="block mb-1 font-medium">
                Escalation After
                Hours
              </label>

              <input
                type="number"
                name="escalation_after_hours"
                value={
                  formData.escalation_after_hours
                }
                onChange={handleChange}
                required
                min="1"
                className="w-full border rounded-lg px-3 py-2"
              />
            </div>
          )}

          {/* Active */}
          <div className="flex items-center gap-2">
            <input
              type="checkbox"
              name="is_active"
              checked={
                formData.is_active
              }
              onChange={handleChange}
            />

            <label>
              Active Rule
            </label>
          </div>

          {/* Buttons */}
          <div className="flex justify-end gap-3 pt-4">
            <button
              type="button"
              onClick={onClose}
              className="border px-4 py-2 rounded-lg"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg"
            >
              {loading
                ? "Creating..."
                : "Create Rule"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
