# Sports Events Dashboard

A FastAPI backend plus a static HTML/CSS/JS frontend that lets you explore sports events, filter by sport/date/search, and see venue and team details. This project complements the Sportradar coding exercise materials in this folder.

## Project Structure

```
app/            # FastAPI application (routers, models, DB access)
frontend/       # Static assets served at /static and / (HTML/CSS/JS)
db/             # SQLite schema and seeding scripts
requirements.txt
```

## Prerequisites

- Python 3.11+ (Python 3.13 tested)
- pip

## Setup and Run

```bash
python -m pip install -r requirements.txt
python db/init_db.py      # create tables from schema.sql
python db/seed.py         # load sample sports, teams, venues, events
python -m uvicorn app.main:app --reload
```

Visit `http://127.0.0.1:8000/` to load the frontend. The app will call `/sports` and `/events` automatically to populate filters and event cards.

## Useful Endpoints

- `GET /sports/` – list all sports
- `GET /events/` – list events (supports `sport_id`, `date`, `search` query params)
- `GET /events/{id}` – detailed event info
- `GET /teams/` / `GET /venues/` – supporting data

## Troubleshooting

- **sqlite3.OperationalError (no such table)** – run `python db/init_db.py` then `python db/seed.py`.
- **sqlite3.ProgrammingError (thread usage)** – already fixed by opening connections with `check_same_thread=False`. Make sure you pulled latest `app/database.py`.
- **Command not found (`uvicorn`)** – run via `python -m uvicorn ...` or add the user Scripts directory to PATH.
- **Frontend 404** – confirm `frontend/` exists and `uvicorn` is started from the project root so FastAPI mounts `/static` correctly.

## Customizing the Frontend

The UI lives entirely under `frontend/`:
- `index.html` – layout and filter controls
- `styles.css` – modern card styling
- `app.js` – fetches data, handles filters, renders cards

Adjust these files as needed; FastAPI serves them automatically at `/` and `/static/*`.
