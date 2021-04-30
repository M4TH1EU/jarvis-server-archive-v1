import random

import openpyxl
# from main import speak
import pyttsx3

import homeassistant.lights
import homeassistant.spotify

wb = openpyxl.load_workbook('Sentences.xlsx')
sheet = wb.get_sheet_by_name('Sentences')

for x in range(1, 9):
    print(x, sheet.cell(row=1, column=1).value)


def answer(answers):
    speak(random.choice(answers))
    print(random.choice(answers))


def recogniseSentence(sentence):
    # hey john
    if sentence in hotwordDetection:
        answer(yesSir)

    # comment ça va
    elif sentence in howAreYouDetection:
        answer(allGoodSir)

    # allume la lumière
    elif sentence in turnOnLightsDetection:
        answer(turningOnLights)
        homeassistant.lights.turnOn("light.lumieres_chambre")

    # éteint la lumière
    elif sentence in turnOffLightsDetection:
        answer(turningOffLights)
        homeassistant.lights.turnOff("light.lumieres_chambre")

    # allume les leds
    elif sentence in turnOnLedsDetection:
        answer(turningOffLights)
        homeassistant.lights.turnOn("light.leds_chambre")

    # éteint les leds
    elif sentence in turnOffLedsDetection:
        answer(turningOffLights)
        homeassistant.lights.turnOff("light.leds_chambre")

    # mets le morceau suivant
    elif sentence in nextTrackDetection:
        answer(nextTrack)
        homeassistant.spotify.nextTrack("media_player.spotify_mathieu_broillet")

    # mets le morceau précédent
    elif sentence in previousTrackDetection:
        homeassistant.spotify.nextTrack("media_player.spotify_mathieu_broillet")
        answer(previousTrack)

    else:
        answer(dontUnderstand)


def speak(text):
    rate = 100  # Sets the default rate of speech
    engine = pyttsx3.init()  # Initialises the speech engine
    voices = engine.getProperty('voices')  # sets the properties for speech
    engine.setProperty('voice', voices[0].sentencesId)  # Gender and type of voice
    engine.setProperty('rate', rate + 50)  # Adjusts the rate of speech
    engine.say(text)  # tells Python to speak variable 'text'
    engine.runAndWait()  # waits for speech to finish and then continues with program
