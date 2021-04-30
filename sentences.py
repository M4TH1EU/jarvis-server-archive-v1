import random
import csv
import openpyxl
# from main import speak
import pyttsx3

import homeassistant.lights
import homeassistant.spotify

sentences = {}

def registerSentences():
    # our csv file and a csv reader (encoded in utf8 for special character compatibility)
    csv_file = open('Sentences.csv', encoding="utf-8")
    csv_reader = csv.reader(csv_file, delimiter='|')

    # column number and id(s)
    column = 0
    sentencesId = csv_file.readline().split("|")

    # for every line in our .csv file
    for lines in csv_reader:

        # for every hotwords in our .csv file (based on first line)
        for sentenceId in sentencesId:

            # if there some empty "fake" column then don't try to register them
            if 'Column' in sentenceId:
                break
            else:
                # fix an issue with first id
                sentenceId = sentenceId.replace('\ufeff', '')

                # creating an entry to be able to use .append afterward
                if sentenceId not in sentences:
                    sentences[sentenceId] = []

                # if the entry is not empty then add it to the sentences dict
                if lines[column] != "":
                    sentences[sentenceId].append(lines[column])

            # increment column
            column = column + 1

        # reset column
        column = 0


def checkAndAnswer(sentence, sentence_id):
    if sentence in getSentences(sentence_id):
        speak(random.choice(getSentences(sentence_id)))
        print(random.choice(getSentences(sentence_id)))


def getSentences(sentence_id):
    return sentences[sentence_id]


def recogniseSentence(sentence):
    # hey john
    if sentence in getSentences('hotwordDetection'):
        checkAndAnswer('hotwordDetection')

    # comment ça va
    elif sentence in howAreYouDetection:
        checkAndAnswer(allGoodSir)

    # allume la lumière
    elif sentence in turnOnLightsDetection:
        checkAndAnswer(turningOnLights)
        homeassistant.lights.turnOn("light.lumieres_chambre")

    # éteint la lumière
    elif sentence in turnOffLightsDetection:
        checkAndAnswer(turningOffLights)
        homeassistant.lights.turnOff("light.lumieres_chambre")

    # allume les leds
    elif sentence in turnOnLedsDetection:
        checkAndAnswer(turningOffLights)
        homeassistant.lights.turnOn("light.leds_chambre")

    # éteint les leds
    elif sentence in turnOffLedsDetection:
        checkAndAnswer(turningOffLights)
        homeassistant.lights.turnOff("light.leds_chambre")

    # mets le morceau suivant
    elif sentence in nextTrackDetection:
        checkAndAnswer(nextTrack)
        homeassistant.spotify.nextTrack("media_player.spotify_mathieu_broillet")

    # mets le morceau précédent
    elif sentence in previousTrackDetection:
        homeassistant.spotify.nextTrack("media_player.spotify_mathieu_broillet")
        checkAndAnswer(previousTrack)

    else:
        checkAndAnswer(dontUnderstand)


def speak(text):
    rate = 100  # Sets the default rate of speech
    engine = pyttsx3.init()  # Initialises the speech engine
    voices = engine.getProperty('voices')  # sets the properties for speech
    engine.setProperty('voice', voices[0].sentencesId)  # Gender and type of voice
    engine.setProperty('rate', rate + 50)  # Adjusts the rate of speech
    engine.say(text)  # tells Python to speak variable 'text'
    engine.runAndWait()  # waits for speech to finish and then continues with program
