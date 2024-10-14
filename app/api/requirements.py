from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from app.models.requirements import (
    Requirement,
    RequirementGroup,
    RequirementCreate,
    RequirementGroupCreate,
    RequirementPublic,
)
from app.services.requirements import (
    get_requirement,
    get_requirements,
    group_exists,
    get_groups,
)
from app.db.database import SessionDep

router = APIRouter(prefix="/requirements")


@router.get("/", response_model=list[RequirementPublic])
async def read_requirements(session: SessionDep, limit: int = 10):
    return get_requirements(session, limit)


@router.get("/{requirement_id}", response_model=RequirementPublic)
async def read_requirement(requirement_id: int, session: SessionDep):
    requirement = get_requirement(session, requirement_id)
    if not requirement:
        raise HTTPException(status_code=404, detail="Requirement not found")
    return requirement


@router.post("/", status_code=201, response_model=RequirementPublic)
async def create_requirement(requirement: RequirementCreate, session: SessionDep):
    # TODO: check if a group exists, otherwise throw an exception
    # if group_exists:
    #     raise HTTPException(status_code=404, detail="Requirement group does not exist")
    db_requirement = Requirement.model_validate(requirement)
    session.add(db_requirement)
    session.commit()
    session.refresh(db_requirement)
    return db_requirement


@router.put("/{requirement_id}")
async def update_vulnerability(
    requirement_id: int, requirement: RequirementCreate, session: SessionDep
) -> dict[str, str]:
    db_requirement = get_requirement(session, requirement_id)
    if not db_requirement:
        raise HTTPException(status_code=404, detail="Requirement not found")
    requirement_data = requirement.model_dump(exclude_unset=True)
    db_requirement.sqlmodel_update(requirement_data)
    session.add(db_requirement)
    session.commit()
    session.refresh(db_requirement)
    return db_requirement


@router.get("/groups/", response_model=list[RequirementGroup])
async def read_groups(session: SessionDep, limit: int = 10):
    return get_groups(session, limit)


@router.post("/groups/", status_code=201, response_model=RequirementGroup)
async def create_group(group: RequirementGroupCreate, session: SessionDep):
    # TODO: check if a group exists, if it does throw an exception
    # if group_exists:
    #     raise HTTPException(status_code=404, detail="Requirement group already exist")
    db_group = RequirementGroup.model_validate(group)
    session.add(db_group)
    session.commit()
    session.refresh(db_group)
    return db_group