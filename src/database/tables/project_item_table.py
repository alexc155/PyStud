import sqlite3

from utils.image import get_image


def insert_project_item(conn: sqlite3.Connection, project_id: int, row: dict) -> bool:
    """Insert project data into the SQLite database."""
    cursor = conn.cursor()

    image = get_image(row["BLItemNo"], row["LDrawColorId"])

    sql = """
    INSERT INTO project_item (
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
        weight) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)
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
            row["Qty"] if row["Qty"] is not None and row["Qty"] != 0 else None,
            row["Weight"],
        ),
    )
    conn.commit()

    print("Added Item")
    return True


def get_project_items(conn: sqlite3.Connection, project_id: int) -> list[dict]:
    """Get project_item data."""
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            project_item.id, 
            project_item.color_name,
            project_item.bl_item_no,
            project_item.ldraw_color_id,
            project_item.bl_color_id,
            project_item.part_name, 
            project_item.image, 
            concat('<img src="', project_item.image, '" style="height: 45px" />') AS image_sm, 
            concat('<img src="', project_item.image, '" style="height: 80px" />') AS image_mid, 
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
    return [dict(zip(columns, row, strict=False)) for row in cursor.fetchall()]


def update_project_item_qty(conn: sqlite3.Connection, id: int, qty: int | None) -> bool:
    """Update a project item."""
    cursor = conn.cursor()
    sql = """
    UPDATE project_item SET        
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


__all__ = ["insert_project_item", "get_project_items", "update_project_item_qty"]
