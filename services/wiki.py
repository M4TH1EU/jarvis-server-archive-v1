import re

import wikipedia
from translate import Translator

import chatbot.chat


def get_description(name):
    wikipedia.set_lang("fr")

    try:
        page = wikipedia.page(name, auto_suggest=True)
    except:
        try:
            try:
                page = wikipedia.page(name, auto_suggest=False)
            except:
                wikipedia.set_lang("en")
                page = wikipedia.page(name, auto_suggest=False)
        except:
            return chatbot.chat.get_response_for_tag('wikipedia_search')

    summary = re.sub("[\(\[].*?[\)\]]", "", page.summary)
    summary = re.sub('/.*?/ ', '', summary, flags=re.DOTALL)
    summary = summary.replace("Inc.", "Incorporation")
    summary = summary.split(". ")[0]
    if "en.wiki" in page.url:
        translator = Translator(to_lang="fr", from_lang="en")
        summary = translator.translate(summary)

    return summary
