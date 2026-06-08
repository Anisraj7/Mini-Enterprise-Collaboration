import { useState } from "react";

export default function WorkspaceFormModal({
  onClose,
  onSubmit,
  initialData = null,
}) {
  const [formData, setFormData] =
    useState({
      name:
        initialData?.name || "",
      description:
        initialData?.description ||
        "",
      avatar_url:
        initialData?.avatar_url ||
        "",
      visibility:
        initialData?.visibility ||
        "PUBLIC",
    });

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState("");

  const handleChange = (
    e
  ) => {
    setFormData({
      ...formData,
      [e.target.name]:
        e.target.value,
    });
  };

  const handleSubmit = async (
    e
  ) => {
    e.preventDefault();

    setError("");

    const payload = {
      ...formData,
      name:
        formData.name.trim(),
      description:
        formData.description.trim(),
    };

    if (!payload.name) {
      setError(
        "Workspace name is required"
      );

      return;
    }

    try {
      setLoading(true);

      await onSubmit(
        payload
      );
    } catch (err) {
      setError(
        err?.response?.data
          ?.detail ||
          "Failed to save workspace"
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div
      className="
        fixed inset-0
        bg-black/40
        flex justify-center items-center
        z-50
      "
    >
      <div
        className="
          bg-white
          w-full max-w-lg
          rounded-xl
          shadow-lg
          p-6
        "
      >
        <div className="flex justify-between items-center mb-5">
          <h2 className="text-xl font-bold">
            {initialData
              ? "Edit Workspace"
              : "Create Workspace"}
          </h2>

          <button
            onClick={onClose}
            className="text-gray-500 hover:text-black"
          >
            ✕
          </button>
        </div>

        <form
          onSubmit={
            handleSubmit
          }
          className="space-y-4"
        >
          {error && (
            <div
              className="
                bg-red-100
                text-red-700
                px-3 py-2
                rounded-lg
                text-sm
              "
            >
              {error}
            </div>
          )}

          <div>
            <label className="block text-sm font-medium mb-1">
              Name
            </label>

            <input
              type="text"
              name="name"
              value={
                formData.name
              }
              onChange={
                handleChange
              }
              className="w-full border rounded-lg px-3 py-2"
              required
              maxLength={150}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Description
            </label>

            <textarea
              name="description"
              value={
                formData.description
              }
              onChange={
                handleChange
              }
              rows={3}
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Avatar URL
            </label>

            <input
              type="text"
              name="avatar_url"
              value={
                formData.avatar_url
              }
              onChange={
                handleChange
              }
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Visibility
            </label>

            <select
              name="visibility"
              value={
                formData.visibility
              }
              onChange={
                handleChange
              }
              className="w-full border rounded-lg px-3 py-2"
            >
              <option value="PUBLIC">
                Public
              </option>

              <option value="PRIVATE">
                Private
              </option>
            </select>
          </div>

          <div className="flex justify-end gap-3 pt-3">
            <button
              type="button"
              onClick={
                onClose
              }
              disabled={
                loading
              }
              className="
                px-4 py-2
                border
                rounded-lg
              "
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={
                loading
              }
              className="
                px-4 py-2
                bg-blue-600
                text-white
                rounded-lg
                disabled:opacity-50
              "
            >
              {loading
                ? "Saving..."
                : initialData
                ? "Update"
                : "Create"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}