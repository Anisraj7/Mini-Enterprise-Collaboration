import API from "../../api/axios";

export const getTeamMembers = async (
  teamId
) => {
  const { data } = await API.get(
    `/teams/${teamId}/members`
  );

  return data;
};

export const addTeamMember = async (
  teamId,
  payload
) => {
  const { data } = await API.post(
    `/teams/${teamId}/members`,
    payload
  );

  return data;
};

export const removeTeamMember = async (
  teamId,
  userId
) => {
  const { data } = await API.delete(
    `/teams/${teamId}/members/${userId}`
  );

  return data;
};