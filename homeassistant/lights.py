import json

import homeassistant.homeassistant
from homeassistant.homeassistant import call_service


def turn_on(entity_id):
    """
    Turn on a light

    Parameters
    ----------
    entity_id : str
    """

    call_service('{"entity_id": "' + entity_id + '" }', "light/turn_on")


def turn_off(entity_id):
    """
    Turn off a light

    Parameters
    ----------
    entity_id : str
    """
    call_service('{"entity_id": "' + entity_id + '" }', "light/turn_off")


def is_on(entity_id):
    return json.loads(homeassistant.homeassistant.get_state(entity_id))['state'] == 'on'


def change_color_with_name(entity_id, color):
    """
    Change the color of a specified light with human readable color

    Parameters
    ----------
    entity_id : str
    color : str
    """
    call_service('{"entity_id": "' + entity_id +
                '", "color_name": "' + color + '" }', "light/turn_on")


def change_color_with_rgb(entity_id, r, g, b):
    """
    Change the color of a specified light with RGB code

    Parameters
    ----------
    entity_id : str
    r : int
    g : int
    b : int

    """
    call_service('{"entity_id": "' + entity_id +
                '", "rgb_color": "[' + r + ',' + g + ',' + b + ']" }', "light/turn_on")


def change_brightness(entity_id, brightness):
    """
    Change the brightness of a specified light

    Parameters
    ----------
    entity_id : str
    brightness : int

    """
    call_service('{"entity_id": "' + entity_id +
                '", "brightness": "' + brightness + '" }', "light/turn_on")
