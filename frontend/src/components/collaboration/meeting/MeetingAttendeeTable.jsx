import { useState } from "react";

export default function MeetingAttendees({
  attendees = [],
  onAdd,
  onRemove,
}) {
  const [userId, setUserId] =
    useState("");

  const handleSubmit = (e) => {
    e.preventDefault();

    onAdd({
      user_id: Number(userId),
    });

    setUserId("");
  };

  return (
    <div className="bg-white border rounded-lg p-4">
      <h2 className="text-lg font-semibold mb-4">
        Meeting Attendees
      </h2>

      <form
        onSubmit={handleSubmit}
        className="flex gap-3 mb-6"
      >
        <input
          type="number"
          value={userId}
          onChange={(e) =>
            setUserId(
              e.target.value
            )
          }
          placeholder="User ID"
          className="border rounded px-3 py-2"
        />

        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Add Attendee
        </button>
      </form>

      <table className="w-full">
        <thead>
          <tr className="border-b">
            <th className="p-2 text-left">
              User ID
            </th>

            <th className="p-2 text-left">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          {attendees.map(
            (attendee) => (
              <tr
                key={
                  attendee.id ||
                  attendee.user_id
                }
                className="border-b"
              >
                <td className="p-2">
                  {
                    attendee.user_id
                  }
                </td>

                <td className="p-2">
                  <button
                    onClick={() =>
                      onRemove(
                        attendee.user_id
                      )
                    }
                    className="text-red-600"
                  >
                    Remove
                  </button>
                </td>
              </tr>
            )
          )}

          {!attendees.length && (
            <tr>
              <td
                colSpan={2}
                className="p-4 text-center text-gray-500"
              >
                No attendees found
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}