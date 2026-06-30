import API from "../../api/axios";

export const getTeamWorkload =
  async (teamId) => {
    const { data } = await API.get(
      `/teams/${teamId}/workload`
    );

    return data;
  };

export const getProjectWorkload =
  async (projectId) => {
    const { data } = await API.get(
      `/projects/${projectId}/workload`
    );

    return data;
  };