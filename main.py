"""variables"""
import struct
import time

import pvporcupine
import pyaudio
import speech_recognition as sr

import sentences

porcupine = None
pa = None
audio_stream = None
r = sr.Recognizer()

source = sr.Microphone()

"""Functions"""


def listen(recognizer, audio):
    try:
        porcupine = pvporcupine.create(keywords=['jarvis'])
        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)

            if keyword_index >= 0:
                sentences.answer('yesSir')  # answer with something like "yes sir ?"
                recognize_main()  # starts listening for your sentence

    except:
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
