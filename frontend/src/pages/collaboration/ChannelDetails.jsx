import { useCallback, useEffect, useState } from "react";

import { useParams } from "react-router-dom";

import { Users, Lock, Globe } from "lucide-react";

import { getChannel } from "../../services/collaboration/channelService";

import { getChannelMembers } from "../../services/collaboration/channelMemberService";

import ChannelMessageList from "../../components/collaboration/channel/ChannelMessageList";

export default function ChannelDetails() {
  const { channelId } = useParams();

  const [channel, setChannel] = useState(null);

  const [members, setMembers] = useState([]);

  const [loading, setLoading] = useState(true);

  const [activeTab, setActiveTab] = useState("messages");

  const loadChannel = useCallback(async () => {
    try {
      setLoading(true);

      const [channelData, memberData] = await Promise.all([
        getChannel(channelId),
        getChannelMembers(channelId),
      ]);

      setChannel(channelData);

      setMembers(Array.isArray(memberData) ? memberData : []);
    } catch (error) {
      console.error(error);

      setChannel(null);

      setMembers([]);
    } finally {
      setLoading(false);
    }
  }, [channelId]);

  useEffect(() => {
    loadChannel();
  }, [loadChannel]);

  if (loading) {
    return <div>Loading channel...</div>;
  }

  if (!channel) {
    return <div>Channel not found</div>;
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">#{channel.name}</h1>

        <p className="text-gray-500 mt-1">
          {channel.description || "No description"}
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
            channel.channel_type === "PUBLIC"
              ? "bg-green-100 text-green-700"
              : "bg-orange-100 text-orange-700"
          }
        `}
        >
          {channel.channel_type === "PUBLIC" ? (
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

        {channel.is_archived && (
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
          <button
            onClick={() => setActiveTab("messages")}
            className={`pb-3 ${
              activeTab === "messages"
                ? "border-b-2 border-blue-600 text-blue-600 font-medium"
                : "text-gray-500"
            }`}
          >
            Messages
          </button>

          <button
            onClick={() => setActiveTab("tasks")}
            className={`pb-3 ${
              activeTab === "tasks"
                ? "border-b-2 border-blue-600 text-blue-600 font-medium"
                : "text-gray-500"
            }`}
          >
            Tasks
          </button>

          <button
            onClick={() => setActiveTab("documents")}
            className={`pb-3 ${
              activeTab === "documents"
                ? "border-b-2 border-blue-600 text-blue-600 font-medium"
                : "text-gray-500"
            }`}
          >
            Documents
          </button>

          <button
            onClick={() => setActiveTab("members")}
            className={`pb-3 ${
              activeTab === "members"
                ? "border-b-2 border-blue-600 text-blue-600 font-medium"
                : "text-gray-500"
            }`}
          >
            Members
          </button>
        </div>
      </div>

      {/* Messages */}
      {activeTab === "messages" && <ChannelMessageList channelId={channelId} />}

      {/* Tasks */}
      {activeTab === "tasks" && (
        <div className="bg-white rounded-xl border p-5">
          Channel Tasks Coming Soon
        </div>
      )}

      {/* Documents */}
      {activeTab === "documents" && (
        <div className="bg-white rounded-xl border p-5">
          Channel Documents Coming Soon
        </div>
      )}

      {/* Members */}
      {activeTab === "members" && (
        <>
          <div className="grid md:grid-cols-2 gap-5">
            <div
              className="
              bg-white
              border
              rounded-xl
              p-5
            "
            >
              <div className="flex items-center gap-2 mb-2">
                <Users size={18} />

                <span className="font-semibold">Members</span>
              </div>

              <div className="text-3xl font-bold">{members.length}</div>
            </div>
          </div>

          <div className="bg-white rounded-xl border p-5">
            <h2 className="font-semibold mb-4">Channel Members</h2>

            {members.length === 0 ? (
              <p className="text-gray-500">No members found</p>
            ) : (
              <div className="space-y-2">
                {members.map((member) => (
                  <div
                    key={member.id}
                    className="
                      border
                      rounded-lg
                      p-3
                    "
                  >
                    User ID: {member.user_id}
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
