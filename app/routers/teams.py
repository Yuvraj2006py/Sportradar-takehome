from fastapi import APIRouter, Depends
from app.database import get_db
from app.models import TeamResponse, TeamListResponse

router = APIRouter(prefix="/teams")


@router.get("/", response_model=TeamListResponse)
def get_teams(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("""
        SELECT
            id,
            name,
            sport_id_foreignkey AS sport_id
        FROM Team
    """)
    rows = cursor.fetchall()
    teams_list = [TeamResponse(id=row["id"], name=row["name"], sport_id=row["sport_id"]) for row in rows]
    return TeamListResponse(teams=teams_list)

    
