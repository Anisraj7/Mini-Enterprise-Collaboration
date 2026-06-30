import API from "../../api/axios";

export const getProjectDocuments =
  async (projectId) => {
    const { data } = await API.get(
      `/projects/${projectId}/documents`
    );

    return data;
  };

export const uploadProjectDocument =
  async (projectId, formData) => {
    const { data } = await API.post(
      `/projects/${projectId}/documents`,
      formData,
      {
        headers: {
          "Content-Type":
            "multipart/form-data",
        },
      }
    );

    return data;
  };

export const deleteProjectDocument =
  async (documentId) => {
    const { data } = await API.delete(
      `/project-documents/${documentId}`
    );

    return data;
  };

export const downloadProjectDocument =
  async (documentId) => {
    const response = await API.get(
      `/project-documents/${documentId}/download`,
      {
        responseType: "blob",
      }
    );

    return response;
  };
