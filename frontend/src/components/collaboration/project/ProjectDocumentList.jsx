export default function ProjectDocumentList({
  documents,
  onDelete,
  getDownloadUrl,
}) {
  return (
    <table className="w-full">
      <tbody>
        {documents.map((doc) => (
          <tr key={doc.id}>
            <td className="p-2">
              {doc.file_name}
            </td>

            <td className="p-2 flex gap-3">
              <a
                href={getDownloadUrl(
                  doc.id
                )}
                target="_blank"
                rel="noreferrer"
              >
                Download
              </a>

              <button
                onClick={() =>
                  onDelete(doc.id)
                }
                className="text-red-600"
              >
                Delete
              </button>
            </td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}