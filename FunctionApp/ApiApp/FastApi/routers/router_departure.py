from fastapi import APIRouter, Depends
from FastApi.models.departure import Departure
from FastApi.helpers.database import get_db
from FastApi.helpers.error_handler import handle_exceptions
import sqlite3

router = APIRouter()


@router.get(
    path="/departures",
    response_model=list[Departure],
    tags=["Departures"],
)
@handle_exceptions
async def get_departures(db: sqlite3.Connection = Depends(get_db)):
    with db:
        cursor = db.cursor()
        cursor.execute("SELECT * FROM departures")
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
    return rows
