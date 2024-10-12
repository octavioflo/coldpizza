from sqlmodel import SQLModel, Field
from enum import Enum


class SeverityLevel(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class Status(str, Enum):
    OPEN = "Open"
    IN_PROGRESS = "In Progress"
    RESOLVED = "Resolved"
    CLOSED = "Closed"


class Vulnerability(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    severity_level: SeverityLevel
    status: Status
    discovery_date: str
    reported_by: str


class VulnerabilityCreate(Vulnerability):
    pass