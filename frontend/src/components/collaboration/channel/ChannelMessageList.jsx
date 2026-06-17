import { useEffect, useState } from "react";

import {
  getChannelMessages,
  createChannelMessage,
} from "../../../services/collaboration/channelMessageService";

import ChannelMessageComposer from "./ChannelMessageComposer";
import ChannelMessageItem from "./ChannelMessageItem";

export default function ChannelMessageList({
  channelId,
}) {
  const [messages, setMessages] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [sending, setSending] =
    useState(false);

  const [error, setError] =
    useState("");

  const [page, setPage] =
    useState(1);

  const [totalPages, setTotalPages] =
    useState(1);

  const loadMessages = async (
    currentPage = page
  ) => {
    try {
      setLoading(true);
      setError("");

      const response =
        await getChannelMessages(
          channelId,
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

  const handleSend = async (
    payload
  ) => {
    try {
      setSending(true);

      await createChannelMessage(
        channelId,
        payload
      );

      setPage(1);

      await loadMessages(1);
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
    if (channelId) {
      loadMessages(page);
    }
  }, [channelId, page]);

  if (loading) {
    return (
      <div className="text-center py-6">
        Loading messages...
      </div>
    );
  }

  return (
    <div className="space-y-4">
      <ChannelMessageComposer
        onSend={handleSend}
        loading={sending}
      />

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

      {messages.length === 0 ? (
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
          No messages found
        </div>
      ) : (
        <div className="space-y-3">
          {messages.map(
            (message) => (
              <ChannelMessageItem
                key={message.id}
                message={message}
              />
            )
          )}
        </div>
      )}

      {totalPages > 1 && (
        <div className="flex justify-center gap-3 pt-2">
          <button
            onClick={() =>
              setPage(
                (prev) =>
                  prev - 1
              )
            }
            disabled={page <= 1}
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

          <span className="self-center text-sm">
            Page {page} of{" "}
            {totalPages}
          </span>

          <button
            onClick={() =>
              setPage(
                (prev) =>
                  prev + 1
              )
            }
            disabled={
              page >= totalPages
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