export default function DateRangeFilter({ startDate, endDate, onStartDateChange, onEndDateChange }) {
  return (
    <div className="flex flex-wrap gap-3">
      <input
        type="date"
        value={startDate}
        onChange={(event) => onStartDateChange(event.target.value)}
        className="rounded-lg border border-gray-200 px-3 py-2 text-sm"
      />
      <input
        type="date"
        value={endDate}
        onChange={(event) => onEndDateChange(event.target.value)}
        className="rounded-lg border border-gray-200 px-3 py-2 text-sm"
      />
    </div>
  );
}
