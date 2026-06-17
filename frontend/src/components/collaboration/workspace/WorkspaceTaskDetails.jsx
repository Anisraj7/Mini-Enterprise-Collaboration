import { useEffect, useState } from "react";

import {
  getWorkspaceTask,
  assignWorkspaceTask,
} from "../../../services/workspaceTaskService";

import {
  getTaskDocuments,
  uploadTaskDocument,
  deleteTaskDocument,
  downloadTaskDocument,
} from "../../../services/taskDocumentService";

export default function WorkspaceTaskDetails({
  workspaceId,
  taskId,
  members = [],
}) {
  const [task, setTask] =
    useState(null);

  const [documents, setDocuments] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [uploading, setUploading] =
    useState(false);

  const [assigning, setAssigning] =
    useState(false);

  const [selectedUser, setSelectedUser] =
    useState("");

  const [documentType, setDocumentType] =
    useState("OTHER");

  const [file, setFile] =
    useState(null);

  const loadData = async () => {
    try {
      setLoading(true);

      const [
        taskData,
        documentData,
      ] = await Promise.all([
        getWorkspaceTask(
          workspaceId,
          taskId
        ),
        getTaskDocuments(taskId),
      ]);

      setTask(taskData);

      setDocuments(
        documentData || []
      );

      setSelectedUser(
        taskData.assigned_to_id || ""
      );
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleAssign =
    async () => {
      if (!selectedUser)
        return;

      try {
        setAssigning(true);

        const updatedTask =
          await assignWorkspaceTask(
            workspaceId,
            taskId,
            Number(selectedUser)
          );

        setTask(updatedTask);
      } catch (err) {
        console.error(err);
      } finally {
        setAssigning(false);
      }
    };

  const handleUpload =
    async (e) => {
      e.preventDefault();

      if (!file) return;

      try {
        setUploading(true);

        const formData =
          new FormData();

        formData.append(
          "document_type",
          documentType
        );

        formData.append(
          "file",
          file
        );

        await uploadTaskDocument(
          taskId,
          formData
        );

        setFile(null);

        await loadData();
      } catch (err) {
        console.error(err);
      } finally {
        setUploading(false);
      }
    };

  const handleDelete =
    async (documentId) => {
      if (
        !window.confirm(
          "Delete document?"
        )
      ) {
        return;
      }

      try {
        await deleteTaskDocument(
          documentId
        );

        await loadData();
      } catch (err) {
        console.error(err);
      }
    };

  useEffect(() => {
    if (taskId) {
      loadData();
    }
  }, [taskId]);

  if (loading) {
    return (
      <div>
        Loading task...
      </div>
    );
  }

  if (!task) {
    return (
      <div>
        Task not found
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white border rounded-xl p-5">
        <h2 className="text-xl font-semibold">
          {task.title}
        </h2>

        <p className="mt-2 text-gray-600">
          {task.description}
        </p>

        <div className="mt-4 flex flex-wrap gap-3 text-sm">
          <span>
            Status:
            {" "}
            {task.status}
          </span>

          <span>
            Priority:
            {" "}
            {task.priority}
          </span>

          {task.due_date && (
            <span>
              Due:
              {" "}
              {new Date(
                task.due_date
              ).toLocaleString()}
            </span>
          )}
        </div>
      </div>

      <div className="bg-white border rounded-xl p-5">
        <h3 className="font-semibold mb-4">
          Assignment
        </h3>

        <div className="flex gap-3">
          <select
            value={
              selectedUser
            }
            onChange={(e) =>
              setSelectedUser(
                e.target.value
              )
            }
            className="border rounded-lg p-2"
          >
            <option value="">
              Select User
            </option>

            {members.map(
              (member) => (
                <option
                  key={
                    member.user_id
                  }
                  value={
                    member.user_id
                  }
                >
                  User #
                  {
                    member.user_id
                  }
                </option>
              )
            )}
          </select>

          <button
            onClick={
              handleAssign
            }
            disabled={
              assigning
            }
            className="
              px-4
              py-2
              bg-blue-600
              text-white
              rounded-lg
            "
          >
            {assigning
              ? "Assigning..."
              : "Assign"}
          </button>
        </div>
      </div>

      <div className="bg-white border rounded-xl p-5">
        <h3 className="font-semibold mb-4">
          Documents
        </h3>

        <form
          onSubmit={
            handleUpload
          }
          className="space-y-3 mb-6"
        >
          <select
            value={
              documentType
            }
            onChange={(e) =>
              setDocumentType(
                e.target.value
              )
            }
            className="border rounded-lg p-2"
          >
            <option value="REQUIREMENT">
              REQUIREMENT
            </option>

            <option value="SPECIFICATION">
              SPECIFICATION
            </option>

            <option value="REFERENCE">
              REFERENCE
            </option>

            <option value="DELIVERABLE">
              DELIVERABLE
            </option>

            <option value="OTHER">
              OTHER
            </option>
          </select>

          <input
            type="file"
            onChange={(e) =>
              setFile(
                e.target.files[0]
              )
            }
          />

          <button
            type="submit"
            disabled={
              uploading
            }
            className="
              px-4
              py-2
              bg-green-600
              text-white
              rounded-lg
            "
          >
            {uploading
              ? "Uploading..."
              : "Upload"}
          </button>
        </form>

        {documents.length === 0 ? (
          <p className="text-gray-500">
            No documents uploaded
          </p>
        ) : (
          <div className="space-y-2">
            {documents.map(
              (doc) => (
                <div
                  key={doc.id}
                  className="
                    border
                    rounded-lg
                    p-3
                    flex
                    justify-between
                    items-center
                  "
                >
                  <div>
                    <div className="font-medium">
                      {doc.file_name}
                    </div>

                    <div className="text-xs text-gray-500">
                      {
                        doc.document_type
                      }
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() =>
                        downloadTaskDocument(
                          doc.id
                        )
                      }
                      className="
                        px-3
                        py-1
                        border
                        rounded
                      "
                    >
                      Download
                    </button>

                    <button
                      onClick={() =>
                        handleDelete(
                          doc.id
                        )
                      }
                      className="
                        px-3
                        py-1
                        border
                        rounded
                        text-red-600
                      "
                    >
                      Delete
                    </button>
                  </div>
                </div>
              )
            )}
          </div>
        )}
      </div>
    </div>
  );
}