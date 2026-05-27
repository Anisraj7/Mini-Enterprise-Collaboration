export default function FilterBar({
  children,
}) {
  return (
    <div className="bg-white p-4 rounded-xl shadow mb-4 flex flex-wrap gap-4">
      {children}
    </div>
  );
}