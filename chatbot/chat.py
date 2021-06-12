import os

import torch
from unidecode import unidecode

import intents.intents
import pathfile
from chatbot.model import NeuralNet
from chatbot.nltk_utils import bag_of_words, tokenize

path = os.path.dirname(pathfile.__file__)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

file = path + "/chatbot/data.pth"
data = torch.load(file)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()


def get_tag_for_sentence(input_sentence):
    """
    Return the matching tag of the input_sentence given in parameter.
    It usually is what the STT engine recognise or what the user's type when using no-voice mode

    Parameters
    ----------
    input_sentence is your sentence

    Returns tag from the intents.json file
    -------

    """
    sentence = unidecode(input_sentence)  # convert accent to better recognition
    sentence = tokenize(sentence)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)

    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    if prob.item() > 0.75 and len(sentence) > 2:
        return intents.intents.get_matching_intent_for_tag(tag).get('tag')
    else:
        return 'dont_understand'
