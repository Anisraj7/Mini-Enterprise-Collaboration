import {
  Edit,
  UserCheck,
  UserX,
} from "lucide-react";

export default function UserTable({
  users,
  onEdit,
  onActivate,
  onDeactivate,
}) {
  return (
    <div className="bg-white rounded-xl shadow-sm border overflow-hidden">
      <table className="w-full">
        <thead className="bg-slate-50">
          <tr>
            <th className="text-left px-4 py-3">
              Name
            </th>

            <th className="text-left px-4 py-3">
              Email
            </th>

            <th className="text-left px-4 py-3">
              Role
            </th>

            <th className="text-left px-4 py-3">
              Status
            </th>

            <th className="text-right px-4 py-3">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          {users?.length > 0 ? (
            users.map((user) => (
              <tr
                key={user.id}
                className="border-t"
              >
                <td className="px-4 py-3">
                  {user.name}
                </td>

                <td className="px-4 py-3">
                  {user.email}
                </td>

                <td className="px-4 py-3">
                  <span className="px-2 py-1 rounded bg-slate-100 text-sm">
                    {user.role}
                  </span>
                </td>

                <td className="px-4 py-3">
                  {user.is_active ? (
                    <span className="px-2 py-1 rounded bg-green-100 text-green-700 text-sm">
                      Active
                    </span>
                  ) : (
                    <span className="px-2 py-1 rounded bg-red-100 text-red-700 text-sm">
                      Inactive
                    </span>
                  )}
                </td>

                <td className="px-4 py-3">
                  <div className="flex justify-end gap-2">
                    <button
                      onClick={() =>
                        onEdit(user)
                      }
                      className="p-2 rounded-lg text-blue-600 hover:bg-blue-50"
                    >
                      <Edit size={18} />
                    </button>

                    {user.is_active ? (
                      <button
                        onClick={() =>
                          onDeactivate(user)
                        }
                        className="p-2 rounded-lg text-red-600 hover:bg-red-50"
                      >
                        <UserX size={18} />
                      </button>
                    ) : (
                      <button
                        onClick={() =>
                          onActivate(user)
                        }
                        className="p-2 rounded-lg text-green-600 hover:bg-green-50"
                      >
                        <UserCheck size={18} />
                      </button>
                    )}
                  </div>
                </td>
              </tr>
            ))
          ) : (
            <tr>
              <td
                colSpan="5"
                className="px-4 py-8 text-center text-slate-500"
              >
                No users found
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}