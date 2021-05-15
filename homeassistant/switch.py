from homeassistant.homeassistant import call_service


def turn_on(entity_id):
    """
    Turn on a switch

    Parameters
    ----------
    entity_id : str
    """

    call_service('{"entity_id": "' + entity_id + '" }', "switch/turn_on")


def turn_off(entity_id):
    """
    Turn off a switch

    Parameters
    ----------
    entity_id : str
    """
    call_service('{"entity_id": "' + entity_id + '" }', "switch/turn_off")


def toggle(entity_id):
    """
    Toggle a switch

    Parameters
    ----------
    entity_id : str
    """
    call_service('{"entity_id": "' + entity_id + '" }', "switch/toggle")

