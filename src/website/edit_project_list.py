import sqlite3

from nicegui import app, ui

from database.tables.owned_table import update_owned
from database.tables.project_item_table import get_project_items, update_project_item_qty
from utils.colours import build_colour_block, get_colours


@ui.refreshable
async def edit_project_list(db: sqlite3.Connection, project_id: int, project_name: str) -> None:
    if project_name == "none":
        ui.label("No project selected.")
        return

    def __on_cell_value_changed(event) -> None:
        """Handle cell value changes in the grid."""
        data_id = event.args["data"]["id"]
        qty: int = int(event.args["data"]["qty"])
        update_project_item_qty(conn=db, id=data_id, qty=qty)

        owned: int = int(event.args["data"]["owned"]) if event.args["data"]["owned"] else 0
        part = event.args["data"]["bl_item_no"]
        colour: int = int(event.args["data"]["ldraw_color_id"])
        update_owned(conn=db, part=part, colour=colour, owned=owned)

    all_colours = get_colours()

    def __format_project_items(project_items: list[dict]) -> list[dict]:
        for project_item in project_items:
            colour = next(
                (x for x in all_colours if int(x["id"]) == int(project_item["ldraw_color_id"])), {"name": "None", "rgb": "CCCCCC"}
            )
            project_item["colorName"] = build_colour_block(colour)
            project_item["buy"] = int(project_item["qty"]) - (int(project_item["owned"]) if project_item["owned"] is not None else 0)
            if int(project_item["buy"]) <= 0:
                project_item["buy"] = None

        return project_items

    ui.label(project_name)
    project_items = __format_project_items(get_project_items(db, project_id))

    column_defs = [
        {
            "field": "id",
            "headerName": "Id",
            "editable": False,
            "flex": 1,
        },
        {
            "field": "colorName",
            "headerName": "Color Name",
            "editable": False,
            "filter": "agTextColumnFilter",
            "flex": 3,
        },
        {
            "field": "part_name",
            "headerName": "Part Name",
            "editable": False,
            "filter": "agTextColumnFilter",
            "flex": 5,
        },
        {
            "field": "image_sm",
            "headerName": "Image",
            "editable": False,
            "flex": 1,
        },
        {
            "field": "qty",
            "headerName": "Quantity",
            "editable": True,
            "type": "number",
            "flex": 1,
        },
        {
            "field": "owned",
            "headerName": "Owned",
            "editable": True,
            "type": "number",
            "flex": 1,
        },
        {
            "field": "buy",
            "headerName": "To Buy",
            "editable": False,
            "type": "number",
            "filter": "agNumberColumnFilter",
            "flex": 1,
        },
    ]

    ui.add_css(".ag-root-wrapper-body.ag-layout-normal { height: 100% !important }")

    (
        ui.aggrid(
            {
                "columnDefs": column_defs,
                "rowData": project_items,
                "rowSelection": "multiple",
                ":getRowHeight": "params => 50",
            },
            html_columns=[1, 3],
        )
        .on("cellValueChanged", __on_cell_value_changed)
        .classes(f"w-full overflow-auto {'ag-theme-balham-dark' if app.storage.user['dark_mode'] else 'ag-theme-balham'}")
        .style(add="height: 100%")
    )


__all__ = ["edit_project_list"]
