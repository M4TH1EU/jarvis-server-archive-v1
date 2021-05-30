import json
import os

import requests
from homeassistant_api import Client
from requests.structures import CaseInsensitiveDict

token = os.getenv('HOMEASSISTANT_API_TOKEN')  # long-term token
ha_url = os.getenv('HOMEASSISTANT_API_URL')  # https://my.homeassistant.com/api/
client = Client(ha_url, token)
service_domains = client.get_services()


def call_api(domain, service, data):
    """
    Used to call homeassistant api
    Parameters
    ----------
    domain: str (ex. light or media_player)
    service: str (ex. turn_on or toggle)
    data: dict

    Returns
    -------

    """

    service_domains.__getattribute__(domain).services.__getattribute__(service).trigger(**data)


def call_service(data, service):
    """
    Call a specific service (POST) on the HA API with a given payload

    Parameters
    ----------
    data : str
    service : str

    Examples
    ----------
    payload : {"entity_id": "light.bathroom" }
    service : light/turn_on
    """

    try:
        url_service = ha_url + "services/" + service
        headers = CaseInsensitiveDict()
        headers["Authorization"] = 'Bearer ' + token
        headers["Content-Type"] = "application/json; charset=utf8"

        requests.post(url_service, headers=headers, data=data.encode("utf8"))
    except:
        print("Error when calling HomeAssistant API")


def get_state(entity_id):
    """
        Retrieve the state of an entity on the HA API

        Parameters
        ----------
        entity_id : str
        """

    return client.get_entity(entity_id)


def send_notification(device, title, message, action1=None, action2=None, action3=None):
    data = {
        'message': message,
        'title': title,
        'data': {
            'actions': [
                {}, {}, {}
            ]
        }
    }

    if action1 is not None:
        data['data']['actions'][0]['action'] = action1[0]
        data['data']['actions'][0]['title'] = action1[1]
        if 2 < len(action1):
            data['data']['actions'][0]['uri'] = action1[2]

    if action2 is not None:
        data['data']['actions'][1]['action'] = action2[0]
        data['data']['actions'][1]['title'] = action2[1]
        if 2 < len(action2):
            data['data']['actions'][1]['uri'] = action2[2]

    if action3 is not None:
        data['data']['actions'][2]['action'] = action3[0]
        data['data']['actions'][2]['title'] = action3[1]
        if 2 < len(action3):
            data['data']['actions'][2]['uri'] = action3[2]

    call_api("notify", device, **{"data": data})


def is_home(entity_id):
    return get_state(entity_id).state == 'home'
