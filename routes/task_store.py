from pathlib import Path
import sqlite3
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / "appdata.db"
SQLITE_HEADER = b"SQLite format 3\x00"


def _backup_if_not_sqlite_file() -> None:
    if not DB_PATH.exists():
        return

    if DB_PATH.stat().st_size == 0:
        return

    with DB_PATH.open("rb") as db_file:
        header = db_file.read(16)

    if header == SQLITE_HEADER:
        return

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = DB_PATH.with_name(f"{DB_PATH.stem}.invalid_{timestamp}{DB_PATH.suffix}")
    DB_PATH.replace(backup_path)


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    _backup_if_not_sqlite_file()

    with get_connection() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )


def add_task(title: str) -> dict:
    with get_connection() as conn:
        cursor = conn.execute(
            "INSERT INTO tasks (title, completed) VALUES (?, 0)",
            (title,)
        )
        task_id = cursor.lastrowid

        row = conn.execute(
            "SELECT id, title, completed, created_at FROM tasks WHERE id = ?",
            (task_id,)
        ).fetchone()

    return {
        "id": row["id"],
        "title": row["title"],
        "completed": bool(row["completed"]),
        "created_at": row["created_at"],
    }


def list_tasks() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, completed, created_at FROM tasks ORDER BY id DESC"
        ).fetchall()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "completed": bool(row["completed"]),
            "created_at": row["created_at"],
        }
        for row in rows
    ]
