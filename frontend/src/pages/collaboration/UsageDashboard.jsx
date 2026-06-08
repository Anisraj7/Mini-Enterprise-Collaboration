import { useCallback, useEffect, useState } from "react";

import { Activity, Building2, Hash, RefreshCw, Users } from "lucide-react";

import {
  getOrganizationUsage,
  recalculateOrganizationUsage,
} from "../../services/collaboration/organizationService";

import { useParams } from "react-router-dom";

export default function UsageDashboard() {
  const { organizationId } = useParams();

  const [usage, setUsage] = useState(null);

  const [loading, setLoading] = useState(true);

  const [recalculating, setRecalculating] = useState(false);

  const loadUsage = useCallback(async () => {
    try {
      const data = await getOrganizationUsage(organizationId);

      setUsage(data);
    } catch (error) {
      console.error(error);

      alert("Failed to load usage");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadUsage();
  }, [loadUsage]);

  const handleRecalculate = async () => {
    try {
      setRecalculating(true);

      const data = await recalculateOrganizationUsage(organizationId);

      setUsage(data);

      alert("Usage recalculated successfully");
    } catch (error) {
      console.error(error);

      alert(error?.response?.data?.detail || "Failed to recalculate usage");
    } finally {
      setRecalculating(false);
    }
  };

  if (loading) {
    return <div>Loading usage...</div>;
  }

  if (!usage) {
    return <div>Usage data unavailable.</div>;
  }

  const cards = [
    {
      title: "Workspaces",
      value: usage.workspace_count ?? 0,
      icon: Building2,
    },
    {
      title: "Channels",
      value: usage.channel_count ?? 0,
      icon: Hash,
    },
    {
      title: "Members",
      value: usage.member_count ?? 0,
      icon: Users,
    },
    {
      title: "Storage (MB)",
      value: usage.storage_used_mb ?? 0,
      icon: Activity,
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">Organization Usage</h1>

          <p className="text-gray-500">
            Collaboration usage statistics and limits.
          </p>
        </div>

        <button
          onClick={handleRecalculate}
          disabled={recalculating}
          className="flex items-center gap-2 bg-blue-600 text-white px-4 py-2 rounded-lg disabled:opacity-50"
        >
          <RefreshCw size={18} />

          {recalculating ? "Recalculating..." : "Recalculate Usage"}
        </button>
      </div>

      <div className="grid md:grid-cols-2 xl:grid-cols-4 gap-5">
        {cards.map((card) => {
          const Icon = card.icon;

          return (
            <div key={card.title} className="bg-white border rounded-xl p-5">
              <div className="flex justify-between">
                <div>
                  <p className="text-gray-500 text-sm">{card.title}</p>

                  <h2 className="text-3xl font-bold mt-2">{card.value}</h2>
                </div>

                <Icon size={26} />
              </div>
            </div>
          );
        })}
      </div>

      <div className="bg-white border rounded-xl p-5">
        <h2 className="font-semibold mb-3">Last Calculation</h2>

        <p className="text-gray-600">
          {usage.last_calculated_at
            ? new Date(usage.last_calculated_at).toLocaleString()
            : "Not calculated yet"}
        </p>
      </div>
    </div>
  );
}
