import API from "../../api/axios";

export const getWorkspaceTasks = async (
  workspaceId,
  page = 1,
  size = 10
) => {
  const response = await API.get(
    `/workspaces/${workspaceId}/tasks`,
    {
      params: {
        page,
        size,
      },
    }
  );

  return response.data;
};

export const getWorkspaceTask = async (
  workspaceId,
  taskId
) => {
  const response = await API.get(
    `/workspaces/${workspaceId}/tasks/${taskId}`
  );

  return response.data;
};

export const createWorkspaceTask = async (
  workspaceId,
  payload
) => {
  const response = await API.post(
    `/workspaces/${workspaceId}/tasks`,
    payload
  );

  return response.data;
};

export const assignWorkspaceTask = async (
  workspaceId,
  taskId,
  assignedToId
) => {
  const response = await API.patch(
    `/workspaces/${workspaceId}/tasks/${taskId}/assign`,
    {
      assigned_to_id: assignedToId,
    }
  );

  return response.data;
};