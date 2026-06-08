import {
  Trash2,
} from "lucide-react";

export default function MemberTable({
  members,
  onRoleChange,
  onRemove,
}) {
  return (
    <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
      <table className="w-full">
        <thead className="bg-slate-50">
          <tr>
            <th className="text-left px-4 py-3">
              User
            </th>

            <th className="text-left px-4 py-3">
              Email
            </th>

            <th className="text-left px-4 py-3">
              Role
            </th>

            <th className="text-right px-4 py-3">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          {members.map((member) => (
            <tr
              key={member.id}
              className="border-t"
            >
              <td className="px-4 py-3">
                {member.user?.name || "Unknown"}
              </td>

              <td className="px-4 py-3">
                {member.user?.email || "-"}
              </td>

              <td className="px-4 py-3">
                <select
                  value={member.role}
                  onChange={(e) =>
                    onRoleChange(
                      member,
                      e.target.value
                    )
                  }
                  className="border rounded-lg px-3 py-2"
                >
                  <option value="WORKSPACE_ADMIN">
                    Workspace Admin
                  </option>

                  <option value="MANAGER">
                    Manager
                  </option>

                  <option value="EMPLOYEE">
                    Employee
                  </option>
                </select>
              </td>

              <td className="px-4 py-3">
                <div className="flex justify-end">
                  <button
                    onClick={() =>
                      onRemove(member)
                    }
                    className="p-2 rounded-lg text-red-600 hover:bg-red-50"
                  >
                    <Trash2 size={18} />
                  </button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}