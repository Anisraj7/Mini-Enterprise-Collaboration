import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";
import API from "../api/axios";
import Navbar from "../components/Navbar";


export default function AssignTask() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [users, setUsers] = useState([]);
  const [selectedUser, setSelectedUser] = useState("");
  const [error, setError] = useState("");

  useEffect(() => {
    const loadUsers = async () => {
      try {
        const response = await API.get("/users/assignable");
        setUsers(response.data);
      } catch {
        setError("Unable to load assignable users.");
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
      navigate("/dashboard");
    } catch (err) {
      setError(err.response?.data?.detail || "Unable to assign task.");
    }
  };

  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar />

      <div className="p-6 max-w-xl mx-auto">
        <div className="bg-white p-6 rounded-xl shadow">
          <h2 className="text-xl font-bold mb-4">Assign Task</h2>

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

          <button
            onClick={handleAssign}
            disabled={!selectedUser}
            className="bg-indigo-600 text-white px-4 py-2 rounded hover:bg-indigo-700 disabled:bg-indigo-300"
          >
            Assign
          </button>
        </div>
      </div>
    </div>
  );
}
