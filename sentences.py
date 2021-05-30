import datetime as datetime
import importlib

import spacy
from nltk.corpus import stopwords
from unidecode import unidecode

import chatbot.chat
import homeassistant.homeassistant
import homeassistant.light
import homeassistant.mediaplayer
import homeassistant.switch
import homeassistant.weather
import intents.intents

sentences = {}
last_answer = ""
nlp = "waiting"  # create blank object while loading the real model in a background thread


def load_nlp():
    global nlp
    nlp = spacy.load("fr_core_news_sm")
    print("Spacy loaded.")


def import_service_and_return_method(module, name):
    mod = importlib.import_module(module)
    met = getattr(mod, name)

    return met


def recogniseSentence(sentence):
    tag = chatbot.chat.get_tag_for_sentence(sentence)

    if tag is None:
        return "don't understand"
        # TODO: implement I18N or something similar for langs
        # return chatbot.chat.get_response_for_tag_custom('dont_understand')

    if intents.intents.does_tag_has_service(tag):
        service = intents.intents.get_tag_service(tag)
        data = intents.intents.get_data_for_tag(tag)

        # add the tag to data
        data['tag'] = tag

        # if the data contains "sentence: true" then replace "true" by the sentence
        # if 'sentence' in data and data['sentence'] is True:
        # TODO: find why data doesn't reset itself on next recognition
        data['sentence'] = sentence

        print(data)
        print(service)

        if service.startswith("homeassistant"):

            # used for service like "homeassistant$/weather/summary", we need to run the summary() method in weather.py and not call the H.A API
            if service.startswith("homeassistant$"):
                # see the elif(..."jarvis") below for more informations on what this does
                name = service.removeprefix('homeassistant$/').split("/")[1]
                service = service.removeprefix('homeassistant$/').split("/")[0]
                method = import_service_and_return_method("homeassistant." + service, name)
                return method(data)
            else:
                service = service.removeprefix('homeassistant/')
                if 'entity_id' in data:
                    entity_id = data.get('entity_id')

                    homeassistant.homeassistant.call_service('{"entity_id": "' + entity_id + '" }', service)
                else:
                    raise Exception("HomeAssistant services need an entity_id in data")

        elif service.startswith("jarvis"):
            # splitting the service name from the intent (summary in "jarvis/weather/summary)
            name = service.removeprefix('jarvis/').split("/")[1]

            # splitting the service from the intent (weather in "jarvis/weather/summary)
            service = service.removeprefix('jarvis/').split("/")[0]

            # importing the service method extracted from the service in the intent
            method = import_service_and_return_method("services." + service, name)

            # returns what the method from the service returned
            return method(data)

        return intents.intents.get_random_response_for_tag(tag)
    else:

        # il est quelle heure
        if is_tag(tag, 'what_time_is_it'):
            current_time = datetime.datetime.now().strftime("%H:%M")
            current_time = current_time.replace('00:', 'minuit ')
            current_time = current_time.replace('12:', 'midi ')

            return intents.intents.get_random_response_for_tag('what_time_is_it') + " " + current_time

    return intents.intents.get_random_response_for_tag(tag)


def is_tag(tag, name):
    return tag == name


def get_sentence_without_stopwords(sentence):
    stop_words_french = set(stopwords.words('french'))
    filtered_sentence = [w for w in sentence.lower().split() if w not in stop_words_french]
    filtered_sentence = " ".join(filtered_sentence)
    return filtered_sentence


def get_sentence_without_patterns_words(sentence, tag):
    patterns = intents.intents.get_list_of_patterns_for_tag(tag)
    patterns_stop_words = " ".join(patterns).lower().split()

    sentence_without_patterns_words = ' '.join(
        filter(lambda x: x.lower() not in patterns_stop_words, sentence.split()))

    return sentence_without_patterns_words


def get_sentence_without_stopwords_and_pattern(sentence, tag):
    filtered_sentence = get_sentence_without_stopwords(sentence)
    filtered_sentence = get_sentence_without_patterns_words(filtered_sentence, tag)
    return filtered_sentence


def get_person_in_sentence(sentence, play_song=False):
    global nlp
    if nlp is None:
        raise Exception("Spacy NLP engine is not setup yet")
    else:
        doc = nlp(sentence)

        for ent in doc.ents:
            if ent.label_ == 'PER':
                return ent.text

        if play_song:
            for word in doc:
                # print(word.text, word.pos_) # prints every words from the sentence with their types

                de_words = ['de ', 'd\'', 'des']

                # support for lowercase name with spotify (play_song)
                for de_word in de_words:
                    if word.text == de_word.replace(' ', '') and (str(word.pos_) == 'ADP' or str(word.pos_) == 'DET'):
                        person = sentence.split(" ".join([de_word]))[1]
                        return person

    return "none"


def get_ascii_sentence(sentence):
    return unidecode(sentence)
