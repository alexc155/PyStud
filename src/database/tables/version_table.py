import sqlite3


def insert_version(conn: sqlite3.Connection) -> int | None:
    """Insert test data into the SQLite database."""
    cursor = conn.cursor()
    sql = "INSERT INTO version (name) VALUES (?)"
    cursor.execute(sql, ("1.0.0",))
    conn.commit()
    print("Test data inserted successfully.")
    return cursor.lastrowid


def get_version(conn: sqlite3.Connection) -> dict:
    """Retrieve the version from the SQLite database."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM version ORDER BY id DESC LIMIT 1")
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "name": row[1]}
    else:
        return {"id": None, "name": None}


def truncate_version(conn: sqlite3.Connection) -> None:
    """Delete all entries from the version table."""
    cursor = conn.cursor()
    cursor.execute("DELETE FROM version")
    conn.commit()
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='version';")
    conn.commit()

    print("All entries in the version table deleted successfully.")


__all__ = [
    "insert_version",
    "get_version",
    "truncate_version",
]
