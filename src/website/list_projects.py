import sqlite3

from nicegui import app, ui

from database.tables.project_table import delete_project, get_projects
from website.edit_project_list import edit_project_list


def list_projects(db: sqlite3.Connection, tabs: ui.tabs):
    def __select_project(db: sqlite3.Connection, project: dict, tabs: ui.tabs):
        app.storage.general["project"] = {"id": project["id"], "name": project["name"]}
        edit_project_list.refresh(db, project["id"], project["name"])
        tabs.value = "Project List"

    def __delete(db: sqlite3.Connection, project: dict) -> None:
        delete_project(db, int(project["id"]))
        ui.notify(f"Deleted project {project['name']}")
        __refresh_projects.refresh()

    @ui.refreshable
    def __refresh_projects(db: sqlite3.Connection, tabs: ui.tabs):
        """Refresh the list of projects."""

        if tabs.value != "All Projects":
            return

        __projects = get_projects(db)

        project_list.clear()

        with project_list:
            for project in __projects:
                with ui.card():
                    with ui.row().classes("justify-between w-full"):
                        ui.label(project["name"])
                    with ui.row():
                        ui.button(
                            "edit",
                            on_click=lambda project=project: __select_project(
                                db,
                                project,  # type: ignore
                                tabs,
                            ),
                        )
                        ui.button(
                            "delete",
                            on_click=lambda project=project: __delete(
                                db,
                                project,  # type: ignore
                            ),
                            color="red",
                        )

    ui.label("All Projects")

    ui.timer(2.0, lambda: __refresh_projects(db, tabs))

    project_list = ui.row()


__all__ = ["list_projects"]
