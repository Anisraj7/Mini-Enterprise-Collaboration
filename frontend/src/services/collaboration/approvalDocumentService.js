import API from "../../api/axios";

export const getApprovalDocuments =
  async (approvalId) => {
    const response =
      await API.get(
        `/approvals/${approvalId}/documents`
      );

    return response.data;
  };

export const uploadApprovalDocument =
  async (
    approvalId,
    formData
  ) => {
    const response =
      await API.post(
        `/approvals/${approvalId}/documents`,
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

export const deleteApprovalDocument =
  async (documentId) => {
    const response =
      await API.delete(
        `/approvals/documents/${documentId}`
      );

    return response.data;
  };

export const downloadApprovalDocument =
  async (documentId) => {
    const response =
      await API.get(
        `/approvals/documents/${documentId}/download`,
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
      `approval-document-${documentId}`;

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