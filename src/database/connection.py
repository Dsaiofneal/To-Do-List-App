import sqlite3

from config import DB_PATH, SCHEMA_PATH


def get_connection() -> sqlite3.Connection:
    """Returns a connection to the SQLite database with Row factory enabled."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    """Initializes the database using the schema file if the database doesn't exist."""
    if not DB_PATH.exists():
        with sqlite3.connect(DB_PATH) as conn:
            schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
            conn.executescript(schema_sql)


def get_or_create_default_user_id(conn: sqlite3.Connection) -> int:
    """Helper to ensure at least one user exists in the database."""
    row = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
    if row:
        return row["id"]

    cursor = conn.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        ("default_user", "default@example.com", "changeme"),
    )
    return cursor.lastrowid
