import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import {
  getTeamWorkload,
  getProjectWorkload,
} from "../../services/collaboration/workloadService";

export default function WorkloadDashboard() {
  const { teamId, projectId } =
    useParams();

  const [workload, setWorkload] =
    useState(null);

  const [loading, setLoading] =
    useState(true);

  const loadWorkload =
    async () => {
      try {
        setLoading(true);

        let response;

        if (teamId) {
          response =
            await getTeamWorkload(
              teamId
            );
        } else {
          response =
            await getProjectWorkload(
              projectId
            );
        }

        setWorkload(response);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

  useEffect(() => {
    loadWorkload();
  }, [teamId, projectId]);

  if (loading) {
    return (
      <div className="p-6">
        Loading workload...
      </div>
    );
  }

  if (!workload) {
    return (
      <div className="p-6">
        No workload data available
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold">
          Workload Dashboard
        </h1>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">

        <div className="bg-white border rounded-lg p-4">
          <p className="text-sm text-gray-500">
            Total Tasks
          </p>

          <p className="text-2xl font-bold">
            {workload.total_tasks ??
              0}
          </p>
        </div>

        <div className="bg-white border rounded-lg p-4">
          <p className="text-sm text-gray-500">
            Completed
          </p>

          <p className="text-2xl font-bold text-green-600">
            {workload.completed_tasks ??
              0}
          </p>
        </div>

        <div className="bg-white border rounded-lg p-4">
          <p className="text-sm text-gray-500">
            Pending
          </p>

          <p className="text-2xl font-bold text-yellow-600">
            {workload.pending_tasks ??
              0}
          </p>
        </div>

        <div className="bg-white border rounded-lg p-4">
          <p className="text-sm text-gray-500">
            Overdue
          </p>

          <p className="text-2xl font-bold text-red-600">
            {workload.overdue_tasks ??
              0}
          </p>
        </div>

      </div>

      {(workload.users ||
        workload.members ||
        workload.teams) && (
        <div className="bg-white border rounded-lg">
          <div className="p-4 border-b">
            <h2 className="font-semibold">
              Breakdown
            </h2>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b bg-gray-50">
                  <th className="p-3 text-left">
                    Name
                  </th>

                  <th className="p-3 text-left">
                    Assigned
                  </th>

                  <th className="p-3 text-left">
                    Completed
                  </th>

                  <th className="p-3 text-left">
                    Pending
                  </th>

                  <th className="p-3 text-left">
                    Overdue
                  </th>
                </tr>
              </thead>

              <tbody>
                {(
                  workload.users ||
                  workload.members ||
                  workload.teams ||
                  []
                ).map(
                  (
                    item,
                    index
                  ) => (
                    <tr
                      key={
                        item.id ||
                        index
                      }
                      className="border-b"
                    >
                      <td className="p-3">
                        {item.name ||
                          item.username ||
                          item.team_name}
                      </td>

                      <td className="p-3">
                        {item.assigned ??
                          item.total_tasks ??
                          0}
                      </td>

                      <td className="p-3">
                        {item.completed ??
                          item.completed_tasks ??
                          0}
                      </td>

                      <td className="p-3">
                        {item.pending ??
                          item.pending_tasks ??
                          0}
                      </td>

                      <td className="p-3">
                        {item.overdue ??
                          item.overdue_tasks ??
                          0}
                      </td>
                    </tr>
                  )
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}