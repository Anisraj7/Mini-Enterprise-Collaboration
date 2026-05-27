import { useEffect, useState } from "react";

import {
  Ban,
  Check,
  Plus,
  AlertTriangle,
  Clock3,
  ShieldAlert,
} from "lucide-react";

import API from "../api/axios";

import ConfirmModal from "../components/ConfirmModal";
import DataTable from "../components/DataTable";
import ErrorMessage from "../components/ErrorMessage";
import LoadingSpinner from "../components/LoadingSpinner";
import Navbar from "../components/Navbar";
import PageHeader from "../components/PageHeader";
import StatusBadge from "../components/StatusBadge";
import UserSelectDropdown from "../components/UserSelectDropdown";

const formatDateTime = (value) =>
  value
    ? new Date(value).toLocaleString()
    : "N/A";

const initialForm = {
  approval_id: "",
  escalated_to: "",
  reason: "",
};

const actionBtn =
  "rounded-xl p-2 text-white transition";

const StatCard = ({
  title,
  value,
  icon: Icon,
  color,
}) => (
  <div className="rounded-2xl border bg-white p-5 shadow-sm">
    <div className="flex items-center justify-between">
      <div>
        <p className="text-sm text-gray-500">
          {title}
        </p>

        <h3
          className={`mt-1 text-3xl font-bold text-${color}-600`}
        >
          {value}
        </h3>
      </div>

      <div
        className={`rounded-2xl bg-${color}-100 p-3 text-${color}-600`}
      >
        <Icon size={24} />
      </div>
    </div>
  </div>
);

