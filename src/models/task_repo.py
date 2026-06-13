from database.connection import get_connection, get_or_create_default_user_id


def add_task(
    title: str,
    description: str = None,
    priority: str = "medium",
    category_id: int = None,
) -> dict:
    with get_connection() as conn:
        user_id = get_or_create_default_user_id(conn)
        cursor = conn.execute(
            "INSERT INTO tasks (user_id, title, description, priority, category_id, status) VALUES (?, ?, ?, ?, ?, ?)",
            (user_id, title.strip(), description, priority, category_id, "pending"),
        )
        task_id = cursor.lastrowid
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return dict(row)


def list_tasks() -> list[dict]:
    with get_connection() as conn:
        rows = conn.execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return [dict(row) for row in rows]


def get_task(task_id: int) -> dict:
    with get_connection() as conn:
        row = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    return dict(row) if row else None


def update_task(
    task_id: int, title: str, description: str, status: str, priority: str
) -> bool:
    with get_connection() as conn:
        conn.execute(
            """UPDATE tasks
               SET title = ?, description = ?, status = ?, priority = ?, updated_at = datetime('now')
               WHERE id = ?""",
            (title, description, status, priority, task_id),
        )
    return True


def delete_task(task_id: int) -> bool:
    with get_connection() as conn:
        conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    return True
