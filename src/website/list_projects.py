import sqlite3

from nicegui import ui

from database.tables.project_table import delete_project, get_projects
from website.edit_project_cards import edit_project_cards
from website.edit_project_list import edit_project_list


def __select_project(db: sqlite3.Connection, project: dict, tabs: ui.tabs):
    edit_project_list.refresh(db, project["id"], project["name"])
    edit_project_cards.refresh(db, project["id"], project["name"])
    tabs.value = "Project List"


def __delete(db: sqlite3.Connection, project: dict) -> None:
    delete_project(db, int(project["id"]))
    edit_project_list.refresh(db, "none")
    edit_project_cards.refresh(db, "none")
    ui.notify(f"Deleted project {project['name']}")
    __refresh_projects.refresh()


@ui.refreshable
def __refresh_projects(db: sqlite3.Connection, tabs: ui.tabs):
    """Refresh the list of projects."""
    __projects = get_projects(db)
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
    ui.notify("Projects refreshed!")


def list_projects(db: sqlite3.Connection, tabs: ui.tabs):
    ui.label("All Projects")

    ui.button("Refresh").on("click", __refresh_projects(db, tabs))
    ui.label("This is where you can see all projects.")


__all__ = ["list_projects"]
