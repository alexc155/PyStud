import sqlite3


def connect() -> sqlite3.Connection:
    try:
        conn = sqlite3.connect("PyStud.db", check_same_thread=False)
        print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")

        return conn

    except sqlite3.OperationalError as e:
        print("Failed to open database:", e)
        raise e


def close(conn: sqlite3.Connection) -> None:
    """Close the SQLite database connection."""
    try:
        conn.close()
        print("SQLite database connection closed.")
    except sqlite3.OperationalError as e:
        print("Failed to close database:", e)


def create_tables(conn: sqlite3.Connection) -> None:
    """Create necessary tables in the SQLite database."""
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS project (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name,
            status,
            item_count INTEGER,
            total_count INTEGER,
            UNIQUE(name)
        )
        """
    )
    conn.commit()
    
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS project_item (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            bl_item_no,
            element_id,
            ldraw_id,
            part_name,
            bl_color_id INTEGER,
            ldraw_color_id INTEGER,
            color_name,
            color_category,
            image,
            qty INTEGER,
            weight,
            UNIQUE(project_id, bl_item_no, element_id, bl_color_id)
        )
        """
    )
    conn.commit()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS owned (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            part,
            color INTEGER,
            image,
            quantity INTEGER,
            UNIQUE(part, color)
        )
        """
    )
    conn.commit()

    print("Tables created successfully.")


__all__ = [
    "connect",
    "close",
    "create_tables",
]
