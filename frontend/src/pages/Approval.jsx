import { useEffect, useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";

export default function Approval() {
  const [approvals, setApprovals] = useState([]);
  const [history, setHistory] = useState([]);
  const [selectedApproval, setSelectedApproval] = useState(null);
  const [commentsByApproval, setCommentsByApproval] = useState({});
  const [form, setForm] = useState({ title: "", description: "" });
  const [user, setUser] = useState(null);
  const [error, setError] = useState("");

  const fetchApprovals = async () => {
    const res = await API.get("/approvals/");
    setApprovals(res.data);
  };

  useEffect(() => {
    const loadPage = async () => {
      const [userResponse, approvalsResponse] = await Promise.all([
        API.get("/auth/me"),
        API.get("/approvals/"),
      ]);
      setUser(userResponse.data);
      setApprovals(approvalsResponse.data);
    };

    loadPage().catch((err) => setError(err.response?.data?.detail || "Unable to load approvals."));
  }, []);

  const submitApproval = async () => {
    if (!form.title.trim()) {
      setError("Approval title is required.");
      return;
    }
    try {
      await API.post("/approvals/", form);
      setForm({ title: "", description: "" });
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
      await API.patch(`/approvals/${id}/action`, { action, comment: actionComment });
      setCommentsByApproval((prev) => ({ ...prev, [id]: "" }));
      setError("");
      await fetchApprovals();
      if (selectedApproval === id) await loadHistory(id);
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to update approval.");
    }
  };

  const loadHistory = async (id) => {
    try {
      const res = await API.get(`/approvals/${id}/history`);
      setHistory(res.data);
      setSelectedApproval(id);
      setError("");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to load approval history.");
    }
  };

  const updateActionComment = (id, value) => {
    setCommentsByApproval((prev) => ({ ...prev, [id]: value }));
  };

  const canActOnApproval = (approval) => {
    if (!user || approval.status === "approved" || approval.status === "rejected") return false;
    if (user.role === "admin") return true;
    return user.role === "manager" && approval.current_level === "manager";
  };

  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar />
      <div className="p-6 max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold text-gray-700 mb-6">Approval Requests</h1>
        {error && <p className="text-sm text-red-600 mb-4">{error}</p>}

        <div className="bg-white p-5 rounded-xl shadow mb-6">
          <h2 className="font-semibold mb-3">Submit Approval Request</h2>
          <input value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} className="border p-2 rounded w-full mb-3" placeholder="Title" />
          <textarea value={form.description} onChange={(e) => setForm({ ...form, description: e.target.value })} className="border p-2 rounded w-full mb-3" placeholder="Description" />
          <button onClick={submitApproval} className="bg-indigo-600 text-white px-4 py-2 rounded">Submit Request</button>
        </div>

        <div className="space-y-4">
          {approvals.map((approval) => {
            const canAct = canActOnApproval(approval);

            return (
              <div key={approval.id} className="bg-white p-5 rounded-xl shadow">
              <div className="flex flex-wrap justify-between gap-3 items-center">
                <div>
                  <h2 className="font-semibold text-lg">{approval.title}</h2>
                  <p className="text-sm text-gray-500">{approval.description}</p>
                </div>
                <span className={`px-3 py-1 rounded-full text-white text-xs ${
                  approval.status === "approved" ? "bg-green-500" : approval.status === "rejected" ? "bg-red-500" : "bg-yellow-500"
                }`}>
                  {approval.status}
                </span>
              </div>

              <p className="text-xs text-gray-400 mt-2">Level: {approval.current_level}</p>

              {canAct && (
                <input
                  placeholder="Action comment (required for reject)"
                  value={commentsByApproval[approval.id] || ""}
                  onChange={(e) => updateActionComment(approval.id, e.target.value)}
                  className="border mt-3 w-full p-2 rounded"
                />
              )}

              <div className="flex flex-wrap gap-2 mt-4">
                {canAct && (
                  <>
                    <button onClick={() => handleAction(approval.id, "approve")} className="bg-green-500 text-white px-3 py-1 rounded">Approve</button>
                    <button onClick={() => handleAction(approval.id, "reject")} className="bg-red-500 text-white px-3 py-1 rounded">Reject</button>
                    <button onClick={() => handleAction(approval.id, "hold")} className="bg-gray-500 text-white px-3 py-1 rounded">Hold</button>
                  </>
                )}
                <button onClick={() => loadHistory(approval.id)} className="bg-indigo-500 text-white px-3 py-1 rounded">History</button>
              </div>

              {selectedApproval === approval.id && (
                <div className="mt-4 bg-gray-100 p-3 rounded">
                  <h3 className="font-semibold mb-2">History</h3>
                  {history.map((item) => (
                    <div key={item.id} className="mb-2 text-sm">
                      <p><b>{item.action}</b> by {item.action_by_name || `User ${item.action_by}`}</p>
                      <p className="text-gray-500">{item.comment || "No comment"}</p>
                      <p className="text-xs text-gray-400">{new Date(item.created_at).toLocaleString()}</p>
                    </div>
                  ))}
                  {history.length === 0 && <p className="text-sm text-gray-500">No history yet</p>}
                </div>
              )}
              </div>
            );
          })}
          {approvals.length === 0 && <p className="text-sm text-gray-500">No approval requests found.</p>}
        </div>
      </div>
    </div>
  );
}
