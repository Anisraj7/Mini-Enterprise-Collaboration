import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { getProjectById } from "../../services/collaboration/projectService";

import { getTeams } from "../../services/collaboration/teamService";

import {
  getProjectTeams,
  assignProjectTeam,
  removeProjectTeam,
} from "../../services/collaboration/projectTeamService";

import {
  getProjectDocuments,
  uploadProjectDocument,
  deleteProjectDocument,
  downloadProjectDocument,
} from "../../services/collaboration/projectDocumentService";

import { getProjectWorkload } from "../../services/collaboration/workloadService";

export default function ProjectDetails() {
  const { projectId } = useParams();

  const [project, setProject] = useState(null);

  const [teams, setTeams] = useState([]);

  const [documents, setDocuments] = useState([]);

  const [workload, setWorkload] = useState(null);

  const [teamId, setTeamId] = useState("");

  const [file, setFile] = useState(null);

  const [loading, setLoading] = useState(true);
  const [availableTeams, setAvailableTeams] = useState([]);
  const [error, setError] = useState("");

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      setError("");

      const projectData = await getProjectById(projectId);
      setProject(projectData);

      const [teamsResult, documentsResult, workloadResult, availableTeamsResult] =
        await Promise.allSettled([
          getProjectTeams(projectId),
          getProjectDocuments(projectId),
          getProjectWorkload(projectId),
          getTeams(),
        ]);

      if (teamsResult.status === "fulfilled") {
        setTeams(
          Array.isArray(teamsResult.value)
            ? teamsResult.value
            : teamsResult.value.items || [],
        );
      } else {
        console.error(teamsResult.reason);
        setTeams([]);
      }

      if (documentsResult.status === "fulfilled") {
        setDocuments(
          Array.isArray(documentsResult.value)
            ? documentsResult.value
            : documentsResult.value.items || [],
        );
      } else {
        console.error(documentsResult.reason);
        setDocuments([]);
      }

      if (workloadResult.status === "fulfilled") {
        setWorkload(workloadResult.value);
      } else {
        console.error(workloadResult.reason);
        setWorkload(null);
      }

      if (availableTeamsResult.status === "fulfilled") {
        setAvailableTeams(
          Array.isArray(availableTeamsResult.value)
            ? availableTeamsResult.value
            : availableTeamsResult.value.items || [],
        );
      } else {
        console.error(availableTeamsResult.reason);
        setAvailableTeams([]);
      }
    } catch (error) {
      console.error(error);
      setProject(null);
      setError(
        error.response?.data?.detail || "Unable to load project",
      );
    } finally {
      setLoading(false);
    }
  }, [projectId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleAssignTeam = async (e) => {
    e.preventDefault();

    try {
      await assignProjectTeam(projectId, {
        team_id: Number(teamId),
      });

      setTeamId("");

      loadData();
    } catch (error) {
      console.error(error);
    }
  };

  const handleRemoveTeam = async (teamIdValue) => {
    try {
      await removeProjectTeam(projectId, teamIdValue);

      loadData();
    } catch (error) {
      console.error(error);
    }
  };

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) return;

    try {
      const formData = new FormData();

      formData.append("file", file);
      formData.append("document_type", "OTHER");

      await uploadProjectDocument(projectId, formData);

      setFile(null);

      loadData();
    } catch (error) {
      console.error(error);
    }
  };

  const handleDeleteDocument = async (documentId) => {
    try {
      await deleteProjectDocument(documentId);

      loadData();
    } catch (error) {
      console.error(error);
    }
  };

  const handleDownloadDocument = async (document) => {
    try {
      const response = await downloadProjectDocument(document.id);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = window.document.createElement("a");

      link.href = url;
      link.download = document.file_name;
      link.click();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error(error);
    }
  };

  if (loading) {
    return <div className="p-6">Loading project...</div>;
  }

  if (!project) {
    return <div className="p-6">{error || "Project not found"}</div>;
  }

  return (
    <div className="p-6 space-y-6">
      <div className="bg-white border rounded-lg p-4">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">{project.name}</h1>

            <p className="text-gray-600 mt-2">{project.description}</p>
          </div>

          <Link
            to={`/projects/${projectId}/calendar`}
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Calendar
          </Link>

          <Link
            to={`/projects/${projectId}/workload`}
            className="bg-green-600 text-white px-4 py-2 rounded-lg"
          >
            Workload
          </Link>
        </div>
      </div>

      <div className="bg-white border rounded-lg p-4">
        <h2 className="font-semibold text-lg mb-4">Assign Team</h2>

        <form onSubmit={handleAssignTeam} className="flex gap-2">
          <select
            value={teamId}
            onChange={(e) => setTeamId(e.target.value)}
            className="border rounded px-3 py-2 w-64"
          >
            <option value="">Select Team</option>

            {availableTeams.map((team) => (
              <option key={team.id} value={team.id}>
                {team.name}
              </option>
            ))}
          </select>

          <button
            type="submit"
            className="bg-green-600 text-white px-4 py-2 rounded"
          >
            Assign
          </button>
        </form>
      </div>

      <div className="bg-white border rounded-lg p-4">
        <h2 className="font-semibold text-lg mb-4">Assigned Teams</h2>

        <table className="w-full">
          <thead>
            <tr>
              <th className="text-left p-2">Team ID</th>

              <th className="text-left p-2">Team Name</th>

              <th className="text-left p-2">Action</th>
            </tr>
          </thead>

          <tbody>
            {teams.map((team) => (
              <tr key={team.id || team.team_id}>
                <td className="p-2">{team.team_id ?? team.id}</td>

                <td className="p-2">{team.team_name ?? team.name}</td>

                <td className="p-2">
                  <button
                    onClick={() => handleRemoveTeam(team.team_id ?? team.id)}
                    className="text-red-600"
                  >
                    Remove
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="bg-white border rounded-lg p-4">
        <h2 className="font-semibold text-lg mb-4">Upload Document</h2>

        <form onSubmit={handleUpload} className="flex gap-2">
          <input type="file" onChange={(e) => setFile(e.target.files?.[0])} />

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Upload
          </button>
        </form>
      </div>

      <div className="bg-white border rounded-lg p-4">
        <h2 className="font-semibold text-lg mb-4">Documents</h2>

        <table className="w-full">
          <thead>
            <tr>
              <th className="text-left p-2">Name</th>

              <th className="text-left p-2">Actions</th>
            </tr>
          </thead>

          <tbody>
            {documents.map((document) => (
              <tr key={document.id}>
                <td className="p-2">{document.file_name}</td>

                <td className="p-2 flex gap-4">
                  <button
                    type="button"
                    onClick={() => handleDownloadDocument(document)}
                    className="text-blue-600"
                  >
                    Download
                  </button>

                  <button
                    onClick={() => handleDeleteDocument(document.id)}
                    className="text-red-600"
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {workload && (
        <div className="bg-white border rounded-lg p-4">
          <h2 className="font-semibold text-lg mb-4">Project Workload</h2>

          <div className="grid grid-cols-4 gap-4">
            <div>
              <p className="text-gray-500 text-sm">Total</p>
              <p className="text-xl font-bold">{workload.total_tasks}</p>
            </div>

            <div>
              <p className="text-gray-500 text-sm">Completed</p>
              <p className="text-xl font-bold">{workload.completed_tasks}</p>
            </div>

            <div>
              <p className="text-gray-500 text-sm">Pending</p>
              <p className="text-xl font-bold">{workload.pending_tasks}</p>
            </div>

            <div>
              <p className="text-gray-500 text-sm">Overdue</p>
              <p className="text-xl font-bold">{workload.overdue_tasks}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
