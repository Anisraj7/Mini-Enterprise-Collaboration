import API from "../../api/axios";

export const getChannelMessages = async (
  channelId,
  page = 1,
  size = 10
) => {
  const response = await API.get(
    `/channels/${channelId}/messages`,
    {
      params: {
        page,
        size,
      },
    }
  );

  return response.data;
};

export const createChannelMessage = async (
  channelId,
  payload
) => {
  const response = await API.post(
    `/channels/${channelId}/messages`,
    payload
  );

  return response.data;
};

// Reserved for future backend support
export const updateChannelMessage = async (
  messageId,
  payload
) => {
  const response = await API.put(
    `/channel-messages/${messageId}`,
    payload
  );

  return response.data;
};

export const deleteChannelMessage = async (
  messageId
) => {
  const response = await API.delete(
    `/channel-messages/${messageId}`
  );

  return response.data;
};