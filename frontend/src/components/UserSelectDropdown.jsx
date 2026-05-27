import { useEffect, useState } from "react";

import API from "../api/axios";

export default function UserSelectDropdown({ value, onChange, roles = ["manager", "admin"], className = "" }) {
  const [users, setUsers] = useState([]);
  const rolesKey = roles.join(",");

  useEffect(() => {
    const allowedRoles = rolesKey.split(",");
    API.get("/users/assignable")
      .then((response) => {
        const candidates = Array.isArray(response.data) ? response.data : [];
        setUsers(candidates.filter((user) => allowedRoles.includes(user.role)));
      })
      .catch(() => setUsers([]));
  }, [rolesKey]);

  return (
    <select
      value={value}
      onChange={(event) => onChange(event.target.value)}
      className={`rounded-lg border border-gray-200 px-3 py-2 text-sm ${className}`}
    >
      <option value="">Select user</option>
      {users.map((user) => (
        <option key={user.id} value={user.id}>
          {user.name} ({user.role})
        </option>
      ))}
    </select>
  );
}
