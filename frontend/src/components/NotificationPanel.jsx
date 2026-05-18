import { useCallback, useEffect, useState } from "react";
import API from "../api/axios";
import { getUserWebSocketUrl } from "../api/websocket";
import { getPageItems } from "../api/pagination";

export default function NotificationPanel({
  onUnreadCountChange,
}) {

  const [notifications, setNotifications] = useState([]);

  // Fetch notifications from backend
  const fetchNotifications = useCallback(async () => {

    try {

      const response = await API.get("/notifications/");

      // FIXED PAGINATION RESPONSE
      setNotifications(getPageItems(response.data));

    } catch (error) {
      console.log(error);
    }

  }, []);

  useEffect(() => {

    let ws;

    const init = async () => {

      try {

        const userResponse = await API.get("/auth/me");

        await fetchNotifications();

        ws = new WebSocket(
          getUserWebSocketUrl(userResponse.data.id)
        );

        ws.onopen = () => {
          console.log("WebSocket Connected");
        };

        ws.onmessage = (event) => {

          let parsedMessage;

          try {

            parsedMessage = JSON.parse(event.data);

          } catch {

            parsedMessage = {
              message: event.data
            };
          }

          const newNotification = {
            id: Date.now(),
            message:
              parsedMessage.message ||
              "New notification",
            is_read: false,
            created_at: new Date(),
          };

          setNotifications((prev) => [
            newNotification,
            ...(Array.isArray(prev)
              ? prev
              : []),
          ]);
        };

        ws.onclose = () => {
          console.log("WebSocket Disconnected");
        };

      } catch (error) {

        console.log(error);
      }
    };

    init();

    return () => {
      ws?.close();
    };

  }, [fetchNotifications]);

  // Mark notification as read
  const markAsRead = async (id) => {

    try {

      await API.patch(
        `/notifications/${id}/read`
      );

      setNotifications((prev) =>
        prev.map((notif) =>
          notif.id === id
            ? {
                ...notif,
                is_read: true
              }
            : notif
        )
      );

    } catch (error) {

      console.log(error);
    }
  };

  // SAFE FILTER
  const unreadCount = Array.isArray(
    notifications
  )
    ? notifications.filter(
        (n) => !n.is_read
      ).length
    : 0;

  useEffect(() => {

    onUnreadCountChange?.(
      unreadCount
    );

  }, [
    onUnreadCountChange,
    unreadCount
  ]);

  return (

    <div className="w-full max-w-md bg-white shadow-2xl rounded-xl p-4 border border-gray-200">

      {/* Header */}
      <div className="flex justify-between items-center mb-4">

        <h2 className="text-xl font-bold">
          Notifications
        </h2>

        <span className="bg-red-500 text-white text-sm px-2 py-1 rounded-full">
          {unreadCount}
        </span>

      </div>

      {/* Notifications List */}
      <div className="space-y-3 max-h-[400px] overflow-y-auto">

        {notifications.length === 0 ? (

          <p className="text-gray-500">
            No notifications
          </p>

        ) : (

          notifications.map(
            (notif, index) => (

              <div
                key={notif.id || index}
                className={`p-3 rounded-lg border flex justify-between items-center ${
                  notif.is_read
                    ? "bg-gray-100"
                    : "bg-blue-50 border-blue-400"
                }`}
              >

                <div>

                  <p className="text-sm font-medium">
                    {notif.message}
                  </p>

                  {notif.created_at && (

                    <p className="text-xs text-gray-500 mt-1">

                      {new Date(
                        notif.created_at
                      ).toLocaleString()}

                    </p>

                  )}

                </div>

                {!notif.is_read &&
                  notif.id && (

                  <button
                    onClick={() =>
                      markAsRead(
                        notif.id
                      )
                    }
                    className="text-xs bg-blue-500 text-white px-2 py-1 rounded"
                  >
                    Read
                  </button>

                )}

              </div>

            )
          )

        )}

      </div>

    </div>
  );
}
