from enum import Enum


class ProjectDocumentType(str, Enum):
    REQUIREMENT = "REQUIREMENT"
    DESIGN = "DESIGN"
    TEST = "TEST"
    RELEASE = "RELEASE"
    OTHER = "OTHER"