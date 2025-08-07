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

    def handle_cell_value_change(e):
        ui.notify(f"Updated row to: {e.args['data']}")

    grid = (
        ui.aggrid(
            {
                "columnDefs": [
                    {"headerName": "Id", "field": "id", "checkboxSelection": True},
                    {"headerName": "Color", "field": "colorName", "filter": "agTextColumnFilter", "floatingFilter": True},
                    {"headerName": "Part", "field": "partName", "filter": "agTextColumnFilter", "floatingFilter": True},
                    {"headerName": "Image", "field": "image"},
                    {"headerName": "Quantity", "field": "quantity", "editable": True},
                ],
                "rowData": owned_items,
                "rowSelection": "multiple",
                ":getRowHeight": "params => 50",
            },
            html_columns=[1, 3],
        )
        .on("cellValueChanged", handle_cell_value_change)
        .classes("w-full")
    )

    grid.classes(
        add="ag-theme-balham-dark" if app.storage.user["dark_mode"] else "ag-theme-balham", remove="ag-theme-balham ag-theme-balham-dark"
    )

    async def __update_colours_dialog():
        rows = await grid.get_selected_rows()
        if rows:
            with ui.dialog().classes(add="w-full") as dialog:
                with ui.row().classes("w-full h-[80vh] overflow-scroll justify-center").style("background-color: #333333; padding-top: 20px"):
                    for colour in all_colours:
                        with ui.card().style("width: 300px"):
                            ui.html(build_colour_block(colour)).style(add="cursor: pointer").on(
                                "click", lambda colour_id=colour["id"]: __update_colour(db, rows, colour_id)
                            )

                ui.button("Close", on_click=dialog.close)

            dialog.open()
        else:
            ui.notify("No rows selected.")

    ui.button("Select all", on_click=lambda: grid.run_grid_method("selectAll"))
    ui.button("Update Colours", on_click=__update_colours_dialog)

    ui.add_css(".q-dialog__inner--minimized > div { max-width: none !important }")


__all__ = ["edit_owned"]
