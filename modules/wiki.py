import re

import wikipedia
from translate import Translator

import sentences


def getDescription(name):
    wikipedia.set_lang("fr")

    try:
        page = wikipedia.page(name, auto_suggest=True)
    except wikipedia.exceptions.PageError:
        try:
            try:
                page = wikipedia.page(name, auto_suggest=False)
            except wikipedia.exceptions.DisambiguationError:
                wikipedia.set_lang("en")
                page = wikipedia.page(name, auto_suggest=False)
        except wikipedia.exceptions.PageError:
            print(sentences.getRandomSentenceFromId('wikipediaNotFound'))
            return

    summary = re.sub("[\(\[].*?[\)\]]", "", page.summary)
    summary = summary.replace("Inc.", "Inc")
    summary = summary.split(". ")[0]
    if "en.wiki" in page.url:
        translator = Translator(to_lang="fr", from_lang="en")
        summary = translator.translate(summary)
    print(summary)
    sentences.speak(summary)
