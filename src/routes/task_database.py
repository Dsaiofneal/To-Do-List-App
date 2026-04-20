from pathlib import Path
import sqlite3

BASE_DIR = Path(__file__).resolve().parents
DB_PATH = BASE_DIR / 'src' / 'todo.db'
SQLITE_HEADER = b'SQLite format 3\x00'

# I want to write a function that will back up the file and check to see if its SQL
# will write after main function is done

def get_connection() -> sqlite3.Connection: #this basically just means that the function is expected to return the sqlite3 connection
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:

    
    with get_connection() as conn:
        conn.execute(
            'INSERT INTO tasks (title, completed) VALUES (?, ?)',
            (title, 0)
        )