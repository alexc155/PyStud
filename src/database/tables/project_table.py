import csv
import sqlite3

from utils.image import get_image


def insert_project(conn: sqlite3.Connection, name: str, project_file: str) -> bool:
    """Insert project data into the SQLite database."""
    cursor = conn.cursor()

    for row in csv.DictReader(project_file.splitlines(), delimiter=","):
        image = get_image(row["BLItemNo"], row["LDrawColorId"])

        sql = """
        INSERT INTO project (
            name,
            bl_item_no,
            element_id,
            ldraw_id,
            part_name,
            bl_color_id,
            ldraw_color_id,
            color_name,
            color_category,
            image,
            qty,
            weight) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """
        cursor.execute(
            sql,
            (
                name,
                row["BLItemNo"],
                row["ElementId"],
                row["LdrawId"],
                row["PartName"],
                row["BLColorId"],
                row["LDrawColorId"],
                row["ColorName"],
                row["ColorCategory"],
                image,
                row["Qty"] if row["Qty"] is not None and row["Qty"] != 0 else None,
                row["Weight"],
            ),
        )
        conn.commit()

    print("Imported")
    return True


def get_projects(conn: sqlite3.Connection) -> list[str]:
    """Get all project names from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT name FROM project")
    return cursor.fetchall()


def get_project_items(conn: sqlite3.Connection, name: str) -> list[dict]:
    """Get project data by name."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            project.id, 
            project.color_name,
            project.bl_item_no,
            project.ldraw_color_id,
            project.bl_color_id,
            project.part_name, 
            project.image, 
            concat('<img src="', project.image, '" style="height: 45px" />') AS image_sm, 
            concat('<img src="', project.image, '" style="height: 80px" />') AS image_mid, 
            project.qty, 
            owned.quantity AS owned 
        FROM project 
        LEFT JOIN owned ON project.bl_item_no = owned.part AND project.ldraw_color_id = owned.color
        WHERE project.name = ?
        ORDER BY project.ldraw_color_id, project.part_name
        """,
        (name,),
    )
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row, strict=False)) for row in cursor.fetchall()]


def delete_project(conn: sqlite3.Connection, name: str) -> bool:
    """Delete a project by name."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM project WHERE name = ?", (name,))
    conn.commit()
    return cursor.rowcount > 0


def update_project_item_qty(conn: sqlite3.Connection, id: int, qty: int | None) -> bool:
    """Update a project item."""
    cursor = conn.cursor()
    sql = """
    UPDATE project SET        
        qty = ?
        WHERE id = ?
    """

    cursor.execute(
        sql,
        (
            qty if qty is not None and int(qty) > 0 else None,
            id,
        ),
    )
    conn.commit()
    return cursor.rowcount > 0


__all__ = [
    "insert_project",
    "get_projects",
    "get_project_items",
    "delete_project",
    "update_project_item_qty",
]
