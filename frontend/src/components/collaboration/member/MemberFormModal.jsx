import { useState } from "react";

export default function MemberFormModal({
  onClose,
  onSubmit,
}) {
  const [formData, setFormData] =
    useState({
      user_id: "",
      role: "EMPLOYEE",
    });

  const handleSubmit = (
    e
  ) => {
    e.preventDefault();

    onSubmit({
      ...formData,
      user_id: Number(
        formData.user_id
      ),
    });
  };

  return (
    <div className="fixed inset-0 bg-black/40 flex justify-center items-center z-50">
      <div className="bg-white rounded-xl w-full max-w-md p-6">
        <div className="flex justify-between items-center mb-5">
          <h2 className="text-lg font-bold">
            Add Member
          </h2>

          <button
            type="button"
            onClick={onClose}
          >
            ✕
          </button>
        </div>

        <form
          onSubmit={
            handleSubmit
          }
          className="space-y-4"
        >
          <div>
            <label className="block mb-1 text-sm">
              User ID
            </label>

            <input
              type="number"
              value={
                formData.user_id
              }
              onChange={(
                e
              ) =>
                setFormData({
                  ...formData,
                  user_id:
                    e.target
                      .value,
                })
              }
              className="w-full border rounded-lg px-3 py-2"
              required
            />
          </div>

          <div>
            <label className="block mb-1 text-sm">
              Role
            </label>

            <select
              value={
                formData.role
              }
              onChange={(
                e
              ) =>
                setFormData({
                  ...formData,
                  role: e
                    .target
                    .value,
                })
              }
              className="w-full border rounded-lg px-3 py-2"
            >
              <option value="EMPLOYEE">
                Employee
              </option>

              <option value="MANAGER">
                Manager
              </option>

              <option value="WORKSPACE_ADMIN">
                Workspace Admin
              </option>
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
              Add
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}