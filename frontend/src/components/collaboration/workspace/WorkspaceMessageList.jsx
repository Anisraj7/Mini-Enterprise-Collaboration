import { useEffect, useState } from "react";

import {
  getWorkspaceMessages,
  createWorkspaceMessage,
} from "../../../services/collaboration/workspaceMessageService";

import WorkspaceMessageItem from "./WorkspaceMessageItem";
import WorkspaceMessageComposer from "./WorkspaceMessageComposer";

const WorkspaceMessageList = ({
  workspaceId,
}) => {
  const [messages, setMessages] =
    useState([]);

  const [loading, setLoading] =
    useState(false);

  const [sending, setSending] =
    useState(false);

  const [error, setError] =
    useState("");

  const [page, setPage] =
    useState(1);

  const [totalPages, setTotalPages] =
    useState(1);

  const loadMessages =
    async (currentPage = page) => {
      try {
        setLoading(true);
        setError("");

        const response =
          await getWorkspaceMessages(
            workspaceId,
            currentPage
          );

        setMessages(
          response.items || []
        );

        setTotalPages(
          response.pages || 1
        );
      } catch (err) {
        console.error(err);

        setError(
          "Failed to load messages"
        );
      } finally {
        setLoading(false);
      }
    };

  const handleSend =
    async (payload) => {
      try {
        setSending(true);

        await createWorkspaceMessage(
          workspaceId,
          payload
        );

        await loadMessages(1);

        setPage(1);
      } catch (err) {
        console.error(err);

        setError(
          "Failed to send message"
        );
      } finally {
        setSending(false);
      }
    };

  useEffect(() => {
    if (workspaceId) {
      loadMessages(page);
    }
  }, [workspaceId, page]);

  if (loading) {
    return (
      <div className="bg-white border rounded-xl p-8 text-center text-gray-500">
        Loading messages...
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <WorkspaceMessageComposer
        onSend={handleSend}
        loading={sending}
      />

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-600 rounded-xl p-3">
          {error}
        </div>
      )}

      <div className="space-y-3">
        {messages.length === 0 ? (
          <div className="bg-gray-50 border rounded-xl p-8 text-center text-gray-500">
            No messages yet.
            <div className="text-sm mt-1">
              Start the conversation by sending a message.
            </div>
          </div>
        ) : (
          messages.map(
            (message) => (
              <WorkspaceMessageItem
                key={message.id}
                message={message}
              />
            )
          )
        )}
      </div>

      {totalPages > 1 && (
        <div className="flex items-center justify-center gap-4 pt-2">
          <button
            className="px-4 py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={page <= 1}
            onClick={() =>
              setPage(
                (prev) => prev - 1
              )
            }
          >
            Previous
          </button>

          <span className="text-sm text-gray-600">
            Page {page} of{" "}
            {totalPages}
          </span>

          <button
            className="px-4 py-2 border rounded-lg hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            disabled={
              page >= totalPages
            }
            onClick={() =>
              setPage(
                (prev) => prev + 1
              )
            }
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
};

export default WorkspaceMessageList;