import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import API from "../api/axios";


export default function Navbar() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);

  useEffect(() => {
    const loadUser = async () => {
      try {
        const response = await API.get("/auth/me");
        setUser(response.data);
      } catch {
        localStorage.removeItem("token");
        navigate("/");
      }
    };

    loadUser();
  }, [navigate]);

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  return (
    <div className="bg-gradient-to-r from-indigo-600 to-cyan-600 text-white px-6 py-3 flex justify-between items-center shadow-md">
      <div>
        <h1 className="text-lg font-bold">TaskFlow</h1>
        {user && <p className="text-xs text-indigo-100">{user.name} • {user.role}</p>}
      </div>

      <div className="flex items-center gap-6">
        <Link to="/dashboard" className="hover:opacity-80">Dashboard</Link>
        {(user?.role === "admin" || user?.role === "manager") && (
          <Link to="/create-task" className="hover:opacity-80">Create</Link>
        )}
        {user?.role === "admin" && (
          <Link to="/users" className="hover:opacity-80">Users</Link>
        )}
        {(user?.role === "admin" || !user) && (
          <Link to="/register" className="hover:opacity-80">Register</Link>
        )}

        <button
          onClick={() => navigate("/kanban")}
          className="bg-indigo-600 text-white px-3 py-1 rounded"
        >
          Kanban
        </button>

        <button
          onClick={logout}
          className="bg-red-500 px-3 py-1 rounded hover:bg-red-600"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
