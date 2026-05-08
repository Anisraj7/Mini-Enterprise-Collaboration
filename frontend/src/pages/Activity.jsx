import { useEffect, useMemo, useState } from "react";

import {
  CalendarDays,
  ChevronRight,
  RefreshCw,
  Search,
  User,
  Filter,
} from "lucide-react";

import toast from "react-hot-toast";

import API from "../api/axios";
import Navbar from "../components/Navbar";

export default function Activity() {

  const [logs, setLogs] = useState([]);

  const [groupedLogs, setGroupedLogs] =
    useState({});

  const [expanded, setExpanded] =
    useState({});

  const [search, setSearch] =
    useState("");

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  // FETCH LOGS
  const fetchLogs = async () => {

    try {

      setLoading(true);

      const response = await API.get(
        "/activity/"
      );

      setLogs(response.data);

      setError("");

    } catch (err) {

      setError(
        err.response?.data?.detail ||
        "Unable to load activity logs"
      );

    } finally {

      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  // WEBSOCKET
  useEffect(() => {

    const ws = new WebSocket(
      "ws://localhost:8000/ws/1"
    );

    ws.onmessage = async (event) => {

      toast.success(event.data);

      await fetchLogs();
    };

    return () => {
      ws.close();
    };

  }, []);

  // GROUP LOGS
  useEffect(() => {

    let filtered = [...logs];

    if (search) {

      filtered = filtered.filter(
        (log) =>
          log.action
            ?.toLowerCase()
            .includes(search.toLowerCase()) ||
          log.entity_type
            ?.toLowerCase()
            .includes(search.toLowerCase())
      );
    }

    const grouped = {};

    filtered.forEach((log) => {

      const key =
        `${log.entity_type}-${log.entity_id}`;

      if (!grouped[key]) {
        grouped[key] = [];
      }

      grouped[key].push(log);
    });

    setGroupedLogs(grouped);

    const initialExpanded = {};

    Object.keys(grouped).forEach((key) => {
      initialExpanded[key] = true;
    });

    setExpanded(initialExpanded);

  }, [logs, search]);

  // STATS
  const stats = useMemo(() => {

    return {
      total: logs.length,

      tasks: logs.filter(
        (l) => l.entity_type === "task"
      ).length,

      documents: logs.filter(
        (l) => l.entity_type === "document"
      ).length,

      approvals: logs.filter(
        (l) =>
          l.action
            ?.toLowerCase()
            .includes("approve")
      ).length,
    };

  }, [logs]);

  // TOGGLE GROUP
  const toggleGroup = (key) => {

    setExpanded((prev) => ({
      ...prev,
      [key]: !prev[key],
    }));
  };

  // STATUS BADGES
  const getStatusBadge = (status) => {

    const lower =
      status?.toLowerCase() || "";

    if (lower.includes("done")) {
      return "bg-green-100 text-green-700";
    }

    if (lower.includes("progress")) {
      return "bg-blue-100 text-blue-700";
    }

    return "bg-gray-100 text-gray-700";
  };

  return (

    <div className="bg-[#f4f5f7] min-h-screen">

      <Navbar />

      <div className="max-w-[1800px] mx-auto px-4 py-4">

        {/* TOP BAR */}
        <div className="bg-white border rounded-md p-3 mb-4 shadow-sm flex flex-wrap gap-3 items-center justify-between">

          <div className="flex items-center gap-2">

            <Filter
              size={15}
              className="text-gray-500"
            />

            <p className="text-sm font-medium text-gray-600">
              Enterprise Activity Logs
            </p>

          </div>

          <div className="flex items-center gap-3">

            <div className="relative">

              <Search
                className="absolute left-3 top-2.5 text-gray-400"
                size={15}
              />

              <input
                value={search}
                onChange={(e) =>
                  setSearch(e.target.value)
                }
                placeholder="Search activity"
                className="border rounded px-9 py-2 text-sm w-64"
              />

            </div>

            <button
              onClick={fetchLogs}
              className="border bg-white px-3 py-2 rounded text-sm flex items-center gap-2 hover:bg-gray-50"
            >

              <RefreshCw size={14} />

              Refresh

            </button>

          </div>

        </div>

        {/* SUMMARY BAR */}
        <div className="bg-white border rounded-md px-4 py-3 mb-4 shadow-sm flex flex-wrap gap-8 text-sm">

          <div>
            <span className="text-gray-500">
              Total Activities:
            </span>

            <span className="font-semibold ml-2">
              {stats.total}
            </span>
          </div>

          <div>
            <span className="text-gray-500">
              Tasks:
            </span>

            <span className="font-semibold ml-2 text-blue-600">
              {stats.tasks}
            </span>
          </div>

          <div>
            <span className="text-gray-500">
              Documents:
            </span>

            <span className="font-semibold ml-2 text-green-600">
              {stats.documents}
            </span>
          </div>

          <div>
            <span className="text-gray-500">
              Approvals:
            </span>

            <span className="font-semibold ml-2 text-purple-600">
              {stats.approvals}
            </span>
          </div>

        </div>

        {/* ERROR */}
        {error && (

          <div className="bg-red-100 text-red-600 border border-red-200 px-4 py-3 rounded mb-4 text-sm">
            {error}
          </div>

        )}

        {/* TABLE HEADER */}
        <div className="bg-white border rounded-t-md grid grid-cols-6 gap-4 px-4 py-3 text-xs uppercase font-semibold text-gray-500 tracking-wide">

          <div>Date</div>

          <div>Updated By</div>

          <div>Key</div>

          <div>Action</div>

          <div>Description</div>

          <div>Status</div>

        </div>

        {/* ACTIVITY TABLE */}
        <div className="border border-t-0 rounded-b-md overflow-hidden bg-white shadow-sm">

          {loading && (

            <div className="p-6 text-center text-gray-500 text-sm">
              Loading activity logs...
            </div>

          )}

          {!loading &&
            Object.entries(groupedLogs).map(
              ([key, entries]) => {

                const latest = entries[0];

                return (

                  <div
                    key={key}
                    className="border-b last:border-b-0"
                  >

                    {/* GROUP HEADER */}
                    <div
                      className="grid grid-cols-6 gap-4 px-4 py-3 hover:bg-gray-50 text-sm cursor-pointer"
                      onClick={() =>
                        toggleGroup(key)
                      }
                    >

                      <div className="flex items-center gap-2">

                        <ChevronRight
                          size={15}
                          className={`transition-transform ${
                            expanded[key]
                              ? "rotate-90"
                              : ""
                          }`}
                        />

                        <span>
                          {new Date(
                            latest.created_at
                          ).toLocaleString()}
                        </span>

                      </div>

                      <div className="text-blue-600 font-medium flex items-center gap-1">
                        <User size={13} />
                        User {latest.user_id}
                      </div>

                      <div className="font-medium text-indigo-600 uppercase">
                        {latest.entity_type}-
                        {latest.entity_id}
                      </div>

                      <div className="font-medium text-gray-700">
                        {latest.action}
                      </div>

                      <div className="text-gray-600 truncate">
                        {latest.description ||
                          "Enterprise workflow update"}
                      </div>

                      <div>

                        <span
                          className={`px-2 py-1 rounded text-xs font-semibold ${getStatusBadge(latest.status)}`}
                        >
                          {latest.status ||
                            "UPDATED"}
                        </span>

                      </div>

                    </div>

                    {/* EXPANDED HISTORY */}
                    {expanded[key] && (

                      <div className="bg-gray-50 border-t">

                        {entries.slice(1).map((log) => (

                          <div
                            key={log.id}
                            className="grid grid-cols-6 gap-4 px-4 py-2 text-sm border-b last:border-b-0 hover:bg-gray-100"
                          >

                            <div className="flex items-center gap-2 text-gray-500">

                              <CalendarDays size={13} />

                              {new Date(
                                log.created_at
                              ).toLocaleString()}

                            </div>

                            <div className="text-blue-600">
                              User {log.user_id}
                            </div>

                            <div className="font-medium text-indigo-600 uppercase">
                              {log.entity_type}-
                              {log.entity_id}
                            </div>

                            <div>
                              {log.action}
                            </div>

                            <div className="text-gray-500 truncate">
                              {log.description ||
                                "Workflow activity"}
                            </div>

                            <div>

                              <span
                                className={`px-2 py-1 rounded text-xs font-semibold ${getStatusBadge(log.status)}`}
                              >
                                {log.status ||
                                  "UPDATED"}
                              </span>

                            </div>

                          </div>

                        ))}

                      </div>

                    )}

                  </div>
                );
              }
            )}

          {!loading &&
            Object.keys(groupedLogs).length === 0 && (

            <div className="p-10 text-center text-gray-500 text-sm">
              No activity logs found.
            </div>

          )}

        </div>

      </div>

    </div>
  );
}