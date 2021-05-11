import json
import struct
import sys
import time

import pvporcupine
import pyaudio
import pyttsx3
import requests
import speech_recognition as sr
from requests.structures import CaseInsensitiveDict

import sentences

no_voice_mode = False

server_url = "http://127.0.0.1:5000"
token = 'B*TyX&y7bDd5xLXYNw5iaN6X7%QAiqTQ#9nvtgMX3X2risrD64ew!*Q9*ky3PRvrSWYE6euykHycNzQqmViKo%XfoyTCSrJTFSUK*ycP2P$!Psn55iJT4@b4tdxw*XA!'  # test token (nothing private)


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

    try:
        if no_voice_mode:
            data = input("Entrez phrase : ").lower()
        else:
            with sr.Microphone(device_index=0) as source:
                audio = r.listen(source, timeout=3, phrase_time_limit=(7 if not no_voice_mode else 1))

            # now uses Google speech recognition
            data = r.recognize_google(audio, language="fr-FR")
            data = data.lower()  # makes all voice entries show as lower case

        print("DATA : " + data)
        speak(send_to_server(data))

    except sr.UnknownValueError:
        sentences.answer('dontUnderstand')
    except sr.RequestError as e:  # if you get a request error from Google speech engine
        print(
            "Erreur du service Google Speech Recognition ; {0}".format(e))
    listen()


def speak(text):
    print(text)
    rate = 100  # Sets the default rate of speech
    engine = pyttsx3.init()  # Initialises the speech engine
    voices = engine.getProperty('voices')  # sets the properties for speech
    engine.setProperty('voice', voices[0])  # Gender and type of voice
    engine.setProperty('rate', rate + 50)  # Adjusts the rate of speech
    engine.say(text)  # tells Python to speak variable 'text'
    engine.runAndWait()  # waits for speech to finish and then continues with program


def send_to_server(sentence):
    try:
        url_service = server_url + "/send"
        headers = CaseInsensitiveDict()
        headers["Authorization"] = token
        headers["Content-Type"] = "application/json; charset=utf8"
        sentence = json.dumps({"sentence": sentence})

        return json.loads(
            requests.post(url_service, headers=headers, data=sentence.encode("utf8")).content.decode("utf-8"))
    except:
        print("Error when calling HomeAssistant API")


def get_hotword():
    try:
        url_service = server_url + "/hotword"
        headers = CaseInsensitiveDict()
        headers["Authorization"] = token
        headers["Content-Type"] = "application/json; charset=utf8"

        return json.loads(requests.get(url_service, headers=headers).content.decode("utf-8"))
    except:
        print("Error when calling the server API")


if __name__ == '__main__':
    hotword = get_hotword()
    print("Getting hotword from server : " + hotword)

    while 1:  # This starts a loop so the speech recognition is always listening to you
        if 'no-voice' in sys.argv:
            print("[WARN] No voice mode enabled")
            no_voice_mode = True

        start_listening_for_hotword()
