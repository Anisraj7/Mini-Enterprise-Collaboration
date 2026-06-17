import API from "../../api/axios";

export const getTaskDocuments = async (
  taskId
) => {
  const response = await API.get(
    `/tasks/${taskId}/documents`
  );

  return response.data;
};

export const uploadTaskDocument = async (
  taskId,
  formData
) => {
  const response = await API.post(
    `/tasks/${taskId}/documents`,
    formData,
    {
      headers: {
        "Content-Type":
          "multipart/form-data",
      },
    }
  );

  return response.data;
};

export const deleteTaskDocument = async (
  documentId
) => {
  const response = await API.delete(
    `/tasks/documents/${documentId}`
  );

  return response.data;
};

export const downloadTaskDocument =
  async (documentId) => {
    const response =
      await API.get(
        `/tasks/documents/${documentId}/download`,
        {
          responseType: "blob",
        }
      );

    const blob = new Blob([
      response.data,
    ]);

    const url =
      window.URL.createObjectURL(
        blob
      );

    const link =
      document.createElement("a");

    link.href = url;

    const disposition =
      response.headers[
        "content-disposition"
      ];

    let filename =
      `document-${documentId}`;

    if (disposition) {
      const match =
        disposition.match(
          /filename="?([^"]+)"?/
        );

      if (match) {
        filename = match[1];
      }
    }

    link.setAttribute(
      "download",
      filename
    );

    document.body.appendChild(
      link
    );

    link.click();

    link.remove();

    window.URL.revokeObjectURL(
      url
    );
  };