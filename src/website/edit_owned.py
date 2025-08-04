import sqlite3

from nicegui import app, ui

from database.tables import owned_table
from utils.colours import get_colours


@ui.refreshable
async def edit_owned(db: sqlite3.Connection) -> None:
    all_colours = get_colours()

    def _format_owned(owned: list[dict]) -> list[dict]:
        for owned_item in owned:
            colour = next((x for x in all_colours if x["id"] == owned_item["color"]), {"name": "None", "rgb": "CCCCCC"})
            owned_item["colorName"] = (
                f'<div style="width: 80px; height: 25px; background-color: #{colour["rgb"]}; display: inline-block; border: 1px solid #CCCCCC"></div><div style="display: inline-block; height: 25px; vertical-align: top; padding-left: 2px">{colour["name"]}</div>'
            )

        return owned

    ui.label("Owned")
    owned_items = _format_owned(owned_table.get_owned(db))

    grid = (
        ui.aggrid(
            {
                "columnDefs": [
                    {"headerName": "Id", "field": "id", "checkboxSelection": True},
                    {"headerName": "Part", "field": "part", "floatingFilter": True},
                    {"headerName": "Color", "field": "colorName", "floatingFilter": True},
                    {"headerName": "Image", "field": "image"},
                    {"headerName": "Quantity", "field": "quantity"},
                ],
                "rowData": owned_items,
                "rowSelection": "multiple",
                ":getRowHeight": "params => 50",
            },
            html_columns=[2, 3],
        )
        .classes("w-full")
        .on("cellClicked", lambda event: ui.notify(f"Cell value: {event.args['value']}"))
    )

    grid.classes(
        add="ag-theme-balham-dark" if app.storage.user["dark_mode"] else "ag-theme-balham", remove="ag-theme-balham ag-theme-balham-dark"
    )

    async def output_selected_rows():
        rows = await grid.get_selected_rows()
        if rows:
            for row in rows:
                ui.notify(f"{row['name']}, {row['age']}")
        else:
            ui.notify("No rows selected.")

    ui.button("Output selected rows", on_click=output_selected_rows)


__all__ = ["edit_owned"]
