from homeassistant.homeassistant import callService


def turnOn(entity_id):
    """
    Turn on a switch

    Parameters
    ----------
    entity_id : str
    """

    callService('{"entity_id": "' + entity_id + '" }', "switch/turn_on")


def turnOff(entity_id):
    """
    Turn off a switch

    Parameters
    ----------
    entity_id : str
    """
    callService('{"entity_id": "' + entity_id + '" }', "switch/turn_off")


def toggle(entity_id):
    """
    Toggle a switch

    Parameters
    ----------
    entity_id : str
    """
    callService('{"entity_id": "' + entity_id + '" }', "switch/toggle")

