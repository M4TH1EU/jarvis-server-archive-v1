"""variables"""
import time

import pyttsx3
import speech_recognition as sr

import sentences

r = sr.Recognizer()
r.energy_threshold = 1000
keywords = [("hey john", 1), ("john", 1), ]
source = sr.Microphone()

"""Functions"""


def speak(text):
    rate = 100  # Sets the default rate of speech
    engine = pyttsx3.init()  # Initialises the speech engine
    voices = engine.getProperty('voices')  # sets the properties for speech
    engine.setProperty('voice', voices[0].id)  # Gender and type of voice
    engine.setProperty('rate', rate + 50)  # Adjusts the rate of speech
    engine.say(text)  # tells Python to speak variable 'text'
    engine.runAndWait()  # waits for speech to finish and then continues with program


def listen(recognizer, audio):
    try:
        # speech_as_text = recognizer.recognize_sphinx(
        #    audio, keyword_entries=keywords)
        speech_as_text = "john"
        print(speech_as_text)
        if "hey john" in speech_as_text or "john":
            sentences.recogniseSentence(speech_as_text)  # answer with something like "yes sir ?"
            recognize_main()  # starts listening for your sentence
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")


def start_listening_for_hotword():  # initial keyword call
    print("Waiting for a keyword...")  # Prints to screen
    r.listen_in_background(source, listen)  # Sets off recognition sequence
    time.sleep(1000000)  # keeps loop running


def recognize_main():  # Main reply call function
    # r = sr.Recognizer()  # sets r variable
    # with sr.Microphone() as source:  # sets microphone
    #    print("Dites quelques chose!")  # prints to screen
    #    audio = r.listen(source)  # sets variable 'audio'

    data = ""  # assigns user voice entry to variable 'data'
    try:
        # now uses Google speech recognition
        # data = r.recognize_google(audio, language="fr-FR")
        data = input("Entrez phrase : ")
        data = data.lower()  # makes all voice entries show as lower case
        # shows what user said and what was recognised
        # print("Vous avez dit: " + data)

        sentences.recogniseSentence(data)

    except sr.UnknownValueError:  # whenever you have a try statement you have an exception rule
        print("John n'a pas compris votre demande")
        print(data)
    except sr.RequestError as e:  # if you get a request error from Google speech engine
        print(
            "Erreur du service Google Speech Recognition ; {0}".format(e))


"""Main program"""
while 1:  # This starts a loop so the speech recognition is always listening to you
    start_listening_for_hotword()
