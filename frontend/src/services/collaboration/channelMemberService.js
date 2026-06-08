import api from "../../api/axios";

import {
  getPageItems,
} from "../../api/pagination";

export const getChannelMembers =
  async (channelId) => {
    const { data } =
      await api.get(
        `/channels/${channelId}/members`
      );

    return getPageItems(data);
  };

export const joinChannel =
  async (channelId) => {
    const { data } =
      await api.post(
        `/channels/${channelId}/join`
      );

    return data;
  };

export const leaveChannel =
  async (channelId) => {
    const { data } =
      await api.post(
        `/channels/${channelId}/leave`
      );

    return data;
  };