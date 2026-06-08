import { useEffect, useMemo, useState } from "react";

import API from "../api/axios";

import DataTable from "../components/DataTable";
import DateRangeFilter from "../components/DateRangeFilter";
import ErrorMessage from "../components/ErrorMessage";
import FilterBar from "../components/FilterBar";
import LoadingSpinner from "../components/LoadingSpinner";
import PageHeader from "../components/PageHeader";
import SLABadge from "../components/SLABadge";

const formatDateTime = (value) =>
  value
    ? new Date(value).toLocaleString()
    : "N/A";

export default function SLADashboard() {
  const [active, setActive] =
    useState([]);

  const [breached, setBreached] =
    useState([]);

  const [completed, setCompleted] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [error, setError] =
    useState("");

  const [moduleFilter, setModuleFilter] =
    useState("");

  const [statusFilter, setStatusFilter] =
    useState("");

  const [startDate, setStartDate] =
    useState("");

  const [endDate, setEndDate] =
    useState("");

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [
          activeResponse,
          breachedResponse,
          completedResponse,
        ] = await Promise.all([
          API.get("/sla-tracking/active"),
          API.get("/sla-tracking/breached"),
          API.get("/sla-tracking/completed"),
        ]);

        const extractItems = (
          responseData
        ) => {
          if (
            Array.isArray(
              responseData?.items
            )
          ) {
            return responseData.items;
          }

          if (
            Array.isArray(
              responseData
            )
          ) {
            return responseData;
          }

          return [];
        };

        setActive(
          extractItems(
            activeResponse.data
          )
        );

        setBreached(
          extractItems(
            breachedResponse.data
          )
        );

        setCompleted(
          extractItems(
            completedResponse.data
          )
        );

        setError("");
      } catch (err) {
        setError(
          err.response?.data
            ?.detail ||
            "Unable to load SLA dashboard."
        );
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const allRecords =
    useMemo(
      () => [
        ...(Array.isArray(active)
          ? active
          : []),

        ...(Array.isArray(
          breached
        )
          ? breached
          : []),

        ...(Array.isArray(
          completed
        )
          ? completed
          : []),
      ],
      [
        active,
        breached,
        completed,
      ]
    );

  const filteredRecords =
    allRecords.filter(
      (record) => {
        const created =
          record.start_time
            ? new Date(
                record.start_time
              )
            : null;

        const afterStart =
          !startDate ||
          (created &&
            created >=
              new Date(
                `${startDate}T00:00:00`
              ));

        const beforeEnd =
          !endDate ||
          (created &&
            created <=
              new Date(
                `${endDate}T23:59:59`
              ));

        return (
          (!moduleFilter ||
            record.module_name ===
              moduleFilter) &&
          (!statusFilter ||
            record.status ===
              statusFilter) &&
          afterStart &&
          beforeEnd
        );
      }
    );

  const moduleCounts =
    allRecords.reduce(
      (acc, record) => {
        acc[
          record.module_name
        ] =
          (acc[
            record
              .module_name
          ] || 0) + 1;

        return acc;
      },
      {}
    );

  const columns = [
    {
      key: "module_name",
      header: "Module",
    },

    {
      key: "record_id",
      header: "Record ID",
      render: (row) =>
        `#${row.record_id}`,
    },

    {
      key: "status",
      header: "SLA Status",
      render: (row) => (
        <SLABadge
          status={row.status}
        />
      ),
    },

    {
      key: "start_time",
      header: "Start Time",
      render: (row) =>
        formatDateTime(
          row.start_time
        ),
    },

    {
      key: "due_time",
      header: "Due Time",
      render: (row) =>
        formatDateTime(
          row.due_time
        ),
    },

    {
      key: "completed_time",
      header:
        "Completed Time",
      render: (row) =>
        formatDateTime(
          row.completed_time
        ),
    },

    {
      key: "breach_reason",
      header:
        "Breach Reason",
      render: (row) =>
        row.breach_reason ||
        "N/A",
    },
  ];

  return (
    <div className="min-h-screen bg-gray-100">
      <main className="mx-auto max-w-7xl p-6">
        <PageHeader
          title="SLA Dashboard"
          subtitle="Monitor active, breached and completed SLA records"
        />

        <ErrorMessage
          message={error}
        />

        <div className="mb-6 grid grid-cols-1 gap-4 md:grid-cols-4">
          <div className="rounded-lg bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">
              Active SLA
            </p>

            <p className="mt-2 text-3xl font-bold text-blue-600">
              {active.length}
            </p>
          </div>

          <div className="rounded-lg bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">
              Breached SLA
            </p>

            <p className="mt-2 text-3xl font-bold text-red-600">
              {breached.length}
            </p>
          </div>

          <div className="rounded-lg bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">
              Completed SLA
            </p>

            <p className="mt-2 text-3xl font-bold text-green-600">
              {completed.length}
            </p>
          </div>

          <div className="rounded-lg bg-white p-5 shadow-sm">
            <p className="text-sm text-gray-500">
              Module Records
            </p>

            <p className="mt-2 text-sm font-semibold text-gray-700">
              {Object.entries(
                moduleCounts
              )
                .map(
                  (
                    [
                      module,
                      count,
                    ]
                  ) =>
                    `${module}: ${count}`
                )
                .join(" | ") ||
                "N/A"}
            </p>
          </div>
        </div>

        <FilterBar>
          <select
            value={moduleFilter}
            onChange={(
              e
            ) =>
              setModuleFilter(
                e.target.value
              )
            }
            className="rounded-lg border border-gray-200 px-3 py-2 text-sm"
          >
            <option value="">
              All Modules
            </option>

            <option value="Task">
              Task
            </option>

            <option value="Approval">
              Approval
            </option>
          </select>

          <select
            value={statusFilter}
            onChange={(
              e
            ) =>
              setStatusFilter(
                e.target.value
              )
            }
            className="rounded-lg border border-gray-200 px-3 py-2 text-sm"
          >
            <option value="">
              All Statuses
            </option>

            <option value="ACTIVE">
              Active
            </option>

            <option value="BREACHED">
              Breached
            </option>

            <option value="COMPLETED_WITHIN_SLA">
              Completed
            </option>

            <option value="ESCALATED">
              Escalated
            </option>
          </select>

          <DateRangeFilter
            startDate={startDate}
            endDate={endDate}
            onStartDateChange={
              setStartDate
            }
            onEndDateChange={
              setEndDate
            }
          />
        </FilterBar>

        {loading ? (
          <LoadingSpinner />
        ) : (
          <DataTable
            columns={columns}
            rows={filteredRecords}
            emptyMessage="No SLA records found"
          />
        )}
      </main>
    </div>
  );
}