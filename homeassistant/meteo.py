import json

from homeassistant.homeassistant import getState


def getTemperature(entity_id):
    state = getState(entity_id)
    state = '{    "entity_id": "weather.bussigny_sur_oron",    "state": "sunny",    "attributes": {        "temperature": 8.9,        "humidity": 58,        "pressure": 925.6,        "wind_bearing": "WSW",        "wind_speed": 8.6,        "attribution": "Weather forecast from MeteoSwiss (https://www.meteoswiss.admin.ch/)",        "forecast": [            {                "datetime": "2021-05-04",                "templow": 4,                "temperature": 15,                "condition": "rainy"            },            {                "datetime": "2021-05-05",                "templow": 6,                "temperature": 11,                "condition": "rainy"            },            {                "datetime": "2021-05-06",                "templow": 4,                "temperature": 11,                "condition": "rainy"            },            {                "datetime": "2021-05-07",                "templow": 6,                "temperature": 11,                "condition": "rainy"            },            {                "datetime": "2021-05-08",                "templow": 5,                "temperature": 18,                "condition": "sunny"            }        ],        "friendly_name": "Bussigny-sur-Oron"    },    "last_changed": "2021-05-03T07:57:13.828170+00:00",    "last_updated": "2021-05-03T12:00:13.531977+00:00",    "context": {        "id": "f76ffaab25fc0e7d2581aefad64ef866",        "parent_id": null,        "user_id": null    }}'
    print(state)
    json_state = json.loads(state.decode('utf8').replace("'", '"'))
    print(json_state)
