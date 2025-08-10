import re
import time

import requests
from requests.exceptions import HTTPError

from utils.elements import get_elements

all_elements = get_elements()
all_elements.reverse()


def __check_image(url: str, retries_left: int = 3) -> str:
    # print(url)
    # return url
    try:
        response = requests.get(
            url=url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
            },
        )
        response.raise_for_status()
    except HTTPError as http_err:
        if retries_left > 0:
            print(f"HTTP error occurred: {http_err}, retrying... ({retries_left} retries left)")
            time.sleep(1)  # Wait before retrying
            return __check_image(url, retries_left - 1)
        else:
            return ""
    except Exception as err:
        if retries_left > 0:
            print(f"HTTP error occurred: {err}, retrying... ({retries_left} retries left)")
            time.sleep(1)  # Wait before retrying
            return __check_image(url, retries_left - 1)
        else:
            print(f"Other error occurred: {err}")
            return ""
    else:
        return url


def __strip_suffix(part: str) -> str:
    def strip_abc(match_obj) -> str:
        if match_obj.group() is not None:
            return match_obj.group(1)
        return match_obj

    return re.sub(r"(.*\d)([abc])$", strip_abc, part)


def get_image(part_num: str, color_id: int, retries_left: int = 3) -> str:
    try:
        response = requests.get(
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
            time.sleep(1)  # Wait before retrying
            return get_image(part_num, color_id, retries_left - 1)
        else:
            return "http://localhost:8080/Question-Mark-Block.png"
    else:
        elements = [x for x in all_elements if __strip_suffix(x["part_num"]) == __strip_suffix(part_num) and int(x["color_id"]) == color_id]

        elements.extend(
            [
                x
                for x in all_elements
                if __strip_suffix(x["design_id"]) == __strip_suffix(part_num)
                and __strip_suffix(x["part_num"]) != __strip_suffix(part_num)
                and int(x["color_id"]) == color_id
            ]
        )

        elements.extend(
            [x for x in all_elements if __strip_suffix(x["part_num"]) == __strip_suffix(part_num) and int(x["color_id"]) != color_id]
        )

        elements.extend(
            [
                x
                for x in all_elements
                if __strip_suffix(x["part_num"]) == __strip_suffix(part_num)
                and __strip_suffix(x["part_num"]) != __strip_suffix(part_num)
                and int(x["color_id"]) != color_id
            ]
        )

        for element in elements:
            image_response = __check_image(
                f"https://cdn.rebrickable.com/media/thumbs/parts/elements/{element['element_id']}.jpg/85x85p.jpg"
            )
            if image_response != "":
                return image_response

        return "http://localhost:8080/Question-Mark-Block.png"


__all__ = ["get_image"]
