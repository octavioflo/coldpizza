from app.db.database import SessionDep
from app.models.requirements import Requirement, RequirementGroup

from sqlmodel import select


def generate_requirement_id(session: SessionDep) -> str:
    # Get the current maximum ID from the requirements table
    statement = select(Requirement.id).order_by(Requirement.id.desc())
    last_requirement = session.exec(statement).first()

    # Increment to get the new sequence number
    new_sequence_number = 1 if last_requirement is None else last_requirement + 1
    return f"REQ-{new_sequence_number:03d}"


def get_requirements(session: SessionDep, limit: int) -> list[Requirement]:
    requirements = select(Requirement).limit(limit)
    return session.exec(requirements).all()


def get_requirement(session: SessionDep, requirement_id: int) -> Requirement | None:
    return session.get(Requirement, requirement_id)


def group_exists(session: SessionDep, group_name: str) -> bool:
    """Check if a requirement group exists in the database."""
    statement = select(Requirement).where(Requirement.group == group_name)
    result = session.exec(statement).first()

    # Return True if a requirement with the specified group is found, otherwise False
    return result is not None


def get_groups(session: SessionDep, limit: int) -> list[Requirement]:
    groups = select(RequirementGroup).limit(limit)
    return session.exec(groups).all()