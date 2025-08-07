#!/usr/bin/env python3
from nicegui import ui

from database import context
from database.tables import owned_table
from utils.colours import build_colour_block, get_colours
from utils.parts import get_parts

db = context.connect()
all_colours = get_colours()
all_parts = get_parts()


def __format_owned(owned: list[dict]) -> list[dict]:
    for owned_item in owned:
        colour = next((x for x in all_colours if x["id"] == owned_item["color"]), {"name": "None", "rgb": "CCCCCC"})
        owned_item["colorName"] = build_colour_block(colour)

        part = next((x for x in all_parts if x["part_num"] == owned_item["part"]), {"name": "Unknown"})
        owned_item["partName"] = part["name"]
        owned_item["image"] = '<img src="https://img.bricklink.com/ItemImage/PL/3673.png" style="height: 45px" />'

    return owned


columns = [
    {"headerName": "Id", "field": "id", "checkboxSelection": True},
    {"headerName": "Color", "field": "colorName", "filter": "agTextColumnFilter", "floatingFilter": True},
    {"headerName": "Part", "field": "partName", "filter": "agTextColumnFilter", "floatingFilter": True},
    {"headerName": "Image", "field": "image"},
    {"headerName": "Quantity", "field": "quantity", "editable": True},
]
rows = __format_owned(owned_table.get_owned(db))


@ui.page("/")
def page():
    def handle_cell_value_change(e):
        new_row = e.args["data"]
        ui.notify(f"Updated row to: {e.args['data']}")
        rows[:] = [row | new_row if row["id"] == new_row["id"] else row for row in rows]

    grid = (
        ui.aggrid(
            {
                "columnDefs": columns,
                "rowData": rows,
                "rowSelection": "multiple",
                ":getRowHeight": "params => 50",
            },
            html_columns=[1,3],
        )
        .on("rowSelected", lambda msg: print(msg))
        .on("cellValueChanged", handle_cell_value_change)
        .classes("w-full")
    )


ui.run()
