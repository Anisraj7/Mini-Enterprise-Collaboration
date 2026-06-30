export default function TeamCard({
  team,
  onDelete,
}) {
  return (
    <div className="bg-white border rounded-lg p-4">
      <div>
        <h3 className="text-lg font-semibold">
          {team.name}
        </h3>

        <p className="text-gray-600 mt-2">
          {team.description}
        </p>
      </div>

      <div className="mt-4 flex gap-3">
        <a
          href={`/teams/${team.id}`}
          className="text-blue-600"
        >
          View
        </a>

        <button
          onClick={() =>
            onDelete(team.id)
          }
          className="text-red-600"
        >
          Delete
        </button>
      </div>
    </div>
  );
}