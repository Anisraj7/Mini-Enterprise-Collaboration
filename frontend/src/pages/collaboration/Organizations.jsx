import { useCallback, useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  activateOrganization,
  deleteOrganization,
  getOrganizations,
  suspendOrganization,
} from "../../services/collaboration/organizationService";

export default function Organizations() {
  const navigate = useNavigate();

  const [organizations, setOrganizations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState("");

  const loadOrganizations = useCallback(async () => {
    try {
      const data = await getOrganizations();
      setOrganizations(data);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadOrganizations();
  }, [loadOrganizations]);

  const handleSuspend = async (organizationId) => {
    try {
      await suspendOrganization(organizationId);
      await loadOrganizations();
    } catch (error) {
      console.error(error);
    }
  };

  const handleActivate = async (organizationId) => {
    try {
      await activateOrganization(organizationId);
      await loadOrganizations();
    } catch (error) {
      console.error(error);
    }
  };

  const handleDelete = async (organizationId) => {
    if (
      !window.confirm(
        "Delete this organization? This action cannot be undone."
      )
    ) {
      return;
    }

    try {
      await deleteOrganization(organizationId);
      await loadOrganizations();
    } catch (error) {
      console.error(error);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("user");
    localStorage.removeItem("role");

    navigate("/");
  };

  const filteredOrganizations = organizations.filter(
    (organization) =>
      organization.name
        ?.toLowerCase()
        .includes(search.toLowerCase()) ||
      organization.contact_email
        ?.toLowerCase()
        .includes(search.toLowerCase())
  );

  const totalOrganizations = organizations.length;

  const activeOrganizations = organizations.filter(
    (organization) =>
      organization.status === "ACTIVE"
  ).length;

  const suspendedOrganizations = organizations.filter(
    (organization) =>
      organization.status === "SUSPENDED"
  ).length;

  const trialOrganizations = organizations.filter(
    (organization) =>
      organization.status === "TRIAL"
  ).length;

  if (loading) {
    return (
      <div className="p-6">
        Loading organizations...
      </div>
    );
  }

  return (
    <div className="space-y-6">

      {/* Header */}
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold">
            Organization Management
          </h1>

          <p className="text-gray-500 mt-1">
            Manage SaaS organizations and collaboration settings.
          </p>
        </div>

        <div className="flex gap-3">
          <button
            onClick={() =>
              navigate("/organizations/onboard")
            }
            className="bg-blue-600 text-white px-4 py-2 rounded-lg"
          >
            Onboard Organization
          </button>

          <button
            onClick={handleLogout}
            className="bg-gray-200 text-gray-800 px-4 py-2 rounded-lg"
          >
            Logout
          </button>
        </div>
      </div>

      {/* Statistics */}
      <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-4 gap-5">

        <div className="bg-white border rounded-xl p-5">
          <p className="text-sm text-gray-500">
            Total Organizations
          </p>

          <h2 className="text-3xl font-bold mt-2">
            {totalOrganizations}
          </h2>
        </div>

        <div className="bg-white border rounded-xl p-5">
          <p className="text-sm text-gray-500">
            Active
          </p>

          <h2 className="text-3xl font-bold mt-2 text-green-600">
            {activeOrganizations}
          </h2>
        </div>

        <div className="bg-white border rounded-xl p-5">
          <p className="text-sm text-gray-500">
            Suspended
          </p>

          <h2 className="text-3xl font-bold mt-2 text-red-600">
            {suspendedOrganizations}
          </h2>
        </div>

        <div className="bg-white border rounded-xl p-5">
          <p className="text-sm text-gray-500">
            Trial
          </p>

          <h2 className="text-3xl font-bold mt-2 text-yellow-600">
            {trialOrganizations}
          </h2>
        </div>

      </div>

      {/* Search */}
      <div className="bg-white border rounded-xl p-5">
        <input
          type="text"
          placeholder="Search organizations..."
          value={search}
          onChange={(e) =>
            setSearch(e.target.value)
          }
          className="w-full border rounded-lg px-4 py-3"
        />
      </div>

      {/* Table */}
      <div className="bg-white border rounded-xl overflow-hidden">

        <div className="overflow-x-auto">

          <table className="w-full">

            <thead className="bg-gray-50 border-b">
              <tr>
                <th className="text-left px-4 py-3">
                  Name
                </th>

                <th className="text-left px-4 py-3">
                  Email
                </th>

                <th className="text-left px-4 py-3">
                  Plan
                </th>

                <th className="text-left px-4 py-3">
                  Status
                </th>

                <th className="text-left px-4 py-3">
                  Slug
                </th>

                <th className="text-left px-4 py-3">
                  Actions
                </th>
              </tr>
            </thead>

            <tbody>

              {filteredOrganizations.map(
                (organization) => (
                  <tr
                    key={organization.id}
                    className="border-b"
                  >

                    <td className="px-4 py-3 font-medium">
                      {organization.name}
                    </td>

                    <td className="px-4 py-3">
                      {organization.contact_email}
                    </td>

                    <td className="px-4 py-3">
                      {organization.plan}
                    </td>

                    <td className="px-4 py-3">
                      <span
                        className={`px-2 py-1 rounded-full text-xs ${
                          organization.status ===
                          "ACTIVE"
                            ? "bg-green-100 text-green-700"
                            : "bg-red-100 text-red-700"
                        }`}
                      >
                        {organization.status}
                      </span>
                    </td>

                    <td className="px-4 py-3">
                      {organization.slug}
                    </td>

                    <td className="px-4 py-3">

                      <div className="flex flex-wrap gap-2">

                        <button
                          onClick={() =>
                            navigate(
                              `/organizations/${organization.id}`
                            )
                          }
                          className="border px-3 py-1 rounded"
                        >
                          View
                        </button>

                        <button
                          onClick={() =>
                            navigate(
                              `/organizations/${organization.id}/settings`
                            )
                          }
                          className="border px-3 py-1 rounded text-blue-600"
                        >
                          Settings
                        </button>

                        <button
                          onClick={() =>
                            navigate(
                              `/organizations/${organization.id}/usage`
                            )
                          }
                          className="border px-3 py-1 rounded text-purple-600"
                        >
                          Usage
                        </button>

                        {organization.status ===
                        "ACTIVE" ? (
                          <button
                            onClick={() =>
                              handleSuspend(
                                organization.id
                              )
                            }
                            className="border px-3 py-1 rounded text-red-600"
                          >
                            Suspend
                          </button>
                        ) : (
                          <button
                            onClick={() =>
                              handleActivate(
                                organization.id
                              )
                            }
                            className="border px-3 py-1 rounded text-green-600"
                          >
                            Activate
                          </button>
                        )}

                        <button
                          onClick={() =>
                            handleDelete(
                              organization.id
                            )
                          }
                          className="border px-3 py-1 rounded text-gray-700"
                        >
                          Delete
                        </button>

                      </div>

                    </td>

                  </tr>
                )
              )}

              {filteredOrganizations.length ===
                0 && (
                <tr>
                  <td
                    colSpan="6"
                    className="text-center py-8 text-gray-500"
                  >
                    No organizations found.
                  </td>
                </tr>
              )}

            </tbody>

          </table>

        </div>

      </div>

    </div>
  );
}