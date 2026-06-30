from datetime import datetime

from sqlalchemy import (
    Integer,
    ForeignKey,
    Boolean,
    DateTime,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.enums.team import TeamMemberRole


class TeamMember(Base):
    __tablename__ = "team_members"

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
        index=True
    )

    team_id: Mapped[int] = mapped_column(
        ForeignKey("teams.id"),
        nullable=False,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    role: Mapped[TeamMemberRole] = mapped_column(
        Enum(TeamMemberRole),
        nullable=False,
        default=TeamMemberRole.MEMBER
    )

    joined_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    team = relationship(
        "Team",
        back_populates="members"
    )