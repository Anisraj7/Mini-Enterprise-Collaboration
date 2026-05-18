import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";


export default function AssignTask() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState("");
  const [recommendation, setRecommendation] = useState(null);
  const [loadingSmartAssign, setLoadingSmartAssign] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadUsers = async () => {
      try {
        const usersResponse = await API.get("/users/assignable");
        setUsers(usersResponse.data);
      } catch {
        setError("Unable to load assignable users.");
        return;
      }

      try {
        const recommendationResponse = await API.get(
          "/tasks/assignment/recommendation"
        );
        setRecommendation(recommendationResponse.data);
        setSelectedUser(String(recommendationResponse.data.id));
      } catch {
        setRecommendation(null);
      }
    };

    loadUsers();
  }, []);

  const handleAssign = async () => {
    setError("");
    try {
      await API.patch(`/tasks/${id}/assign`, {
        assigned_to_id: Number(selectedUser),
      });
      navigate("/kanban");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to assign task.");
    }
  };

  const handleSmartAssign = async () => {
    setError("");
    setLoadingSmartAssign(true);
    try {
      await API.patch(`/tasks/${id}/smart-assign`);
      navigate("/kanban");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to smart assign task.");
    } finally {
      setLoadingSmartAssign(false);
    }
  };

  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar />

      <div className="p-6 max-w-xl mx-auto">
        <div className="bg-white p-6 rounded-xl shadow">
          <h2 className="text-xl font-bold mb-4">Assign Task</h2>

          {recommendation && (
            <div className="border border-indigo-200 bg-indigo-50 rounded-lg p-4 mb-4">
              <p className="text-sm text-indigo-700 font-semibold">
                Smart recommendation
              </p>
              <p className="text-gray-800 mt-1">
                {recommendation.name} ({recommendation.role})
              </p>
              <p className="text-xs text-gray-600 mt-1">
                {recommendation.active_tasks} active tasks,
                {" "}
                {recommendation.completed_tasks} completed tasks
              </p>
            </div>
          )}

          <select
            value={selectedUser}
            onChange={(e) => setSelectedUser(e.target.value)}
            className="border p-2 w-full mb-4 rounded"
          >
            <option value="">Select User</option>
            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name} ({user.role})
              </option>
            ))}
          </select>

          {error && <p className="text-sm text-red-600 mb-3">{error}</p>}

          <div className="flex flex-col sm:flex-row gap-3">
            <button
              onClick={handleAssign}
              disabled={!selectedUser}
              className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 disabled:bg-indigo-300"
            >
              Assign Selected
            </button>

            <button
              onClick={handleSmartAssign}
              disabled={loadingSmartAssign}
              className="bg-emerald-600 text-white px-4 py-2 rounded hover:bg-emerald-700 disabled:bg-emerald-300"
            >
              {loadingSmartAssign ? "Assigning..." : "Smart Assign"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
