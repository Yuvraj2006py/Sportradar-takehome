import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sports_events.db"
SCHEMA_PATH = BASE_DIR / "schema.sql"


def initialize_db():
    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(f"Schema file missing: {SCHEMA_PATH}")

    with sqlite3.connect(DB_PATH) as conn:
        conn.executescript(SCHEMA_PATH.read_text())
        conn.commit()

    print(f"Database initialized at {DB_PATH}")


if __name__ == "__main__":
    initialize_db()
