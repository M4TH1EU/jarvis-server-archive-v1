import json
import threading

import requests as requests

import homeassistant.homeassistant
import homeassistant.lights
import plugins.alarms


def check_if_lights_are_on_but_not_home(minutes, lights_id, person_id, mobile_app_id):
    if not homeassistant.homeassistant.is_home(person_id):
        if homeassistant.lights.is_on(lights_id):
            homeassistant.homeassistant.send_notification(mobile_app_id,
                                                          'Les lumières sont allumées.',
                                                          'Une ou plusieurs lampes sont toujours allumées alors que vous n\'êtes pas à la maison...',
                                                          action1=['TURNOFFLIGHTS', 'Éteindre'])

    timer = threading.Timer(minutes * 60, check_if_lights_are_on_but_not_home,
                            [minutes, lights_id, person_id, mobile_app_id])
    timer.start()


def check_if_there_is_an_alarm(minutes, person_id):
    if homeassistant.homeassistant.is_home(person_id):
        if plugins.alarms.check():
            # play song
            print("MUSIC MAESTRO")
    timer = threading.Timer(minutes * 60, check_if_there_is_an_alarm, [minutes])
    timer.start()


def check_temperature(minutes, entity_id, mobile_app_id):
    entity_state = json.loads(homeassistant.homeassistant.get_state(entity_id))
    temperature = int(float(entity_state['state']))
    if temperature >= 85:
        friendly_name = entity_state['attributes']['friendly_name']
        homeassistant.homeassistant.send_notification(mobile_app_id,
                                                      'La température est trop haute',
                                                      'La température de ' + friendly_name + ' est trop haute (' +
                                                      str(temperature) + '°C)!')
    timer = threading.Timer(minutes * 60, check_temperature, [minutes, entity_id])
    timer.start()


def check_if_eth_miner_is_offline(minutes, mobile_app_id):
    json_data = json.loads(
        requests.get("https://api.ethermine.org/miner/1C169a48601EC3D342Be36A26F5B387DC8d2155C/dashboard").text)
    active_workers = json_data['data']['currentStatistics']['activeWorkers']
    if active_workers == 1:
        homeassistant.homeassistant.send_notification(mobile_app_id,
                                                      'Un PC de minage est éteint.',
                                                      'Un PC ne mine plus d\'ETH, à controller au plus vite.')
    elif active_workers == 0:
        homeassistant.homeassistant.send_notification(mobile_app_id,
                                                      'Les PC de minage sont éteint.',
                                                      'Les PC ne minent plus d\'ETH, à controller immédiatement!')

    timer = threading.Timer(minutes * 60, check_if_eth_miner_is_offline, [minutes])
    timer.start()


def register():
    check_if_lights_are_on_but_not_home(60, 'light.lumieres_chambre', 'person.mathieu', 'mobile_app_oneplus_8t')
    check_if_there_is_an_alarm(1, 'person.mathieu')
    check_if_eth_miner_is_offline(20, 'mobile_app_oneplus_8t')
    check_temperature(2, 'sensor.processor_temperature', 'mobile_app_oneplus_8t')
    check_temperature(2, 'sensor.tour_mathieu_amd_ryzen_7_3700x_temperatures_cpu_package', 'mobile_app_oneplus_8t')
    check_temperature(2, 'sensor.tour_mathieu_nvidia_nvidia_geforce_rtx_3070_temperatures_gpu_core',
                      'mobile_app_oneplus_8t')
