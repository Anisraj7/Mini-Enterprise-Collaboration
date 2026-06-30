import API from "../../api/axios";

export const getProjectCalendar =
  async (projectId) => {
    const { data } = await API.get(
      `/projects/${projectId}/calendar`
    );

    return data;
  };