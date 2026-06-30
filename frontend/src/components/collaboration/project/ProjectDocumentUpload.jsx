import { useState } from "react";

export default function ProjectDocumentUpload({
  onUpload,
}) {
  const [file, setFile] =
    useState(null);

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();

        if (file) {
          onUpload(file);
        }
      }}
      className="flex gap-2"
    >
      <input
        type="file"
        onChange={(e) =>
          setFile(
            e.target.files[0]
          )
        }
      />

      <button className="bg-blue-600 text-white px-4 py-2 rounded">
        Upload
      </button>
    </form>
  );
}