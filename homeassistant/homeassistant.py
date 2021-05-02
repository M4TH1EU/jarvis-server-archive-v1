import os

import requests
from requests.structures import CaseInsensitiveDict

token = os.getenv('HOMEASSISTANT_API_TOKEN')  # long-term token
ha_url = os.getenv('HOMEASSISTANT_API_URL')  # https://my.homeassistant.com/api/


def callService(data, service):
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
        headers["Content-Type"] = "application/json"

        requests.post(url_service, headers=headers, data=data)
    except:
        print("Error when calling HomeAssistant API")


def getState(entity_id):
    """
        Retrieve the state of an entity (GET) on the HA API with a given payload

        Parameters
        ----------
        entity_id : str
        """

    try:
        url_service = ha_url + "states/" + entity_id
        headers = CaseInsensitiveDict()
        headers["Authorization"] = 'Bearer ' + token
        headers["Content-Type"] = "application/json"

        return requests.get(url_service, headers=headers).content
    except:
        print("Error when calling HomeAssistant API")
        return ""
