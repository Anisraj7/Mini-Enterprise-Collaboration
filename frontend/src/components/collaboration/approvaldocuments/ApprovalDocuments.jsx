import { useEffect, useState } from "react";

import {
  getApprovalDocuments,
  uploadApprovalDocument,
  deleteApprovalDocument,
  downloadApprovalDocument,
} from "../../../services/collaboration/approvalDocumentService";

const DOCUMENT_TYPES = [
  "MEDICAL_CERTIFICATE",
  "INVOICE",
  "QUOTATION",
  "LICENSE",
  "ESTIMATE",
  "OTHER",
];

export default function ApprovalDocuments({
  approvalId,
}) {
  const [documents, setDocuments] =
    useState([]);

  const [loading, setLoading] =
    useState(true);

  const [uploading, setUploading] =
    useState(false);

  const [file, setFile] =
    useState(null);

  const [documentType, setDocumentType] =
    useState("OTHER");

  const loadDocuments =
    async () => {
      try {
        setLoading(true);

        const data =
          await getApprovalDocuments(
            approvalId
          );

        setDocuments(data || []);
      } catch (error) {
        console.error(error);
      } finally {
        setLoading(false);
      }
    };

  useEffect(() => {
    if (approvalId) {
      loadDocuments();
    }
  }, [approvalId]);

  const handleUpload =
    async (e) => {
      e.preventDefault();

      if (!file) return;

      try {
        setUploading(true);

        const formData =
          new FormData();

        formData.append(
          "document_type",
          documentType
        );

        formData.append(
          "file",
          file
        );

        await uploadApprovalDocument(
          approvalId,
          formData
        );

        setFile(null);
        setDocumentType("OTHER");

        await loadDocuments();
      } catch (error) {
        console.error(error);
      } finally {
        setUploading(false);
      }
    };

  const handleDelete =
    async (documentId) => {
      if (
        !window.confirm(
          "Delete this document?"
        )
      ) {
        return;
      }

      try {
        await deleteApprovalDocument(
          documentId
        );

        await loadDocuments();
      } catch (error) {
        console.error(error);
      }
    };

  if (loading) {
    return (
      <div>
        Loading documents...
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="bg-white border rounded-xl p-5">
        <h3 className="font-semibold mb-4">
          Upload Document
        </h3>

        <form
          onSubmit={handleUpload}
          className="space-y-3"
        >
          <select
            value={documentType}
            onChange={(e) =>
              setDocumentType(
                e.target.value
              )
            }
            className="
              w-full
              border
              rounded-lg
              p-3
            "
          >
            {DOCUMENT_TYPES.map(
              (type) => (
                <option
                  key={type}
                  value={type}
                >
                  {type}
                </option>
              )
            )}
          </select>

          <input
            type="file"
            onChange={(e) =>
              setFile(
                e.target.files?.[0]
              )
            }
            className="
              w-full
              border
              rounded-lg
              p-3
            "
          />

          <button
            type="submit"
            disabled={
              uploading || !file
            }
            className="
              px-4
              py-2
              bg-blue-600
              text-white
              rounded-lg
              disabled:opacity-50
            "
          >
            {uploading
              ? "Uploading..."
              : "Upload"}
          </button>
        </form>
      </div>

      <div className="bg-white border rounded-xl p-5">
        <h3 className="font-semibold mb-4">
          Documents
        </h3>

        {documents.length === 0 ? (
          <p className="text-gray-500">
            No documents uploaded
          </p>
        ) : (
          <div className="space-y-3">
            {documents.map(
              (doc) => (
                <div
                  key={doc.id}
                  className="
                    border
                    rounded-lg
                    p-4
                    flex
                    justify-between
                    items-center
                  "
                >
                  <div>
                    <div className="font-medium">
                      {doc.file_name}
                    </div>

                    <div className="text-sm text-gray-500">
                      {
                        doc.document_type
                      }
                    </div>

                    <div className="text-xs text-gray-400 mt-1">
                      {doc.mime_type}
                    </div>

                    <div className="text-xs text-gray-400">
                      {doc.file_size} bytes
                    </div>
                  </div>

                  <div className="flex gap-2">
                    <button
                      onClick={() =>
                        downloadApprovalDocument(
                          doc.id
                        )
                      }
                      className="
                        px-3
                        py-1
                        border
                        rounded
                      "
                    >
                      Download
                    </button>

                    <button
                      onClick={() =>
                        handleDelete(
                          doc.id
                        )
                      }
                      className="
                        px-3
                        py-1
                        border
                        rounded
                        text-red-600
                      "
                    >
                      Delete
                    </button>
                  </div>
                </div>
              )
            )}
          </div>
        )}
      </div>
    </div>
  );
}