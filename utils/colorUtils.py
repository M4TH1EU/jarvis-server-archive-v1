import json
import os

import pathfile

path = os.path.dirname(pathfile.__file__)

with open(path + '\\utils\\colors.json', encoding='utf-8', mode='r') as json_data:
    colors = json.load(json_data)


def does_color_exists(color):
    return color in colors


def get_color_code_for_color(color):
    if does_color_exists(color):
        h = colors[color]
        rgb = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

        # TODO: do something better here
        r = str(rgb).split("(")[1].split(", ")[0]
        g = str(rgb).split(", ")[1]
        b = str(rgb).split(", ")[2].split(")")[0]
        return [r, g, b]
