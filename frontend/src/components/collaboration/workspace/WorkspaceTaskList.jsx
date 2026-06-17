import { useEffect, useState } from "react";

import {
  getWorkspaceTasks,
  createWorkspaceTask,
} from "../../../services/collaboration/workspaceTaskService";

import WorkspaceTaskForm from "./WorkspaceTaskForm";

export default function WorkspaceTaskList({
  workspaceId,
  members = [],
}) {
  const [tasks, setTasks] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [creating, setCreating] =
    useState(false);

  const [showCreate, setShowCreate] =
    useState(false);

  const [error, setError] =
    useState("");

  const [page, setPage] =
    useState(1);

  const [pages, setPages] =
    useState(1);

  const loadTasks = async (
    currentPage = page
  ) => {
    try {
      setLoading(true);
      setError("");

      const response =
        await getWorkspaceTasks(
          workspaceId,
          currentPage
        );

      setTasks(
        response.items || []
      );

      setPages(
        response.pages || 1
      );
    } catch (err) {
      console.error(err);

      setError(
        "Failed to load tasks"
      );
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask =
    async (payload) => {
      try {
        setCreating(true);

        await createWorkspaceTask(
          workspaceId,
          payload
        );

        setShowCreate(false);

        await loadTasks(1);
      } catch (err) {
        console.error(err);

        setError(
          "Failed to create task"
        );
      } finally {
        setCreating(false);
      }
    };

  useEffect(() => {
    if (workspaceId) {
      loadTasks(page);
    }
  }, [workspaceId, page]);

  if (loading) {
    return (
      <div className="text-center py-6">
        Loading tasks...
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between">
        <h2 className="text-xl font-semibold">
          Workspace Tasks
        </h2>

        <button
          onClick={() =>
            setShowCreate(
              !showCreate
            )
          }
          className="
            px-4
            py-2
            bg-blue-600
            text-white
            rounded-lg
          "
        >
          New Task
        </button>
      </div>

      {showCreate && (
        <div className="bg-white border rounded-xl p-5">
          <WorkspaceTaskForm
            members={members}
            onSubmit={
              handleCreateTask
            }
            loading={creating}
          />
        </div>
      )}

      {error && (
        <div
          className="
            bg-red-100
            text-red-700
            p-3
            rounded-lg
          "
        >
          {error}
        </div>
      )}

      {tasks.length === 0 ? (
        <div
          className="
            bg-white
            border
            rounded-xl
            p-6
            text-center
            text-gray-500
          "
        >
          No tasks found
        </div>
      ) : (
        <div className="space-y-3">
          {tasks.map((task) => (
            <div
              key={task.id}
              className="
                bg-white
                border
                rounded-xl
                p-4
              "
            >
              <div className="flex justify-between items-start">
                <div>
                  <h3 className="font-semibold">
                    {task.title}
                  </h3>

                  <p className="text-sm text-gray-500 mt-1">
                    {task.description}
                  </p>
                </div>

                <span
                  className="
                    px-2
                    py-1
                    rounded
                    text-xs
                    bg-gray-100
                  "
                >
                  {task.status}
                </span>
              </div>

              <div className="mt-3 flex gap-2 flex-wrap text-xs text-gray-500">
                <span>
                  Priority:
                  {" "}
                  {task.priority}
                </span>

                {task.assigned_to_id && (
                  <span>
                    Assigned:
                    {" "}
                    #{task.assigned_to_id}
                  </span>
                )}

                {task.due_date && (
                  <span>
                    Due:
                    {" "}
                    {new Date(
                      task.due_date
                    ).toLocaleDateString()}
                  </span>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {pages > 1 && (
        <div className="flex justify-center gap-3">
          <button
            disabled={page <= 1}
            onClick={() =>
              setPage(
                (prev) =>
                  prev - 1
              )
            }
            className="
              px-3
              py-2
              border
              rounded-lg
              disabled:opacity-50
            "
          >
            Previous
          </button>

          <span className="self-center">
            Page {page} of {pages}
          </span>

          <button
            disabled={
              page >= pages
            }
            onClick={() =>
              setPage(
                (prev) =>
                  prev + 1
              )
            }
            className="
              px-3
              py-2
              border
              rounded-lg
              disabled:opacity-50
            "
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}