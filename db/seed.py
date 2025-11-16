import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "sports_events.db"

conn = sqlite3.connect(DB_PATH)
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()

cursor.execute("DELETE FROM EventTeam")
cursor.execute("DELETE FROM Event")
cursor.execute("DELETE FROM Team")
cursor.execute("DELETE FROM Venue")
cursor.execute("DELETE FROM Sport")
conn.commit()

sports = [
    ("Football",),
    ("Basketball",),
    ("Hockey",)
]

cursor.executemany("INSERT INTO Sport (name) VALUES (?)", sports)
conn.commit()

cursor.execute("SELECT * FROM Sport")
sports_rows = cursor.fetchall()
sports_map = {row[1]: row[0] for row in sports_rows}

venues = [
    ("Scotiabank Arena", "Toronto", "Canada"),
    ("Madison Square Garden", "New York", "USA"),
    ("Rogers Centre", "Toronto", "Canada")
]

cursor.executemany(
    "INSERT INTO Venue (name, city, country) VALUES (?, ?, ?)", venues
)
conn.commit()

cursor.execute("SELECT * FROM Venue")
venue_rows = cursor.fetchall()
venue_map = {row[1]: row[0] for row in venue_rows}

teams = [
    ("Toronto Argonauts", sports_map["Football"]),
    ("BC Lions", sports_map["Football"]),
    ("Toronto Raptors", sports_map["Basketball"]),
    ("Chicago Bulls", sports_map["Basketball"]),
    ("Toronto Maple Leafs", sports_map["Hockey"]),
    ("Montreal Canadiens", sports_map["Hockey"])
]

cursor.executemany(
    "INSERT INTO Team (name, sport_id_foreignkey) VALUES (?, ?)", teams
)
conn.commit()

cursor.execute("SELECT * FROM Team")
team_rows = cursor.fetchall()
team_map = {row[1]: row[0] for row in team_rows}

events = [
    (sports_map["Basketball"], venue_map["Scotiabank Arena"],
     "2025-01-10 19:00", "Toronto Raptors vs Chicago Bulls"),

    (sports_map["Hockey"], venue_map["Madison Square Garden"],
     "2025-02-22 20:00", "Maple Leafs vs Canadiens"),

    (sports_map["Football"], venue_map["Rogers Centre"],
     "2025-03-05 18:00", "Argonauts vs Lions")
]

cursor.executemany("""
    INSERT INTO Event (sport_id_foreignkey, venue_id_foreignkey, start_datetime, description)
    VALUES (?, ?, ?, ?)
""", events)
conn.commit()

cursor.execute("SELECT * FROM Event")
event_rows = cursor.fetchall()
event_map = {row[4]: row[0] for row in event_rows}

event_teams = [
    (event_map["Toronto Raptors vs Chicago Bulls"], team_map["Toronto Raptors"]),
    (event_map["Toronto Raptors vs Chicago Bulls"], team_map["Chicago Bulls"]),

    (event_map["Maple Leafs vs Canadiens"], team_map["Toronto Maple Leafs"]),
    (event_map["Maple Leafs vs Canadiens"], team_map["Montreal Canadiens"]),

    (event_map["Argonauts vs Lions"], team_map["Toronto Argonauts"]),
    (event_map["Argonauts vs Lions"], team_map["BC Lions"])
]

cursor.executemany("""
    INSERT INTO EventTeam (event_id_foreignkey, team_id_foreignkey)
    VALUES (?, ?)
""", event_teams)
conn.commit()

conn.close()

print("Database seeded successfully!")
