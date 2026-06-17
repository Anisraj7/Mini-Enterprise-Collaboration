import { format } from "date-fns";

const WorkspaceMessageItem = ({ message }) => {
  const isDeleted = !!message.deleted_at;

  return (
    <div className="bg-white border rounded-xl p-4 shadow-sm hover:shadow-md transition">
      <div className="flex justify-between items-start">
        <div>
          <div className="flex items-center gap-2">
            <div className="h-10 w-10 rounded-full bg-indigo-100 flex items-center justify-center font-semibold text-indigo-700">
              U
            </div>

            <div>
              <div className="font-semibold text-gray-900">
                {message.sender_name || `User #${message.sender_id}`}
              </div>

              <div className="text-xs text-gray-500">
                {message.created_at &&
                  format(new Date(message.created_at), "dd MMM yyyy • HH:mm")}

                {message.edited_at && (
                  <span className="ml-2 text-amber-600">• Edited</span>
                )}
              </div>
            </div>
          </div>
        </div>

        <div className="flex gap-2">
          <button
            disabled
            className="px-3 py-1 text-xs border rounded-lg text-gray-400 cursor-not-allowed"
            title="Coming soon"
          >
            Edit
          </button>

          <button
            disabled
            className="px-3 py-1 text-xs border rounded-lg text-gray-400 cursor-not-allowed"
            title="Coming soon"
          >
            Delete
          </button>
        </div>
      </div>

      <div className="mt-4 pt-4 border-t">
        {isDeleted ? (
          <div className="italic text-gray-400">This message was deleted</div>
        ) : (
          <div
            className="text-gray-700 leading-relaxed"
            style={{
              whiteSpace: "pre-wrap",
            }}
          >
            {message.content}
          </div>
        )}
      </div>
    </div>
  );
};

export default WorkspaceMessageItem;
