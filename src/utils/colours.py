import colorsys
import math
from csv import DictReader


def __step(r: int, g: int, b: int, repetitions: int = 1) -> tuple:
    lum = math.sqrt(0.241 * r + 0.691 * g + 0.068 * b)

    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    h2 = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2 = int(v * repetitions)

    if h2 % 2 == 1:
        v2 = repetitions - v2
        lum2 = repetitions - lum2

    return (h2, lum2, v2)


def get_colours() -> list[dict[str, str]]:
    with open("./src/database/colors.csv") as data:
        dict_reader = DictReader(data)

        list_of_dict = list(dict_reader)

        list_of_dict.sort(
            key=lambda key: __step(int(f"0x{key['rgb'][:2]}", 16), int(f"0x{key['rgb'][2:4]}", 16), int(f"0x{key['rgb'][4:6]}", 16), 8)
        )

        return list_of_dict


def build_colour_block(colour: dict[str, str]) -> str:
    return f'<div style="width: 70px; height: 25px; background-color: #{colour["rgb"]}; display: inline-block; border: 1px solid #CCCCCC"></div><div style="display: inline-block; height: 25px; vertical-align: top; padding-left: 2px">{colour["name"]}</div>'


__all__ = ["get_colours", "build_colour_block"]
