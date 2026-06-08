import {
  useCallback,
  useEffect,
  useState,
} from "react";

import {
  useParams,
} from "react-router-dom";

import ChannelCard from "../../components/collaboration/channel/ChannelCard";

import ChannelFormModal from "../../components/collaboration/channel/ChannelFormModal";

import {
  getChannels,
  createChannel,
} from "../../services/collaboration/channelService";

export default function Channels() {
  const { workspaceId } =
    useParams();

  const [channels, setChannels] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [showModal, setShowModal] =
    useState(false);

  const loadChannels =
    useCallback(async () => {
      try {
        setLoading(true);

        const data =
          await getChannels(
            workspaceId
          );

        setChannels(
          data || []
        );
      } catch (error) {
        console.error(error);

        setChannels([]);
      } finally {
        setLoading(false);
      }
    }, [workspaceId]);

  useEffect(() => {
    loadChannels();
  }, [loadChannels]);

  const handleCreate =
    async (payload) => {
      try {
        await createChannel({
          workspace_id:
            Number(
              workspaceId
            ),
          ...payload,
        });

        setShowModal(false);

        await loadChannels();
      } catch (error) {
        console.error(error);
      }
    };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold">
            Workspace Channels
          </h1>

          <p className="text-gray-500">
            Workspace #{workspaceId}
          </p>
        </div>

        <button
          onClick={() =>
            setShowModal(true)
          }
          className="
            bg-blue-600
            text-white
            px-4 py-2
            rounded-lg
          "
        >
          Create Channel
        </button>
      </div>

      {loading ? (
        <div>
          Loading channels...
        </div>
      ) : channels.length === 0 ? (
        <div className="text-gray-500">
          No channels found
        </div>
      ) : (
        <div
          className="
            grid
            md:grid-cols-2
            xl:grid-cols-3
            gap-4
          "
        >
          {channels.map(
            (channel) => (
              <ChannelCard
                key={
                  channel.id
                }
                channel={
                  channel
                }
                onRefresh={
                  loadChannels
                }
              />
            )
          )}
        </div>
      )}

      {showModal && (
        <ChannelFormModal
          onClose={() =>
            setShowModal(false)
          }
          onSubmit={
            handleCreate
          }
        />
      )}
    </div>
  );
}