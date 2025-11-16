from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app.models import (
    EventResponse,
    EventListResponse,
    SportResponse,
    VenueResponse,
    TeamResponse
)

router = APIRouter(prefix="/events")


@router.get("/", response_model=EventListResponse)
def get_events(
    sport_id: int | None = None,
    date: str | None = None,
    search: str | None = None,
    db=Depends(get_db)
):
    cursor = db.cursor()

    base_query = """
        SELECT
            Event.id AS event_id,
            Event.start_datetime,
            Event.description,

            Sport.id AS sport_id,
            Sport.name AS sport_name,

            Venue.id AS venue_id,
            Venue.name AS venue_name,
            Venue.city AS venue_city,
            Venue.country AS venue_country

        FROM Event
        LEFT JOIN Sport ON Sport.id = Event.sport_id_foreignkey
        LEFT JOIN Venue ON Venue.id = Event.venue_id_foreignkey
    """

    conditions = []
    params = []

    if sport_id is not None:
        conditions.append("Event.sport_id_foreignkey = ?")
        params.append(sport_id)

    if date is not None:
        conditions.append("Event.start_datetime LIKE ?")
        params.append(f"{date}%")
    
    if search is not None:
        conditions.append("""
            (
                Event.description LIKE ?
                OR Sport.name LIKE ?
                OR Venue.name LIKE ?
                OR Event.id IN (
                    SELECT event_id_foreignkey 
                    FROM EventTeam
                    JOIN Team ON Team.id = EventTeam.team_id_foreignkey
                    WHERE Team.name LIKE ?
                )
            )
        """)

        params.extend([
            f"%{search}%",
            f"%{search}%",
            f"%{search}%",
            f"%{search}%"
        ])


    if conditions:
        base_query += " WHERE " + " AND ".join(conditions)

    cursor.execute(base_query, params)
    event_rows = cursor.fetchall()
    events_output = []

    for row in event_rows:

        cursor.execute("""
        SELECT
            Team.id,
            Team.name,
            Team.sport_id_foreignkey AS sport_id
        FROM EventTeam
        JOIN Team ON Team.id = EventTeam.team_id_foreignkey
        WHERE EventTeam.event_id_foreignkey = ?
        """, (row["event_id"],))

        team_rows = cursor.fetchall()
        team_list = [
            TeamResponse(
                id=team["id"],
                name=team["name"],
                sport_id=team["sport_id"]
            )
            for team in team_rows
        ]

        sport_obj = SportResponse(
            id=row["sport_id"],
            name=row["sport_name"]
        )

        venue_obj = VenueResponse(
            id=row["venue_id"],
            name=row["venue_name"],
            city=row["venue_city"],
            country=row["venue_country"]
        )

        event_obj = EventResponse(
            id=row["event_id"],
            start_datetime=row["start_datetime"],
            description=row["description"],
            sport=sport_obj,
            venue=venue_obj,
            teams=team_list
        )

        events_output.append(event_obj)

    return EventListResponse(events=events_output)


@router.get("/{event_id}", response_model=EventResponse)
def get_event(event_id: int, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("""
        SELECT
            Event.id AS event_id,
            Event.start_datetime,
            Event.description,

            Sport.id AS sport_id,
            Sport.name AS sport_name,

            Venue.id AS venue_id,
            Venue.name AS venue_name,
            Venue.city AS venue_city,
            Venue.country AS venue_country

        FROM Event
        LEFT JOIN Sport ON Sport.id = Event.sport_id_foreignkey
        LEFT JOIN Venue ON Venue.id = Event.venue_id_foreignkey
        WHERE Event.id = ?
    """, (event_id,))

    row = cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Event not found")

    cursor.execute("""
        SELECT
            Team.id,
            Team.name,
            Team.sport_id_foreignkey AS sport_id
        FROM EventTeam
        JOIN Team ON Team.id = EventTeam.team_id_foreignkey
        WHERE EventTeam.event_id_foreignkey = ?
    """, (event_id,))

    team_rows = cursor.fetchall()

    team_list = [
        TeamResponse(
            id=team["id"],
            name=team["name"],
            sport_id=team["sport_id"]
        )
        for team in team_rows
    ]

    sport_obj = SportResponse(
        id=row["sport_id"],
        name=row["sport_name"]
    )

    venue_obj = VenueResponse(
        id=row["venue_id"],
        name=row["venue_name"],
        city=row["venue_city"],
        country=row["venue_country"]
    )

    return EventResponse(
        id=row["event_id"],
        start_datetime=row["start_datetime"],
        description=row["description"],
        sport=sport_obj,
        venue=venue_obj,
        teams=team_list
    )
