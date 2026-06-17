from __future__ import annotations

import os
import shutil
from pathlib import Path

from fastapi import UploadFile


UPLOAD_DIR = Path("uploads")

TASK_UPLOAD_DIR = UPLOAD_DIR / "tasks"

APPROVAL_UPLOAD_DIR = UPLOAD_DIR / "approvals"


class FileStorage:

    @staticmethod
    def save_task_file(
        task_id: int,
        file: UploadFile,
    ) -> str:

        folder = TASK_UPLOAD_DIR / f"task_{task_id}"

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = folder/file.filename

        with open(
            file_path,
            "wb",
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer,
            )

        return str(file_path)

    @staticmethod
    def save_approval_file(
        approval_id: int,
        file: UploadFile,
    ) -> str:

        folder = (
            APPROVAL_UPLOAD_DIR
            / f"approval_{approval_id}"
        )

        folder.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = folder / file.filename

        with open(
            file_path,
            "wb",
        ) as buffer:

            shutil.copyfileobj(
                file.file,
                buffer,
            )

        return str(file_path)

    @staticmethod
    def delete_file(
        file_path: str,
    ) -> None:

        if os.path.exists(file_path):

            os.remove(file_path)