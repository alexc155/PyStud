import sqlite3

from nicegui import events, ui

from database.tables import owned_table


def __add_owned(db: sqlite3.Connection, owned_file: str, tabs: ui.tabs):
    owned_table.insert_owned(db, owned_file)
    tabs.value = "Owned"


def import_owned(db: sqlite3.Connection, tabs: ui.tabs):
    ui.label("Import Owned List")
    owned_file = ui.textarea()

    owned_file.set_visibility(False)

    def __handle_upload(e: events.UploadEventArguments):
        text = e.content.read().decode("utf-8")
        owned_file.value = text

    ui.upload(on_upload=__handle_upload).props("accept=.csv").classes("max-w-full")

    ui.button(
        "Add owned list",
        on_click=lambda: __add_owned(db, owned_file.value, tabs),
    ).props("primary")


__all__ = ["import_owned"]
