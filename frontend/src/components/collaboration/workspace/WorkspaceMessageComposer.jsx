import { useState } from "react";

const WorkspaceMessageComposer = ({
  onSend,
  loading = false,
}) => {
  const [content, setContent] =
    useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const value = content.trim();

    if (!value) return;

    await onSend({
      content: value,
    });

    setContent("");
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white border rounded-xl shadow-sm"
    >
      <div className="p-4">
        <div className="mb-3">
          <label className="block text-sm font-medium text-gray-700 mb-2">
            New Message
          </label>

          <textarea
            rows={4}
            placeholder="Share an update, ask a question, or collaborate with your team..."
            value={content}
            onChange={(e) =>
              setContent(e.target.value)
            }
            disabled={loading}
            className="
              w-full
              border
              rounded-xl
              p-3
              resize-none
              focus:outline-none
              focus:ring-2
              focus:ring-indigo-500
              focus:border-indigo-500
            "
          />
        </div>

        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">
            {content.length} characters
          </span>

          <button
            type="submit"
            disabled={
              loading ||
              !content.trim()
            }
            className="
              px-4
              py-2
              bg-indigo-600
              text-white
              rounded-lg
              hover:bg-indigo-700
              disabled:opacity-50
              disabled:cursor-not-allowed
              transition
            "
          >
            {loading
              ? "Sending..."
              : "Send Message"}
          </button>
        </div>
      </div>
    </form>
  );
};

export default WorkspaceMessageComposer;