import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import {
  getTeams,
  createTeam,
  deleteTeam,
} from "../../services/collaboration/teamService";

import { getWorkspaces } from "../../services/collaboration/workspaceService";

export default function Teams() {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [workspaces, setWorkspaces] = useState([]);

  const [formData, setFormData] = useState({
    workspace_id: "",
    name: "",
    description: "",
  });

  const loadTeams = async () => {
    try {
      setLoading(true);

      const [teamsResponse, workspacesResponse] = await Promise.all([
        getTeams(),
        getWorkspaces(),
      ]);

      setTeams(
        Array.isArray(teamsResponse)
          ? teamsResponse
          : teamsResponse.items || [],
      );

      setWorkspaces(
        Array.isArray(workspacesResponse)
          ? workspacesResponse
          : workspacesResponse.items || [],
      );
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadTeams();
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
      await createTeam(formData);

      setFormData({
        workspace_id: "",
        name: "",
        description: "",
      });

      loadTeams();
    } catch (error) {
      console.error(error);
    }
  };

  const handleDelete = async (teamId) => {
    try {
      await deleteTeam(teamId);
      loadTeams();
    } catch (error) {
      console.error(error);
    }
  };

  if (loading) {
    return <div className="p-6">Loading teams...</div>;
  }

  return (
    <div className="p-6 space-y-6">
      <div>
        <h1 className="text-2xl font-semibold">Teams</h1>
      </div>

      <div className="bg-white rounded-lg border p-4">
        <form onSubmit={handleSubmit} className="grid gap-4">
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

          <input
            name="name"
            value={formData.name}
            onChange={handleChange}
            placeholder="Team Name"
            className="border rounded px-3 py-2"
          />

          <textarea
            name="description"
            value={formData.description}
            onChange={handleChange}
            placeholder="Description"
            className="border rounded px-3 py-2"
          />

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Create Team
          </button>
        </form>
      </div>

      <div className="bg-white border rounded-lg overflow-hidden">
        <table className="w-full">
          <thead>
            <tr className="border-b bg-gray-50">
              <th className="p-3 text-left">Name</th>

              <th className="p-3 text-left">Description</th>

              <th className="p-3 text-left">Actions</th>
            </tr>
          </thead>

          <tbody>
            {teams.map((team) => (
              <tr key={team.id} className="border-b">
                <td className="p-3">{team.name}</td>

                <td className="p-3">{team.description}</td>

                <td className="p-3 flex gap-2">
                  <Link to={`/teams/${team.id}`} className="text-blue-600">
                    View
                  </Link>

                  <button
                    onClick={() => handleDelete(team.id)}
                    className="text-red-600"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}

            {!teams.length && (
              <tr>
                <td colSpan={3} className="p-6 text-center">
                  No teams found
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
