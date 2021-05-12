import json
import threading

import requests as requests

import homeassistant.homeassistant
import homeassistant.lights
import plugins.alarms


def check_if_lights_are_on_but_not_home(minutes):
    if not homeassistant.homeassistant.is_home('person.mathieu'):
        if homeassistant.lights.is_on('light.lumieres_chambre'):
            homeassistant.homeassistant.sendNotification('mobile_app_oneplus_8t',
                                                         'Les lumières sont allumées.',
                                                         'Une ou plusieurs lampes sont toujours allumées alors que vous n\'êtes pas à la maison...',
                                                         action1=['TURNOFFLIGHTS', 'Éteindre'])

    timer = threading.Timer(minutes * 60, check_if_lights_are_on_but_not_home, [minutes])
    timer.start()


def check_if_there_is_an_alarm(minutes):
    if homeassistant.homeassistant.is_home('person.mathieu'):
        if plugins.alarms.check():
            # play song
            print("MUSIC MAESTRO")
    timer = threading.Timer(minutes * 60, check_if_there_is_an_alarm, [minutes])
    timer.start()


def check_temperature(minutes, entity_id):
    entity_state = json.loads(homeassistant.homeassistant.getState(entity_id))
    temperature = int(float(entity_state['state']))
    if temperature >= 85:
        friendly_name = entity_state['attributes']['friendly_name']
        homeassistant.homeassistant.sendNotification('mobile_app_oneplus_8t',
                                                     'La température est trop haute',
                                                     'La température de ' + friendly_name + ' est trop haute (' +
                                                     str(temperature) + '°C)!')
    timer = threading.Timer(minutes * 60, check_temperature, [minutes, entity_id])
    timer.start()


def check_if_eth_miner_is_offline(minutes):
    json_data = json.loads(
        requests.get("https://api.ethermine.org/miner/1C169a48601EC3D342Be36A26F5B387DC8d2155C/dashboard").text)
    active_workers = json_data['data']['currentStatistics']['activeWorkers']
    if active_workers == 1:
        homeassistant.homeassistant.sendNotification('mobile_app_oneplus_8t',
                                                     'Un PC de minage est éteint.',
                                                     'Un PC ne mine plus d\'ETH, à controller au plus vite.')
    elif active_workers == 0:
        homeassistant.homeassistant.sendNotification('mobile_app_oneplus_8t',
                                                     'Les PC de minage sont éteint.',
                                                     'Les PC ne minent plus d\'ETH, à controller immédiatement!')

    timer = threading.Timer(minutes * 60, check_if_eth_miner_is_offline, [minutes])
    timer.start()


def register():
    check_if_lights_are_on_but_not_home(60)
    check_if_there_is_an_alarm(1)
    check_if_eth_miner_is_offline(20)
    check_temperature(2, 'sensor.processor_temperature')
    check_temperature(2, 'sensor.tour_mathieu_amd_ryzen_7_3700x_temperatures_cpu_package')
    check_temperature(2, 'sensor.tour_mathieu_nvidia_nvidia_geforce_rtx_3070_temperatures_gpu_core')
