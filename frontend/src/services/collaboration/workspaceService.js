import api from "../../api/axios";
import { getPageItems } from "../../api/pagination";

export const getWorkspaces = async () => {
  const { data } = await api.get("/workspaces");

  return getPageItems(data);
};

export const getWorkspaceById = async (
  workspaceId
) => {
  const { data } = await api.get(
    `/workspaces/${workspaceId}`
  );

  return data;
};

export const createWorkspace = async (
  payload
) => {
  const { data } = await api.post(
    "/workspaces",
    payload
  );

  return data;
};

export const updateWorkspace = async (
  workspaceId,
  payload
) => {
  const { data } = await api.put(
    `/workspaces/${workspaceId}`,
    payload
  );

  return data;
};

export const archiveWorkspace = async (
  workspaceId
) => {
  const { data } = await api.patch(
    `/workspaces/${workspaceId}/archive`
  );

  return data;
};

export const restoreWorkspace = async (
  workspaceId
) => {
  const { data } = await api.patch(
    `/workspaces/${workspaceId}/restore`
  );

  return data;
};