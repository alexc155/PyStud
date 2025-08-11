import csv
import io
import sqlite3
import time

from nicegui import app

from utils.image import get_image


def insert_project_item(conn: sqlite3.Connection, project_id: int, row: dict, internet: bool, retries: int = 10) -> bool:
    """Insert project data into the SQLite database."""

    cursor = conn.cursor()

    try:
        image = get_image(row["BLItemNo"], int(row["LDrawColorId"]), internet)

        sql = """INSERT OR IGNORE INTO project_item (
            project_id,
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
            weight) 
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
        """
        cursor.execute(
            sql,
            (
                project_id,
                row["BLItemNo"],
                row["ElementId"],
                row["LdrawId"],
                row["PartName"],
                row["BLColorId"],
                row["LDrawColorId"],
                row["ColorName"],
                row["ColorCategory"],
                image,
                int(row["Qty"]) if row["Qty"] is not None and int(row["Qty"]) != 0 else None,
                row["Weight"],
            ),
        )
        conn.commit()

        cursor.execute(
            """UPDATE project 
                SET item_count = (SELECT COUNT(*) FROM project_item WHERE project_id = ?)
                WHERE id = ?
            """,
            (
                project_id,
                project_id,
            ),
        )

    except Exception as err:
        if retries > 0:
            time.sleep(1)
            return insert_project_item(conn, project_id, row, internet, retries - 1)
        else:
            print(f"Failed to insert a project item! ({err})", row)
            raise err

    return True


def update_broken_image(conn: sqlite3.Connection, project_item: dict) -> None:
    if project_item["image"] != "":
        return
    else:
        image = get_image(project_item["bl_item_no"], int(project_item["ldraw_color_id"]), True)
        cursor = conn.cursor()
        cursor.execute(
            """UPDATE
                project_item
            SET
                image = ?
            WHERE id = ?
            """,
            (image, project_item["id"]),
        )

        project_item["image"] = image


def get_project_items(conn: sqlite3.Connection, project_id: int) -> list[dict]:
    """Get project_item data."""
    cursor = conn.cursor()
    cursor.execute(
        """SELECT 
            project_item.id, 
            project_item.color_name,
            project_item.bl_item_no,
            project_item.ldraw_color_id,
            project_item.bl_color_id,
            project_item.part_name, 
            project_item.image, 
            project_item.qty, 
            owned.quantity AS owned 
        FROM project_item 
        LEFT JOIN owned ON project_item.bl_item_no = owned.part AND project_item.ldraw_color_id = owned.color
        WHERE project_item.project_id = ?
        ORDER BY project_item.ldraw_color_id, project_item.part_name
        """,
        (project_id,),
    )
    columns = [column[0] for column in cursor.description]
    project_items = [dict(zip(columns, row, strict=False)) for row in cursor.fetchall()]

    if app.storage.general["internet"]:
        for project_item in project_items:
            update_broken_image(conn, project_item)

    return project_items


def update_project_item_qty(conn: sqlite3.Connection, id: int, qty: int | None) -> bool:
    """Update a project item."""
    cursor = conn.cursor()
    sql = """UPDATE project_item SET        
        qty = ?
    WHERE id = ?
    """

    cursor.execute(
        sql,
        (
            qty if qty is not None and qty > 0 else None,
            id,
        ),
    )
    conn.commit()
    return cursor.rowcount > 0


def get_to_buy(conn: sqlite3.Connection, project_id: int) -> str:
    cursor = conn.cursor()
    cursor.execute(
        """SELECT 
            project_item.bl_item_no AS BLItemNo,
            project_item.element_id AS ElementId,
            project_item.ldraw_id AS LdrawId,
            project_item.part_name AS PartName, 
            project_item.bl_color_id AS BLColorId,
            project_item.ldraw_color_id AS LDrawColorId,
            project_item.color_name AS ColorName,
            project_item.color_category AS ColorCategory,
            project_item.qty - IFNULL(owned.quantity, 0) AS Qty,
            project_item.weight AS Weight
        FROM project_item 
        LEFT JOIN owned ON project_item.bl_item_no = owned.part AND project_item.ldraw_color_id = owned.color
        WHERE project_item.project_id = ?
            AND project_item.qty - IFNULL(owned.quantity, 0) > 0
        """,
        (project_id,),
    )
    columns = [column[0] for column in cursor.description]
    data = [dict(zip(columns, row, strict=False)) for row in cursor.fetchall()]

    csv_response = io.StringIO()
    writer = csv.DictWriter(csv_response, fieldnames=columns)
    writer.writeheader()
    writer.writerows(data)
    return csv_response.getvalue()


__all__ = ["insert_project_item", "get_project_items", "update_project_item_qty"]
