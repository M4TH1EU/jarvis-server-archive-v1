import glob
import itertools
import json
import os
import random

import pathfile

path = os.path.dirname(pathfile.__file__)

intents = dict()


def get_all_intents():
    global intents

    if len(intents) >= 1:
        return intents
    else:
        result = []

        files = glob.glob(path + "/intents/**/*.json", recursive=True)
        for f in files:
            with open(f, "rb") as infile:
                result.append(json.load(infile)['intents'])

        all_intents = list(map(dict, itertools.chain.from_iterable(result)))
        return all_intents


def get_matching_intent_for_tag(tag):
    for intent in get_all_intents():
        if intent.get('tag') == tag:
            return intent
    raise Exception("Intent for tag " + tag + " not found!")


def get_random_response_for_tag(tag):
    """
    Return a random sentence using it's tag.

    Parameters
    ----------
    tag is the intent's tag

    Returns
    -------

    """

    intent = get_matching_intent_for_tag(tag)
    return random.choice(intent.get('responses'))


def get_list_of_patterns_for_tag(tag):
    intent = get_matching_intent_for_tag(tag)
    return intent.get('patterns')


def get_random_from_list_for_tag(tag, list_name):
    intent = get_matching_intent_for_tag(tag)
    if list_name in intent:
        return random.choice(intent.get(list_name))


def does_tag_has_service(tag):
    intent = get_matching_intent_for_tag(tag)

    if intent.get('service') is not None:
        return True
    else:
        return False


def get_tag_service(tag):
    """

    Parameters
    ----------
    tag

    Returns
    -------
    str
    """

    intent = get_matching_intent_for_tag(tag)
    return intent.get('service')


def get_from_intent_for_tag(field_name, tag):
    intent = get_matching_intent_for_tag(tag)

    if intent.get(field_name) is not None:
        return intent.get(field_name)

    return None


def get_from_data_for_tag(field_name, tag):
    intent = get_matching_intent_for_tag(tag)

    data = intent.get('data')
    if data is not None:
        if data.get(field_name) is not None:
            return data.get(field_name)

    return None


def get_data_for_tag(tag):
    intent = get_matching_intent_for_tag(tag)

    if intent.get('data') is not None:
        return intent.get('data')
    else:
        entity_id = get_from_data_for_tag('entity_id', tag)
        if entity_id is not None:
            return {"entity_id": entity_id}

    return dict()
