import sqlite3

from nicegui import app, ui

from database.tables.project_item_table import get_to_buy
from database.tables.project_table import delete_project, get_projects


def list_projects(db: sqlite3.Connection, tabs: ui.tabs):
    def __select_project(project: dict, tabs: ui.tabs):
        app.storage.general["project"] = {"id": project["id"], "name": project["name"]}
        tabs.value = "Project List"

    def __delete(project: dict) -> None:
        delete_project(db, int(project["id"]))
        ui.notify(f"Deleted project {project['name']}")
        __refresh_projects.refresh()

    def __export_to_buy(project: dict) -> None:
        to_buy = get_to_buy(db, int(project["id"]))
        ui.download.content(to_buy, "to-buy.csv")
        ui.notify(f"Exported project {project['name']}")

    @ui.refreshable
    def __refresh_projects(tabs: ui.tabs):
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
                        ui.button("edit").on_click(lambda e, project=project: __select_project(project, tabs))
                        ui.button("delete", color="red").on_click(lambda e, project=project: __delete(project))
                        ui.button("export to buy", color="green").on_click(lambda e, project=project: __export_to_buy(project))

    ui.label("All Projects")

    ui.timer(2.0, lambda: __refresh_projects(tabs))

    project_list = ui.row()


__all__ = ["list_projects"]
