"""variables"""
import struct
import sys
import time

import pvporcupine
import pyaudio
import speech_recognition as sr

import automations
import sentences

no_voice_mode = False

# to avoid permission denied errors (enable when non developping)
# elevate()

"""Functions"""


def listen():
    if no_voice_mode:
        recognize_main()  # starts listening for your sentence
    else:
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

        except Exception as e:
            print("Oops! Une erreur est survenue/je n'ai pas compris")
            print(e)
            # start_listening_for_hotword()


def start_listening_for_hotword():  # initial keyword call
    print("Waiting for a keyword...")  # Prints to screen
    listen()
    time.sleep(1000000)  # keeps loop running


def recognize_main():  # Main reply call function
    r = sr.Recognizer()

    with sr.Microphone(device_index=0) as source:
        try:
            if no_voice_mode:
                data = input("Entrez phrase : ").lower()
            else:
                audio = r.listen(source, timeout=3, phrase_time_limit=(7 if not no_voice_mode else 1))

                # now uses Google speech recognition
                data = r.recognize_google(audio, language="fr-FR")
                data = data.lower()  # makes all voice entries show as lower case

            print("DATA : " + data)

            # add support for multiples actions in one sentence (two actions here)
            if " et " in data:
                phrases = data.split(" et ")
                sentences.recogniseSentence(phrases[0])
                sentences.recogniseSentence(phrases[1])
            else:
                sentences.recogniseSentence(data)

        except sr.UnknownValueError:
            sentences.answer('dontUnderstand')
        except sr.RequestError as e:  # if you get a request error from Google speech engine
            print(
                "Erreur du service Google Speech Recognition ; {0}".format(e))

    listen()


"""Main program"""
while 1:  # This starts a loop so the speech recognition is always listening to you
    if 'no-voice' in sys.argv:
        print("[WARN] No voice mode enabled")
        no_voice_mode = True

    sentences.registerSentences()
    automations.register()
    start_listening_for_hotword()
