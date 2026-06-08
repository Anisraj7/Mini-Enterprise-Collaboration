import { useEffect, useState } from "react";

import {
  CheckCircle2,
  Clock3,
  FileText,
  PauseCircle,
  Search,
  ShieldCheck,
  User,
  XCircle,
  History,
} from "lucide-react";

import toast from "react-hot-toast";
import { useNavigate } from "react-router-dom";

import API from "../api/axios";
import { getPageItems } from "../api/pagination";
import SLABadge from "../components/SLABadge";
import StatusBadge from "../components/StatusBadge";

export default function Approval() {
  const navigate = useNavigate();

  const [approvals, setApprovals] = useState([]);

  const [history, setHistory] = useState([]);

  const [selectedApproval, setSelectedApproval] = useState(null);

  const [commentsByApproval, setCommentsByApproval] = useState({});

  const [form, setForm] = useState({
    title: "",
    description: "",
  });

  const [user, setUser] = useState(null);

  const [search, setSearch] = useState("");

  const [filter, setFilter] = useState("all");

  const [error, setError] = useState("");

  const fetchApprovals = async () => {
    const res = await API.get("/approvals/");

    setApprovals(getPageItems(res.data));
  };

  useEffect(() => {
    const loadPage = async () => {
      const [userResponse, approvalsResponse] = await Promise.all([
        API.get("/auth/me"),
        API.get("/approvals/"),
      ]);

      setUser(userResponse.data);

      setApprovals(getPageItems(approvalsResponse.data));
    };

    loadPage().catch((err) =>
      setError(err.response?.data?.detail || "Unable to load approvals."),
    );
  }, []);

  const submitApproval = async () => {
    if (!form.title.trim()) {
      setError("Approval title is required.");

      return;
    }

    try {
      await API.post("/approvals/", form);

      toast.success("Approval submitted");

      setForm({
        title: "",
        description: "",
      });

      setError("");

      await fetchApprovals();
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to submit approval.");
    }
  };

  const handleAction = async (id, action) => {
    const actionComment = commentsByApproval[id] || "";

    if (action === "reject" && !actionComment.trim()) {
      setError("Comment required for rejection.");

      return;
    }

    try {
      await API.patch(`/approvals/${id}/action`, {
        action,
        comment: actionComment,
      });

      toast.success(`Approval ${action}ed`);

      setCommentsByApproval((prev) => ({
        ...prev,
        [id]: "",
      }));

      setError("");

      await fetchApprovals();

      if (selectedApproval === id) {
        await loadHistory(id);
      }
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to update approval.");
    }
  };

  const loadHistory = async (id) => {
    try {
      const res = await API.get(`/approvals/${id}/history`);

      setHistory(getPageItems(res.data));

      setSelectedApproval(id);

      setError("");
    } catch (err) {
      setError(
        err.response?.data?.detail || "Unable to load approval history.",
      );
    }
  };

  const updateActionComment = (id, value) => {
    setCommentsByApproval((prev) => ({
      ...prev,
      [id]: value,
    }));
  };

  const canActOnApproval = (approval) => {
    if (
      !user ||
      approval.status === "approved" ||
      approval.status === "rejected"
    ) {
      return false;
    }

    if (canManageApprovals) {
      return true;
    }

    return user.role === "manager" && approval.current_level === "manager";
  };

  const filteredApprovals = approvals.filter((approval) => {
    const matchesSearch = approval.title
      ?.toLowerCase()
      .includes(search.toLowerCase());

    const matchesFilter = filter === "all" ? true : approval.status === filter;

    return matchesSearch && matchesFilter;
  });

  const canManageApprovals = ["organization_admin", "workspace_admin"].includes(
    user?.role,
  );

  const canEscalateApproval = [
    "organization_admin",
    "workspace_admin",
    "manager",
  ].includes(user?.role);

  return (
    <div className="bg-gradient-to-br from-slate-100 via-indigo-50 to-cyan-50 min-h-screen">

      <div className="p-6 max-w-7xl mx-auto">
        {/* HEADER */}
        <div className="flex flex-wrap justify-between items-center gap-4 mb-6">
          <div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-indigo-600 to-cyan-500 bg-clip-text text-transparent">
              Approval Requests
            </h1>

            <p className="text-gray-500 mt-1">
              Enterprise approval workflow management
            </p>
          </div>

          <div className="flex flex-wrap gap-3">
            {/* SEARCH */}
            <div className="relative">
              <Search
                size={16}
                className="absolute left-3 top-3 text-gray-400"
              />

              <input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search approvals..."
                className="bg-white border border-gray-200 rounded-xl pl-10 pr-4 py-2 text-sm shadow-sm outline-none focus:ring-2 focus:ring-indigo-200"
              />
            </div>

            {/* FILTER TABS */}
            <div className="flex bg-white rounded-xl shadow-sm border overflow-hidden">
              {["all", "pending", "approved", "rejected"].map((item) => (
                <button
                  key={item}
                  onClick={() => setFilter(item)}
                  className={`
                    px-4 py-2 text-sm font-medium capitalize transition-all
                    ${
                      filter === item
                        ? "bg-gradient-to-r from-indigo-600 to-cyan-500 text-white"
                        : "text-gray-600 hover:bg-gray-100"
                    }
                  `}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* ERROR */}
        {error && (
          <div className="bg-red-100 border border-red-200 text-red-600 px-4 py-3 rounded-xl mb-5 text-sm">
            {error}
          </div>
        )}

        {/* SUBMIT FORM */}
        <div className="bg-white/90 backdrop-blur-sm p-6 rounded-3xl shadow-lg border border-white mb-8">
          <div className="flex items-center gap-2 mb-5">
            <ShieldCheck size={22} className="text-indigo-600" />

            <h2 className="font-bold text-xl text-gray-700">
              Submit Approval Request
            </h2>
          </div>

          <div className="grid md:grid-cols-2 gap-4 mb-4">
            <div>
              <label className="text-sm font-medium text-gray-500 mb-2 block">
                Approval Title
              </label>

              <input
                value={form.title}
                onChange={(e) =>
                  setForm({
                    ...form,
                    title: e.target.value,
                  })
                }
                className="border border-gray-200 p-3 rounded-2xl w-full text-sm outline-none focus:ring-2 focus:ring-indigo-200 transition"
                placeholder="Enter title"
              />
            </div>

            <div>
              <label className="text-sm font-medium text-gray-500 mb-2 block">
                Request Type
              </label>

              <select className="border border-gray-200 p-3 rounded-2xl w-full text-sm outline-none focus:ring-2 focus:ring-indigo-200 transition">
                <option>Task Approval</option>

                <option>Document Approval</option>

                <option>Leave Approval</option>
              </select>
            </div>
          </div>

          <div className="mb-5">
            <label className="text-sm font-medium text-gray-500 mb-2 block">
              Description
            </label>

            <textarea
              value={form.description}
              onChange={(e) =>
                setForm({
                  ...form,
                  description: e.target.value,
                })
              }
              className="border border-gray-200 p-3 rounded-2xl w-full text-sm outline-none focus:ring-2 focus:ring-indigo-200 transition"
              rows="4"
              placeholder="Describe your request..."
            />
          </div>

          <button
            onClick={submitApproval}
            className="bg-gradient-to-r from-indigo-600 to-cyan-500 hover:scale-[1.02] transition-all text-white px-6 py-3 rounded-2xl shadow-md font-medium"
          >
            Submit Request
          </button>
        </div>

        {/* APPROVAL CARDS */}
        <div className="space-y-5">
          {filteredApprovals.map((approval) => {
            const canAct = canActOnApproval(approval);

            return (
              <div
                key={approval.id}
                className="bg-white/90 backdrop-blur-sm p-6 rounded-3xl shadow-md border border-white hover:shadow-xl transition-all"
              >
                {/* TOP */}
                <div className="flex flex-wrap justify-between gap-4">
                  <div>
                    <div className="flex items-center gap-3">
                      <div className="bg-indigo-100 p-2 rounded-xl">
                        <FileText size={18} className="text-indigo-600" />
                      </div>

                      <div>
                        <h2 className="font-bold text-lg text-gray-800">
                          {approval.title}
                        </h2>

                        <p className="text-sm text-gray-500 mt-1">
                          {approval.description}
                        </p>
                      </div>
                    </div>
                  </div>

                  {/* STATUS */}
                  <div>
                    <span
                      className={`
                          px-4 py-2 rounded-full text-xs font-bold uppercase shadow-sm
                          ${
                            approval.status === "approved"
                              ? "bg-green-100 text-green-700"
                              : approval.status === "rejected"
                                ? "bg-red-100 text-red-700"
                                : approval.status === "hold"
                                  ? "bg-gray-100 text-gray-700"
                                  : "bg-yellow-100 text-yellow-700"
                          }
                        `}
                    >
                      {approval.status}
                    </span>
                  </div>
                </div>

                <div className="mt-5 grid gap-4 md:grid-cols-4">
                  <div className="rounded-2xl bg-gray-50 p-4">
                    <p className="mb-2 text-xs text-gray-400">SLA Status</p>
                    {approval.sla_status ? (
                      <SLABadge status={approval.sla_status} />
                    ) : (
                      <span className="text-sm text-gray-500">Not tracked</span>
                    )}
                  </div>
                  <div className="rounded-2xl bg-gray-50 p-4">
                    <p className="mb-2 text-xs text-gray-400">SLA Due Time</p>
                    <p className="text-sm font-semibold text-gray-700">
                      {approval.sla_due_time
                        ? new Date(approval.sla_due_time).toLocaleString()
                        : "N/A"}
                    </p>
                  </div>
                  <div className="rounded-2xl bg-gray-50 p-4">
                    <p className="mb-2 text-xs text-gray-400">Escalated</p>
                    <StatusBadge
                      status={approval.is_escalated ? "Active" : "Disabled"}
                    />
                  </div>
                  <div className="rounded-2xl bg-gray-50 p-4">
                    <p className="mb-2 text-xs text-gray-400">Escalated To</p>
                    <p className="text-sm font-semibold text-gray-700">
                      {approval.current_escalation_to || "N/A"}
                    </p>
                  </div>
                </div>

                {/* INFO */}
                <div className="flex flex-wrap gap-6 mt-5 text-sm text-gray-500">
                  <div className="flex items-center gap-2">
                    <User size={15} />

                    {approval.requested_by_name ||
                      `User ${approval.requested_by}`}
                  </div>

                  <div className="flex items-center gap-2">
                    <Clock3 size={15} />

                    {approval.created_at
                      ? new Date(approval.created_at).toLocaleString()
                      : "N/A"}
                  </div>
                </div>

                {/* COMMENT */}
                {canAct && (
                  <textarea
                    placeholder="Action comment (required for rejection)"
                    value={commentsByApproval[approval.id] || ""}
                    onChange={(e) =>
                      updateActionComment(approval.id, e.target.value)
                    }
                    className="border border-gray-200 mt-5 w-full p-3 rounded-2xl text-sm outline-none focus:ring-2 focus:ring-indigo-200"
                    rows="3"
                  />
                )}

                {/* ACTIONS */}
                <div className="flex flex-wrap gap-3 mt-5">
                  {canAct && (
                    <>
                      <button
                        onClick={() => handleAction(approval.id, "approve")}
                        className="bg-green-100 hover:bg-green-200 text-green-700 px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2 transition"
                      >
                        <CheckCircle2 size={16} />
                        Approve
                      </button>

                      <button
                        onClick={() => handleAction(approval.id, "reject")}
                        className="bg-red-100 hover:bg-red-200 text-red-700 px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2 transition"
                      >
                        <XCircle size={16} />
                        Reject
                      </button>

                      <button
                        onClick={() => handleAction(approval.id, "hold")}
                        className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2 transition"
                      >
                        <PauseCircle size={16} />
                        Hold
                      </button>
                    </>
                  )}

                  <button
                    onClick={() => loadHistory(approval.id)}
                    className="bg-indigo-100 hover:bg-indigo-200 text-indigo-700 px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2 transition"
                  >
                    <History size={16} />
                    History
                  </button>

                  {canEscalateApproval && (
                    <button
                      onClick={() => navigate("/approval-escalations")}
                      className="bg-orange-100 hover:bg-orange-200 text-orange-700 px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2 transition"
                    >
                      <ShieldCheck size={16} />
                      Escalate
                    </button>
                  )}
                </div>

                {/* HISTORY */}
                {selectedApproval === approval.id && (
                  <div className="mt-5 bg-gradient-to-r from-slate-50 to-indigo-50 border border-indigo-100 p-5 rounded-2xl">
                    <h3 className="font-semibold text-gray-700 mb-4">
                      Approval History
                    </h3>

                    <div className="space-y-3">
                      {history.map((item) => (
                        <div
                          key={item.id}
                          className="bg-white p-4 rounded-2xl border shadow-sm"
                        >
                          <div className="flex justify-between gap-4">
                            <div>
                              <p className="font-semibold capitalize text-gray-700">
                                {item.action}
                              </p>

                              <p className="text-sm text-gray-500 mt-1">
                                by{" "}
                                {item.action_by_name ||
                                  `User ${item.action_by}`}
                              </p>

                              <p className="text-sm text-gray-400 mt-2">
                                {item.comment || "No comment"}
                              </p>
                            </div>

                            <p className="text-xs text-gray-400">
                              {new Date(item.created_at).toLocaleString()}
                            </p>
                          </div>
                        </div>
                      ))}

                      {history.length === 0 && (
                        <p className="text-sm text-gray-500">No history yet</p>
                      )}
                    </div>
                  </div>
                )}
              </div>
            );
          })}

          {filteredApprovals.length === 0 && (
            <div className="bg-white p-10 rounded-3xl shadow-md text-center text-gray-500">
              No approval requests found.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
