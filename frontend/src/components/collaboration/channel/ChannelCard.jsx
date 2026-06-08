import {
  Archive,
  RotateCcw,
  Hash,
  Pencil,
} from "lucide-react";

import {
  useState,
} from "react";

import { Link } from "react-router-dom";

import ChannelFormModal from "./ChannelFormModal";

import {
  archiveChannel,
  restoreChannel,
  updateChannel,
} from "../../../services/collaboration/channelService";

export default function ChannelCard({
  channel,
  onRefresh,
}) {
  const [showEdit, setShowEdit] =
    useState(false);

  const handleArchive = async () => {
    try {
      await archiveChannel(
        channel.id
      );

      await onRefresh();
    } catch (error) {
      console.error(error);
    }
  };

  const handleRestore = async () => {
    try {
      await restoreChannel(
        channel.id
      );

      await onRefresh();
    } catch (error) {
      console.error(error);
    }
  };

  const handleUpdate = async (
    payload
  ) => {
    try {
      await updateChannel(
        channel.id,
        payload
      );

      setShowEdit(false);

      await onRefresh();
    } catch (error) {
      console.error(error);
    }
  };

  const getTypeClass = () => {
    switch (
      channel.channel_type
    ) {
      case "PRIVATE":
        return "bg-orange-100 text-orange-700";

      case "ANNOUNCEMENT":
        return "bg-purple-100 text-purple-700";

      case "PROJECT":
        return "bg-cyan-100 text-cyan-700";

      default:
        return "bg-green-100 text-green-700";
    }
  };

  return (
    <>
      <div
        className="
          bg-white
          border
          rounded-xl
          p-5
          shadow-sm
          hover:shadow-md
          transition
        "
      >
        <div className="flex justify-between items-start">
          <div>
            <Link
              to={`/channels/${channel.id}`}
            >
              <h3
                className="
                  font-bold
                  text-lg
                  hover:text-blue-600
                "
              >
                #{channel.name}
              </h3>
            </Link>

            <p className="text-sm text-gray-500">
              {channel.description ||
                "No description"}
            </p>
          </div>

          <div className="flex flex-col gap-2 items-end">
            <span
              className={`
                text-xs
                px-2
                py-1
                rounded-full
                ${getTypeClass()}
              `}
            >
              {channel.channel_type}
            </span>

            {channel.is_archived && (
              <span
                className="
                  text-xs
                  bg-red-100
                  text-red-700
                  px-2
                  py-1
                  rounded-full
                "
              >
                ARCHIVED
              </span>
            )}
          </div>
        </div>

        <div
          className="
            mt-4
            flex
            items-center
            gap-2
            text-gray-500
          "
        >
          <Hash size={16} />
          <span>Channel</span>
        </div>

        <div className="mt-5 flex gap-2 flex-wrap">
          <button
            onClick={() =>
              setShowEdit(true)
            }
            className="
              flex
              gap-2
              items-center
              bg-blue-100
              text-blue-700
              px-3
              py-2
              rounded-lg
            "
          >
            <Pencil size={16} />
            Edit
          </button>

          {channel.is_archived ? (
            <button
              onClick={
                handleRestore
              }
              className="
                flex
                gap-2
                items-center
                bg-green-100
                text-green-700
                px-3
                py-2
                rounded-lg
              "
            >
              <RotateCcw size={16} />
              Restore
            </button>
          ) : (
            <button
              onClick={
                handleArchive
              }
              className="
                flex
                gap-2
                items-center
                bg-red-100
                text-red-700
                px-3
                py-2
                rounded-lg
              "
            >
              <Archive size={16} />
              Archive
            </button>
          )}
        </div>
      </div>

      {showEdit && (
        <ChannelFormModal
          initialData={channel}
          onClose={() =>
            setShowEdit(false)
          }
          onSubmit={
            handleUpdate
          }
        />
      )}
    </>
  );
}