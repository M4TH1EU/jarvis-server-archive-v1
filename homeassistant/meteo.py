import json

from homeassistant.homeassistant import getState


def getTemperature(entity_id):
    state = getState(entity_id)
    json_state = json.loads(state.decode('utf8').replace("'", '"'))
    print(json_state)
