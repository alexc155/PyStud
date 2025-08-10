import csv
import sqlite3

from utils.image import get_image


def __upsert(conn: sqlite3.Connection, cursor: sqlite3.Cursor, row: dict, add_to_existing: bool) -> None:
    sqlExisting = """
            SELECT COUNT(*) AS count
            FROM owned
            WHERE part = ?
                AND color = ?
                """

    cursor.execute(sqlExisting, (row["Part"], int(row["Color"])))
    columns = [column[0] for column in cursor.description]

    if [dict(zip(columns, row, strict=False)) for row in cursor.fetchall()][0]["count"] > 0:
        # update
        sql = f"""
            UPDATE owned
            SET quantity = {"quantity + ?" if add_to_existing else "?"}
            WHERE part = ?
                AND color = ?
            """
        cursor.execute(sql, (int(row["Quantity"]), row["Part"], int(row["Color"])))
    else:
        image = get_image(row["Part"], int(row["Color"]))

        sql = """
                INSERT INTO owned (
                    part,
                    color,
                    image,
                    quantity
                ) VALUES (?,?,?,?)
                """
        cursor.execute(sql, (row["Part"], int(row["Color"]), image, int(row["Quantity"])))

    conn.commit()


def insert_owned(conn: sqlite3.Connection, owned_file: str) -> bool:
    """Insert owned elements into the SQLite database."""
    cursor = conn.cursor()

    for row in csv.DictReader(owned_file.splitlines(), delimiter=","):
        __upsert(conn, cursor, row, True)
    return True


def get_owned(conn: sqlite3.Connection) -> list[dict]:
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT 
            id,
            part,
            color,
            concat('<img src="', image, '" style="height: 45px" />') AS image, 
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


def update_owned(conn: sqlite3.Connection, part: str, colour: int, owned: int | None) -> bool:
    cursor = conn.cursor()

    __upsert(conn, cursor, {"Part": part, "Color": colour, "Quantity": owned}, False)

    return True


def update_colour(conn: sqlite3.Connection, id: int, colour: int) -> bool:
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 
            id,
            part as Part,
            color as Color,
            quantity as Quantity
        FROM owned 
        WHERE id = ?
        """,
        (id,),
    )
    columns = [column[0] for column in cursor.description]
    row = [dict(zip(columns, row, strict=False)) for row in cursor.fetchall()]

    delete_owned(conn, id)

    row[0]["Color"] = colour

    __upsert(conn, cursor, row[0], True)

    return True


__all__ = ["insert_owned", "get_owned", "delete_owned", "update_owned", "update_colour"]
