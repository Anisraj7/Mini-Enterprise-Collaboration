import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import { useNavigate } from "react-router-dom";

import {
  getOrganizationById,
  getOnboardingStatus,
  updateOrganization,
} from "../../services/collaboration/organizationService";

export default function OrganizationDetails() {
  const { organizationId } = useParams();

  const [organization, setOrganization] = useState(null);

  const [onboarding, setOnboarding] = useState(null);

  const [loading, setLoading] = useState(true);

  const [editMode, setEditMode] = useState(false);

  const [formData, setFormData] = useState({
    name: "",
    contact_email: "",
    phone: "",
    address: "",
    industry: "",
    plan: "",
  });

  const navigate = useNavigate();

  const currentUser = JSON.parse(localStorage.getItem("user") || "{}");

  const [saving, setSaving] = useState(false);

  const loadData = useCallback(async () => {
    try {
      const organizationData = await getOrganizationById(organizationId);

      setOrganization(organizationData);

      setFormData({
        name: organizationData.name || "",
        contact_email: organizationData.contact_email || "",
        phone: organizationData.phone || "",
        address: organizationData.address || "",
        industry: organizationData.industry || "",
        plan: organizationData.plan || "",
      });

      try {
        const onboardingData = await getOnboardingStatus(organizationId);

        setOnboarding(onboardingData);
      } catch {
        setOnboarding(null);
      }
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, [organizationId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleFormChange = (event) => {
    const { name, value } = event.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleEdit = () => {
    setEditMode(true);
  };

  const handleCancel = () => {
    if (organization) {
      setFormData({
        name: organization.name || "",
        contact_email: organization.contact_email || "",
        phone: organization.phone || "",
        address: organization.address || "",
        industry: organization.industry || "",
        plan: organization.plan || "",
      });
    }
    setEditMode(false);
  };

  const handleSave = async () => {
    if (!organization) {
      return;
    }

    setSaving(true);

    try {
      const updated = await updateOrganization(organizationId, formData);

      setOrganization(updated);
      setEditMode(false);
    } catch (error) {
      console.error(error);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <div>Loading organization...</div>;
  }

  if (!organization) {
    return <div>Organization not found.</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">{organization.name}</h1>

        <p className="text-gray-500">Organization Details</p>
      </div>

      {/* Organization Information */}
      <div className="bg-white border rounded-xl p-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4 mb-4">
          <div>
            <h2 className="text-xl font-semibold">Organization Information</h2>
          </div>

          <div className="flex gap-3">
            {editMode ? (
              <>
                <button
                  onClick={handleCancel}
                  className="border px-4 py-2 rounded-lg text-gray-700"
                >
                  Cancel
                </button>

                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg"
                >
                  {saving ? "Saving..." : "Save"}
                </button>
              </>
            ) : (
              <>
                {["super_admin", "organization_admin"].includes(
                  currentUser?.role,
                ) && (
                  <button
                    onClick={() => navigate("/organization-users")}
                    className="bg-green-600 text-white px-4 py-2 rounded-lg hover:bg-green-700"
                  >
                    Manage Users
                  </button>
                )}

                {["super_admin", "organization_admin"].includes(
                  currentUser?.role,
                ) && (
                  <button
                    onClick={handleEdit}
                    className="bg-blue-600 text-white px-4 py-2 rounded-lg"
                  >
                    Edit
                  </button>
                )}
              </>
            )}
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-4">
          <div>
            <p className="text-sm text-gray-500">Name</p>
            {editMode ? (
              <input
                name="name"
                value={formData.name}
                onChange={handleFormChange}
                className="w-full border rounded-lg px-4 py-2"
              />
            ) : (
              <p>{organization.name}</p>
            )}
          </div>

          <div>
            <p className="text-sm text-gray-500">Slug</p>
            <p>{organization.slug}</p>
          </div>

          <div>
            <p className="text-sm text-gray-500">Contact Email</p>
            {editMode ? (
              <input
                name="contact_email"
                value={formData.contact_email}
                onChange={handleFormChange}
                className="w-full border rounded-lg px-4 py-2"
              />
            ) : (
              <p>{organization.contact_email}</p>
            )}
          </div>

          <div>
            <p className="text-sm text-gray-500">Phone</p>
            {editMode ? (
              <input
                name="phone"
                value={formData.phone}
                onChange={handleFormChange}
                className="w-full border rounded-lg px-4 py-2"
              />
            ) : (
              <p>{organization.phone || "-"}</p>
            )}
          </div>

          <div>
            <p className="text-sm text-gray-500">Industry</p>
            {editMode ? (
              <input
                name="industry"
                value={formData.industry}
                onChange={handleFormChange}
                className="w-full border rounded-lg px-4 py-2"
              />
            ) : (
              <p>{organization.industry || "-"}</p>
            )}
          </div>

          <div>
            <p className="text-sm text-gray-500">Plan</p>
            {editMode ? (
              <input
                name="plan"
                value={formData.plan}
                onChange={handleFormChange}
                className="w-full border rounded-lg px-4 py-2"
              />
            ) : (
              <p>{organization.plan}</p>
            )}
          </div>

          <div>
            <p className="text-sm text-gray-500">Status</p>
            <p>{organization.status}</p>
          </div>

          <div>
            <p className="text-sm text-gray-500">Created</p>
            <p>{new Date(organization.created_at).toLocaleString()}</p>
          </div>
        </div>
      </div>

      {/* Onboarding */}
      <div className="bg-white border rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-4">Onboarding Status</h2>

        {onboarding ? (
          <div className="space-y-3">
            <div>
              <span className="font-medium">Status:</span>{" "}
              {onboarding.onboarding_status}
            </div>

            <div>
              <span className="font-medium">Settings Created:</span>{" "}
              {onboarding.settings_created ? "Yes" : "No"}
            </div>

            <div>
              <span className="font-medium">Default Workspace:</span>{" "}
              {onboarding.default_workspace_created ? "Yes" : "No"}
            </div>

            <div>
              <span className="font-medium">Admin User ID:</span>{" "}
              {onboarding.admin_user_id || "-"}
            </div>
          </div>
        ) : (
          <p className="text-gray-500">No onboarding record found.</p>
        )}
      </div>

      {/* Future Sections */}
      {/* <div className="bg-white border rounded-xl p-6">
        <h2 className="text-xl font-semibold mb-2">Phase 10A</h2>

        <p className="text-gray-500">
          Collaboration Settings, Usage Statistics, Workspaces and Channels will
          be linked here.
        </p>
      </div> */}
    </div>
  );
}
