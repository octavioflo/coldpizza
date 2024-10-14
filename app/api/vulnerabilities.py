from fastapi import APIRouter, HTTPException
from fastapi.encoders import jsonable_encoder

from app.models.vulnerabilities.vulnerabilities import Vulnerability
from app.services.vulnerabilities import get_vulnerabilities, get_vulnerability
from app.db.database import SessionDep

router = APIRouter(prefix="/vulnerabilities")

vulnerability_list = [
    {
        "id": 1,
        "name": "sql_injection",
    },
    {
        "id": 2,
        "name": "xss",
    },
]


@router.get("/", response_model=list[Vulnerability])
async def read_vulnerabilities(session: SessionDep, limit: int = 10):
    return get_vulnerabilities(session, limit)


@router.get("/{vulnerability_id}", response_model=Vulnerability)
async def read_vulnerability(vulnerability_id: int, session: SessionDep):
    vulnerability = get_vulnerability(session, vulnerability_id)
    if not vulnerability:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    return vulnerability


@router.post("/", status_code=201)
async def create_vulnerability(vulnerability: Vulnerability) -> dict[str, str]:
    vulnerability_list.append({"id": vulnerability.id, "name": vulnerability.name})
    return {"status": "ok"}


@router.put("/{vulnerability_id}")
async def update_vulnerability(
    vulnerability_id: int, vulnerability: Vulnerability
) -> dict[str, str]:
    vulnerability_list[vulnerability_id] = jsonable_encoder(vulnerability)
    return {"status": "ok"}
