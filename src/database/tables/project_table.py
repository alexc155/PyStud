import csv
import sqlite3

from database.tables.project_item_table import insert_project_item


def insert_project(conn: sqlite3.Connection, name: str, project_file: str) -> bool:
    """Insert project data into the SQLite database."""
    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO project (
            name,
            status
        )
        VALUES (?,?)
        """,
        (name, "Importing..."),
    )

    project_id = cursor.lastrowid

    if project_id is None:
        raise ImportError()

    for row in csv.DictReader(project_file.splitlines(), delimiter=","):
        insert_project_item(conn, project_id, row)

    print("Imported")
    return True


def get_projects(conn: sqlite3.Connection) -> list[dict]:
    """Get all project names from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM project")
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row, strict=False)) for row in cursor.fetchall()]


def delete_project(conn: sqlite3.Connection, id: int) -> bool:
    """Delete a project by name."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM project_item WHERE project_id = ?", (id,))
    conn.commit()
    cursor.execute("DELETE FROM project WHERE id = ?", (id,))
    conn.commit()
    return cursor.rowcount > 0


__all__ = [
    "insert_project",
    "get_projects",
    "delete_project",
]
