import os
import pickle
from datetime import datetime, time

import intents.intents

alarms_file = (os.path.dirname(__file__).replace("\\services", "") + '\\config\\alarms')


def create_alarm(sentence):
    spoke_time = "7h30"
    # TODO: get the day and the hour in the sentence
    spoke_time = spoke_time.replace("demain", "").replace("matin", "").replace(" ", "")

    hours = spoke_time.split("h")[0]
    minutes = spoke_time.split("h")[1]

    spoke_time = time(hour=int(hours), minute=int(minutes))
    time_formatted = spoke_time.strftime("%H:%M")

    add_alarm(time_formatted)

    return intents.intents.get_random_response_for_tag('alarm').replace("%time", time_formatted)


def check():
    current_time = datetime.now().strftime("%H:%M")
    if current_time in get_alarms():
        return True
    else:
        return False


def get_alarms():
    return read_alarms()


def add_alarm(time):
    alarms = get_alarms()
    alarms.append(time)
    write_alarms(alarms)


def read_alarms():
    if not os.path.exists(alarms_file):
        write_alarms([])

    infile = open(alarms_file, 'rb')
    alarms = pickle.load(infile)
    infile.close()
    return alarms


def write_alarms(alarms):
    outfile = open(alarms_file, 'wb')
    pickle.dump(alarms, outfile)
    outfile.close()
