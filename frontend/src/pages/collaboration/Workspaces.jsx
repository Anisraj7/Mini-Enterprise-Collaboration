import { useCallback, useEffect, useState } from "react";

import WorkspaceCard from "../../components/collaboration/workspace/WorkspaceCard";
import WorkspaceFormModal from "../../components/collaboration/workspace/WorkspaceFormModal";

import {
  getWorkspaces,
  createWorkspace,
  updateWorkspace,
} from "../../services/collaboration/workspaceService";

import {
  getPageItems,
} from "../../api/pagination";

export default function Workspaces() {
  const [workspaces, setWorkspaces] =
    useState([]);

  const [showModal, setShowModal] =
    useState(false);

  const [editingWorkspace, setEditingWorkspace] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const fetchWorkspaces =
    useCallback(async () => {
      try {
        setLoading(true);

        const data =
          await getWorkspaces();

        setWorkspaces(
          getPageItems(data)
        );
      } catch (error) {
        console.error(
          "Failed to load workspaces",
          error
        );

        setWorkspaces([]);
      } finally {
        setLoading(false);
      }
    }, []);

  useEffect(() => {
    fetchWorkspaces();
  }, [fetchWorkspaces]);

  const handleSubmit = async (
    payload
  ) => {
    try {
      if (editingWorkspace) {
        await updateWorkspace(
          editingWorkspace.id,
          payload
        );
      } else {
        await createWorkspace(
          payload
        );
      }

      setShowModal(false);

      setEditingWorkspace(null);

      await fetchWorkspaces();
    } catch (error) {
      console.error(
        "Failed to save workspace",
        error
      );
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">
            Workspaces
          </h1>

          <p className="text-gray-500">
            Manage collaboration
            workspaces
          </p>
        </div>

        <button
          onClick={() => {
            setEditingWorkspace(
              null
            );

            setShowModal(true);
          }}
          className="
            px-4
            py-2
            bg-blue-600
            text-white
            rounded-lg
            hover:bg-blue-700
          "
        >
          Create Workspace
        </button>
      </div>

      {loading ? (
        <div>Loading...</div>
      ) : workspaces.length === 0 ? (
        <div className="text-gray-500">
          No workspaces found
        </div>
      ) : (
        <div
          className="
            grid
            grid-cols-1
            md:grid-cols-2
            xl:grid-cols-3
            gap-4
          "
        >
          {workspaces.map(
            (workspace) => (
              <WorkspaceCard
                key={workspace.id}
                workspace={
                  workspace
                }
                onRefresh={
                  fetchWorkspaces
                }
                onEdit={(
                  workspace
                ) => {
                  setEditingWorkspace(
                    workspace
                  );

                  setShowModal(
                    true
                  );
                }}
              />
            )
          )}
        </div>
      )}

      {showModal && (
        <WorkspaceFormModal
          initialData={
            editingWorkspace
          }
          onClose={() => {
            setShowModal(
              false
            );

            setEditingWorkspace(
              null
            );
          }}
          onSubmit={
            handleSubmit
          }
        />
      )}
    </div>
  );
}