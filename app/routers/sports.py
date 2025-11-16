from fastapi import APIRouter, Depends
from app.database import get_db
from app.models import SportResponse, SportListResponse

router = APIRouter(prefix="/sports")


@router.get("/", response_model=SportListResponse)
def get_sports(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name FROM Sport")
    rows = cursor.fetchall()
    sports_list = [SportResponse(id=row["id"], name=row["name"]) for row in rows]
    return SportListResponse(sports=sports_list)