export default function ApprovalEscalations() {

  const [escalations, setEscalations] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [success, setSuccess] =
    useState("");

  const [modal, setModal] =
    useState(null);

  const [selected, setSelected] =
    useState(null);

  const [form, setForm] =
    useState(initialForm);

  // =====================================
  // HELPERS
  // =====================================

  const setMessage = (
    type,
    message
  ) => {

    setError(
      type === "error"
        ? message
        : ""
    );

    setSuccess(
      type === "success"
        ? message
        : ""
    );
  };

  const closeModal = () => {

    setModal(null);

    setSelected(null);
  };

  // =====================================
  // FETCH ESCALATIONS
  // =====================================

  const fetchEscalations =
    async () => {

      try {

        setLoading(true);

        const { data } =
          await API.get(
            "/approval-escalations"
          );

        setEscalations(
          data || []
        );

      } catch (err) {

        setMessage(
          "error",
          err.response?.data
            ?.detail ||
            "Unable to load approval escalations."
        );

      } finally {

        setLoading(false);
      }
    };

  useEffect(() => {
    fetchEscalations();
  }, []);

  // =====================================
  // CREATE ESCALATION
  // =====================================

  const createEscalation =
    async (event) => {

      event.preventDefault();

      if (
        !form.approval_id ||
        !form.escalated_to ||
        !form.reason.trim()
      ) {

        return setMessage(
          "error",
          "Approval, escalation user, and reason are required."
        );
      }

      try {

        const payload = {
          approval_id: Number(
            form.approval_id
          ),

          escalated_to:
            typeof form.escalated_to ===
            "object"
              ? form
                  .escalated_to.id
              : Number(
                  form.escalated_to
                ),

          reason:
            form.reason.trim(),
        };

        await API.post(
          "/approval-escalations",
          payload
        );

        setMessage(
          "success",
          "Approval escalated successfully."
        );

        setForm(initialForm);

        closeModal();

        fetchEscalations();

      } catch (err) {

        setMessage(
          "error",
          err.response?.data
            ?.detail ||
            "Unable to create escalation."
        );
      }
    };

  // =====================================
  // UPDATE ESCALATION
  // =====================================

  const updateEscalation =
    async (action) => {

      try {

        await API.put(
          `/approval-escalations/${selected.id}/${action}`
        );

        setMessage(
          "success",
          `Escalation ${action}d successfully.`
        );

        closeModal();

        fetchEscalations();

      } catch (err) {

        setMessage(
          "error",
          err.response?.data
            ?.detail ||
            `Unable to ${action} escalation.`
        );
      }
    };

  // =====================================
  // STATS
  // =====================================

  const stats = {
    PENDING:
      escalations.filter(
        ({ status }) =>
          status === "PENDING"
      ).length,

    RESOLVED:
      escalations.filter(
        ({ status }) =>
          status === "RESOLVED"
      ).length,

    CANCELLED:
      escalations.filter(
        ({ status }) =>
          status === "CANCELLED"
      ).length,
  };

  // =====================================
  // TABLE COLUMNS
  // =====================================

  const columns = [

    {
      key: "approval",
      header: "Approval",

      render: (row) => (

        <div>

          <p className="font-semibold text-gray-800">

            {row.approval?.title ||
              "Untitled Approval"}

          </p>

          <p className="text-xs text-gray-500">

            #{row.approval_id}

          </p>

        </div>

      ),
    },

    {
      key: "escalated_from",
      header: "Escalated From",

      render: (row) => (

        <p className="font-medium text-gray-800">

          {row
            .escalated_from_user
            ?.full_name ||

            row
              .escalated_from_user
              ?.name ||

            `User #${row.escalated_from}`}

        </p>

      ),
    },

    {
      key: "escalated_to",
      header: "Escalated To",

      render: (row) => (

        <p className="font-medium text-gray-800">

          {row
            .escalated_to_user
            ?.full_name ||

            row
              .escalated_to_user
              ?.name ||

            `User #${row.escalated_to}`}

        </p>

      ),
    },

    {
      key: "reason",
      header: "Reason",

      render: (row) => (

        <div className="max-w-[250px] break-words">

          {row.reason}

        </div>

      ),
    },

    {
      key: "escalation_level",
      header: "Level",

      render: (row) => (

        <div className="font-semibold text-orange-600">

          L{row.escalation_level}

        </div>

      ),
    },

    {
      key: "status",
      header: "Status",

      render: (row) => (
        <StatusBadge
          status={row.status}
        />
      ),
    },

    {
      key: "created_at",
      header: "Escalated At",

      render: (row) =>
        formatDateTime(
          row.created_at
        ),
    },

    {
      key: "actions",
      header: "Actions",

      render: (row) =>
        row.status ===
        "PENDING" ? (

          <div className="flex gap-2">

            {[
              [
                "resolve",
                Check,
                "green",
              ],

              [
                "cancel",
                Ban,
                "red",
              ],
            ].map(
              ([
                type,
                Icon,
                color,
              ]) => (

                <button
                  key={type}
                  onClick={() => {
                    setSelected(
                      row
                    );

                    setModal(
                      type
                    );
                  }}
                  className={`${actionBtn} bg-${color}-600 hover:bg-${color}-700`}
                >
                  <Icon size={15} />
                </button>

              )
            )}

          </div>

        ) : (

          <span className="text-sm text-gray-400">

            No Actions

          </span>

        ),
    },
  ];

  return (

    <div className="min-h-screen bg-gray-100">

      <Navbar />

      <main className="mx-auto max-w-7xl p-6">

        <PageHeader
          title="Approval Escalations"
          subtitle="Manage delayed approvals and escalation workflow"
          actions={

            <button
              onClick={() =>
                setModal("create")
              }
              className="
                flex
                items-center
                gap-2
                rounded-xl
                bg-blue-600
                px-5
                py-2.5
                text-sm
                font-semibold
                text-white
                hover:bg-blue-700
              "
            >

              <Plus size={16} />

              Escalate Approval

            </button>

          }
        />

        {/* STATS */}

        <div className="mb-6 grid gap-4 md:grid-cols-3">

          <StatCard
            title="Pending Escalations"
            value={stats.PENDING}
            icon={Clock3}
            color="orange"
          />

          <StatCard
            title="Resolved Escalations"
            value={stats.RESOLVED}
            icon={Check}
            color="green"
          />

          <StatCard
            title="Cancelled Escalations"
            value={stats.CANCELLED}
            icon={ShieldAlert}
            color="red"
          />

        </div>

        {/* ALERTS */}

        {success && (

          <div className="mb-4 rounded-xl border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">

            {success}

          </div>

        )}

        <ErrorMessage
          message={error}
        />

        {/* TABLE */}

        {loading ? (

          <LoadingSpinner />

        ) : (

          <div className="rounded-2xl border bg-white p-4 shadow-sm">

            <DataTable
              columns={columns}
              rows={escalations}
              emptyMessage="No escalation records found"
            />

          </div>

        )}

        {/* CREATE MODAL */}

        {modal === "create" && (

          <div className="fixed inset-0 z-50 overflow-y-auto bg-black/50 backdrop-blur-sm">

            <div className="flex min-h-screen items-center justify-center p-4">

              <form
                onSubmit={
                  createEscalation
                }
                className="w-full max-w-xl rounded-3xl bg-white p-6 shadow-2xl"
              >

                <div className="mb-6 flex items-center gap-3">

                  <div className="rounded-2xl bg-red-100 p-3 text-red-600">

                    <AlertTriangle
                      size={22}
                    />

                  </div>

                  <div>

                    <h2 className="text-2xl font-bold text-gray-800">

                      Escalate Approval

                    </h2>

                    <p className="text-sm text-gray-500">

                      Escalate workflow to higher authority

                    </p>

                  </div>

                </div>

                <div className="space-y-5">

                  <div>

                    <label className="mb-2 block text-sm font-medium text-gray-700">

                      Approval ID

                    </label>

                    <input
                      type="number"
                      min="1"
                      placeholder="Enter approval ID"
                      value={
                        form.approval_id
                      }
                      onChange={(
                        e
                      ) =>
                        setForm({
                          ...form,
                          approval_id:
                            e.target
                              .value,
                        })
                      }
                      className="w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-blue-500"
                    />

                  </div>

                  <div>

                    <label className="mb-2 block text-sm font-medium text-gray-700">

                      Escalate To

                    </label>

                    <UserSelectDropdown
                      value={
                        form.escalated_to ||
                        ""
                      }
                      onChange={(
                        value
                      ) =>
                        setForm({
                          ...form,
                          escalated_to:
                            value,
                        })
                      }
                      className="w-full"
                    />

                  </div>

                  <div>

                    <label className="mb-2 block text-sm font-medium text-gray-700">

                      Escalation Reason

                    </label>

                    <textarea
                      placeholder="Enter escalation reason"
                      value={
                        form.reason
                      }
                      onChange={(
                        e
                      ) =>
                        setForm({
                          ...form,
                          reason:
                            e.target
                              .value,
                        })
                      }
                      className="min-h-[140px] w-full rounded-xl border border-gray-200 px-4 py-3 text-sm outline-none focus:border-blue-500"
                    />

                  </div>

                </div>

                <div className="mt-6 flex justify-end gap-3">

                  <button
                    type="button"
                    onClick={
                      closeModal
                    }
                    className="rounded-xl border border-gray-300 px-5 py-2.5 text-sm font-medium hover:bg-gray-100"
                  >

                    Cancel

                  </button>

                  <button
                    type="submit"
                    className="rounded-xl bg-red-600 px-5 py-2.5 text-sm font-semibold text-white hover:bg-red-700"
                  >

                    Escalate Approval

                  </button>

                </div>

              </form>

            </div>

          </div>

        )}

        {/* RESOLVE */}

        <ConfirmModal
          isOpen={
            modal === "resolve"
          }
          title="Resolve Escalation"
          message="Are you sure you want to resolve this escalation?"
          onConfirm={() =>
            updateEscalation(
              "resolve"
            )
          }
          onClose={closeModal}
        />

        {/* CANCEL */}

        <ConfirmModal
          isOpen={
            modal === "cancel"
          }
          title="Cancel Escalation"
          message="Are you sure you want to cancel this escalation?"
          onConfirm={() =>
            updateEscalation(
              "cancel"
            )
          }
          onClose={closeModal}
        />

      </main>

    </div>
  );
}