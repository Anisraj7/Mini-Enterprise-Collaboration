import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  getProjects,
  createProject,
  deleteProject,
} from "../../services/collaboration/projectService";

import { getWorkspaces } from "../../services/collaboration/workspaceService";

import { getUsers } from "../../services/collaboration/memberService";

const STATUS_COLORS = {
  PLANNED: "bg-gray-100 text-gray-800",
  ACTIVE: "bg-green-100 text-green-800",
  ON_HOLD: "bg-yellow-100 text-yellow-800",
  COMPLETED: "bg-blue-100 text-blue-800",
  CANCELLED: "bg-red-100 text-red-800",
};

const PRIORITY_COLORS = {
  LOW: "bg-gray-100 text-gray-800",
  MEDIUM: "bg-blue-100 text-blue-800",
  HIGH: "bg-orange-100 text-orange-800",
  CRITICAL: "bg-red-100 text-red-800",
};

export default function Projects() {
  const [projects, setProjects] = useState([]);

  const [loading, setLoading] = useState(true);

  const [workspaces, setWorkspaces] = useState([]);
  const [users, setUsers] = useState([]);

  const [formData, setFormData] = useState({
    workspace_id: "",
    owner_id: "",
    name: "",
    description: "",
    priority: "MEDIUM",
    start_date: "",
    end_date: "",
  });

  const loadProjects = async () => {
    try {
      setLoading(true);

      const [projectResponse, workspaceResponse, userResponse] =
        await Promise.all([getProjects(), getWorkspaces(), getUsers()]);

      setProjects(
        Array.isArray(projectResponse)
          ? projectResponse
          : projectResponse.items || [],
      );

      setWorkspaces(
        Array.isArray(workspaceResponse)
          ? workspaceResponse
          : workspaceResponse.items || [],
      );

      setUsers(
        Array.isArray(userResponse) ? userResponse : userResponse.items || [],
      );
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadProjects();
  }, []);

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      await createProject(formData);

      setFormData({
        workspace_id: "",
        owner_id: "",
        name: "",
        description: "",
        priority: "MEDIUM",
        start_date: "",
        end_date: "",
      });

      loadProjects();
    } catch (error) {
      console.error(error);
    }
  };

  const handleDelete = async (projectId) => {
    try {
      await deleteProject(projectId);

      loadProjects();
    } catch (error) {
      console.error(error);
    }
  };

  if (loading) {
    return <div className="p-6">Loading projects...</div>;
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-bold">Projects</h1>
      </div>

      <div className="bg-white border rounded-lg p-4">
        <form onSubmit={handleSubmit} className="grid grid-cols-2 gap-4">
          <select
            name="workspace_id"
            value={formData.workspace_id}
            onChange={handleChange}
            className="border rounded px-3 py-2"
            required
          >
            <option value="">Select Workspace</option>

            {workspaces.map((workspace) => (
              <option key={workspace.id} value={workspace.id}>
                {workspace.name}
              </option>
            ))}
          </select>

          <select
            name="owner_id"
            value={formData.owner_id}
            onChange={handleChange}
            className="border rounded px-3 py-2"
            required
          >
            <option value="">Select Owner</option>

            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name} ({user.email})
              </option>
            ))}
          </select>

          <input
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Project Name"
            className="border rounded px-3 py-2 col-span-2"
          />

          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Description"
            className="border rounded px-3 py-2 col-span-2"
          />

          <select
            name="priority"
            value={formData.priority}
            onChange={handleChange}
            className="border rounded px-3 py-2"
          >
            <option value="LOW">LOW</option>
            <option value="MEDIUM">MEDIUM</option>
            <option value="HIGH">HIGH</option>
            <option value="CRITICAL">CRITICAL</option>
          </select>

          <input
            type="date"
            name="start_date"
            value={formData.start_date}
            onChange={handleChange}
            className="border rounded px-3 py-2"
          />

          <input
            type="date"
            name="end_date"
            value={formData.end_date}
            onChange={handleChange}
            className="border rounded px-3 py-2"
          />

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Create Project
          </button>
        </form>
      </div>

      <div className="grid gap-4">
        {projects.map((project) => (
          <div key={project.id} className="bg-white border rounded-lg p-4">
            <div className="flex justify-between">
              <div>
                <h2 className="font-semibold text-lg">{project.name}</h2>

                <p className="text-gray-600">{project.description}</p>
              </div>

              <div className="flex gap-2">
                <span
                  className={`px-2 py-1 rounded text-xs ${
                    STATUS_COLORS[project.status]
                  }`}
                >
                  {project.status}
                </span>

                <span
                  className={`px-2 py-1 rounded text-xs ${
                    PRIORITY_COLORS[project.priority]
                  }`}
                >
                  {project.priority}
                </span>
              </div>
            </div>

            <div className="mt-4 flex gap-4">
              <Link to={`/projects/${project.id}`} className="text-blue-600">
                View
              </Link>

              <button
                onClick={() => handleDelete(project.id)}
                className="text-red-600"
              >
                Delete
              </button>
            </div>
          </div>
        ))}

        {!projects.length && (
          <div className="bg-white border rounded-lg p-6 text-center">
            No projects found
          </div>
        )}
      </div>
    </div>
  );
}
