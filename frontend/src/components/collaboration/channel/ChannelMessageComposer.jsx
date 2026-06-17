import { useState } from "react";

export default function ChannelMessageComposer({
  onSend,
  loading = false,
}) {
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
      className="bg-white rounded-xl border p-4"
    >
      <textarea
        value={content}
        onChange={(e) =>
          setContent(e.target.value)
        }
        placeholder="Type a message..."
        rows={3}
        disabled={loading}
        className="
          w-full
          border
          rounded-lg
          p-3
          resize-none
        "
      />

      <div className="flex justify-end mt-3">
        <button
          type="submit"
          disabled={
            loading ||
            !content.trim()
          }
          className="
            px-4
            py-2
            bg-blue-600
            text-white
            rounded-lg
            disabled:opacity-50
          "
        >
          {loading
            ? "Sending..."
            : "Send"}
        </button>
      </div>
    </form>
  );
}