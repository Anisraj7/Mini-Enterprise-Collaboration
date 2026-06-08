import { useEffect, useState } from "react";

export default function UserFormModal({
  onClose,
  onSubmit,
  editingUser = null,
}) {
  const [formData, setFormData] = useState({
    name: "",
    email: "",
    password: "",
    role: "employee",
  });

  useEffect(() => {
    if (editingUser) {
      setFormData({
        name: editingUser.name || "",
        email: editingUser.email || "",
        password: "",
        role: editingUser.role || "EMPLOYEE",
      });
    }
  }, [editingUser]);

  const handleSubmit = (e) => {
    e.preventDefault();

    const payload = {
      name: formData.name.trim(),
      email: formData.email.trim(),
      role: formData.role,
    };

    if (formData.password.trim()) {
      payload.password = formData.password;
    }

    onSubmit(payload);
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex justify-center items-center z-50">
      <div className="bg-white rounded-xl w-full max-w-md p-6">
        <div className="flex justify-between items-center mb-5">
          <h2 className="text-lg font-bold">
            {editingUser ? "Edit User" : "Create User"}
          </h2>

          <button type="button" onClick={onClose}>
            ✕
          </button>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block mb-1 text-sm">Name</label>

            <input
              type="text"
              value={formData.name}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  name: e.target.value,
                })
              }
              className="w-full border rounded-lg px-3 py-2"
              required
            />
          </div>

          <div>
            <label className="block mb-1 text-sm">Email</label>

            <input
              type="email"
              value={formData.email}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  email: e.target.value,
                })
              }
              className="w-full border rounded-lg px-3 py-2"
              required
            />
          </div>

          <div>
            <label className="block mb-1 text-sm">Password</label>

            <input
              type="password"
              value={formData.password}
              onChange={(e) =>
                setFormData({
                  ...formData,
                  password: e.target.value,
                })
              }
              className="w-full border rounded-lg px-3 py-2"
              placeholder={
                editingUser ? "Leave blank to keep current password" : ""
              }
              required={!editingUser}
            />
          </div>

          <div>
            <label className="block mb-1 text-sm">Role</label>

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
              <option value="employee">Employee</option>

              <option value="manager">Manager</option>

              <option value="workspace_admin">Workspace Admin</option>

              <option value="organization_admin">Organization Admin</option>
            </select>
          </div>

          <div className="flex justify-end gap-2">
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
              {editingUser ? "Update" : "Create"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
