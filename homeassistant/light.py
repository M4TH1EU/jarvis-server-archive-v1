import json

import homeassistant.homeassistant
import intents.intents
from homeassistant.homeassistant import call_service
from sentences import get_sentence_without_stopwords_and_pattern, get_ascii_sentence
from utils import colorUtils


def turn_on(entity_id):
    """
    Turn on a light

    Parameters
    ----------
    entity_id : str
    """

    homeassistant.homeassistant.call_api("light", "turn_on", {'entity_id': entity_id})


def turn_on(data):
    """
    Turn on a light using data from intent

    Parameters
    ----------
    data : dict
    """

    tag = "none"
    if 'tag' in data:
        tag = data.get('tag')

        if 'entity_id' in data:
            entity_id = data.get('entity_id')

            if 'sentence' in data:
                sentence = get_ascii_sentence(data.get('sentence'))

                color = get_sentence_without_stopwords_and_pattern(sentence, tag)
                if not color and colorUtils.does_color_exists(color):
                    rgb = colorUtils.get_color_code_for_color(color)
                    homeassistant.light.change_color_with_rgb(entity_id, rgb)
                else:
                    homeassistant.light.turn_on(entity_id)
            else:
                homeassistant.light.turn_on(entity_id)

        return intents.intents.get_random_response_for_tag(tag)

    raise Exception("light.turn_on needs tag, sentence, entity_id as data")


def turn_off(entity_id):
    """
    Turn off a light

    Parameters
    ----------
    entity_id : str
    """
    call_service('{"entity_id": "' + entity_id + '" }', "light/turn_off")


def is_on(entity_id):
    return homeassistant.homeassistant.get_state(entity_id).state == 'on'


def change_color_with_name(entity_id, color):
    """
    Change the color of a specified light with human readable color

    Parameters
    ----------
    entity_id : str
    color : str
    """
    homeassistant.homeassistant.call_api("light", "turn_on", {'entity_id': entity_id, 'color_name': color})


def change_color_with_rgb(entity_id, rgb):
    """
    Change the color of a specified light with RGB code

    Parameters
    ----------
    entity_id : str
    rgb: list

    """
    homeassistant.homeassistant.call_api("light", "turn_on", {'entity_id': entity_id, 'rgb_color': str(rgb)})


def change_brightness(entity_id, brightness):
    """
    Change the brightness of a specified light

    Parameters
    ----------
    entity_id : str
    brightness : int

    """

    homeassistant.homeassistant.call_api("light", "turn_on", {'entity_id': entity_id, 'brightness': brightness})
