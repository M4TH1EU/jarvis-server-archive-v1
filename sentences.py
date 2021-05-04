import csv
# from main import speak
import datetime as datetime
import random

import beepy
import pyttsx3

import homeassistant.lights
import homeassistant.meteo
import homeassistant.spotify
from plugins import wiki, spotipy

sentences = {}
last_answer = ""


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
                # fix issue with unicode caracter
                sentenceId = sentenceId.replace('\ufeff', '').replace('\n', '')

                # creating an entry to be able to use .append afterward
                if sentenceId not in sentences:
                    sentences[sentenceId] = []

                # if the entry is not empty then add it to the sentences dict
                if lines[column] != "":
                    sentences[sentenceId].append(lines[column].lower())

            # increment column
            column = column + 1

        # reset column
        column = 0


def answer(sentence_id):
    if getSentencesById(sentence_id):
        speak(random.choice(getSentencesById(sentence_id)))
    else:
        speak(random.choice(getSentencesById("dontUnderstand")))
        beepy.beep(sound='coin')


def getSentences():
    return sentences


def getLastAnswer():
    return last_answer


def getSentencesById(sentence_id):
    return sentences[sentence_id]


def getRandomSentenceFromId(sentence_id):
    """
    Return a random sentence from the CSV file for a specific sentence (id)

    Parameters
    ----------
    sentence_id

    Returns
    -------
    str

    """
    return random.choice(getSentencesById(sentence_id))


def recogniseSentence(sentence):
    # hey jarvis
    if sentence in getSentencesById('hotwordDetection'):
        answer('yesSir')

    # comment ça va
    elif sentence in getSentencesById('howAreYouDetection'):
        answer('allGoodSir')

    # allume la lumière
    elif sentence in getSentencesById('turnOnLightsDetection'):
        answer('turningOnLights')
        homeassistant.lights.turnOn("light.lumieres_chambre")

    # éteint la lumière
    elif sentence in getSentencesById('turnOffLightsDetection'):
        answer('turningOffLights')
        homeassistant.lights.turnOff("light.lumieres_chambre")

    # allume les leds
    elif sentence in getSentencesById('turnOnLedsDetection'):
        answer('turningOnLights')
        homeassistant.lights.turnOn("light.leds_chambre")

    # éteint les leds
    elif sentence in getSentencesById('turnOffLedsDetection'):
        answer('turningOffLights')
        homeassistant.lights.turnOff("light.leds_chambre")

    # mets le morceau suivant
    elif sentence in getSentencesById('nextTrackDetection'):
        answer('nextTrack')
        homeassistant.spotify.nextTrack("media_player.spotify_mathieu_broillet")

    # mets le morceau précédent
    elif sentence in getSentencesById('previousTrackDetection'):
        answer('previousTrack')
        homeassistant.spotify.previousTrack("media_player.spotify_mathieu_broillet")

    # relance la musique
    elif sentence in getSentencesById('resumeMusicDetection'):
        answer('resumeMusic')
        homeassistant.spotify.play("media_player.spotify_mathieu_broillet")

    # mets la musique sur pause
    elif sentence in getSentencesById('pauseMusicDetection'):
        answer('pauseMusic')
        homeassistant.spotify.pause("media_player.spotify_mathieu_broillet")

    # monte le son
    elif sentence in getSentencesById('turnUpVolumeDetection'):
        answer('turningUpVolume')
        homeassistant.spotify.turnUpVolume("media_player.spotify_mathieu_broillet")

    # baisse le son
    elif sentence in getSentencesById('turnDownVolumeDetection'):
        answer('turningDownVolume')
        homeassistant.spotify.turnDownVolume("media_player.spotify_mathieu_broillet")

    # il est quelle heure
    elif sentence in getSentencesById('whatTimeIsIt'):
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(getRandomSentenceFromId('itIsTime') + " " + current_time)

    # non rien finalement
    elif sentence in getSentencesById('nothingDetection'):
        beepy.beep(sound='error')

    else:

        # cherche XYZ sur wikipédia
        if is_custom_sentence('wikiDetection', sentence):
            speak(wiki.getDescription(get_words_out_of_custom_sentence('wikiDetection', sentence)))

        elif sentence in getSentencesById('weatherInfoDetection'):
            homeassistant_weather_entity_id = 'weather.bussigny_sur_oron'
            today_date = datetime.date.today().strftime("%Y-%m-%d")
            today_hour = datetime.datetime.now().hour

            sera = "est"
            faire = "fait"

            if today_hour <= 10:
                sera = "sera"
                faire = "fera"

            sentence_meteo = getRandomSentenceFromId('weatherInfo')
            sentence_meteo = sentence_meteo.replace('&sera', sera)
            sentence_meteo = sentence_meteo.replace('&faire', faire)
            sentence_meteo = sentence_meteo.replace('%condition',
                                                    homeassistant.meteo.getCondition(homeassistant_weather_entity_id))
            sentence_meteo = sentence_meteo.replace('%temperature',
                                                    homeassistant.meteo.getTemperature(homeassistant_weather_entity_id))
            sentence_meteo = sentence_meteo.replace('%lowtemp', homeassistant.meteo.getTemperatureLow(
                homeassistant_weather_entity_id))
            sentence_meteo = sentence_meteo.replace('%wind_speed',
                                                    homeassistant.meteo.getWindSpeed(homeassistant_weather_entity_id))
            sentence_meteo = sentence_meteo.replace('%wind_words', "faible")
            speak(sentence_meteo)

        # joue i'm still standing de elton john
        elif is_custom_sentence('playSong', sentence):
            # print("custom : " + get_words_out_of_custom_sentence('playSong', sentence))

            words = get_words_out_of_custom_sentence('playSong', sentence).replace("'", '')
            song = words

            # talking to the user while spotify is searching
            answer('doneSir')

            if " de " in words:
                song = words.split(" de ")[0]
                artist = words.split(" de ")[1]
                spotipy.playSong(artist, song)
            else:
                spotipy.playSongWithoutArtist(song)
        else:
            answer('dontUnderstand')


def speak(text):
    rate = 100  # Sets the default rate of speech
    engine = pyttsx3.init()  # Initialises the speech engine
    voices = engine.getProperty('voices')  # sets the properties for speech
    engine.setProperty('voice', voices[0])  # Gender and type of voice
    engine.setProperty('rate', rate + 50)  # Adjusts the rate of speech
    engine.say(text)  # tells Python to speak variable 'text'
    engine.runAndWait()  # waits for speech to finish and then continues with program


def is_custom_sentence(sentence_id, sentence):
    if sentence.startswith(tuple(getSentencesById(sentence_id))):
        return True
    else:
        return False


def get_words_out_of_custom_sentence(sentence_id, sentence):
    for var in getSentencesById(sentence_id):
        if sentence.startswith(var):
            custom_words_found = [word for word in sentence.split() if word not in var.split()]
            return " ".join(custom_words_found)
