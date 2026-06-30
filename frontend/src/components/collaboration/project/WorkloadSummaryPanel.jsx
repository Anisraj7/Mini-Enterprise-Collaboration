export default function WorkloadSummaryPanel({
  workload,
}) {
  if (!workload) return null;

  return (
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
  );
}