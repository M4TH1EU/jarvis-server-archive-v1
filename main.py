"""variables"""
import time

import speech_recognition as sr

import sentences

r = sr.Recognizer()
r.energy_threshold = 1
keywords = [("hey john", 1), ("john", 1), ]
source = sr.Microphone()

"""Functions"""


def listen(recognizer, audio):
    try:
        speech_as_text = recognizer.recognize_sphinx(
            audio, keyword_entries=keywords)
        print(speech_as_text)
        if "hey john" in speech_as_text or "john":
            sentences.answer('yesSir')  # answer with something like "yes sir ?"
            recognize_main()  # starts listening for your sentence
    except sr.UnknownValueError:
        print("Oops! Didn't catch that")


def start_listening_for_hotword():  # initial keyword call
    print("Waiting for a keyword...")  # Prints to screen
    r.listen_in_background(source, listen)  # Sets off recognition sequence
    time.sleep(1000000)  # keeps loop running


def recognize_main():  # Main reply call function
    r = sr.Recognizer()
    print("Dites quelques chose!")
    audio = r.listen(source)
    data = ""

    try:
        # now uses Google speech recognition
        data = r.recognize_google(audio, language="fr-FR")
        # data = input("Entrez phrase : ")
        data = data.lower()  # makes all voice entries show as lower case
        # shows what user said and what was recognised
        # print("Vous avez dit: " + data)

        sentences.recogniseSentence(data)
        print("finish")
    except sr.UnknownValueError:
        print("John n'a pas compris votre demande")
        print(data)
    except sr.RequestError as e:  # if you get a request error from Google speech engine
        print(
            "Erreur du service Google Speech Recognition ; {0}".format(e))


"""Main program"""
while 1:  # This starts a loop so the speech recognition is always listening to you
    sentences.registerSentences()
    start_listening_for_hotword()
