import API from "../../api/axios";

export const getWorkspaceMessages = async (
  workspaceId,
  page = 1,
  size = 10
) => {
  const response = await API.get(
    `/workspaces/${workspaceId}/messages`,
    {
      params: {
        page,
        size,
      },
    }
  );

  return response.data;
};

export const createWorkspaceMessage = async (
  workspaceId,
  payload
) => {
  const response = await API.post(
    `/workspaces/${workspaceId}/messages`,
    payload
  );

  return response.data;
};