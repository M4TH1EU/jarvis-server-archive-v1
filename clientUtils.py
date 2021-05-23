import json
import os

import requests
from requests.structures import CaseInsensitiveDict

client_url = "http://127.0.0.1:5001"
token = os.getenv('JARVIS_API_KEY')


def ask_for_microphone_output(record_for_seconds, speech_before_input):
    data = {
        'record_for_seconds': record_for_seconds,
        'speech_before_input': speech_before_input
    }

    call_client_api("POST", "/record", json.dumps(data))


def ask_for_input(listen_for_seconds, speech_before_input):
    data = {
        'listen_for_seconds': listen_for_seconds,
        'speech_before_input': speech_before_input
    }

    call_client_api("POST", "/input", json.dumps(data))


def speak(speech):
    data = {
        'speech': speech
    }
    call_client_api("POST", "/speak", data)


def sound(sound_name):
    data = {
        'sound_name': sound_name
    }
    call_client_api("POST", "/sound", data)


def call_client_api(method, url, json_data=None):
    if json_data is None:
        json_data = {}

    try:
        url_service = client_url + url

        headers = CaseInsensitiveDict()
        headers["Authorization"] = token
        headers["Content-Type"] = "application/json; charset=utf8"

        if method == 'GET':
            return json.loads(requests.get(url_service, headers=headers).content.decode("utf-8"))
        elif method == 'POST':
            json_data = json.dumps(json_data)
            return json.loads(
                requests.post(url_service, headers=headers, data=json_data.encode("utf8")).content.decode("utf-8"))
    except:
        print("Error when calling the client API")
