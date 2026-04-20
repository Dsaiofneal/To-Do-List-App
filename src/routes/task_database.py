from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parents[1]
DB_PATH = BASE_DIR / 'todo.db'
SCHEMA_PATH = BASE_DIR / 'todo_schema.sql'
SQLITE_HEADER = b'SQLite format 3\x00'        

def get_connection() -> sqlite3.Connection: #this basically just means that the function is expected to return the sqlite3 connection
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    
    if not DB_PATH.exists():
         with sqlite3.connect(DB_PATH) as conn:
             schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
             conn.executescript(schema_sql)
             
             
def _get_or_create_default_user_id(conn: sqlite3.Connection) -> int:
    row = conn.execute("SELECT id FROM users LIMIT 1").fetchone()
    if row:
        return row["id"]

    cursor = conn.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
        ("default_user", "default@example.com", "changeme"),
    )
    return cursor.lastrowid
 
 
def add_task(title: str) -> dict:
    with get_connection() as conn:
        user_id = _get_or_create_default_user_id(conn)

        cursor = conn.execute(
            "INSERT INTO tasks (user_id, title, status) VALUES (?, ?, ?)",
            (user_id, title.strip(), "pending"),
        )
        task_id = cursor.lastrowid

        row = conn.execute(
            "SELECT id, title, status, created_at FROM tasks WHERE id = ?",
            (task_id,),
        ).fetchone()

    return {
        "id": row["id"],
        "title": row["title"],
        "completed": row["status"] == "completed",  # keeps your API shape
        "created_at": row["created_at"],
    }

def list_tasks() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, status, created_at FROM tasks ORDER BY id DESC"
        ).fetchall()

    return [
        {
            "id": row["id"],
            "title": row["title"],
            "completed": row["status"] == "completed",
            "created_at": row["created_at"],
        }
        for row in rows
    ]