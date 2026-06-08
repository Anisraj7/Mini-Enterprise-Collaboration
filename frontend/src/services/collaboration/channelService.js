import api from "../../api/axios";

import {
  getPageItems,
} from "../../api/pagination";

export const getChannels = async (
  workspaceId
) => {
  const { data } = await api.get(
    `/workspaces/${workspaceId}/channels`
  );

  return getPageItems(data);
};

export const getChannel = async (
  channelId
) => {
  const { data } = await api.get(
    `/channels/${channelId}`
  );

  return data;
};

export const createChannel = async (
  payload
) => {
  const { data } = await api.post(
    "/channels",
    payload
  );

  return data;
};

export const updateChannel = async (
  channelId,
  payload
) => {
  const { data } = await api.put(
    `/channels/${channelId}`,
    payload
  );

  return data;
};

export const archiveChannel = async (
  channelId
) => {
  const { data } = await api.patch(
    `/channels/${channelId}/archive`
  );

  return data;
};

export const restoreChannel = async (
  channelId
) => {
  const { data } = await api.patch(
    `/channels/${channelId}/restore`
  );

  return data;
};