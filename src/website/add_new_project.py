import sqlite3

from nicegui import events, ui

from database.tables import project_table


def __add_project(db: sqlite3.Connection, project_name: str, project_file: str, tabs: ui.tabs):
    project_table.insert_project(db, project_name, project_file)
    tabs.value = "All Projects"


def import_project(db: sqlite3.Connection, tabs: ui.tabs):
    ui.label("Import Project")
    project_name = ui.input(label="Project Name", placeholder="Enter project name")

    project_file = ui.textarea()

    project_file.set_visibility(False)

    def __handle_upload(e: events.UploadEventArguments):
        text = e.content.read().decode("utf-8")
        project_file.value = text

    ui.upload(on_upload=__handle_upload).props("accept=.csv").classes("max-w-full")

    ui.button(
        "Add Project",
        on_click=lambda: __add_project(db, project_name.value, project_file.value, tabs),
    ).props("primary")


__all__ = ["import_project"]
