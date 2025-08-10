import sqlite3

from nicegui import app, events, ui

from database.tables.owned_table import delete_owned, get_owned, update_colour, update_owned
from utils.colours import build_colour_block, get_colours
from utils.parts import get_parts


@ui.refreshable
async def edit_owned(db: sqlite3.Connection) -> None:
    all_colours = get_colours()
    all_parts = get_parts()

    def __format_owned(owned: list[dict]) -> list[dict]:
        for owned_item in owned:
            colour = next((x for x in all_colours if int(x["id"]) == int(owned_item["color"])), {"name": "None", "rgb": "CCCCCC"})
            owned_item["colorName"] = build_colour_block(colour)

            part = next((x for x in all_parts if x["part_num"] == owned_item["part"]), {"name": "Unknown"})
            owned_item["partName"] = part["name"]

        return owned

    async def __delete() -> None:
        with ui.dialog() as confirm_dialog, ui.card():
            ui.label("Are you sure?")
            with ui.row():
                ui.button("Yes").on_click(lambda: confirm_dialog.submit("Yes"))
                ui.button("No").on_click(lambda: confirm_dialog.submit("No"))

        rows = await grid.get_selected_rows()
        if rows:
            result = await confirm_dialog
            if result == "Yes":
                for row in rows:
                    delete_owned(db, row["id"])
                edit_owned.refresh(db)
        else:
            ui.notify("No rows selected.")

    ui.label("Owned")
    owned_items = __format_owned(get_owned(db))

    def __update_quantity(event: events.GenericEventArguments) -> None:
        id = event.args["data"]["id"]
        owned: int = event.args["data"]["quantity"]
        part = event.args["data"]["part"]
        colour: int = event.args["data"]["color"]
        delete_owned(conn=db, id=id)
        update_owned(conn=db, part=part, colour=colour, owned=owned)

    ui.add_css(".ag-root-wrapper-body.ag-layout-normal { height: 100% !important }")

    grid = (
        ui.aggrid(
            {
                "columnDefs": [
                    {"headerName": "Id", "field": "id", "checkboxSelection": True},
                    {"headerName": "Color", "field": "colorName", "filter": "agTextColumnFilter"},
                    {"headerName": "Part", "field": "partName", "filter": "agTextColumnFilter"},
                    {"headerName": "Image", "field": "image"},
                    {"headerName": "Quantity", "field": "quantity", "editable": True},
                ],
                "rowData": owned_items,
                "rowSelection": "multiple",
                ":getRowHeight": "params => 50",
            },
            html_columns=[1, 3],
            theme="balham-dark" if app.storage.user["dark_mode"] else "balham",
        )
        .on("cellValueChanged", __update_quantity)
        .classes(f"w-full overflow-auto {'ag-theme-balham-dark' if app.storage.user['dark_mode'] else 'ag-theme-balham'}")
        .style(add="height: 100%")
    )

    async def __update_colours_dialog():
        def __filter_colours(colours: list[dict], colour_filter: str) -> list[dict]:
            if colour_filter == "":
                return colours

            return [x for x in colours if colour_filter.lower() in x["name"].lower()]

        def __update_colour(rows: list[dict], colourId: int) -> None:
            for row in rows:
                update_colour(db, row["id"], colourId)
            edit_owned.refresh(db)

        def __build_colour_table(colour_table: ui.row, rows: list[dict], colour_filter: str) -> None:
            colour_table.clear()
            filtered_colours = __filter_colours(all_colours, colour_filter)
            with colour_table:
                for colour in filtered_colours:
                    with ui.card().style("width: 300px"):
                        ui.html(build_colour_block(colour)).style(add="cursor: pointer").on(
                            "click",
                            lambda colour_id=int(colour["id"]): __update_colour(rows, colour_id),  # type: ignore
                        )

        rows = await grid.get_selected_rows()
        if rows:
            with (
                ui.dialog().classes(add="w-full") as dialog,
                ui.row()
                .classes("justify-center")
                .style(f"background-color: {'#333333' if app.storage.user['dark_mode'] else '#FFFFFF'}; padding-bottom: 20px;"),
            ):
                with ui.row().classes("w-full").style(f"background-color: {'#333333' if app.storage.user['dark_mode'] else '#FFFFFF'};"):
                    ui.input(
                        label="Filter",
                        placeholder="Enter a colour name",
                        on_change=lambda e: __build_colour_table(colour_table, rows, e.value),
                    ).style("padding: 0 0 20px 20px")
                with (
                    ui.row()
                    .classes("w-full h-[80vh] overflow-scroll justify-center")
                    .style(
                        f"background-color: {'#333333' if app.storage.user['dark_mode'] else '#FFFFFF'}; padding: 20px 0 20px 0"
                    ) as colour_table
                ):
                    __build_colour_table(colour_table, rows, "")

                ui.button("Close").on_click(dialog.close)

            dialog.open()
        else:
            ui.notify("No rows selected.")

    ui.button("Select all").on_click(lambda: grid.run_grid_method("selectAll"))
    ui.button("Update colours").on_click(__update_colours_dialog)
    ui.button("Delete selected").on_click(__delete)

    ui.add_css(".q-dialog__inner--minimized > div { max-width: none !important }")


__all__ = ["edit_owned"]
