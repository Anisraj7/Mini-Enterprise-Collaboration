import { useEffect, useState } from "react";

import API from "../api/axios";
import ErrorMessage from "../components/ErrorMessage";
import LoadingSpinner from "../components/LoadingSpinner";
import Navbar from "../components/Navbar";
import PageHeader from "../components/PageHeader";
import ToggleSwitch from "../components/ToggleSwitch";

const preferenceFields = [
  ["in_app_enabled", "In-app Notifications"],
  ["email_enabled", "Email Notifications"],
  ["task_notifications", "Task Notifications"],
  ["approval_notifications", "Approval Notifications"],
  ["escalation_notifications", "Escalation Notifications"],
  ["document_notifications", "Document Notifications"],
];

export default function NotificationPreferences() {
  const [preferences, setPreferences] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  useEffect(() => {
    API.get("/notification-preferences/me")
      .then((response) => {
        const data = response.data?.items
          ? response.data.items[0]
          : response.data;

        setPreferences(data || {});
        setError("");
      })
      .catch((err) =>
        setError(
          err.response?.data?.detail ||
            "Unable to load notification preferences.",
        ),
      )
      .finally(() => setLoading(false));
  }, []);

  const savePreferences = async () => {
    try {
      setSaving(true);
      await API.put("/notification-preferences/me", preferences);
      setSuccess("Preferences updated successfully.");
      setError("");
    } catch (err) {
      setError(
        err.response?.data?.detail ||
          "Unable to update notification preferences.",
      );
      setSuccess("");
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <main className="mx-auto max-w-3xl p-6">
        <PageHeader
          title="Notification Preferences"
          subtitle="Choose which workflow notifications you receive"
        />
        <ErrorMessage message={error} />
        {success && (
          <div className="mb-4 rounded-lg border border-green-200 bg-green-50 px-4 py-3 text-sm text-green-700">
            {success}
          </div>
        )}

        {loading || !preferences ? (
          <LoadingSpinner />
        ) : (
          <div className="rounded-lg bg-white p-6 shadow-sm">
            <div className="divide-y divide-gray-100">
              {preferences &&
                preferenceFields.map(([key, label]) => (
                  <div
                    key={key}
                    className="flex items-center justify-between gap-4 py-4"
                  >
                    <span className="font-medium text-gray-800">{label}</span>
                    <ToggleSwitch
                      label={label}
                      checked={Boolean(preferences[key])}
                      onChange={(value) =>
                        setPreferences((prev) => ({
                          ...prev,
                          [key]: value,
                        }))
                      }
                    />
                  </div>
                ))}
            </div>
            <div className="mt-6 flex justify-end">
              <button
                type="button"
                disabled={saving}
                onClick={savePreferences}
                className="rounded-lg bg-blue-600 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-700 disabled:bg-gray-300"
              >
                {saving ? "Saving..." : "Save Preferences"}
              </button>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}
