import sqlite3

conn = sqlite3.connect('season.sqlite')
cur = conn.cursor()

cur.executescript('''
DROP TABLE IF EXISTS Team;
DROP TABLE IF EXISTS Season;
DROP TABLE IF EXISTS Round;
DROP TABLE IF EXISTS Match;
CREATE TABLE Team (
    id  INTEGER NOT NULL PRIMARY KEY UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Season (
    id  INTEGER NOT NULL PRIMARY KEY UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Round (
    id  INTEGER NOT NULL PRIMARY KEY UNIQUE,
    name    TEXT UNIQUE
);
CREATE TABLE Match (
    season_id  INTEGER,
    round_id INTEGER,
    home_team_id  INTEGER,
    guest_team_id INTEGER,
    result TEXT,
    date TEXT
);
''')
