import re

import requests

from utils.elements import get_elements

all_elements = get_elements()
all_elements.reverse()


def get_image(part_num: str, color_id: int, internet: bool) -> str:
    if not internet:
        return ""

    def __strip_suffix(part: str) -> str:
        def __strip_abc(match_obj) -> str:
            if match_obj.group() is not None:
                return match_obj.group(1)
            return match_obj

        return re.sub(r"(.*\d)([abc])$", __strip_abc, part)

    def __check_image(url: str, retries_left: int = 3) -> str:
        try:
            response = requests.head(
                url=url,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
                },
            )
            response.raise_for_status()
        except Exception as err:
            if retries_left > 0:
                print(f"HTTP error occurred: {err}, retrying... ({retries_left} retries left)")
                return __check_image(url, retries_left - 1)
            else:
                return ""
        else:
            return url

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
        image_response = __check_image(f"https://cdn.rebrickable.com/media/thumbs/parts/elements/{element['element_id']}.jpg/85x85p.jpg")
        if image_response != "":
            return image_response

    return "/Question-Mark-Block.png"


__all__ = ["get_image"]
