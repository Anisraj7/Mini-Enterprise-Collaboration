import { useCallback, useEffect, useState } from "react";

import { Link, useParams } from "react-router-dom";

import {
  Users,
  MessageSquare,
  Lock,
  Globe,
} from "lucide-react";

import { getChannels } from "../../services/collaboration/channelService";

import { getMembers } from "../../services/collaboration/memberService";

import { getWorkspaceById } from "../../services/collaboration/workspaceService";

export default function WorkspaceDetails() {
  const { workspaceId } = useParams();

  const [workspace, setWorkspace] =
    useState(null);

  const [channels, setChannels] =
    useState([]);

  const [members, setMembers] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const loadData =
    useCallback(async () => {
      try {
        setLoading(true);

        const [
          workspaceData,
          channelData,
          memberData,
        ] = await Promise.all([
          getWorkspaceById(
            workspaceId
          ),
          getChannels(
            workspaceId
          ),
          getMembers(
            workspaceId
          ),
        ]);

        setWorkspace(
          workspaceData
        );

        setChannels(
          channelData || []
        );

        setMembers(
          memberData || []
        );
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
    return (
      <div>
        Loading workspace...
      </div>
    );
  }

  if (!workspace) {
    return (
      <div>
        Workspace not found
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">
          {workspace.name}
        </h1>

        <p className="text-gray-500 mt-1">
          {workspace.description ||
            "No description"}
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
              workspace.visibility ===
              "PUBLIC"
                ? "bg-green-100 text-green-700"
                : "bg-orange-100 text-orange-700"
            }
          `}
        >
          {workspace.visibility ===
          "PUBLIC" ? (
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

            <h2 className="font-semibold">
              Members
            </h2>
          </div>

          <p className="text-3xl font-bold">
            {members.length}
          </p>
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
            <MessageSquare
              size={18}
            />

            <h2 className="font-semibold">
              Channels
            </h2>
          </div>

          <p className="text-3xl font-bold">
            {channels.length}
          </p>
        </Link>
      </div>

      <div className="bg-white rounded-xl border p-5">
        <h2 className="font-semibold mb-4">
          Recent Channels
        </h2>

        {channels.length === 0 ? (
          <p className="text-gray-500">
            No channels found
          </p>
        ) : (
          <div className="space-y-2">
            {channels.map(
              (channel) => (
                <Link
                  key={
                    channel.id
                  }
                  to={`/channels/${channel.id}`}
                  className="
                    block
                    border
                    rounded-lg
                    p-3
                    hover:bg-gray-50
                  "
                >
                  <div className="font-medium">
                    {channel.name}
                  </div>

                  <div className="text-sm text-gray-500">
                    {
                      channel.channel_type
                    }
                  </div>
                </Link>
              )
            )}
          </div>
        )}
      </div>
    </div>
  );
}