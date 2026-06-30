from sqlalchemy.orm import Session

from app.models.project_document import ProjectDocument


class ProjectDocumentRepository:

    @staticmethod
    def create(
        db: Session,
        document: ProjectDocument
    ) -> ProjectDocument:
        db.add(document)
        db.commit()
        db.refresh(document)
        return document

    @staticmethod
    def get_by_id(
        db: Session,
        document_id: int,
        organization_id: int
    ) -> ProjectDocument | None:
        return (
            db.query(ProjectDocument)
            .filter(
                ProjectDocument.id == document_id,
                ProjectDocument.organization_id == organization_id
            )
            .first()
        )

    @staticmethod
    def get_project_documents(
        db: Session,
        project_id: int
    ) -> list[ProjectDocument]:
        return (
            db.query(ProjectDocument)
            .filter(
                ProjectDocument.project_id == project_id
            )
            .all()
        )

    @staticmethod
    def delete(
        db: Session,
        document: ProjectDocument
    ):
        db.delete(document)
        db.commit()