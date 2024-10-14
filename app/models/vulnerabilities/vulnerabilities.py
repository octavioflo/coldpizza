from sqlmodel import SQLModel, Field
from enum import Enum


class SeverityLevel(str, Enum):
    INFO = "info"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Status(str, Enum):
    OPEN = "open"
    FALSE_POSITIVE = "false_positive"
    CONFIRMED = "confirmed"
    RESOLVED = "resolved"
    REOPENED = "reopened"


class IssueType(str, Enum):
    SAST = "sast"
    DAST = "dast"
    SCA = "sca"
    CONTAINER = "container"
    IAC = "iac"
    CLOUD = "cloud"
    CODE_REVIEW = "code_review"
    PENTEST = "pentest"
    BUG_BOUNTY = "bug_bounty"
    THREAT_MODEL = "threat_model"
    COMPLIANCE = "compliance"
    INCIDENT_RESPONSE = "incident_response"


class Identifier(str, Enum):
    SANS = "cwe"
    OWASP = "owasp"
    CVE = "cve"


class Vulnerability(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    description: str
    severity_level: SeverityLevel
    adjusted_severity_level: SeverityLevel  # this is an adjusted severity that has been placed after a review occurs
    status: Status
    new: bool  # if this is the first time we identified an issue we label it as new.
    issue_type: IssueType
    discovery_date: str
    reported_by: str
    scan_id: int
    tool_name: str
    remediation_guidance: str


class VulnerabilitySast(Vulnerability, table=True):
    filename: str
    line_number: int
    vulnerability_type: str


class VulnerabilityCreate(Vulnerability):
    pass
