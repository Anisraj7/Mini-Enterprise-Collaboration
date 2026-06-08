import { useCallback, useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
  getOrganizationSettings,
  updateOrganizationSettings,
} from "../../services/collaboration/organizationService";

export default function OrganizationSettings() {
  const { organizationId } = useParams();

  const [settings, setSettings] = useState({
    max_workspaces: 0,
    max_channels_per_workspace: 0,
    max_workspace_members: 0,
    max_storage_mb: 0,
    workspace_enabled: false,
    channel_enabled: false,
  });

  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const loadSettings = useCallback(async () => {
    try {
      setLoading(true);

      const data = await getOrganizationSettings(
        organizationId
      );

      setSettings({
        max_workspaces: data.max_workspaces ?? 0,
        max_channels_per_workspace:
          data.max_channels_per_workspace ?? 0,
        max_workspace_members:
          data.max_workspace_members ?? 0,
        max_storage_mb:
          data.max_storage_mb ?? 0,
        workspace_enabled:
          data.workspace_enabled ?? false,
        channel_enabled:
          data.channel_enabled ?? false,
      });
    } catch (error) {
      console.error(error);

      alert(
        error?.response?.data?.detail ||
        "Failed to load settings"
      );
    } finally {
      setLoading(false);
    }
  }, [organizationId]);

  useEffect(() => {
    if (organizationId) {
      loadSettings();
    }
  }, [loadSettings, organizationId]);

  const handleChange = (e) => {
    const {
      name,
      value,
      type,
      checked,
    } = e.target;

    setSettings((prev) => ({
      ...prev,
      [name]:
        type === "checkbox"
          ? checked
          : type === "number"
          ? Number(value)
          : value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      setSaving(true);

      await updateOrganizationSettings(
        organizationId,
        {
          max_workspaces:
            settings.max_workspaces,

          max_channels_per_workspace:
            settings.max_channels_per_workspace,

          max_workspace_members:
            settings.max_workspace_members,

          max_storage_mb:
            settings.max_storage_mb,

          workspace_enabled:
            settings.workspace_enabled,

          channel_enabled:
            settings.channel_enabled,
        }
      );

      alert(
        "Settings updated successfully"
      );

      await loadSettings();
    } catch (error) {
      console.error(error);

      alert(
        error?.response?.data?.detail ||
        "Failed to update settings"
      );
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return (
      <div className="p-6">
        Loading settings...
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white border rounded-xl p-6">
        <h1 className="text-2xl font-bold mb-2">
          Organization Settings
        </h1>

        <p className="text-gray-500 mb-6">
          Configure collaboration limits
          and feature access for this
          organization.
        </p>

        <form
          onSubmit={handleSubmit}
          className="space-y-5"
        >
          <div>
            <label className="block mb-2 font-medium">
              Maximum Workspaces
            </label>

            <input
              type="number"
              min="1"
              name="max_workspaces"
              value={settings.max_workspaces}
              onChange={handleChange}
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>

          <div>
            <label className="block mb-2 font-medium">
              Maximum Channels Per Workspace
            </label>

            <input
              type="number"
              min="1"
              name="max_channels_per_workspace"
              value={
                settings.max_channels_per_workspace
              }
              onChange={handleChange}
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>

          <div>
            <label className="block mb-2 font-medium">
              Maximum Workspace Members
            </label>

            <input
              type="number"
              min="1"
              name="max_workspace_members"
              value={
                settings.max_workspace_members
              }
              onChange={handleChange}
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>

          <div>
            <label className="block mb-2 font-medium">
              Maximum Storage (MB)
            </label>

            <input
              type="number"
              min="1"
              name="max_storage_mb"
              value={settings.max_storage_mb}
              onChange={handleChange}
              className="w-full border rounded-lg px-3 py-2"
            />
          </div>

          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              name="workspace_enabled"
              checked={
                settings.workspace_enabled
              }
              onChange={handleChange}
            />

            Enable Workspace Module
          </label>

          <label className="flex items-center gap-3">
            <input
              type="checkbox"
              name="channel_enabled"
              checked={
                settings.channel_enabled
              }
              onChange={handleChange}
            />

            Enable Channel Module
          </label>

          <button
            type="submit"
            disabled={saving}
            className="bg-blue-600 text-white px-5 py-2 rounded-lg disabled:opacity-50"
          >
            {saving
              ? "Saving..."
              : "Save Settings"}
          </button>
        </form>
      </div>
    </div>
  );
}