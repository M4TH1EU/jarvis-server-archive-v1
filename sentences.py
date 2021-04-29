import random

# from main import speak
import homeassistant.lights

yesSir = ["Oui monsieur?",
          "Oui?",
          "Que puis-je faire pour vous?",
          "Que puis-je faire pour vous monsieur?"]

allGoodSir = ["Je vais bien monsieur.",
              "Tout va bien",
              "Tout va bien monsieur",
              "Je vais bien merci"]

dontUnderstand = ["Je suis désolé, je n'ai pas compris",
                  "Je ne suis pas sur de comprendre votre de demande.",
                  "Je n'ai pas compris votre demande"]

turningOnLights = ["J'allume les lumières", "J'allume la lumière", "Les lumières s'allument monsieur"]
turningOffLights = ["J'éteinds les lumières", "J'éteinds la lumière", "Les lumières s'éteignent monsieur"]


def answer(answers):
    # speak(random.choice(answers))
    print(random.choice(answers))


def recogniseSentence(sentence):
    if sentence in ("john", "hey john"):
        answer(yesSir)
    elif sentence in ("comment ca va", "ca va"):
        answer(allGoodSir)
    elif sentence in ("allume la lumière", "allume les lumières"):
        homeassistant.lights.turnOn("light.lumieres_chambre")
        answer(turningOnLights)
    elif sentence in ("éteint la lumière", "éteint les lumières"):
        homeassistant.lights.turnOff("light.lumieres_chambre")
        answer(turningOffLights)
    elif sentence in ("allume les leds", "allume les bandes leds"):
        homeassistant.lights.turnOn("light.leds_chambre")
        answer(turningOffLights)
    elif sentence in ("éteint les leds", "éteint les bandes leds"):
        homeassistant.lights.turnOff("light.leds_chambre")
        answer(turningOffLights)
    else:
        answer(dontUnderstand)
