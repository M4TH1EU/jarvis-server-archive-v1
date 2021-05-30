import glob
import itertools
import json
import os

import pathfile

path = os.path.dirname(pathfile.__file__)

files = glob.glob(path + "\\intents\\*.json")


def get_all_intents():
    result = []
    for f in files:
        with open(f, "rb") as infile:
            result.append(json.load(infile)['intents'])

    all = list(map(dict, itertools.chain.from_iterable(result)))
    return all
