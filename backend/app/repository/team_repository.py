from sqlalchemy.orm import Session

from app.models.team import Team


class TeamRepository:

    @staticmethod
    def create(db: Session, team: Team) -> Team:
        db.add(team)
        db.commit()
        db.refresh(team)
        return team

    @staticmethod
    def get_by_id(
        db: Session,
        team_id: int,
        organization_id: int
    ) -> Team | None:
        return (
            db.query(Team)
            .filter(
                Team.id == team_id,
                Team.organization_id == organization_id,
                Team.is_active.is_(True)
            )
            .first()
        )

    @staticmethod
    def get_all(
        db: Session,
        organization_id: int
    ) -> list[Team]:
        return (
            db.query(Team)
            .filter(
                Team.organization_id == organization_id,
                Team.is_active.is_(True)
            )
            .all()
        )

    @staticmethod
    def update(
        db: Session,
        team: Team
    ) -> Team:
        db.commit()
        db.refresh(team)
        return team

    @staticmethod
    def delete(
        db: Session,
        team: Team
    ) -> Team:
        team.is_active = False
        db.commit()
        db.refresh(team)
        return team