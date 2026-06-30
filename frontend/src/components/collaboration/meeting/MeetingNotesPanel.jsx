import { useState } from "react";

export default function MeetingNotesPanel({
  notes,
  onAdd,
}) {
  const [note, setNote] =
    useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!note.trim()) return;

    onAdd(note);

    setNote("");
  };

  return (
    <div>
      <form
        onSubmit={handleSubmit}
        className="space-y-3"
      >
        <textarea
          value={note}
          onChange={(e) =>
            setNote(
              e.target.value
            )
          }
          placeholder="Meeting note"
          className="w-full border rounded px-3 py-2"
        />

        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Add Note
        </button>
      </form>

      <div className="mt-4 space-y-2">
        {notes.map((item) => (
          <div
            key={item.id}
            className="border rounded p-3"
          >
            {item.content}
          </div>
        ))}
      </div>
    </div>
  );
}