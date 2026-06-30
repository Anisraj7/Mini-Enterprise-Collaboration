import API from "../../api/axios";

export const getProjects = async (
  params = {}
) => {
  const { data } = await API.get(
    "/projects",
    {
      params,
    }
  );

  return data;
};

export const getProjectById = async (
  projectId
) => {
  const { data } = await API.get(
    `/projects/${projectId}`
  );

  return data;
};

export const createProject = async (
  payload
) => {
  const { data } = await API.post(
    "/projects",
    payload
  );

  return data;
};

export const updateProject = async (
  projectId,
  payload
) => {
  const { data } = await API.put(
    `/projects/${projectId}`,
    payload
  );

  return data;
};

export const deleteProject = async (
  projectId
) => {
  const { data } = await API.delete(
    `/projects/${projectId}`
  );

  return data;
};