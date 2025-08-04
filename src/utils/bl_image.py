import base64
import sqlite3
import time

import requests
from requests.exceptions import HTTPError


def get_image(BLItemNo: str, BLColorId: str, retries_left: int = 3) -> str:
    try:
        response = requests.get(
            url=f"https://img.bricklink.com/ItemImage/PN/{BLColorId}/{BLItemNo}.png",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            },
        )
        response.raise_for_status()
    except HTTPError as http_err:
        if retries_left > 0:
            print(f"HTTP error occurred: {http_err}, retrying... ({retries_left} retries left)")
            time.sleep(3)  # Wait before retrying
            return get_image(BLItemNo, BLColorId, retries_left - 1)
        else:
            print("Max retries reached. Returning default image.")
            # Return a default image if all retries fail
            response = requests.get(
                url=f"https://img.bricklink.com/ItemImage/PL/{BLItemNo}.png",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
                },
            )
            binary_content = sqlite3.Binary(response.content)
            encoded_image = base64.b64encode(binary_content).decode("utf-8")
            encoded_image = encoded_image.replace("\n", "")
            return encoded_image
    except Exception as err:
        if retries_left > 0:
            print(f"HTTP error occurred: {err}, retrying... ({retries_left} retries left)")
            time.sleep(3)  # Wait before retrying
            return get_image(BLItemNo, BLColorId, retries_left - 1)
        else:
            print(f"Other error occurred: {err}")
            response = requests.get(
                url="https://static.bricklink.com/clone/img/no_image_m.png",
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
                },
            )
            binary_content = sqlite3.Binary(response.content)
            encoded_image = base64.b64encode(binary_content).decode("utf-8")
            encoded_image = encoded_image.replace("\n", "")
            return encoded_image
    else:
        print("Success!")
        binary_content = sqlite3.Binary(response.content)
        encoded_image = base64.b64encode(binary_content).decode("utf-8")
        encoded_image = encoded_image.replace("\n", "")
        return encoded_image


__all__ = ["get_image"]
