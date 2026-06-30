import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";

import { getTeamById } from "../../services/collaboration/teamService";

import {
  getTeamMembers,
  addTeamMember,
  removeTeamMember,
} from "../../services/collaboration/teamMemberService";

import { getTeamWorkload } from "../../services/collaboration/workloadService";
import { getUsers } from "../../services/collaboration/memberService";

export default function TeamDetails() {
  const { teamId } = useParams();

  const [team, setTeam] = useState(null);

  const [members, setMembers] = useState([]);

  const [workload, setWorkload] = useState(null);

  const [loading, setLoading] = useState(true);

  const [userId, setUserId] = useState("");

  const [users, setUsers] = useState([]);

  const loadData = async () => {
    try {
      setLoading(true);

      const [teamData, membersData, workloadData, usersData] =
        await Promise.all([
          getTeamById(teamId),
          getTeamMembers(teamId),
          getTeamWorkload(teamId),
          getUsers(),
        ]);

      setUsers(Array.isArray(usersData) ? usersData : usersData.items || []);

      setTeam(teamData);

      setMembers(
        Array.isArray(membersData) ? membersData : membersData.items || [],
      );

      setWorkload(workloadData);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [teamId]);

  const handleAddMember = async (e) => {
    e.preventDefault();

    try {
      await addTeamMember(teamId, {
        user_id: Number(userId),
      });

      setUserId("");

      loadData();
    } catch (error) {
      console.error(error);
    }
  };

  const handleRemoveMember = async (memberUserId) => {
    try {
      await removeTeamMember(teamId, memberUserId);

      loadData();
    } catch (error) {
      console.error(error);
    }
  };

  if (loading) {
    return <div className="p-6">Loading...</div>;
  }

  if (!team) {
    return <div className="p-6">Team not found</div>;
  }


  return (
    <div className="p-6 space-y-6">
      <div className="bg-white border rounded-lg p-4">
        <div className="flex justify-between items-center">
          <div>
            <h1 className="text-2xl font-bold">{team.name}</h1>

            <p className="mt-2 text-gray-600">{team.description}</p>
          </div>

          <Link
            to={`/teams/${teamId}/workload`}
            className="bg-green-600 text-white px-4 py-2 rounded-lg"
          >
            Workload
          </Link>
        </div>
      </div>

      <div className="bg-white border rounded-lg p-4">
        <h2 className="text-lg font-semibold mb-4">Add Member</h2>

        <form onSubmit={handleAddMember} className="flex gap-2">
          <select
            value={userId}
            onChange={(e) => setUserId(e.target.value)}
            className="border rounded px-3 py-2 w-64"
          >
            <option value="">Select User</option>

            {users.map((user) => (
              <option key={user.id} value={user.id}>
                {user.name} • {user.role.replaceAll("_", " ")}
              </option>
            ))}
          </select>

          <button
            type="submit"
            className="bg-blue-600 text-white px-4 py-2 rounded"
          >
            Add
          </button>
        </form>
      </div>

      <div className="bg-white border rounded-lg p-4">
        <h2 className="text-lg font-semibold mb-4">Team Members</h2>

        <table className="w-full">
          <thead>
            <tr>
              <th className="text-left p-2">User ID</th>

              <th className="text-left p-2">Role</th>

              <th className="text-left p-2">Actions</th>
            </tr>
          </thead>

          <tbody>
            {members.map((member) => (
              <tr key={member.id || member.user_id}>
                <td className="p-2">{member.user_id}</td>

                <td className="p-2">{member.role}</td>

                <td className="p-2">
                  <button
                    onClick={() => handleRemoveMember(member.user_id)}
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

      {workload && (
        <div className="bg-white border rounded-lg p-4">
          <h2 className="text-lg font-semibold mb-4">Team Workload</h2>

          <div className="grid grid-cols-4 gap-4">
            <div>
              <p className="text-sm text-gray-500">Total</p>

              <p className="text-xl font-bold">{workload.total_tasks}</p>
            </div>

            <div>
              <p className="text-sm text-gray-500">Completed</p>

              <p className="text-xl font-bold">{workload.completed_tasks}</p>
            </div>

            <div>
              <p className="text-sm text-gray-500">Pending</p>

              <p className="text-xl font-bold">{workload.pending_tasks}</p>
            </div>

            <div>
              <p className="text-sm text-gray-500">Overdue</p>

              <p className="text-xl font-bold">{workload.overdue_tasks}</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
