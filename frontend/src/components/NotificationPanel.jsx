import { useEffect, useState } from "react";
import API from "../api/axios";

export default function NotificationPanel() {

  const [notifications, setNotifications] = useState([]);

  useEffect(() => {

    let ws;

    const init = async () => {
      const userResponse = await API.get("/auth/me");
      fetchNotifications();

      ws = new WebSocket(
        `ws://localhost:8000/ws/${userResponse.data.id}`
      );

      ws.onopen = () => {
        console.log("WebSocket Connected");
      };

      ws.onmessage = (event) => {

        const newNotification = {
          message: event.data,
          is_read: false
        };

        setNotifications((prev) => [
          newNotification,
          ...prev
        ]);
      };

      ws.onclose = () => {
        console.log("WebSocket Disconnected");
      };
    };

    init().catch(console.log);

    return () => {
      ws?.close();
    };

  }, []);

  // Fetch notifications from backend
  const fetchNotifications = async () => {

    try {

      const response = await API.get("/notifications/");

      setNotifications(response.data);

    } catch (error) {
      console.log(error);
    }
  };

  // Mark notification as read
  const markAsRead = async (id) => {

    try {

      await API.patch(`/notifications/${id}/read`);

      setNotifications((prev) =>
        prev.map((notif) =>
          notif.id === id
            ? { ...notif, is_read: true }
            : notif
        )
      );

    } catch (error) {
      console.log(error);
    }
  };

  // Count unread notifications
  const unreadCount = notifications.filter(
    (n) => !n.is_read
  ).length;

  return (
    <div className="w-full max-w-md bg-white shadow-lg rounded-xl p-4">

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

          notifications.map((notif, index) => (

            <div
              key={index}
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

              {!notif.is_read && notif.id && (
                <button
                  onClick={() => markAsRead(notif.id)}
                  className="text-xs bg-blue-500 text-white px-2 py-1 rounded"
                >
                  Read
                </button>
              )}

            </div>

          ))
        )}

      </div>

    </div>
  );
}
