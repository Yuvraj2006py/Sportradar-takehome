CREATE TABLE Sport(
    id integer PRIMARY KEY,
    name TEXT
);
CREATE TABLE Venue(
    id integer PRIMARY KEY,
    name TEXT,
    city TEXT,
    country TEXT
);
CREATE TABLE Team(
    id integer PRIMARY KEY,
    name TEXT,
    sport_id_foreignkey integer,
    FOREIGN KEY(sport_id_foreignkey) REFERENCES Sport(id)
);
CREATE TABLE Event(
    id integer PRIMARY KEY,
    sport_id_foreignkey integer,
    venue_id_foreignkey integer,
    start_datetime TEXT,
    description TEXT,
    FOREIGN KEY(sport_id_foreignkey) REFERENCES Sport(id),
    FOREIGN KEY(venue_id_foreignkey) REFERENCES Venue(id)
);
CREATE TABLE EventTeam(
    id integer PRIMARY KEY,
    event_id_foreignkey integer,
    team_id_foreignkey integer,
    FOREIGN KEY(event_id_foreignkey) REFERENCES Event(id),
    FOREIGN KEY(team_id_foreignkey) REFERENCES Team(id)
);


