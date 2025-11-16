from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.routers import events, sports, teams, venues

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI()
app.include_router(events.router)
app.include_router(sports.router)
app.include_router(teams.router)
app.include_router(venues.router)

if FRONTEND_DIR.exists():
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")


@app.get("/")
def home():
    if not FRONTEND_DIR.exists():
        return {"message": "Frontend not found"}
    return FileResponse(FRONTEND_DIR / "index.html")
