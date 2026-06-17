import api from "../../api/axios";

import {
  getPageItems,
} from "../../api/pagination";

export const getMembers = async (
  workspaceId,
  search = ""
) => {
  const { data } = await api.get(
    `/workspaces/${workspaceId}/members`,
    {
      params: {
        search,
      },
    }
  );

  return getPageItems(data);
};

export const addMember = async (
  payload
) => {
  const { data } = await api.post(
    `/workspaces/${payload.workspace_id}/members`,
    payload
  );

  return data;
};

export const updateMemberRole = async (
  payload
) => {
  const { data } = await api.patch(
    `/workspaces/${payload.workspace_id}/members/${payload.user_id}/role`,
    {
      role: payload.role,
    }
  );

  return data;
};

export const removeMember = async (
  workspaceId,
  userId
) => {
  const { data } = await api.delete(
    `/workspaces/${workspaceId}/members/${userId}`
  );

  return data;
};

export const getUsers = async () => {
  const { data } = await api.get("/users");

  return data.items || [];
};