import sqlite3

from nicegui import app, ui

from website.add_new_owned import import_owned
from website.add_new_project import import_project
from website.edit_owned import edit_owned
from website.edit_project import edit_project_cards, edit_project_list
from website.list_projects import list_projects


async def layout(db: sqlite3.Connection):
    with ui.header().classes(replace="row items-center"):
        ui.label("PyStud").classes("font-bold").style("padding: 0 10px 0 10px")
        with ui.tabs() as tabs:
            ui.tab("Import Project")
            ui.tab("Import Owned List")
            ui.tab("All Projects")
            ui.tab("Project List")
            ui.tab("Project Cards")
            ui.tab("Owned")

        ui.space()
        # NOTE dark mode will be persistent for each user across tabs and server restarts
        ui.dark_mode().bind_value(app.storage.user, "dark_mode")
        ui.checkbox().bind_value(app.storage.user, "dark_mode")
        ui.icon("brightness_auto").props("material").classes("text-2xl").style("padding: 0 10px 0 0")

    with ui.tab_panels(tabs, value="Owned").classes("w-full"):
        with ui.tab_panel("Import Project"):
            import_project(db, tabs)
        with ui.tab_panel("Import Owned List"):
            import_owned(db, tabs)
        with ui.tab_panel("All Projects"):
            list_projects(db, tabs)
        with ui.tab_panel("Project List"):
            await edit_project_list(db, "none")
        with ui.tab_panel("Project Cards"):
            await edit_project_cards(db, "none")
        with ui.tab_panel("Owned"):
            await edit_owned(db)


__all__ = ["layout"]
