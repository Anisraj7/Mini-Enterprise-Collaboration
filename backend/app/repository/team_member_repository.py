from sqlalchemy.orm import Session

from app.models.team_member import TeamMember


class TeamMemberRepository:

    @staticmethod
    def create(
        db: Session,
        member: TeamMember,
    ) -> TeamMember:
        db.add(member)
        db.commit()
        db.refresh(member)
        return member

    @staticmethod
    def get_team_members(
        db: Session,
        team_id: int,
    ) -> list[TeamMember]:
        return (
            db.query(TeamMember)
            .filter(
                TeamMember.team_id == team_id,
                TeamMember.is_active.is_(True),
            )
            .all()
        )

    @staticmethod
    def get_member(
        db: Session,
        team_id: int,
        user_id: int,
    ) -> TeamMember | None:
        return (
            db.query(TeamMember)
            .filter(
                TeamMember.team_id == team_id,
                TeamMember.user_id == user_id,
                TeamMember.is_active.is_(True),
            )
            .first()
        )

    @staticmethod
    def delete(
        db: Session,
        member: TeamMember,
    ):
        member.is_active = False
        db.commit()
        db.refresh(member)
        return member