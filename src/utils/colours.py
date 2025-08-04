import colorsys
import math
from csv import DictReader


def __step(r, g, b, repetitions=1):
    lum = math.sqrt(0.241 * r + 0.691 * g + 0.068 * b)

    h, s, v = colorsys.rgb_to_hsv(r, g, b)

    h2 = int(h * repetitions)
    lum2 = int(lum * repetitions)
    v2 = int(v * repetitions)

    if h2 % 2 == 1:
        v2 = repetitions - v2
        lum2 = repetitions - lum2

    return (h2, lum2, v2)

def __sort(r, g, b):
    x = (r * 255 * 255) + (g * 255) + b
    return x

def get_colours():
    with open("./src/database/colors.csv") as data:
        dict_reader = DictReader(data)

        list_of_dict = list(dict_reader)

        # list_of_dict.sort(
        #     key=lambda key: __step(int(f"0x{key['rgb'][:2]}", 16), int(f"0x{key['rgb'][2:4]}", 16), int(f"0x{key['rgb'][4:6]}", 16), 8)
        # )

        list_of_dict.sort(
            key=lambda key: __sort(int(f"0x{key['rgb'][:2]}", 16), int(f"0x{key['rgb'][2:4]}", 16), int(f"0x{key['rgb'][4:6]}", 16))
        )

        return list_of_dict