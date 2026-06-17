import { format } from "date-fns";

export default function ChannelMessageItem({ message }) {
  const isDeleted = !!message.deleted_at;

  return (
    <div className="bg-white rounded-xl border p-4">
      <div className="flex items-start justify-between">
        <div>
          <div className="font-medium">
            {message.sender_name || `User #${message.sender_id}`}
          </div>

          <div className="text-xs text-gray-500">
            {message.created_at &&
              format(new Date(message.created_at), "dd MMM yyyy HH:mm")}

            {message.edited_at && <span className="ml-2">(edited)</span>}
          </div>
        </div>

        {/* Future edit/delete actions */}
        <div className="flex gap-2">
          <button
            disabled
            className="
              text-xs
              px-2
              py-1
              border
              rounded
              opacity-50
              cursor-not-allowed
            "
          >
            Edit
          </button>

          <button
            disabled
            className="
              text-xs
              px-2
              py-1
              border
              rounded
              opacity-50
              cursor-not-allowed
            "
          >
            Delete
          </button>
        </div>
      </div>

      <div className="mt-3">
        {isDeleted ? (
          <p className="italic text-gray-400">This message was deleted</p>
        ) : (
          <p className="whitespace-pre-wrap">{message.content}</p>
        )}
      </div>
    </div>
  );
}
