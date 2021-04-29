import requests
from requests.structures import CaseInsensitiveDict

token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiI3NWIzNDMyYTQ2NDI0ZWU1YWJiNTc3OTk0M2RhZTg1MSIsImlhdCI6MTYxOTY4Njc2NywiZXhwIjoxOTM1MDQ2NzY3fQ.uR-SfCKJiDqm4NzIWR9rgQ8lAzQAWcm_yj3_PE9tVeQ"
ha_url = "https://homeassistant.broillet.org/api/"


def callApiPost(data, service):
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

    url_service = ha_url + "services/" + service
    headers = CaseInsensitiveDict()
    headers["Authorization"] = 'Bearer ' + token
    headers["Content-Type"] = "application/json"

    requests.post(url_service, headers=headers, data=data)
