import os
import sqlite3
import logging
from typing import Generator

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "timetable.db")


def get_db() -> Generator[sqlite3.Connection, None, None]:
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        conn.row_factory = sqlite3.Row
        yield conn


def init_db():
    with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
        with conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS departures (
                    Id INTEGER PRIMARY KEY AUTOINCREMENT,
                    TrainNumber TEXT NOT NULL,
                    Origin TEXT NOT NULL,
                    Destination TEXT NOT NULL,
                    DepartureTime TEXT NOT NULL,
                    ArrivalTime TEXT NOT NULL,
                    Platform INTEGER,
                    Status TEXT NOT NULL DEFAULT 'On time',
                    DelayMinutes INTEGER
                )
            """)

            cursor.execute("SELECT COUNT(*) FROM departures")
            if cursor.fetchone()[0] == 0:
                sample_departures = [
                    ("IC 342", "Copenhagen", "Aarhus", "2026-04-14T08:15:00", "2026-04-14T11:20:00", 3, "On time", None),
                    ("RE 1720", "Odense", "Copenhagen", "2026-04-14T09:00:00", "2026-04-14T10:32:00", 7, "Delayed", 12),
                    ("IC 855", "Aarhus", "Aalborg", "2026-04-14T10:45:00", "2026-04-14T12:10:00", 1, "On time", None),
                    ("RE 4410", "Copenhagen", "Odense", "2026-04-14T12:30:00", "2026-04-14T14:05:00", 5, "Cancelled", None),
                    ("IC 190", "Aalborg", "Copenhagen", "2026-04-14T14:00:00", "2026-04-14T18:30:00", 2, "Delayed", 5),
                ]
                cursor.executemany(
                    "INSERT INTO departures (TrainNumber, Origin, Destination, DepartureTime, ArrivalTime, Platform, Status, DelayMinutes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                    sample_departures,
                )
                logging.info("Seeded %d sample departures.", len(sample_departures))
