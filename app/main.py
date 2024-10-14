from fastapi import FastAPI

from app.db.database import create_db_and_tables
from app.api import vulnerabilities, requirements


app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(vulnerabilities.router)
app.include_router(requirements.router)
