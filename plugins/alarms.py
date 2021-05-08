import os
import pickle

alarms_file = (os.path.dirname(__file__).replace("\\plugins", "") + '\\config\\alarms')


def getAlarms():
    return readAlarms()


def addAlarm(time):
    alarms = getAlarms()
    print(alarms)
    alarms.append(str(time))
    print(alarms)

    writeAlarms(alarms)
    # set


def readAlarms():
    if not os.path.exists(alarms_file):
        writeAlarms([])

    infile = open(alarms_file, 'rb')
    alarms = pickle.load(infile)
    infile.close()
    return alarms


def writeAlarms(alarms):
    outfile = open(alarms_file, 'wb')
    pickle.dump(alarms, outfile)
    outfile.close()