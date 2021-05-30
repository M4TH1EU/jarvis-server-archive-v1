import json
from datetime import datetime

import intents.intents
from homeassistant.homeassistant import get_state

conditions = {"clear-night": "étoillé",
              "cloudy": "nuageux",
              "fog": "brumeux",
              "hail": "pluvieux avec quelques passages de grêles",
              "lightning": "orageux",
              "lightning-rainy": "orageux",
              "partlycloudy": "partiellement nuageux",
              "pouring": "pluvieux",
              "rainy": "pluvieux",
              "snowny": "neigeux",
              "snowny-rainy": "neigeux avec quelques passage de pluie",
              "sunny": "ensoleillé",
              "windy": "venteux",
              "exceptional": "exceptionnel"
              }


def get_temperature(entity_id):
    return str(int(get_attribute(entity_id, 'temperature'))) + "°"


def get_temperature_low(entity_id):
    today_date = datetime.today().date().strftime("%Y-%m-%d")
    return str(int(get_attribute_for_day(entity_id, 'templow', today_date))) + "°"


def get_condition(entity_id):
    return conditions.get(json.loads(get_state(entity_id))['state'])


def get_low_temp(entity_id):
    # TODO : investigate why no templow for today's day
    # return str(int(get_attribute(entity_id, 'templow'))) + "°"
    return "0°"


def get_wind_speed(entity_id):
    return int(get_attribute(entity_id, 'wind_speed'))


def get_humidity(entity_id):
    return get_attribute(entity_id, 'humidity')


def get_wind_bearing(entity_id):
    return get_attribute(entity_id, 'wind_bearing')


def get_attribute(entity_id, name):
    """

    Parameters
    ----------
    entity_id : entity id from home assistant
    name : temperature, humidity, pressure, wind_bearing, wind_speed

    Returns
    -------

    The value of the given attribute

    """
    state = get_state(entity_id)
    json_state = json.loads(state)
    return json_state['attributes'][name]


def get_temperature_for_day(entity_id, day_date):
    return str(int(get_attribute_for_day(entity_id, 'temperature', day_date))), "°"


def get_condition_for_day(entity_id, day_date):
    return conditions.get(get_attribute_for_day(entity_id, 'condition', day_date))


def get_temperature_low_for_day(entity_id, day_date):
    return str(int(get_attribute_for_day(entity_id, 'templow', day_date))) + "°"


def get_attribute_for_day(entity_id, name, day_date):
    """

    Parameters
    ----------
    entity_id
    name : templow, temperature, condition
    day_date : 2021-01-28

    Returns
    -------

    """
    state = get_state(entity_id)
    forecast_array = json.loads(state)['attributes']['forecast']

    for forecast in forecast_array:
        if forecast['datetime'] == day_date:
            return forecast[name]

    return 0


def summary(data):
    """
        Return a random sentence from the weather tag with replaced keywords (temps, wind, etc.)
        Parameters
        ----------
        data: dict

        Returns
        -------
        str
        """

    if 'entity_id' in data:
        # today_date = date.today().strftime("%Y-%m-%d")
        today_hour = datetime.now().hour

        entity_id = data.get('entity_id')

        sera = "est"
        faire = "fait"

        if today_hour <= 10:
            sera = "sera"
            faire = "fera"

        sentence_weather = intents.intents.get_random_response_for_tag('weather')
        sentence_weather = sentence_weather.replace('&sera', sera)
        sentence_weather = sentence_weather.replace('&faire', faire)
        sentence_weather = sentence_weather.replace('%condition', get_condition(entity_id))
        sentence_weather = sentence_weather.replace('%temperature', get_temperature(entity_id))
        sentence_weather = sentence_weather.replace('%lowtemp', get_low_temp(entity_id))

        wind_speed = int(get_wind_speed(entity_id))

        if wind_speed < 8:
            wind_speed_words = "très faible"
        elif wind_speed < 20:
            wind_speed_words = "calme"
        elif wind_speed < 30:
            wind_speed_words = "agité"
        elif wind_speed < 45:
            wind_speed_words = "fort"
        elif wind_speed < 60:
            wind_speed_words = "très fort"
        elif wind_speed < 80:
            wind_speed_words = "destructeur"
        elif wind_speed < 200:
            wind_speed_words = "massivement destructeur et mortel"
        else:
            wind_speed_words = "non défini"

        sentence_weather = sentence_weather.replace('%wind_speed_words', wind_speed_words)
        sentence_weather = sentence_weather.replace('%wind_speed', str(wind_speed) + ' kilomètres heure')

        return sentence_weather
    else:
        raise Exception("weather.summary needs an entity_id")
