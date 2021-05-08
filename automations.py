import threading

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


def register():
    check_if_lights_are_on_but_not_home(60)
    check_if_there_is_an_alarm(1)
