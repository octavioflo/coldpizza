from sqlmodel import SQLModel, Field
from enum import Enum

from app.models.vulnerabilities.vulnerabilities import Vulnerability

'''
We should consider doing products, service groups, services
'''

class ProgrammingLang(str, Enum):
    PYTHON = "python"
    JAVA = "java"
    SWIFT = "swift"


class Environment(str, Enum):
    FRONTEND = "frontend"
    BACKEND = "backend"
    INTERNAL = "internal"
    EXTERNAL = "external"
    MOBILE = "mobile"
    SAAS = "saas"
    ON_PREM = "on_prem"


class Projects(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    group: str
    description: str
    business_critical: str
    project_owner: str
    environment: str
    language: ProgrammingLang
    git_url: str
    vulnerabilities: Vulnerability
    base_image: str
    scans: str  # this may need to be a model. Listing out the scans that have been done for this project. This could tie into security requirements.
    
