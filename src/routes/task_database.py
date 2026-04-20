from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / 'todo.db'
SQLITE_HEADER = b'SQLite format 3\x00'

# I want to write a function that will back up the file and check to see if its SQL
# will write after main function is done

def get_connection() -> sqlite3.Connection: #this basically just means that the function is expected to return the sqlite3 connection
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:

    
    with get_connection() as conn:
        conn.execute( #made this with AI because I don't understand SQL
            '''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                completed INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            '''
        )
        
def add_task(title: str) -> dict:
    with get_connection() as conn:
        cursor = conn.execute(
            'INSERT INTO tasks (title, completed) VALUES (?, 0)',
            (title,)
        )
        task_id = cursor.lastrowid
        
        row = conn.execute(
            'SELECT id, title, completed, created_at FROM tasks WHERE id = ?',
            (task_id)
        ).fetchone()
        
    return {
        'id': row['id'],
        'title': row['title'],
        'completed': bool(row['completed']), #makes it a boolean
        'created_at': row['created_at'],
    }

def list_tasks() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute(
            'SELECT id, title, completed, created_at FROM tasks ORDER BY id DESC'
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