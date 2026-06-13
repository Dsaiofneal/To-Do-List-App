from pathlib import Path

# Base directory of the project (the 'src' folder)
BASE_DIR = Path(__file__).resolve().parent

# Database configuration
DB_PATH = BASE_DIR / "todo.db"
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"
