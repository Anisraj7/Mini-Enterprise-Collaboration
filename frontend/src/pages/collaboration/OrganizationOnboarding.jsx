import { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  onboardOrganization,
} from "../../services/collaboration/organizationService";

export default function OrganizationOnboarding() {
  const navigate = useNavigate();

  const [loading, setLoading] =
    useState(false);

  const [formData, setFormData] =
    useState({
      organization_name: "",
      organization_email: "",
      admin_name: "",
      admin_email: "",
      password: "",
      create_default_workspace: true,
    });

  const handleChange = (e) => {
    const {
      name,
      value,
      type,
      checked,
    } = e.target;

    setFormData((prev) => ({
      ...prev,
      [name]:
        type === "checkbox"
          ? checked
          : value,
    }));
  };

  const handleSubmit =
    async (e) => {
      e.preventDefault();

      try {
        setLoading(true);

        await onboardOrganization(
          formData
        );

        alert(
          "Organization onboarded successfully"
        );

        setFormData({
          organization_name: "",
          organization_email: "",
          admin_name: "",
          admin_email: "",
          password: "",
          create_default_workspace: true,
        });

        navigate(
          "/organizations"
        );
      } catch (error) {
        console.error(error);

        alert(
          error?.response?.data
            ?.detail ||
            "Failed to onboard organization"
        );
      } finally {
        setLoading(false);
      }
    };

  return (
    <div className="max-w-4xl mx-auto p-6">
      <div className="bg-white rounded-xl border shadow-sm p-8">
        <h1 className="text-3xl font-bold mb-2">
          Organization Onboarding
        </h1>

        <p className="text-gray-500 mb-8">
          Create a new organization
          and its first
          Organization Admin.
        </p>

        <form
          onSubmit={handleSubmit}
          className="space-y-6"
        >
          <div>
            <label className="block mb-2 font-medium">
              Organization Name
            </label>

            <input
              type="text"
              name="organization_name"
              value={
                formData.organization_name
              }
              onChange={
                handleChange
              }
              required
              className="w-full border rounded-lg px-4 py-3"
            />
          </div>

          <div>
            <label className="block mb-2 font-medium">
              Organization Email
            </label>

            <input
              type="email"
              name="organization_email"
              value={
                formData.organization_email
              }
              onChange={
                handleChange
              }
              required
              className="w-full border rounded-lg px-4 py-3"
            />
          </div>

          <div className="border-t pt-6">
            <h2 className="text-lg font-semibold mb-4">
              Organization Admin
            </h2>

            <div className="space-y-4">
              <div>
                <label className="block mb-2 font-medium">
                  Admin Name
                </label>

                <input
                  type="text"
                  name="admin_name"
                  value={
                    formData.admin_name
                  }
                  onChange={
                    handleChange
                  }
                  required
                  className="w-full border rounded-lg px-4 py-3"
                />
              </div>

              <div>
                <label className="block mb-2 font-medium">
                  Admin Email
                </label>

                <input
                  type="email"
                  name="admin_email"
                  value={
                    formData.admin_email
                  }
                  onChange={
                    handleChange
                  }
                  required
                  className="w-full border rounded-lg px-4 py-3"
                />
              </div>

              <div>
                <label className="block mb-2 font-medium">
                  Admin Password
                </label>

                <input
                  type="password"
                  name="password"
                  value={
                    formData.password
                  }
                  onChange={
                    handleChange
                  }
                  minLength={8}
                  required
                  className="w-full border rounded-lg px-4 py-3"
                />
              </div>
            </div>
          </div>

          <div className="flex items-center gap-3">
            <input
              type="checkbox"
              name="create_default_workspace"
              checked={
                formData.create_default_workspace
              }
              onChange={
                handleChange
              }
            />

            <label>
              Create Default Workspace
            </label>
          </div>

          <div className="flex justify-end gap-3">
            <button
              type="button"
              onClick={() =>
                navigate(-1)
              }
              className="px-5 py-3 border rounded-lg"
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={loading}
              className="px-5 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {loading
                ? "Creating..."
                : "Create Organization"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}