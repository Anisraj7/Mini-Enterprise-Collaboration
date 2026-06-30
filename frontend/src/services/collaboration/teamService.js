import API from "../../api/axios";

export const getTeams = async (params = {}) => {
  const { data } = await API.get("/teams", { params });
  return data;
};

export const getTeamById = async (teamId) => {
  const { data } = await API.get(`/teams/${teamId}`);
  return data;
};

export const createTeam = async (payload) => {
  const { data } = await API.post("/teams", payload);
  return data;
};

export const updateTeam = async (teamId, payload) => {
  const { data } = await API.put(
    `/teams/${teamId}`,
    payload
  );

  return data;
};

export const deleteTeam = async (teamId) => {
  const { data } = await API.delete(
    `/teams/${teamId}`
  );

  return data;
};