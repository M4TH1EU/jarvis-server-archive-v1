import csv
import datetime as datetime
import random

import homeassistant.homeassistant
import homeassistant.lights
import homeassistant.meteo
import homeassistant.spotify
import homeassistant.switch
import plugins.alarms
import plugins.shazam
from plugins import wiki, spotipy

sentences = {}
last_answer = ""


def registerSentences():
    try:
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

        csv_file.close()
    except UnicodeDecodeError as e:
        print("Error loading sentences.csv, check if saved with CSV (| delimited) and encoded in UTF-8 ")


def get_answer(sentence_id):
    if getSentencesById(sentence_id):
        return random.choice(getSentencesById(sentence_id))
    else:
        return random.choice(getSentencesById("dontUnderstand"))


def get_custom_answer(text):
    return text


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
        return get_answer('yesSir')

    # comment ça va
    elif sentence in getSentencesById('howAreYouDetection'):
        return get_answer('allGoodSir')

    # allume la lumière
    elif sentence in getSentencesById('turnOnLightsDetection'):
        homeassistant.lights.turnOn("light.lumieres_chambre")
        return get_answer('turningOnLights')

    # éteint la lumière
    elif sentence in getSentencesById('turnOffLightsDetection'):
        homeassistant.lights.turnOff("light.lumieres_chambre")
        return get_answer('turningOffLights')

    # allume les leds
    elif sentence in getSentencesById('turnOnLedsDetection'):
        homeassistant.lights.turnOn("light.leds_chambre")
        return get_answer('turningOnLights')

    # éteint les leds
    elif sentence in getSentencesById('turnOffLedsDetection'):
        homeassistant.lights.turnOff("light.leds_chambre")
        return get_answer('turningOffLights')

    # mets le morceau suivant
    elif sentence in getSentencesById('nextTrackDetection'):
        homeassistant.spotify.nextTrack("media_player.spotify_mathieu_broillet")
        return get_answer('nextTrack')

    # mets le morceau précédent
    elif sentence in getSentencesById('previousTrackDetection'):
        homeassistant.spotify.previousTrack("media_player.spotify_mathieu_broillet")
        return get_answer('previousTrack')

    # relance la musique
    elif sentence in getSentencesById('resumeMusicDetection'):
        homeassistant.spotify.play("media_player.spotify_mathieu_broillet")
        return get_answer('resumeMusic')

    # mets la musique sur pause
    elif sentence in getSentencesById('pauseMusicDetection'):
        homeassistant.spotify.pause("media_player.spotify_mathieu_broillet")
        return get_answer('pauseMusic')

    # monte le son
    elif sentence in getSentencesById('turnUpVolumeDetection'):
        homeassistant.spotify.turnUpVolume("media_player.spotify_mathieu_broillet")
        return get_answer('turningUpVolume')

    # baisse le son
    elif sentence in getSentencesById('turnDownVolumeDetection'):
        homeassistant.spotify.turnDownVolume("media_player.spotify_mathieu_broillet")
        return get_answer('turningDownVolume')

    # il est quelle heure
    elif sentence in getSentencesById('whatTimeIsIt'):
        current_time = datetime.datetime.now().strftime("%H:%M")
        return get_custom_answer(getRandomSentenceFromId('itIsTime') + " " + current_time)

    # non rien finalement
    elif sentence in getSentencesById('nothingDetection'):
        # TODO: find a way to replace the beepy sound
        return "Ok"

    # allume l'imprimante 3d
    elif sentence in getSentencesById('turnOn3DPrinterDetection'):
        homeassistant.switch.turnOn('switch.bfd9b202b8140c15780fpe')
        return get_answer('turningOn3DPrinter')

    # éteint l'imprimante 3d
    elif sentence in getSentencesById('turnOff3DPrinterDetection'):
        homeassistant.switch.turnOff('switch.bfd9b202b8140c15780fpe')
        return get_answer('turningOff3DPrinter')

    # allume le pc
    elif sentence in getSentencesById('turnOnPCDetection'):
        homeassistant.switch.turnOn('switch.wake_on_lan_pc_tour')
        return get_answer('turningOnPC')

    # éteint le pc
    elif sentence in getSentencesById('turnOffPCDetection'):
        homeassistant.switch.turnOff('switch.wake_on_lan_pc_tour')
        return get_answer('turningOffPC')

    # mets le pc en veille
    elif sentence in getSentencesById('putComputerToSleepDetection'):
        homeassistant.homeassistant.callService('', 'shell_command/sleep_tour_mathieu')
        return get_answer('doneSir')

    # allume la tablette
    elif sentence in getSentencesById('turnOnKioskTabletDetection'):
        homeassistant.lights.turnOn('light.mi_pad_screen')
        return get_answer('turningOnKioskTablet')

    # éteint la tablette
    elif sentence in getSentencesById('turnOffKioskTabletDetection'):
        homeassistant.switch.turnOff('light.mi_pad_screen')
        return get_answer('turningOffKioskTablet')

    # c'est quoi le titre de cette chanson
    elif sentence in getSentencesById('whatThatSongDetection'):

        title = ""
        singer = ""

        answer_sentence = getRandomSentenceFromId('songTitle')

        if plugins.spotipy.is_music_playing():
            song_info = plugins.spotipy.get_infos_playing_song()

            title = song_info[0]
            singer = song_info[1]
        else:
            get_answer('songRecognition')
            song = plugins.shazam.recognise_song()
            if len(song) > 0:
                title = song[0]
                singer = song[1]
                # track_id = song[2]
            else:
                get_answer('songNotFound')

        answer_sentence = answer_sentence.replace("%title", title)
        answer_sentence = answer_sentence.replace("%singer", singer)
        return get_custom_answer(answer_sentence)

    else:

        # cherche XYZ sur wikipédia
        if is_custom_sentence('wikiDetection', sentence):
            get_custom_answer(wiki.getDescription(get_words_out_of_custom_sentence('wikiDetection', sentence)))

        # mets le réveil à 6h45
        elif is_custom_sentence('alarmClockDetection', sentence):
            spoke_time = get_words_out_of_custom_sentence('alarmClockDetection', sentence)
            spoke_time = spoke_time.replace("demain", "").replace("matin", "").replace(" ", "")

            hours = spoke_time.split("h")[0]
            minutes = spoke_time.split("h")[1]

            spoke_time = datetime.time(hour=int(hours), minute=int(minutes))
            plugins.alarms.add_alarm(spoke_time.strftime("%H:%M"))

        # quel temps fait il
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
            return get_custom_answer(sentence_meteo)

        # joue i'm still standing de elton john
        elif is_custom_sentence('playSong', sentence):
            print("custom : " + get_words_out_of_custom_sentence('playSong', sentence))

            words = get_words_out_of_custom_sentence('playSong', sentence).replace("'", '')
            song = words

            if " de " in words:
                song = words.split(" de ")[0]
                artist = words.split(" de ")[1]
                spotipy.playSong(artist, song)
            else:
                if " de " in sentence:
                    spotipy.playArtist(song)
                else:
                    spotipy.playSongWithoutArtist(song)

            return get_answer('doneSir')

        else:
            return get_answer('dontUnderstand')


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
