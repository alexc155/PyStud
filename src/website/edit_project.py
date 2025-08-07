import sqlite3

from nicegui import app, ui

from database.tables import owned_table, project_table
from utils.colours import build_colour_block, get_colours


@ui.refreshable
async def edit_project_list(db: sqlite3.Connection, project_name: str):
    if project_name == "none":
        ui.label("No project selected.")
        return

    def __on_cell_value_changed(event):
        """Handle cell value changes in the grid."""
        data_id = event.args["data"]["id"]
        qty = event.args["data"]["qty"]
        project_table.update_project_item_qty(conn=db, id=data_id, qty=qty)

        owned = event.args["data"]["owned"]
        part = event.args["data"]["bl_item_no"]
        colour = event.args["data"]["ldraw_color_id"]
        owned_table.update_owned(conn=db, part=part, colour=colour, owned=owned)

    all_colours = get_colours()

    def __format_project(project: list[dict]) -> list[dict]:
        for project_item in project:
            colour = next((x for x in all_colours if x["id"] == project_item["ldraw_color_id"]), {"name": "None", "rgb": "CCCCCC"})
            project_item["colorName"] = build_colour_block(colour)

        return project

    ui.label(project_name)
    project_items = __format_project(project_table.get_project_items(db, project_name))

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


def __update_project_item_qty(val: int, db: sqlite3.Connection, project_name: str, id: int):
    project_table.update_project_item_qty(db, id, val)
    [item for item in project_items if item["id"] == id][0]["qty"] = val
    edit_project_list.refresh(db, project_name)


def __update_project_item_owned(val: int, db: sqlite3.Connection, project_name: str, id: int, part: str, colour: int):
    owned_table.update_owned(conn=db, part=part, colour=colour, owned=val)
    [item for item in project_items if item["id"] == id][0]["owned"] = val
    edit_project_list.refresh(db, project_name)


@ui.refreshable
async def edit_project_cards(db: sqlite3.Connection, project_name: str):
    if project_name == "none":
        ui.label("No project selected.")
        return

    @ui.refreshable
    def __show_cards(card_items):
        results.clear()
        with results:
            for card_item in card_items:
                card_id = card_item["id"]
                part = card_item["bl_item_no"]
                colour = card_item["ldraw_color_id"]
                qty_input = card_item["qty"] if card_item["qty"] else "0"
                owned_input = card_item["owned"] if card_item["owned"] else "0"
                with (
                    ui.card().style("width: 310px"),
                    ui.grid(rows=3, columns=2).classes("gap-0"),
                ):
                    ui.label(f"{card_item['color_name']} {card_item['part_name']}").classes("col-span-full gap-0 overflow-scroll").style(
                        "max-width: 300px"
                    )
                    ui.html(card_item["image_mid"]).classes("row-span-2 col-span-1").style("min-width: 150px")

                    with ui.row(wrap=False).classes("row-span-1 col-span-1"):
                        ui.input("Quantity", value=qty_input).props("rounded outlined dense type=number").style(
                            "max-width: 100px;"
                        ).on_value_change(
                            lambda e, card_id=card_id: __update_project_item_qty(
                                int(e.value or "0"),
                                db,
                                project_name,
                                card_id,
                            )
                        )
                    with ui.row(wrap=False).classes("row-span-1 col-span-1"):
                        ui.input("Owned", value=owned_input).props("rounded outlined dense type=number").style(
                            "max-width: 100px;"
                        ).on_value_change(
                            lambda e, card_id=card_id, part=part, colour=colour: __update_project_item_owned(
                                int(e.value or "0"), db, project_name, card_id, part, colour
                            )
                        )

    def __filter_items():
        """Filter items based on color and part name."""
        filtered_items = [
            item
            for item in project_items
            if (color_filter.value or "").lower() in item["color_name"].lower()
            and (part_filter.value or "").lower() in item["part_name"].lower()
        ]
        __show_cards.refresh(filtered_items)

    ui.label(project_name)

    with ui.row(wrap=False):
        color_filter = ui.input("Color", value="").props("clearable")
        part_filter = ui.input("Part Name", value="").props("clearable")
        ui.button("Refresh", on_click=__filter_items)

    global project_items
    project_items = project_table.get_project_items(db, project_name)

    results = ui.row().classes("h-[80vh] overflow-scroll")

    __show_cards(project_items)


__all__ = ["edit_project_cards", "edit_project_list"]
