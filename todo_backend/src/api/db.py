"""
db.py - SQLite database handler for the Todo backend

Handles connection and CRUD operations abstracted for Todo items.
"""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "todo.db"

def initialize_db():
    """Ensure the tasks table exists, creating it if necessary."""
    with sqlite3.connect(DB_PATH) as conn:
        c = conn.cursor()
        c.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER DEFAULT 0
            );
        """)
        conn.commit()

@contextmanager
def get_connection():
    """Context manager for a SQLite DB connection."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()
