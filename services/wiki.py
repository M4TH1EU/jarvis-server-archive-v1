import re

import wikipedia
from translate import Translator

import chatbot.chat
from sentences import get_person_in_sentence, get_sentence_without_stopwords_and_pattern


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

    # remove everything between (...)
    summary = re.sub("[\(].*?[\)]", "", page.summary)
    # remove everything between [...]
    summary = re.sub("[\[].*?[\]]", "", summary)
    # remove everything between /.../
    summary = re.sub('/.*?/ ', '', summary, flags=re.DOTALL)
    # replace inc. by incorporation (for pronunciation)
    summary = summary.replace("Inc.", "Incorporation")
    # keep only the first sentence
    summary = summary.split(". ")[0]

    if "en.wiki" in page.url:
        translator = Translator(to_lang="fr", from_lang="en")
        summary = translator.translate(summary)

    return summary


def search_wikipedia(sentence):
    sentence = sentence[0].lower() + sentence[1:]

    person_name = get_person_in_sentence(sentence)
    if person_name != "none":
        print("Search with person name: ", person_name)
        return get_description(person_name)
    else:
        filtered_sentence = get_sentence_without_stopwords_and_pattern(sentence, 'wikipedia_search')

        print("Search : ", filtered_sentence)
        return get_description(filtered_sentence)
