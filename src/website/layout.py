import sqlite3

from nicegui import app, events, ui

from website.add_new_owned import import_owned
from website.add_new_project import import_project
from website.edit_owned import edit_owned
from website.edit_project_cards import edit_project_cards
from website.edit_project_list import edit_project_list
from website.list_projects import list_projects


async def layout(db: sqlite3.Connection):
    project = app.storage.general.get("project", {"id": 0, "name": "none"})

    def __tab_change(e: events.ValueChangeEventArguments):
        match e.value:
            case "Project List":
                edit_project_list.refresh(db, project["id"], project["name"])
                return
            case "Project Cards":
                edit_project_cards.refresh(db, project["id"], project["name"])
                return
            case "Owned":
                edit_owned.refresh(db)
                return
            case _:
                return

    def __dark_mode_change(_: events.ValueChangeEventArguments):
        edit_project_list.refresh(db, project["id"], project["name"])
        edit_project_cards.refresh(db, project["id"], project["name"])
        edit_owned.refresh(db)

    with ui.header().classes(replace="row items-center"):
        ui.label("PyStud").classes("font-bold").style("padding: 0 10px 0 10px")
        with ui.tabs().on_value_change(__tab_change) as tabs:
            ui.tab("Import Project")
            ui.tab("Import Owned List")
            ui.tab("All Projects")
            ui.tab("Project List")
            ui.tab("Project Cards")
            ui.tab("Owned")

        ui.space()

        ui.dark_mode().bind_value(app.storage.user, "dark_mode")
        ui.checkbox().bind_value(app.storage.user, "dark_mode").on_value_change(__dark_mode_change)
        ui.icon("brightness_auto").props("material").classes("text-2xl").style("padding: 0 10px 0 0")

    with ui.tab_panels(tabs, value="All Projects").classes("w-full"):
        with ui.tab_panel("Import Project"):
            import_project(db, tabs)
        with ui.tab_panel("Import Owned List"):
            import_owned(db, tabs)
        with ui.tab_panel("All Projects"):
            list_projects(db, tabs)
        with ui.tab_panel("Project List"):
            await edit_project_list(db, project["id"], project["name"])
        with ui.tab_panel("Project Cards"):
            await edit_project_cards(db, project["id"], project["name"])
        with ui.tab_panel("Owned"):
            await edit_owned(db)

    return


__all__ = ["layout"]
