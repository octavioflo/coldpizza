from fastapi import APIRouter
from app.models.vulnerabilities import Vulnerability
from fastapi.encoders import jsonable_encoder

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


@router.get("/")
async def read_vulnerabilities(limit: int = 10) -> list[dict]:
    return vulnerability_list[:limit]


@router.get("/{vulnerability_id}")
async def read_vulnerability(vulnerability_id: int) -> dict:
    return next(
        (
            vulnerability
            for vulnerability in vulnerability_list
            if vulnerability["id"] == vulnerability_id
        ),
        None,
    )


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
