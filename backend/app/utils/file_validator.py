from fastapi import (
    HTTPException,
    UploadFile,
    status,
)


class FileValidator:

    MAX_FILE_SIZE = 10 * 1024 * 1024

    ALLOWED_TYPES = {
        "application/pdf",
        "image/png",
        "image/jpeg",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    }

    @staticmethod
    def validate(
        file: UploadFile,
    ) -> None:

        if (
            file.content_type
            not in FileValidator.ALLOWED_TYPES
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unsupported file type",
            )

        file.file.seek(
            0,
            2,
        )

        file_size = file.file.tell()

        file.file.seek(0)

        if (
            file_size
            > FileValidator.MAX_FILE_SIZE
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File exceeds 10MB limit",
            )