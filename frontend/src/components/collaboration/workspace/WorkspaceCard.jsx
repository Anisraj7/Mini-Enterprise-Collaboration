import {
  Archive,
  RotateCcw,
  Users,
  Calendar,
  Pencil,
} from "lucide-react";

import { Link } from "react-router-dom";

import {
  archiveWorkspace,
  restoreWorkspace,
} from "../../../services/collaboration/workspaceService";

export default function WorkspaceCard({
  workspace,
  onRefresh,
  onEdit,
}) {
  const handleArchive = async () => {
    const confirmed = window.confirm(
      `Archive workspace "${workspace.name}"?`
    );

    if (!confirmed) return;

    try {
      await archiveWorkspace(
        workspace.id
      );

      await onRefresh();
    } catch (error) {
      console.error(error);
    }
  };

  const handleRestore = async () => {
    try {
      await restoreWorkspace(
        workspace.id
      );

      await onRefresh();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div
      className={`
        bg-white
        rounded-xl
        border
        shadow-sm
        p-5
        transition
        hover:shadow-md
        ${
          workspace.is_archived
            ? "opacity-75"
            : ""
        }
      `}
    >
      <div className="flex justify-between items-start">
        <div className="flex gap-3">
          <div
            className="
              w-12 h-12
              rounded-full
              bg-blue-100
              flex items-center justify-center
              font-bold
              text-blue-700
            "
          >
            {workspace.name
              ?.charAt(0)
              ?.toUpperCase()}
          </div>

          <div>
            <Link
              to={`/workspaces/${workspace.id}`}
            >
              <h3
                className="
                  font-bold
                  text-lg
                  hover:text-blue-600
                "
              >
                {workspace.name}
              </h3>
            </Link>

            <p className="text-sm text-gray-500">
              {workspace.description ||
                "No description"}
            </p>
          </div>
        </div>

        <div className="flex flex-col gap-2 items-end">
          <span
            className={`px-2 py-1 text-xs rounded-full ${
              workspace.visibility ===
              "PUBLIC"
                ? "bg-green-100 text-green-700"
                : "bg-orange-100 text-orange-700"
            }`}
          >
            {workspace.visibility}
          </span>

          {workspace.is_archived && (
            <span
              className="
                px-2 py-1
                text-xs
                rounded-full
                bg-red-100
                text-red-700
              "
            >
              ARCHIVED
            </span>
          )}
        </div>
      </div>

      <div
        className="
          mt-4
          flex
          items-center
          gap-4
          text-gray-500
          text-sm
        "
      >
        <div className="flex items-center gap-1">
          <Users size={16} />
          <span>Workspace</span>
        </div>

        {workspace.created_at && (
          <div className="flex items-center gap-1">
            <Calendar size={16} />
            <span>
              {new Date(
                workspace.created_at
              ).toLocaleDateString()}
            </span>
          </div>
        )}
      </div>

      <div className="mt-5 flex gap-2">
        <button
          onClick={() =>
            onEdit(workspace)
          }
          className="
            flex items-center gap-2
            px-3 py-2
            rounded-lg
            bg-blue-100
            text-blue-700
            hover:bg-blue-200
          "
        >
          <Pencil size={16} />
          Edit
        </button>

        {workspace.is_archived ? (
          <button
            onClick={handleRestore}
            className="
              flex items-center gap-2
              px-3 py-2
              rounded-lg
              bg-green-100
              text-green-700
              hover:bg-green-200
            "
          >
            <RotateCcw size={16} />
            Restore
          </button>
        ) : (
          <button
            onClick={handleArchive}
            className="
              flex items-center gap-2
              px-3 py-2
              rounded-lg
              bg-red-100
              text-red-700
              hover:bg-red-200
            "
          >
            <Archive size={16} />
            Archive
          </button>
        )}
      </div>
    </div>
  );
}