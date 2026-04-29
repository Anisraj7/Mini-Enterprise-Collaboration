import { useEffect, useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";

export default function Activity() {
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    API.get("/activity/")
      .then((res) => setLogs(res.data))
      .catch((err) => setError(err.response?.data?.detail || "Unable to load activity logs."));
  }, []);

  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar />
      <div className="p-6 max-w-5xl mx-auto">
        <h1 className="text-2xl font-bold mb-4">Activity Logs</h1>
        {error && <p className="text-sm text-red-600 mb-4">{error}</p>}
        <div className="space-y-2">
          {logs.map((log) => (
            <div key={log.id} className="bg-white p-3 rounded shadow">
              <p><b>{log.action}</b> on {log.entity_type} #{log.entity_id}</p>
              <p className="text-xs text-gray-500">User {log.user_id} - {new Date(log.created_at).toLocaleString()}</p>
            </div>
          ))}
          {logs.length === 0 && !error && <p className="text-sm text-gray-500">No activity yet.</p>}
        </div>
      </div>
    </div>
  );
}
