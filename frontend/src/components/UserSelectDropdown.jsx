import { useEffect, useState } from "react";
import API from "../api/axios";

export default function UserSelectDropdown({
  value,
  onChange,
  roles = [
    "organization_admin",
    "workspace_admin",
    "manager",
  ],
  className = "",
}) {
  const [users, setUsers] = useState([]);

  const rolesKey = roles.join(",");

  useEffect(() => {
    const loadUsers = async () => {
      try {
        const response = await API.get("/users/assignable");

        const candidates = Array.isArray(response.data)
          ? response.data
          : response.data?.items || [];

        const allowedRoles = rolesKey
          .split(",")
          .map((role) => role.toLowerCase());

        const filteredUsers = candidates.filter((user) =>
          allowedRoles.includes(
            String(user.role).toLowerCase()
          )
        );

        setUsers(filteredUsers);

        console.log("Users:", filteredUsers);
      } catch (error) {
        console.error(error);
        setUsers([]);
      }
    };

    loadUsers();
  }, [rolesKey]);

  return (
    <select
      value={value}
      onChange={(event) => onChange(event.target.value)}
      className={`rounded-lg border border-gray-200 px-3 py-2 text-sm ${className}`}
    >
      <option value="">
        Select User
      </option>

      {users.map((user) => (
        <option
          key={user.id}
          value={user.id}
        >
          {user.name} ({user.role})
        </option>
      ))}
    </select>
  );
}