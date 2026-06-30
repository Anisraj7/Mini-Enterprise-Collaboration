from sqlalchemy.orm import Session

from app.models.project_team import ProjectTeam


class ProjectTeamRepository:

    @staticmethod
    def create(
        db: Session,
        project_team: ProjectTeam
    ) -> ProjectTeam:
        db.add(project_team)
        db.commit()
        db.refresh(project_team)
        return project_team

    @staticmethod
    def get_project_teams(
        db: Session,
        project_id: int
    ) -> list[ProjectTeam]:
        return (
            db.query(ProjectTeam)
            .filter(
                ProjectTeam.project_id == project_id
            )
            .all()
        )

    @staticmethod
    def get_mapping(
        db: Session,
        project_id: int,
        team_id: int
    ) -> ProjectTeam | None:
        return (
            db.query(ProjectTeam)
            .filter(
                ProjectTeam.project_id == project_id,
                ProjectTeam.team_id == team_id
            )
            .first()
        )

    @staticmethod
    def delete(
        db: Session,
        mapping: ProjectTeam
    ) -> None:
        db.delete(mapping)
        db.commit()