# macOS packaging support
from multiprocessing import freeze_support

freeze_support()

import os  # noqa: E402

import requests  # noqa: E402

try:
    os.makedirs("./PyStud/resources")
    print("Nested directories './PyStud/resources' created successfully.")
except FileExistsError:
    pass
except PermissionError:
    print("Permission denied: Unable to create './PyStud/resources'.")
except Exception as e:
    print(f"An error occurred: {e}")

if not os.path.isfile("./PyStud/resources/colors.csv"):
    response = requests.get(
        url="https://raw.githubusercontent.com/alexc155/PyStud/refs/heads/main/PyStud/resources/colors.csv",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )
    with open("./PyStud/resources/colors.csv", "wb") as download:
        download.write(response.content)

if not os.path.isfile("./PyStud/resources/elements.csv"):
    response = requests.get(
        url="https://raw.githubusercontent.com/alexc155/PyStud/refs/heads/main/PyStud/resources/elements.csv",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )
    with open("./PyStud/resources/elements.csv", "wb") as download:
        download.write(response.content)

if not os.path.isfile("./PyStud/resources/parts.csv"):
    response = requests.get(
        url="https://raw.githubusercontent.com/alexc155/PyStud/refs/heads/main/PyStud/resources/parts.csv",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )
    with open("./PyStud/resources/parts.csv", "wb") as download:
        download.write(response.content)

if not os.path.isfile("./PyStud/resources/Question-Mark-Block.png"):
    response = requests.get(
        url="https://raw.githubusercontent.com/alexc155/PyStud/refs/heads/main/src/website/Question-Mark-Block.png",
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )
    with open("./PyStud/resources/Question-Mark-Block.png", "wb") as download:
        download.write(response.content)

from nicegui import app, native, ui  # noqa: E402

from database import context  # noqa: E402
from website.layout import layout  # noqa: E402

# Db stuff
db = context.connect()
context.create_tables(db)

app.add_media_file(local_file="./PyStud/resources/Question-Mark-Block.png", url_path="/Question-Mark-Block.png")

# app.on_exception(lambda: print('Shutdown'))

@ui.page("/")
async def show():
    ui.add_head_html('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.0/css/all.min.css">')

    await layout(db)

app.native.window_args["zoomable"] = True
app.native.window_args["text_select"] = True

app.native.start_args["gui"] = "gtk"

app.native.settings["ALLOW_DOWNLOADS"] = True
app.native.settings["SHOW_DEFAULT_MENUS"] = False

ui.run(reload=False, native=True, port=native.find_open_port(), storage_secret="vruHItTN49uChT", title="PyStud")

# ui.run(reload=False, port=native.find_open_port(), storage_secret="vruHItTN49uChT", title="PyStud")
# ui.run(reload=True, port=native.find_open_port(), storage_secret="vruHItTN49uChT", title="PyStud")
