import API from "../../api/axios";

export const getProjectTeams = async (
  projectId
) => {
  const { data } = await API.get(
    `/projects/${projectId}/teams`
  );

  return data;
};

export const assignProjectTeam = async (
  projectId,
  payload
) => {
  const { data } = await API.post(
    `/projects/${projectId}/teams`,
    payload
  );

  return data;
};

export const removeProjectTeam = async (
  projectId,
  teamId
) => {
  const { data } = await API.delete(
    `/projects/${projectId}/teams/${teamId}`
  );

  return data;
};