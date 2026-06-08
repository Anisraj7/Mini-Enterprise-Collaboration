import { useState } from "react";

export default function ChannelFormModal({
  onClose,
  onSubmit,
  initialData = null,
}) {
  const [formData, setFormData] = useState({
    name: initialData?.name || "",
    description: initialData?.description || "",
    channel_type: initialData?.channel_type || "PUBLIC",
  });

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    setError("");

    const payload = {
      ...formData,
      name: formData.name.trim(),
      description: formData.description.trim(),
    };

    if (!payload.name) {
      setError("Channel name is required");
      return;
    }

    try {
      setLoading(true);

      await onSubmit(payload);
    } catch (err) {
      setError(err?.response?.data?.detail || "Failed to save channel");
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
          rounded-xl
          w-full
          max-w-md
          p-6
          shadow-lg
        "
      >
        <div className="flex justify-between mb-5">
          <h2 className="font-bold text-lg">
            {initialData ? "Edit Channel" : "Create Channel"}
          </h2>

          <button onClick={onClose} disabled={loading}>
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
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
              Channel Name
            </label>

            <input
              type="text"
              name="name"
              value={formData.name}
              onChange={handleChange}
              className="
                w-full
                border
                rounded-lg
                px-3 py-2
              "
              required
              maxLength={100}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Description
            </label>

            <textarea
              name="description"
              value={formData.description}
              onChange={handleChange}
              rows={3}
              className="
                w-full
                border
                rounded-lg
                px-3 py-2
              "
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-1">
              Channel Type
            </label>

            <select
              name="channel_type"
              value={formData.channel_type}
              onChange={handleChange}
              className="
                w-full
                border
                rounded-lg
                px-3 py-2
              "
            >
              <option value="PUBLIC">Public</option>

              <option value="PRIVATE">Private</option>

              <option value="ANNOUNCEMENT">Announcement</option>

              <option value="PROJECT">Project</option>
            </select>
          </div>

          <div className="flex justify-end gap-2">
            <button
              type="button"
              onClick={onClose}
              disabled={loading}
              className="
                border
                px-4 py-2
                rounded-lg
              "
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={loading}
              className="
                bg-blue-600
                text-white
                px-4 py-2
                rounded-lg
                disabled:opacity-50
              "
            >
              {loading ? "Saving..." : initialData ? "Update" : "Create"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
