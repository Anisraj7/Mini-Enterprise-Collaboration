import API from "../../api/axios";

export const getChannelTasks = async (
  channelId,
  page = 1,
  size = 10
) => {
  const response = await API.get(
    `/channels/${channelId}/tasks`,
    {
      params: {
        page,
        size,
      },
    }
  );

  return response.data;
};

export const getChannelTask = async (
  channelId,
  taskId
) => {
  const response = await API.get(
    `/channels/${channelId}/tasks/${taskId}`
  );

  return response.data;
};

export const createChannelTask = async (
  channelId,
  workspaceId,
  payload
) => {
  const response = await API.post(
    `/channels/${channelId}/tasks`,
    payload,
    {
      params: {
        workspace_id: workspaceId,
      },
    }
  );

  return response.data;
};

export const assignChannelTask = async (
  channelId,
  taskId,
  assignedToId
) => {
  const response = await API.patch(
    `/channels/${channelId}/tasks/${taskId}/assign`,
    {
      assigned_to_id: assignedToId,
    }
  );

  return response.data;
};