import { Link } from "react-router-dom";

export default function ProjectCard({
  project,
  onDelete,
}) {
  return (
    <div className="bg-white border rounded-lg p-4">
      <h3 className="font-semibold text-lg">
        {project.name}
      </h3>

      <p className="text-gray-600 mt-2">
        {project.description}
      </p>

      <div className="flex gap-2 mt-3">
        <span className="px-2 py-1 rounded bg-blue-100 text-blue-800 text-xs">
          {project.status}
        </span>

        <span className="px-2 py-1 rounded bg-orange-100 text-orange-800 text-xs">
          {project.priority}
        </span>
      </div>

      <div className="mt-4 flex gap-3">
        <Link
          to={`/projects/${project.id}`}
          className="text-blue-600"
        >
          View
        </Link>

        <button
          onClick={() =>
            onDelete(project.id)
          }
          className="text-red-600"
        >
          Delete
        </button>
      </div>
    </div>
  );
}