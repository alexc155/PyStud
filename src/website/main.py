# macOS packaging support
from multiprocessing import freeze_support  # noqa

freeze_support()  # noqa

# all your other imports and code

from nicegui import app, native, ui

from database import context
from website.layout import layout

# Db stuff
db = context.connect()
context.create_tables(db)

app.add_media_file(local_file="src/website/Question-Mark-Block.png", url_path="/Question-Mark-Block.png")


@ui.page("/")
async def show():
    ui.add_head_html('<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/7.0.0/css/all.min.css">')

    await layout(db)


ui.run(reload=False, port=native.find_open_port(), storage_secret="vruHItTN49uChT")
# ui.run(reload=True, port=native.find_open_port(), storage_secret="vruHItTN49uChT")
