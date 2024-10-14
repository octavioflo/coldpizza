from sqlmodel import Relationship, SQLModel, Field
from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class RequirementStatus(Enum):
    MET = "met"
    NOT_MET = "not_met"


class RequirementGroup(SQLModel, table=True):
    name: str = Field(nullable=False, unique=True)
    description: str | None
    requirements: list["Requirement"] = Relationship(back_populates="group")
    id: int | None = Field(default=None, primary_key=True)


class RequirementGroupCreate(BaseModel):
    name: str
    description: str


class RequirementBase(SQLModel):
    name: str = Field(default="", nullable=False)
    description: str = Field(default="", nullable=False)
    status: RequirementStatus = Field(
        default=RequirementStatus.NOT_MET.value, nullable=False
    )
    # TODO: standards: str
    acceptance_criteria: str = Field(default="", nullable=False)


class Requirement(RequirementBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    archive: bool = Field(default=False)
    group_id: int = Field(foreign_key="requirementgroup.id")
    group: RequirementGroup | None = Relationship(back_populates="requirements")
    date_created: datetime = Field(default_factory=datetime.utcnow)
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class RequirementCreate(RequirementBase):
    group: str


class RequirementPublic(RequirementBase):
    id: int
    archive: bool
    group: RequirementGroup
    date_created: datetime
    last_updated: datetime


# TODO:
#   "revision_history": [
#     {
#       "version": "1.0",
#       "date": "2024-10-01",
#       "author": "Security Team Lead",
#       "changes": "Initial version",
#       "comments": "some comment."
#     }
