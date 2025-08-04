import sqlite3

from nicegui import ui

from database.tables.project_table import delete_project, get_projects
from website.edit_project import edit_project_cards, edit_project_list


def __select_project(db: sqlite3.Connection, project: dict[str, str], tabs: ui.tabs):
    edit_project_list.refresh(db, project["name"])
    edit_project_cards.refresh(db, project["name"])
    tabs.value = "Project List"
    # Here you can add logic to handle the selected project, e.g., display its details


def __delete(db: sqlite3.Connection, project: dict[str, str]) -> None:
    delete_project(db, project["name"])
    edit_project_list.refresh(db, "none")
    edit_project_cards.refresh(db, "none")
    ui.notify(f"Deleted project {project['name']}")
    __refresh_projects.refresh()


@ui.refreshable
def __refresh_projects(db: sqlite3.Connection, tabs: ui.tabs):
    """Refresh the list of projects."""
    __projects = get_projects(db)
    for project in __projects:
        project_dict = {"name": project[0]}
        with ui.card():
            with ui.row().classes("justify-between w-full"):
                ui.label(project_dict["name"])
            with ui.row():
                ui.button(
                    "edit",
                    on_click=lambda project_dict=project_dict: __select_project(
                        db,
                        project_dict,  # type: ignore
                        tabs,
                    ),
                )
                ui.button(
                    "delete",
                    on_click=lambda project_dict=project_dict: __delete(
                        db,
                        project_dict,  # type: ignore
                    ),
                    color="red",
                )
    ui.notify("Projects refreshed!")


def list_projects(db: sqlite3.Connection, tabs: ui.tabs):
    ui.label("All Projects")

    ui.button("Refresh").on("click", __refresh_projects(db, tabs))
    ui.label("This is where you can see all projects.")


__all__ = ["list_projects"]
