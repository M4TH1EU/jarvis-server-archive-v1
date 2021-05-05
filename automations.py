import threading

import homeassistant.homeassistant
import homeassistant.lights


def check_if_lights_are_on_but_not_home(minutes):
    if homeassistant.homeassistant.is_home('person.mathieu'):
        if homeassistant.lights.is_on('lumieres_chambre'):
            homeassistant.homeassistant.sendNotification('mobile_app_oneplus_8t', "", "")

    timer = threading.Timer(minutes*60, check_if_lights_are_on_but_not_home, [minutes])
    timer.start()
