import { useEffect, useState } from "react";
import { Edit2, Power } from "lucide-react";

import API from "../api/axios";
import CreateSLAModal from "../components/CreateSLAModal";
import DataTable from "../components/DataTable";
import EditSLAModal from "../components/EditSLAModal";
import ErrorMessage from "../components/ErrorMessage";
import FilterBar from "../components/FilterBar";
import LoadingSpinner from "../components/LoadingSpinner";
import Navbar from "../components/Navbar";
import PageHeader from "../components/PageHeader";
import SLABadge from "../components/SLABadge";
import StatusBadge from "../components/StatusBadge";

export default function SLARules() {
  const [rules, setRules] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [moduleFilter, setModuleFilter] = useState("");
  const [priorityFilter, setPriorityFilter] = useState("");
  const [createOpen, setCreateOpen] = useState(false);
  const [editOpen, setEditOpen] = useState(false);
  const [selectedRule, setSelectedRule] = useState(null);

  const fetchRules = async () => {
    try {
      const response = await API.get("/sla-rules");
      setRules(response.data);
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load SLA rules.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    API.get("/sla-rules")
      .then((response) => {
        setRules(response.data);
        setError("");
      })
      .catch((err) => setError(err.response?.data?.detail || "Unable to load SLA rules."))
      .finally(() => setLoading(false));
  }, []);

  const disableRule = async (rule) => {
    try {
      await API.delete(`/sla-rules/${rule.id}`);
      await fetchRules();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to disable SLA rule.");
    }
  };

  const filteredRules = rules.filter((rule) => {
    return (
      (!moduleFilter || rule.module_name === moduleFilter) &&
      (!priorityFilter || rule.priority === priorityFilter)
    );
  });

  const columns = [
    { key: "id", header: "Rule ID", render: (rule) => `#${rule.id}` },
    { key: "module_name", header: "Module" },
    { key: "priority", header: "Priority", render: (rule) => <SLABadge status={rule.priority} /> },
    { key: "allowed_hours", header: "Allowed Hours", render: (rule) => `${rule.allowed_hours} hrs` },
    { key: "escalation_enabled", header: "Escalation Enabled", render: (rule) => (rule.escalation_enabled ? "Yes" : "No") },
    { key: "escalation_after_hours", header: "Escalation After", render: (rule) => (rule.escalation_after_hours ? `${rule.escalation_after_hours} hrs` : "N/A") },
    { key: "is_active", header: "Status", render: (rule) => <StatusBadge status={rule.is_active ? "Active" : "Disabled"} /> },
    {
      key: "actions",
      header: "Actions",
      render: (rule) => (
        <div className="flex gap-2">
          <button
            type="button"
            title="Edit rule"
            onClick={() => {
              setSelectedRule(rule);
              setEditOpen(true);
            }}
            className="rounded-lg bg-yellow-500 p-2 text-white hover:bg-yellow-600"
          >
            <Edit2 size={15} />
          </button>
          <button
            type="button"
            title="Disable rule"
            disabled={!rule.is_active}
            onClick={() => disableRule(rule)}
            className="rounded-lg bg-red-600 p-2 text-white hover:bg-red-700 disabled:cursor-not-allowed disabled:bg-gray-300"
          >
            <Power size={15} />
          </button>
        </div>
      ),
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <main className="mx-auto max-w-7xl p-6">
        <PageHeader
          title="SLA Rules"
          subtitle="Create and manage module and priority based SLA policies"
          actions={
            <button
              type="button"
              onClick={() => setCreateOpen(true)}
              className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700"
            >
              Create Rule
            </button>
          }
        />

        <ErrorMessage message={error} />

        <FilterBar>
          <select value={moduleFilter} onChange={(event) => setModuleFilter(event.target.value)} className="rounded-lg border border-gray-200 px-3 py-2 text-sm">
            <option value="">All Modules</option>
            <option value="Task">Task</option>
            <option value="Approval">Approval</option>
          </select>
          <select value={priorityFilter} onChange={(event) => setPriorityFilter(event.target.value)} className="rounded-lg border border-gray-200 px-3 py-2 text-sm">
            <option value="">All Priorities</option>
            <option value="Low">Low</option>
            <option value="Medium">Medium</option>
            <option value="High">High</option>
          </select>
        </FilterBar>

        {loading ? <LoadingSpinner /> : <DataTable columns={columns} rows={filteredRules} emptyMessage="No SLA rules found" />}

        <CreateSLAModal isOpen={createOpen} onClose={() => setCreateOpen(false)} onSuccess={fetchRules} />
        <EditSLAModal isOpen={editOpen} onClose={() => setEditOpen(false)} onSuccess={fetchRules} rule={selectedRule} />
      </main>
    </div>
  );
}
