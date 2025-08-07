from nicegui import app, ui

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


ui.run(storage_secret="vruHItTN49uChT")


if __name__ == "__main__":
    print('Please start the app with the "python3 ./src/website/main.py"')
