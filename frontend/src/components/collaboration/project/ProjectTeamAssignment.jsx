import { useState } from "react";

export default function ProjectTeamAssignment({
  teams,
  onAssign,
  onRemove,
}) {
  const [teamId, setTeamId] =
    useState("");

  return (
    <div className="space-y-4">
      <form
        onSubmit={(e) => {
          e.preventDefault();
          onAssign(teamId);
          setTeamId("");
        }}
        className="flex gap-2"
      >
        <input
          value={teamId}
          onChange={(e) =>
            setTeamId(
              e.target.value
            )
          }
          placeholder="Team ID"
          className="border rounded px-3 py-2"
        />

        <button className="bg-green-600 text-white px-4 py-2 rounded">
          Assign
        </button>
      </form>

      <table className="w-full">
        <tbody>
          {teams.map((team) => (
            <tr
              key={
                team.team_id ||
                team.id
              }
            >
              <td className="p-2">
                {team.name ||
                  team.team_name}
              </td>

              <td className="p-2">
                <button
                  onClick={() =>
                    onRemove(
                      team.team_id ||
                        team.id
                    )
                  }
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
  );
}