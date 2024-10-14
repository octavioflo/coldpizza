from app.db.database import SessionDep
from app.models.vulnerabilities.vulnerabilities import Vulnerability

from sqlmodel import select


def get_vulnerabilities(session: SessionDep, limit: int):
    vulnerabilities = select(Vulnerability).limit(limit)
    return session.exec(vulnerabilities).all()


def get_vulnerability(session: SessionDep, vulnerability_id: int) -> Vulnerability | None:
    return session.get(Vulnerability, vulnerability_id)
