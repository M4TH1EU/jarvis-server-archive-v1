import json

from homeassistant.homeassistant import getState


def getTemperature(entity_id):
    return getAttribute(entity_id, 'temperature')

def getTemperatureLow(entity_id):
    return getAttribute(entity_id, 'templow')


def getCondition(entity_id):
    return getAttribute(entity_id, 'condition')


def getLowTemp(entity_id):
    return getAttribute(entity_id, 'templow')


def getWindSpeed(entity_id):
    return getAttribute(entity_id, 'wind_speed')


def getHumidity(entity_id):
    return getAttribute(entity_id, 'humidity')


def getWindBearing(entity_id):
    return getAttribute(entity_id, 'wind_bearing')


def getWindSpeed(entity_id):
    return getAttribute(entity_id, 'wind_speed')


def getAttribute(entity_id, name):
    """

    Parameters
    ----------
    entity_id : entity id from home assistant
    name : temperature, humidity, pressure, wind_bearing, wind_speed

    Returns
    -------

    The value of the given attribute

    """
    state = getState(entity_id)
    state = '{    "entity_id": "weather.bussigny_sur_oron",    "state": "sunny",    "attributes": {        "temperature": 8.9,        "humidity": 58,        "pressure": 925.6,        "wind_bearing": "WSW",        "wind_speed": 8.6,        "attribution": "Weather forecast from MeteoSwiss (https://www.meteoswiss.admin.ch/)",        "forecast": [            {                "datetime": "2021-05-04",                "templow": 4,                "temperature": 15,                "condition": "rainy"            },            {                "datetime": "2021-05-05",                "templow": 6,                "temperature": 11,                "condition": "rainy"            },            {                "datetime": "2021-05-06",                "templow": 4,                "temperature": 11,                "condition": "rainy"            },            {                "datetime": "2021-05-07",                "templow": 6,                "temperature": 11,                "condition": "rainy"            },            {                "datetime": "2021-05-08",                "templow": 5,                "temperature": 18,                "condition": "sunny"            }        ],        "friendly_name": "Bussigny-sur-Oron"    },    "last_changed": "2021-05-03T07:57:13.828170+00:00",    "last_updated": "2021-05-03T12:00:13.531977+00:00",    "context": {        "id": "f76ffaab25fc0e7d2581aefad64ef866",        "parent_id": null,        "user_id": null    }}'
    json_state = json.loads(state)
    return json_state['attributes'][name]


def getTemperatureForDay(entity_id, day_date):
    return getAttributeForDay(entity_id, 'temperature', day_date)


def getConditionForDay(entity_id, day_date):
    return getAttributeForDay(entity_id, 'condition', day_date)


def getTemperatureLowForDay(entity_id, day_date):
    return getAttributeForDay(entity_id, 'templow', day_date)


def getAttributeForDay(entity_id, name, day_date):
    """

    Parameters
    ----------
    entity_id
    name : templow, temperature, condition
    day_date : 2021-01-28

    Returns
    -------

    """
    state = getState(entity_id)
    state = '{    "entity_id": "weather.bussigny_sur_oron",    "state": "sunny",    "attributes": {        "temperature": 8.9,        "humidity": 58,        "pressure": 925.6,        "wind_bearing": "WSW",        "wind_speed": 8.6,        "attribution": "Weather forecast from MeteoSwiss (https://www.meteoswiss.admin.ch/)",        "forecast": [            {                "datetime": "2021-05-04",                "templow": 4,                "temperature": 15,                "condition": "rainy"            },            {                "datetime": "2021-05-05",                "templow": 6,                "temperature": 11,                "condition": "rainy"            },            {                "datetime": "2021-05-06",                "templow": 4,                "temperature": 11,                "condition": "rainy"            },            {                "datetime": "2021-05-07",                "templow": 6,                "temperature": 11,                "condition": "rainy"            },            {                "datetime": "2021-05-08",                "templow": 5,                "temperature": 18,                "condition": "sunny"            }        ],        "friendly_name": "Bussigny-sur-Oron"    },    "last_changed": "2021-05-03T07:57:13.828170+00:00",    "last_updated": "2021-05-03T12:00:13.531977+00:00",    "context": {        "id": "f76ffaab25fc0e7d2581aefad64ef866",        "parent_id": null,        "user_id": null    }}'
    forecast_array = json.loads(state)['attributes']['forecast']

    for forecast in forecast_array:
        if forecast['datetime'] == day_date:
            return forecast[name]

    return 0
