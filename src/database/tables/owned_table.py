import csv
import sqlite3

from utils.bl_image import get_image


def insert_owned(conn: sqlite3.Connection, owned_file: str) -> bool:
    """Insert owned elements into the SQLite database."""
    cursor = conn.cursor()

    for row in csv.DictReader(owned_file.splitlines(), delimiter=","):
        sqlExisting = """
            SELECT COUNT(*)
            FROM owned
            WHERE part = ?
                AND color = ?"""

        existingPart = cursor.execute(sqlExisting, (row["Part"], row["Color"]))

        if len(existingPart.fetchall()) > 0:
            # update
            sql = """
                UPDATE owned
                SET quantity = quantity + ?
                WHERE part = ?
                    AND color = ?"""
            cursor.execute(sql, (row["Quantity"], row["Part"], row["Color"]))
        else:
            image = get_image(row["Part"], row["Color"])

            sql = """
                INSERT INTO owned (
                    part,
                    color,
                    image,
                    quantity
                ) VALUES (?,?,?,?)
                """
            cursor.execute(sql, (row["Part"], row["Color"], image, row["Quantity"]))

        conn.commit()
    return True


def get_owned(conn: sqlite3.Connection) -> list[dict]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            id,
            part,
            color,
            concat('<img src="data:image/png;base64, ', image, '" style="height: 45px" />') AS image, 
            quantity
        FROM owned 
        ORDER BY color, part
        """,
    )
    columns = [column[0] for column in cursor.description]
    return [dict(zip(columns, row, strict=False)) for row in cursor.fetchall()]


def delete_owned(conn: sqlite3.Connection, id: int) -> bool:
    cursor = conn.cursor()
    cursor.execute(
        """
        DELETE
        FROM owned
        WHERE id = ?
        """,
        (id,),
    )

    conn.commit()
    return True


def update_owned(conn: sqlite3.Connection, id: int, owned: int | None) -> bool:
    cursor = conn.cursor()
    sql = """
    UPDATE owned SET        
        quantity = ?
        WHERE id = ?
    """

    cursor.execute(
        sql,
        (
            owned if owned is not None and int(owned) > 0 else None,
            id,
        ),
    )
    conn.commit()
    return cursor.rowcount > 0


__all__ = ["insert_owned", "get_owned", "delete_owned", "update_owned"]
