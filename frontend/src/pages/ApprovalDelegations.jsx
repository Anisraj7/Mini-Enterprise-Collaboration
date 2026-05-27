import { useEffect, useState } from "react";
import { Ban, Plus } from "lucide-react";

import API from "../api/axios";
import ConfirmModal from "../components/ConfirmModal";
import DataTable from "../components/DataTable";
import ErrorMessage from "../components/ErrorMessage";
import LoadingSpinner from "../components/LoadingSpinner";
import Navbar from "../components/Navbar";
import PageHeader from "../components/PageHeader";
import StatusBadge from "../components/StatusBadge";
import UserSelectDropdown from "../components/UserSelectDropdown";

const formatDateTime = (value) => (value ? new Date(value).toLocaleString() : "N/A");

export default function ApprovalDelegations() {
  const [delegations, setDelegations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [modal, setModal] = useState(null);
  const [selected, setSelected] = useState(null);
  const [form, setForm] = useState({ delegatee_id: "", start_date: "", end_date: "", reason: "" });

  const fetchDelegations = async () => {
    try {
      const [mine, active] = await Promise.all([
        API.get("/approval-delegations/me"),
        API.get("/approval-delegations/active"),
      ]);
      const byId = new Map([...mine.data, ...active.data].map((item) => [item.id, item]));
      setDelegations(Array.from(byId.values()));
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load approval delegations.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    Promise.all([
      API.get("/approval-delegations/me"),
      API.get("/approval-delegations/active"),
    ])
      .then(([mine, active]) => {
        const byId = new Map([...mine.data, ...active.data].map((item) => [item.id, item]));
        setDelegations(Array.from(byId.values()));
        setError("");
      })
      .catch((err) => setError(err.response?.data?.detail || "Unable to load approval delegations."))
      .finally(() => setLoading(false));
  }, []);

  const createDelegation = async (event) => {
    event.preventDefault();
    if (!form.delegatee_id || !form.start_date || !form.end_date || !form.reason.trim()) {
      setError("Delegatee, dates, and reason are required.");
      return;
    }
    if (new Date(form.end_date) <= new Date(form.start_date)) {
      setError("End date must be after start date.");
      return;
    }

    try {
      await API.post("/approval-delegations/", {
        delegatee_id: Number(form.delegatee_id),
        start_date: new Date(form.start_date).toISOString(),
        end_date: new Date(form.end_date).toISOString(),
        reason: form.reason,
      });
      setForm({ delegatee_id: "", start_date: "", end_date: "", reason: "" });
      setModal(null);
      await fetchDelegations();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to create delegation.");
    }
  };

  const cancelDelegation = async () => {
    try {
      await API.put(`/approval-delegations/${selected.id}/cancel`);
      setModal(null);
      setSelected(null);
      await fetchDelegations();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to cancel delegation.");
    }
  };

  const columns = [
  {
    key: "delegator_name",
    header: "Delegator",
    render: (row) => row.delegator_name || "N/A",
  },

  {
    key: "delegatee_name",
    header: "Delegatee",
    render: (row) => row.delegatee_name || "N/A",
  },

  {
    key: "start_date",
    header: "Start Date",
    render: (row) => formatDateTime(row.start_date),
  },

  {
    key: "end_date",
    header: "End Date",
    render: (row) => formatDateTime(row.end_date),
  },

  {
    key: "reason",
    header: "Reason",
  },

  {
    key: "is_active",
    header: "Status",
    render: (row) => (
      <StatusBadge
        status={
          row.is_active
            ? "Active"
            : "Cancelled"
        }
      />
    ),
  },

  {
    key: "actions",
    header: "Actions",

    render: (row) =>
      row.is_active ? (
        <button
          type="button"
          title="Cancel delegation"
          onClick={() => {
            setSelected(row);
            setModal("cancel");
          }}
          className="rounded-lg bg-red-600 p-2 text-white hover:bg-red-700"
        >
          <Ban size={15} />
        </button>
      ) : (
        "N/A"
      ),
  },
];

  return (
    <div className="min-h-screen bg-gray-100">
      <Navbar />
      <main className="mx-auto max-w-7xl p-6">
        <PageHeader
          title="Approval Delegations"
          subtitle="Delegate approval responsibility for a selected availability window"
          actions={
            <button type="button" onClick={() => setModal("create")} className="flex items-center gap-2 rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700">
              <Plus size={16} /> Create Delegation
            </button>
          }
        />
        <ErrorMessage message={error} />
        {loading ? <LoadingSpinner /> : <DataTable columns={columns} rows={delegations} emptyMessage="No delegations found" />}

        {modal === "create" && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/40 p-4">
            <form onSubmit={createDelegation} className="w-full max-w-lg rounded-lg bg-white p-6 shadow-xl">
              <h2 className="mb-4 text-xl font-bold">Create Delegation</h2>
              <div className="space-y-4">
                <UserSelectDropdown value={form.delegatee_id} onChange={(value) => setForm({ ...form, delegatee_id: value })} roles={["manager", "admin"]} className="w-full" />
                <input type="datetime-local" value={form.start_date} onChange={(event) => setForm({ ...form, start_date: event.target.value })} className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm" />
                <input type="datetime-local" value={form.end_date} onChange={(event) => setForm({ ...form, end_date: event.target.value })} className="w-full rounded-lg border border-gray-200 px-3 py-2 text-sm" />
                <textarea placeholder="Delegation reason" value={form.reason} onChange={(event) => setForm({ ...form, reason: event.target.value })} className="h-28 w-full rounded-lg border border-gray-200 px-3 py-2 text-sm" />
              </div>
              <div className="mt-5 flex justify-end gap-2">
                <button type="button" onClick={() => setModal(null)} className="rounded-lg border px-4 py-2 text-sm">Cancel</button>
                <button type="submit" className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white">Create</button>
              </div>
            </form>
          </div>
        )}

        <ConfirmModal isOpen={modal === "cancel"} title="Cancel Delegation" message="Cancel this approval delegation?" onConfirm={cancelDelegation} onClose={() => setModal(null)} />
      </main>
    </div>
  );
}
