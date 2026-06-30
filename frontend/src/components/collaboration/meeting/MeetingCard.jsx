import { Link } from "react-router-dom";

export default function MeetingCard({
  meeting,
  onDelete,
}) {
  return (
    <div className="bg-white border rounded-lg p-4">
      <div className="flex justify-between">
        <div>
          <h3 className="font-semibold text-lg">
            {meeting.title}
          </h3>

          <p className="text-gray-600 mt-2">
            {meeting.description}
          </p>

          <p className="text-sm text-gray-500 mt-2">
            {meeting.start_time}
          </p>
        </div>

        <span className="px-2 py-1 rounded text-xs bg-blue-100 text-blue-800">
          {meeting.status}
        </span>
      </div>

      <div className="mt-4 flex gap-3">
        <Link
          to={`/meetings/${meeting.id}`}
          className="text-blue-600"
        >
          View
        </Link>

        <button
          onClick={() =>
            onDelete(meeting.id)
          }
          className="text-red-600"
        >
          Delete
        </button>
      </div>
    </div>
  );
}