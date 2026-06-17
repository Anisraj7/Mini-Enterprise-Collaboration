import { useCallback, useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import { Users, MessageSquare, Lock, Globe } from "lucide-react";

import { getChannels } from "../../services/collaboration/channelService";
import { getMembers } from "../../services/collaboration/memberService";
import { getWorkspaceById } from "../../services/collaboration/workspaceService";

import WorkspaceMessageList from "../../components/collaboration/workspace/WorkspaceMessageList";
import WorkspaceTaskList from "../../components/collaboration/workspace/WorkspaceTaskList";

export default function WorkspaceDetails() {
  const { workspaceId } = useParams();

  const [workspace, setWorkspace] = useState(null);
  const [channels, setChannels] = useState([]);
  const [members, setMembers] = useState([]);
  const [loading, setLoading] = useState(true);

  const [activeTab, setActiveTab] = useState("overview");

  const loadData = useCallback(async () => {
    try {
      setLoading(true);

      const [workspaceData, channelData, memberData] = await Promise.all([
        getWorkspaceById(workspaceId),
        getChannels(workspaceId),
        getMembers(workspaceId),
      ]);

      setWorkspace(workspaceData);
      setChannels(channelData || []);
      setMembers(memberData || []);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }, [workspaceId]);

  useEffect(() => {
    loadData();
  }, [loadData]);

  if (loading) {
    return <div>Loading workspace...</div>;
  }

  if (!workspace) {
    return <div>Workspace not found</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">{workspace.name}</h1>

        <p className="text-gray-500 mt-1">
          {workspace.description || "No description"}
        </p>
      </div>

      <div className="flex gap-2">
        <span
          className={`
            flex
            items-center
            gap-1
            px-3
            py-1
            rounded-full
            text-sm
            ${
              workspace.visibility === "PUBLIC"
                ? "bg-green-100 text-green-700"
                : "bg-orange-100 text-orange-700"
            }
          `}
        >
          {workspace.visibility === "PUBLIC" ? (
            <>
              <Globe size={14} />
              Public
            </>
          ) : (
            <>
              <Lock size={14} />
              Private
            </>
          )}
        </span>

        {workspace.is_archived && (
          <span
            className="
              px-3
              py-1
              rounded-full
              text-sm
              bg-red-100
              text-red-700
            "
          >
            Archived
          </span>
        )}
      </div>

      {/* Tabs */}
      <div className="border-b">
        <div className="flex gap-6 overflow-x-auto">
          {[
            "overview",
            "messages",
            "tasks",
            "documents",
            "members",
            "channels",
          ].map((tab) => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`capitalize pb-3 ${
                activeTab === tab
                  ? "border-b-2 border-blue-600 text-blue-600 font-medium"
                  : "text-gray-500"
              }`}
            >
              {tab}
            </button>
          ))}
        </div>
      </div>

      {/* Overview */}
      {activeTab === "overview" && (
        <>
          <div className="grid md:grid-cols-2 gap-5">
            <Link
              to={`/workspaces/${workspaceId}/members`}
              className="
                bg-white
                rounded-xl
                border
                p-5
                hover:shadow-md
                transition
              "
            >
              <div className="flex items-center gap-2 mb-3">
                <Users size={18} />
                <h2 className="font-semibold">Members</h2>
              </div>

              <p className="text-3xl font-bold">{members.length}</p>
            </Link>

            <Link
              to={`/workspaces/${workspaceId}/channels`}
              className="
                bg-white
                rounded-xl
                border
                p-5
                hover:shadow-md
                transition
              "
            >
              <div className="flex items-center gap-2 mb-3">
                <MessageSquare size={18} />

                <h2 className="font-semibold">Channels</h2>
              </div>

              <p className="text-3xl font-bold">{channels.length}</p>
            </Link>
          </div>

          <div className="bg-white rounded-xl border p-5">
            <h2 className="font-semibold mb-4">Recent Channels</h2>

            {channels.length === 0 ? (
              <p className="text-gray-500">No channels found</p>
            ) : (
              <div className="space-y-2">
                {channels.map((channel) => (
                  <Link
                    key={channel.id}
                    to={`/channels/${channel.id}`}
                    className="
                        block
                        border
                        rounded-lg
                        p-3
                        hover:bg-gray-50
                      "
                  >
                    <div className="font-medium">{channel.name}</div>

                    <div className="text-sm text-gray-500">
                      {channel.channel_type}
                    </div>
                  </Link>
                ))}
              </div>
            )}
          </div>
        </>
      )}

      {/* Messages */}
      {activeTab === "messages" && (
        <div className="bg-white rounded-xl border overflow-hidden">
          <div className="px-5 py-4 border-b bg-gray-50">
            <h3 className="font-semibold">Workspace Discussion</h3>

            <p className="text-sm text-gray-500 mt-1">
              Share updates, ask questions, and coordinate work.
            </p>
          </div>

          <WorkspaceMessageList workspaceId={workspaceId} />
        </div>
      )}

      {/* Tasks */}
      {activeTab === "tasks" && <WorkspaceTaskList workspaceId={workspaceId} />}

      {/* Documents */}
      {activeTab === "documents" && (
        <div className="space-y-6">
          <div className="bg-white rounded-xl border p-5">
            <h3 className="font-semibold mb-4">Task Documents</h3>

            <p className="text-gray-500 text-sm">
              Documents attached to workspace tasks.
            </p>

            <button
              onClick={() => setActiveTab("tasks")}
              className="mt-3 px-4 py-2 rounded-lg bg-indigo-600 text-white"
            >
              View Tasks
            </button>
          </div>

          <div className="bg-white rounded-xl border p-5">
            <h3 className="font-semibold mb-4">Approval Documents</h3>

            <p className="text-gray-500 text-sm">
              Documents attached to approval requests.
            </p>

            <Link
              to="/approvals"
              className="inline-block mt-3 px-4 py-2 rounded-lg bg-indigo-600 text-white"
            >
              View Approvals
            </Link>
          </div>
        </div>
      )}

      {/* Members */}
      {activeTab === "members" && (
        <div className="bg-white rounded-xl border p-5">
          <div className="flex justify-between items-center mb-5">
            <div>
              <h3 className="text-lg font-semibold">Workspace Members</h3>

              <p className="text-sm text-gray-500">
                Manage workspace participants and roles
              </p>
            </div>

            <span className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm">
              {members.length} Members
            </span>
          </div>

          {members.length === 0 ? (
            <div className="text-center py-8 text-gray-500">
              No workspace members found.
            </div>
          ) : (
            <div className="space-y-3">
              {members.map((member) => (
                <div
                  key={member.id}
                  className="flex items-center justify-between border rounded-xl p-4 hover:bg-gray-50 transition"
                >
                  <div>
                    <div className="font-medium">
                      {member.user_name || `User #${member.user_id}`}
                    </div>

                    <div className="text-sm text-gray-500 mt-1">
                      {member.role || "MEMBER"}
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <span
                      className={`px-3 py-1 rounded-full text-xs font-medium ${
                        member.is_active
                          ? "bg-green-100 text-green-700"
                          : "bg-red-100 text-red-700"
                      }`}
                    >
                      {member.is_active ? "Active" : "Inactive"}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Channels */}
      {activeTab === "channels" && (
        <div className="bg-white rounded-xl border p-5">
          <div className="flex justify-between items-center mb-4">
            <h3 className="text-lg font-semibold">Workspace Channels</h3>

            <span className="text-sm text-gray-500">
              {channels.length} Channels
            </span>
          </div>

          {channels.length === 0 ? (
            <p className="text-gray-500">No channels found</p>
          ) : (
            <div className="space-y-2">
              {channels.map((channel) => (
                <Link
                  key={channel.id}
                  to={`/channels/${channel.id}`}
                  className="block border rounded-lg p-3 hover:bg-gray-50"
                >
                  <div className="font-medium">{channel.name}</div>

                  <div className="text-sm text-gray-500">
                    {channel.channel_type}
                  </div>
                </Link>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
