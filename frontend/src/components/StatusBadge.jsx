export default function StatusBadge({ status }) {
  const normalized = String(status || "").toUpperCase();

  const styles = {
    ACTIVE: "bg-green-100 text-green-700",
    DISABLED: "bg-red-100 text-red-700",
    PENDING: "bg-yellow-100 text-yellow-700",
    RESOLVED: "bg-blue-100 text-blue-700",
    CANCELLED: "bg-gray-100 text-gray-700",
    APPROVED: "bg-green-100 text-green-700",
    REJECTED: "bg-red-100 text-red-700",
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
