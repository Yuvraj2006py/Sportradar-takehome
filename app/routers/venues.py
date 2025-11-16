from fastapi import APIRouter, Depends
from app.database import get_db
from app.models import VenueResponse, VenueListResponse

router = APIRouter(prefix="/venues")


@router.get("/", response_model=VenueListResponse)
def get_venues(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, name, city, country FROM Venue")
    rows = cursor.fetchall()
    venues_list = [VenueResponse(id=row["id"], name=row["name"], city=row["city"], country=row["country"]) for row in rows]
    return VenueListResponse(venues=venues_list)