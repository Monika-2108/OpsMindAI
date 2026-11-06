
import sqlite3
from pathlib import Path

DB_PATH = Path("data/opsmind.db")


def get_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS incidents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                severity TEXT DEFAULT 'Medium',
                suggested_solution TEXT,
                actual_solution TEXT,
                outcome TEXT DEFAULT 'Pending',
                root_cause TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()


def save_incident(title, description, severity="Medium"):
    with get_connection() as conn:
        cursor = conn.execute("""
            INSERT INTO incidents (title, description, severity)
            VALUES (?, ?, ?)
        """, (title, description, severity))
        conn.commit()
        return cursor.lastrowid


def save_suggestion(incident_id, suggestion):
    with get_connection() as conn:
        conn.execute("""
            UPDATE incidents
            SET suggested_solution = ?
            WHERE id = ?
        """, (suggestion, incident_id))
        conn.commit()


def update_incident(
    incident_id,
    actual_solution,
    outcome,
    root_cause
):
    with get_connection() as conn:
        conn.execute("""
            UPDATE incidents
            SET actual_solution = ?,
                outcome = ?,
                root_cause = ?
            WHERE id = ?
        """, (
            actual_solution,
            outcome,
            root_cause,
            incident_id
        ))
        conn.commit()


def get_all_incidents():
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM incidents ORDER BY id DESC"
        ).fetchall()


def get_incident(incident_id):
    with get_connection() as conn:
        return conn.execute(
            "SELECT * FROM incidents WHERE id = ?",
            (incident_id,)
        ).fetchone()


def get_incident_count():
    with get_connection() as conn:
        result = conn.execute(
            "SELECT COUNT(*) FROM incidents"
        ).fetchone()
        return result[0]


def get_resolved_count():
    with get_connection() as conn:
        result = conn.execute("""
            SELECT COUNT(*) FROM incidents
            WHERE outcome = 'Resolved'
        """).fetchone()
        return result[0]
