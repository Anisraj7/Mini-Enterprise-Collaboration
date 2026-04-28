import { useEffect, useState } from "react";
import API from "../api/axios";
import Navbar from "../components/Navbar";


export default function Users() {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    const loadUsers = async () => {
      try {
        const response = await API.get("/users/");
        setUsers(response.data);
      } catch (err) {
        setError(err.response?.data?.detail || "Unable to load users.");
      }
    };

    loadUsers();
  }, []);

  return (
    <div className="bg-gray-50 min-h-screen">
      <Navbar />

      <div className="p-6 max-w-5xl mx-auto">
        <div className="bg-white rounded-xl shadow overflow-hidden">
          <div className="p-4 border-b">
            <h2 className="text-xl font-bold">All Users</h2>
            {error && <p className="text-sm text-red-600 mt-2">{error}</p>}
          </div>

          <table className="w-full text-left">
            <thead className="bg-gray-100">
              <tr>
                <th className="p-4">Name</th>
                <th className="p-4">Email</th>
                <th className="p-4">Role</th>
              </tr>
            </thead>

            <tbody>
              {users.map((user) => (
                <tr key={user.id} className="border-t hover:bg-gray-50">
                  <td className="p-4">{user.name}</td>
                  <td className="p-4">{user.email}</td>
                  <td className="p-4">
                    <span className="bg-indigo-500 text-white px-2 py-1 rounded text-xs capitalize">
                      {user.role}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
