import { useEffect, useState } from "react";

import API from "../api/axios";
import DataTable from "../components/DataTable";
import DateRangeFilter from "../components/DateRangeFilter";
import ErrorMessage from "../components/ErrorMessage";
import FilterBar from "../components/FilterBar";
import LoadingSpinner from "../components/LoadingSpinner";
import Navbar from "../components/Navbar";
import PageHeader from "../components/PageHeader";

const formatDateTime = (value) => (value ? new Date(value).toLocaleString() : "N/A");

export default function AuditLogs() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [moduleFilter, setModuleFilter] = useState("");
  const [userFilter, setUserFilter] = useState("");
  const [startDate, setStartDate] = useState("");
  const [endDate, setEndDate] = useState("");
  const [selectedLog, setSelectedLog] = useState(null);

  const fetchLogs = async () => {
    try {
      setLoading(true);
      const params = {};
      if (moduleFilter) params.module_name = moduleFilter;
      if (userFilter) params.user_id = userFilter;

      const response = await API.get("/audit-logs", { params });
      const rows = Array.isArray(response.data) ? response.data : response.data.data || [];
      setLogs(rows);
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load audit logs.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    API.get("/audit-logs")
      .then((response) => {
        const rows = Array.isArray(response.data) ? response.data : response.data.data || [];
        setLogs(rows);
        setError("");
      })
      .catch((err) => setError(err.response?.data?.detail || "Unable to load audit logs."))
      .finally(() => setLoading(false));
  }, []);

  const filteredLogs = logs.filter((log) => {
    const created = log.created_at ? new Date(log.created_at) : null;
    const afterStart = !startDate || (created && created >= new Date(`${startDate}T00:00:00`));
    const beforeEnd = !endDate || (created && created <= new Date(`${endDate}T23:59:59`));
    return afterStart && beforeEnd;
  });

  const columns = [
    { key: "id", header: "Log ID", render: (row) => `#${row.id}` },
    { key: "user_id", header: "User", render: (row) => row.user_id || "System" },
    { key: "module_name", header: "Module" },
    { key: "action_type", header: "Action Type" },
    { key: "record_id", header: "Record ID", render: (row) => row.record_id || "N/A" },
    { key: "ip_address", header: "IP Address", render: (row) => row.ip_address || "N/A" },
    { key: "created_at", header: "Created At", render: (row) => formatDateTime(row.created_at) },
    {
      key: "actions",
      header: "Actions",
      render: (row) => (
        <button type="button" onClick={() => setSelectedLog(row)} className="rounded-lg bg-blue-600 px-3 py-1 text-xs font-semibold text-white hover:bg-blue-700">
          View
        </button>
      ),
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <main className="mx-auto max-w-7xl p-6">
        <PageHeader title="Audit Logs" subtitle="Review backend activity with module, user, request, and data snapshot details" />
        <ErrorMessage message={error} />

        <FilterBar>
          <select value={moduleFilter} onChange={(event) => setModuleFilter(event.target.value)} className="rounded-lg border border-gray-200 px-3 py-2 text-sm">
            <option value="">All Modules</option>
            <option value="Task">Task</option>
            <option value="Approval">Approval</option>
            <option value="SLA">SLA</option>
            <option value="Notification">Notification</option>
            <option value="Document">Document</option>
          </select>
          <input type="number" min="1" placeholder="User ID" value={userFilter} onChange={(event) => setUserFilter(event.target.value)} className="rounded-lg border border-gray-200 px-3 py-2 text-sm" />
          <DateRangeFilter startDate={startDate} endDate={endDate} onStartDateChange={setStartDate} onEndDateChange={setEndDate} />
          <button type="button" onClick={fetchLogs} className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700">
            Apply
          </button>
        </FilterBar>

        {loading ? <LoadingSpinner /> : <DataTable columns={columns} rows={filteredLogs} emptyMessage="No audit logs found" />}

        {selectedLog && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
            <div className="max-h-[85vh] w-full max-w-3xl overflow-y-auto rounded-lg bg-white p-6 shadow-xl">
              <div className="mb-4 flex items-center justify-between">
                <h2 className="text-xl font-bold">Audit Log #{selectedLog.id}</h2>
                <button type="button" onClick={() => setSelectedLog(null)} className="rounded-lg border px-3 py-1 text-sm">Close</button>
              </div>
              <div className="grid gap-4 md:grid-cols-2">
                <pre className="rounded-lg bg-gray-50 p-4 text-xs text-gray-700 whitespace-pre-wrap">Old Data: {selectedLog.old_data || "N/A"}</pre>
                <pre className="rounded-lg bg-gray-50 p-4 text-xs text-gray-700 whitespace-pre-wrap">New Data: {selectedLog.new_data || "N/A"}</pre>
              </div>
              <div className="mt-4 space-y-2 text-sm text-gray-600">
                <p><span className="font-semibold">IP Address:</span> {selectedLog.ip_address || "N/A"}</p>
                <p><span className="font-semibold">User Agent:</span> {selectedLog.user_agent || "N/A"}</p>
                <p><span className="font-semibold">Timestamp:</span> {formatDateTime(selectedLog.created_at)}</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
