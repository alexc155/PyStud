import sqlite3

from nicegui import app, ui

from database.tables import owned_table
from utils.colours import build_colour_block, get_colours
from utils.parts import get_parts


@ui.refreshable
async def edit_owned(db: sqlite3.Connection) -> None:
    all_colours = get_colours()
    all_parts = get_parts()

    def __format_owned(owned: list[dict]) -> list[dict]:
        for owned_item in owned:
            colour = next((x for x in all_colours if x["id"] == owned_item["color"]), {"name": "None", "rgb": "CCCCCC"})
            owned_item["colorName"] = build_colour_block(colour)

            part = next((x for x in all_parts if x["part_num"] == owned_item["part"]), {"name": "Unknown"})
            owned_item["partName"] = part["name"]

        return owned

    def __update_colour(db, rows, colourId) -> None:
        for row in rows:
            owned_table.update_colour(db, row["id"], colourId)
        edit_owned.refresh(db)

    ui.label("Owned")
    owned_items = __format_owned(owned_table.get_owned(db))

    grid = (
        ui.aggrid(
            {
                "columnDefs": [
                    {"headerName": "Id", "field": "id", "checkboxSelection": True},
                    {"headerName": "Color", "field": "colorName", "filter": "agTextColumnFilter", "floatingFilter": True},
                    {"headerName": "Part", "field": "partName", "filter": "agTextColumnFilter", "floatingFilter": True},
                    {"headerName": "Image", "field": "image"},
                    {"headerName": "Quantity", "field": "quantity"},
                ],
                "rowData": owned_items,
                "rowSelection": "multiple",
                ":getRowHeight": "params => 50",
            },
            html_columns=[1, 3],
        )
        .classes("w-full")
        .on("cellClicked", lambda event: ui.notify(f"Cell value: {event.args['value']}"))
    )

    grid.classes(
        add="ag-theme-balham-dark" if app.storage.user["dark_mode"] else "ag-theme-balham", remove="ag-theme-balham ag-theme-balham-dark"
    )

    async def __update_colours_dialog():
        rows = await grid.get_selected_rows()
        if rows:
            with ui.dialog() as dialog, ui.card():
                ui.label("Change Colour")
                with ui.expansion("Colour", icon="palette").classes("w-full"):
                    for colour in all_colours:
                        with ui.row():
                            ui.html(build_colour_block(colour)).on(
                                "click", lambda colour_id=colour["id"]: __update_colour(db, rows, colour_id)
                            )

                ui.button("Close", on_click=dialog.close)

            dialog.open()
        else:
            ui.notify("No rows selected.")

    ui.button("Update Colours", on_click=__update_colours_dialog)


__all__ = ["edit_owned"]
