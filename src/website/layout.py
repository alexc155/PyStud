import sqlite3

from nicegui import app, events, ui

from utils.internet import check_internet_connection
from website.add_new_owned import import_owned
from website.add_new_project import import_project
from website.edit_owned import edit_owned
from website.edit_project_cards import edit_project_cards
from website.edit_project_list import edit_project_list
from website.list_projects import list_projects


async def layout(db: sqlite3.Connection):
    project = app.storage.general.get("project", {"id": 0, "name": "none"})

    def __tab_change(e: events.ValueChangeEventArguments):
        check_internet_connection()
        project = app.storage.general.get("project", {"id": 0, "name": "none"})

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

    def __dark_mode_change(val):
        dark_mode.set_value(val)
        edit_project_list.refresh(db, project["id"], project["name"])
        edit_project_cards.refresh(db, project["id"], project["name"])
        edit_owned.refresh(db)

    def __zoom(adjustment):
        ui.run_javascript(f"""
                            window.document.body.style["zoom"] = parseFloat(window.getComputedStyle(document.body).zoom) + parseFloat({adjustment})
                          """)

    with ui.header().classes(replace="row items-center"):
        ui.label("PyStud").classes("font-bold").style("padding: 0 10px 0 10px")
        with ui.tabs().on_value_change(__tab_change) as tabs:
            ui.tab("All Projects")
            ui.tab("Import Project")
            ui.tab("Import Owned List")
            ui.tab("Project List")
            ui.tab("Project Cards")
            ui.tab("Owned")

        ui.space()

        dark_mode = ui.dark_mode().bind_value(app.storage.user, "dark_mode")

        with ui.element().classes("max-[420px]:hidden").tooltip("Cycle theme mode through dark, light, and system/auto."):
            ui.button(icon="dark_mode", on_click=lambda: __dark_mode_change(None)).props("flat fab-mini color=white").bind_visibility_from(
                dark_mode, "value", value=True
            )
            ui.button(icon="light_mode", on_click=lambda: __dark_mode_change(True)).props("flat fab-mini color=white").bind_visibility_from(
                dark_mode, "value", value=False
            )
            ui.button(icon="brightness_auto", on_click=lambda: __dark_mode_change(False)).props(
                "flat fab-mini color=white"
            ).bind_visibility_from(dark_mode, "value", lambda mode: mode is None)

        ui.button("-", on_click=lambda: __zoom('-0.1'))
        ui.button("+", on_click=lambda: __zoom('0.1'))
        ui.button("exit", on_click=shutdown)

    with ui.tab_panels(tabs, value="All Projects").classes("w-full"):
        with ui.tab_panel("All Projects"):
            list_projects(db, tabs)
        with ui.tab_panel("Import Project"):
            import_project(db, tabs)
        with ui.tab_panel("Import Owned List"):
            import_owned(db, tabs)
        with ui.tab_panel("Project List"):
            await edit_project_list(db, project["id"], project["name"])
        with ui.tab_panel("Project Cards"):
            await edit_project_cards(db, project["id"], project["name"])
        with ui.tab_panel("Owned"):
            await edit_owned(db)

    return


def shutdown():
    ui.run_javascript("window.close()")
    app.shutdown()


__all__ = ["layout"]
