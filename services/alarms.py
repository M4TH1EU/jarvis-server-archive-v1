import os
import pickle
from datetime import datetime

alarms_file = (os.path.dirname(__file__).replace("\\services", "") + '\\config\\alarms')


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
