import { useEffect, useState } from "react";

import { getUsers } from "../../../services/collaboration/memberService";

export default function MemberFormModal({ onClose, onSubmit }) {
  const [formData, setFormData] = useState({
    user_id: "",
    role: "EMPLOYEE",
  });

  const [users, setUsers] = useState([]);

  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const loadUsers = async () => {
      try {
        setLoading(true);

        const data = await getUsers();

        console.log("Users API:", data);

        if (Array.isArray(data)) {
          setUsers(data);
        } else if (Array.isArray(data.items)) {
          setUsers(data.items);
        } else {
          setUsers([]);
        }
      } catch (err) {
        console.error(err);
        setUsers([]);
      } finally {
        setLoading(false);
      }
    };

    loadUsers();
  }, []);

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!formData.user_id) {
      return;
    }

    onSubmit({
      ...formData,
      user_id: Number(formData.user_id),
    });
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
      <div className="bg-white rounded-xl w-full max-w-md p-6 shadow-lg">
        <div className="flex justify-between items-center mb-5">
          <h2 className="text-lg font-bold">Add Member</h2>

          <button
            type="button"
            onClick={onClose}
            className="text-gray-500 hover:text-black"
          >
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1 text-sm font-medium">User</label>

            <select
              value={formData.user_id}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  user_id: e.target.value,
                })
              }
              className="w-full border rounded-lg px-3 py-2"
              disabled={loading}
            >
              <option value="">Select User</option>

              {Array.isArray(users) &&
                users.map((user) => (
                  <option key={user.id} value={user.id}>
                    {user.name} ({user.email})
                  </option>
                ))}
            </select>
          </div>

          <div>
            <label className="block mb-1 text-sm font-medium">Role</label>

            <select
              value={formData.role}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  role: e.target.value,
                })
              }
              className="w-full border rounded-lg px-3 py-2"
            >
              <option value="EMPLOYEE">Employee</option>

              <option value="MANAGER">Manager</option>

              <option value="WORKSPACE_ADMIN">Workspace Admin</option>
            </select>
          </div>

          <div className="flex justify-end gap-2 pt-2">
            <button
              type="button"
              onClick={onClose}
              className="border px-4 py-2 rounded-lg"
            >
              Cancel
            </button>

            <button
              type="submit"
              className="bg-blue-600 text-white px-4 py-2 rounded-lg"
            >
              Add Member
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
