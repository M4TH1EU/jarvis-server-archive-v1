import time

import requests

import clientUtils


def random(data):
    # the token used might be revoked at any time, please register on www.blagues-api.fr and replace it
    response = requests.get(
        'https://www.blagues-api.fr/api/random',
        headers={
            'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNzA4OTcyNzQwOTQ5ODM1ODI2IiwibGltaXQiOjEwMCwia2V5IjoiYmZlUVBSb2xuY2FleHBHc2taRU90VkdKOGxhdWZsZVRSMFJadnR3QXV3c056djdpYlkiLCJjcmVhdGVkX2F0IjoiMjAyMS0wNS0yOVQxNDoyMjo0MCswMDowMCIsImlhdCI6MTYyMjI5ODE2MH0.6VxH_dTdJSddhHoYOtdQl0j9WC3lzXjUujUio5U09Jg'
        }
    )
    data = response.json()
    joke = data['joke']
    answer = data['answer']

    clientUtils.speak(joke)
    time.sleep(2)

    return answer
