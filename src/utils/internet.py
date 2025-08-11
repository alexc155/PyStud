import requests
from nicegui import app


def check_internet_connection(retries_left: int = 3) -> bool:
    try:
        response = requests.head(
            url="https://cdn.rebrickable.com/media/thumbs/nil.png/85x85p.png",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            },
        )
        response.raise_for_status()
    except Exception as err:
        # No internet?
        if retries_left > 0:
            print(f"HTTP error occurred: {err}, retrying... ({retries_left} retries left)")
            return check_internet_connection(retries_left - 1)
        else:
            app.storage.general["internet"] = False
            return False
    else:
        app.storage.general["internet"] = True
        return True
