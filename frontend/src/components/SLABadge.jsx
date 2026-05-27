export default function SLABadge({ status }) {
  const normalized = String(status || "").toUpperCase();

  const styles = {
    ACTIVE: "bg-blue-100 text-blue-700",
    COMPLETED_WITHIN_SLA: "bg-green-100 text-green-700",
    BREACHED: "bg-red-100 text-red-700",
    ESCALATED: "bg-orange-100 text-orange-700",
  };

  return (
    <span
      className={`px-3 py-1 rounded-full text-xs font-semibold ${
        styles[normalized] || "bg-gray-100 text-gray-700"
      }`}
    >
      {String(status || "N/A").replaceAll("_", " ")}
    </span>
  );
}
