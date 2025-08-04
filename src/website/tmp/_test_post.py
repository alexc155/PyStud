import asyncio
import json

import httpx
from nicegui import ui

running_query: asyncio.Task | None = None


def test_post():
    """Test POST request to the /add endpoint."""

    async def post_data():
        async with httpx.AsyncClient() as client:
            global running_query
            if running_query:
                running_query.cancel()
            results.clear()
            running_query = asyncio.create_task(
                client.post("http://localhost:8000/add", json={"x": 5})
            )

            response = await running_query
            if response.text == "":
                return
            with results:
                ui.label(json.dumps(response.json()))
            running_query = None

    ui.button("Test POST - X=5", on_click=post_data).props("flat").classes("mt-4")
    results = ui.row()
