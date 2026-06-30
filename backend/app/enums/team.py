from enum import Enum


class TeamMemberRole(str, Enum):
    LEAD = "LEAD"
    MEMBER = "MEMBER"
    VIEWER = "VIEWER"