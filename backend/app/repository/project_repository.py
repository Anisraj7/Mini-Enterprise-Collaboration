from sqlalchemy.orm import Session

from app.models.project import Project


class ProjectRepository:

    @staticmethod
    def create(
        db: Session,
        project: Project
    ) -> Project:
        db.add(project)
        db.commit()
        db.refresh(project)
        return project

    @staticmethod
    def get_by_id(
        db: Session,
        project_id: int,
        organization_id: int
    ) -> Project | None:
        return (
            db.query(Project)
            .filter(
                Project.id == project_id,
                Project.organization_id == organization_id
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        organization_id: int
    ) -> list[Project]:
        return (
            db.query(Project)
            .filter(Project.organization_id == organization_id)
            .all()
        )
    
    @staticmethod
    def update(
        db: Session,
        project: Project,
    ):
        db.commit()
        db.refresh(project)
        return project


    @staticmethod
    def delete(
        db: Session,
        project: Project,
    ):
        project.is_active = False # type: ignore
        db.commit()
        db.refresh(project)
        return project