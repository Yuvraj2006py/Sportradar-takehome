from pydantic import BaseModel
from typing import List

class SportResponse(BaseModel):
    id: int
    name: str
    
class VenueResponse(BaseModel):
    id: int
    name: str
    city: str
    country: str
    
class TeamResponse(BaseModel):
    id: int
    name: str
    sport_id: int
    
class EventResponse(BaseModel):
    id: int
    start_datetime: str
    description: str
    sport: SportResponse
    venue: VenueResponse
    teams: List[TeamResponse]

class EventListResponse(BaseModel):
    events: List[EventResponse]

class SportListResponse(BaseModel):
    sports: List[SportResponse]

class TeamListResponse(BaseModel):
    teams: List[TeamResponse]

class VenueListResponse(BaseModel):
    venues: List[VenueResponse]
