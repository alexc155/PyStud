import sqlite3

from nicegui import ui

from database.tables.owned_table import update_owned
from database.tables.project_item_table import get_project_items, update_project_item_qty
from website.edit_project_list import edit_project_list


@ui.refreshable
async def edit_project_cards(db: sqlite3.Connection, project_id: int, project_name: str):
    if project_name == "none":
        ui.label("No project selected.")
        return

    def __update_project_item_qty(val: int, id: int):
        update_project_item_qty(db, id, val)
        [item for item in project_items if item["id"] == id][0]["qty"] = val
        edit_project_list.refresh(db, project_name)

    def __update_project_item_owned(val: int, id: int, part: str, colour: int):
        update_owned(conn=db, part=part, colour=colour, owned=val)
        [item for item in project_items if item["id"] == id][0]["owned"] = val
        edit_project_list.refresh(db, project_name)

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
                                card_id,
                            )
                        )
                    with ui.row(wrap=False).classes("row-span-1 col-span-1"):
                        ui.input("Owned", value=owned_input).props("rounded outlined dense type=number").style(
                            "max-width: 100px;"
                        ).on_value_change(
                            lambda e, card_id=card_id, part=part, colour=colour: __update_project_item_owned(
                                int(e.value or "0"), card_id, part, colour
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

    project_items = get_project_items(db, project_id)

    results = ui.row().classes("h-[80vh] overflow-scroll")

    __show_cards(project_items)


__all__ = ["edit_project_cards"]
