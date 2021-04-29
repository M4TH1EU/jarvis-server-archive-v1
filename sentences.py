import random

# from main import speak
import pyttsx3

import homeassistant.lights
import homeassistant.spotify

hotwordDetection = ["john", "hey john"]
yesSir = ["Oui monsieur?", "Oui?", "Que puis-je faire pour vous?", "Que puis-je faire pour vous monsieur?"]

howAreYouDetection = ["comment ca va", "ca va"]
allGoodSir = ["Je vais bien monsieur.", "Tout va bien", "Tout va bien monsieur", "Je vais bien merci"]

dontUnderstand = ["Je suis désolé, je n'ai pas compris", "Je ne suis pas sur de comprendre votre de demande.",
                  "Je n'ai pas compris votre demande"]

turnOnLightsDetection = ["allume la lumière", "allume les lumières"]
turnOffLightsDetection = ["éteint la lumière", "éteint les lumières"]
turningOnLights = ["J'allume les lumières", "J'allume la lumière", "Les lumières s'allument monsieur"]
turningOffLights = ["J'éteinds les lumières", "J'éteinds la lumière", "Les lumières s'éteignent monsieur"]

turnOnLedsDetection = ["allume les leds", "allume les bandes leds"]
turnOffLedsDetection = ["éteint les leds", "éteint les bandes leds"]

nextTrackDetection = ["morceau suivant", "mets le morceau suivant", "joue le titre suivant", "joue le morceau suivant"]
previousTrackDetection = ["morceau précédent", "mets le morceau précédent", "joue le titre précédent",
                          "joue le morceau précédent", "rejoue le morceau précédent"]
nextTrack = ["Voici le morceau suivant monsieur", "Voici le morceau suivant", "Je passe cette chanson",
             "Morceau suivant"]
previousTrack = ["Voici le morceau précédent", "Voici le morceau précédent monsieur", "Voilà le morceau précédent"]


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
    engine.setProperty('voice', voices[0].id)  # Gender and type of voice
    engine.setProperty('rate', rate + 50)  # Adjusts the rate of speech
    engine.say(text)  # tells Python to speak variable 'text'
    engine.runAndWait()  # waits for speech to finish and then continues with program
