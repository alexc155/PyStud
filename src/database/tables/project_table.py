import asyncio
import csv
import sqlite3
from types import CoroutineType

from database.tables.project_item_table import insert_project_item


async def __insert_project_items(conn: sqlite3.Connection, project_items: list[str], cursor, project_id: int) -> None:
    threads: list[CoroutineType] = list()

    for row in csv.DictReader(project_items, delimiter=","):
        thread = asyncio.to_thread(lambda row=row: insert_project_item(conn, project_id, row))

        threads.append(thread)

    await asyncio.gather(*threads)

    cursor.execute(
        """UPDATE project 
        SET status = ''
        WHERE id = ?
        """,
        (project_id,),
    )

    print("Imported")


async def insert_project(conn: sqlite3.Connection, name: str, project_file: str) -> bool:
    """Insert project data into the SQLite database."""
    project_items = project_file.splitlines()

    cursor = conn.cursor()

    cursor.execute(
        """INSERT INTO project (
            name,
            status,
            item_count,
            total_count
        )
        VALUES (?,?,?,?)
        """,
        (name, "Importing", 0, len(project_items)),
    )

    project_id = cursor.lastrowid

    if project_id is None:
        raise ImportError()

    await __insert_project_items(conn, project_items, cursor, project_id)
    return True


def get_projects(conn: sqlite3.Connection) -> list[dict]:
    """Get all project names from the database."""
    cursor = conn.cursor()
    cursor.execute("""SELECT 
                    id, 
                    CASE status WHEN '' THEN name ELSE CONCAT(name, ' - ', status, ' ', item_count, ' of ', total_count) END AS name, 
                    status, 
                    item_count, 
                    total_count 
                   FROM project""")
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
