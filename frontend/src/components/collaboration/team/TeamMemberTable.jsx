import { useState } from "react";

export default function TeamMembers({
  members = [],
  onAdd,
  onRemove,
}) {
  const [formData, setFormData] =
    useState({
      user_id: "",
      role: "MEMBER",
    });

  const handleSubmit = (e) => {
    e.preventDefault();

    onAdd({
      user_id: Number(
        formData.user_id
      ),
      role: formData.role,
    });

    setFormData({
      user_id: "",
      role: "MEMBER",
    });
  };

  return (
    <div className="bg-white border rounded-lg p-4">
      <h2 className="text-lg font-semibold mb-4">
        Team Members
      </h2>

      <form
        onSubmit={handleSubmit}
        className="flex flex-wrap gap-3 mb-6"
      >
        <input
          type="number"
          placeholder="User ID"
          value={formData.user_id}
          onChange={(e) =>
            setFormData({
              ...formData,
              user_id:
                e.target.value,
            })
          }
          className="border rounded px-3 py-2"
        />

        <select
          value={formData.role}
          onChange={(e) =>
            setFormData({
              ...formData,
              role:
                e.target.value,
            })
          }
          className="border rounded px-3 py-2"
        >
          <option value="LEAD">
            LEAD
          </option>
          <option value="MEMBER">
            MEMBER
          </option>
          <option value="VIEWER">
            VIEWER
          </option>
        </select>

        <button
          type="submit"
          className="bg-green-600 text-white px-4 py-2 rounded"
        >
          Add Member
        </button>
      </form>

      <table className="w-full">
        <thead>
          <tr className="border-b">
            <th className="p-2 text-left">
              User ID
            </th>

            <th className="p-2 text-left">
              Role
            </th>

            <th className="p-2 text-left">
              Actions
            </th>
          </tr>
        </thead>

        <tbody>
          {members.map(
            (member) => (
              <tr
                key={
                  member.id ||
                  member.user_id
                }
                className="border-b"
              >
                <td className="p-2">
                  {
                    member.user_id
                  }
                </td>

                <td className="p-2">
                  {member.role}
                </td>

                <td className="p-2">
                  <button
                    onClick={() =>
                      onRemove(
                        member.user_id
                      )
                    }
                    className="text-red-600"
                  >
                    Remove
                  </button>
                </td>
              </tr>
            )
          )}

          {!members.length && (
            <tr>
              <td
                colSpan={3}
                className="p-4 text-center text-gray-500"
              >
                No members found
              </td>
            </tr>
          )}
        </tbody>
      </table>
    </div>
  );
}