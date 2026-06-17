from enum import Enum


class UserRole(str, Enum):

    SUPER_ADMIN = "super_admin"

    ORGANIZATION_ADMIN = "organization_admin"

    WORKSPACE_ADMIN = "workspace_admin"

    MANAGER = "manager"

    EMPLOYEE = "employee"
    

class WorkspaceMemberRole(str, Enum):
    ADMIN = "ADMIN"
    MEMBER = "MEMBER"
    
class ChannelMemberRole(str, Enum):
    MODERATOR = "MODERATOR"
    MEMBER = "MEMBER"