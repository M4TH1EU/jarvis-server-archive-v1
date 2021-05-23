import json
import random

import torch
from nltk.corpus import stopwords
from unidecode import unidecode

from chatbot.model import NeuralNet
from chatbot.nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('chatbot/intents.json', encoding='utf-8', mode='r') as json_data:
    intents = json.load(json_data)

FILE = "chatbot/data.pth"
data = torch.load(FILE)

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
        for intent in intents['intents']:
            if tag == intent["tag"]:
                stop_words = set(stopwords.words('french'))
                filtered_sentence = [w for w in sentence if not w in stop_words]

                print("SENTENCE : ", sentence)
                print("SENTENCE FILTERED : ", filtered_sentence)

                return tag
    else:
        return get_response_for_tag_custom('dont_understand')


def get_response_for_tag(tag):
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])


def get_response_for_tag_custom(tag):
    for intent in intents['custom']:
        if intent['tag'] == tag:
            return random.choice(intent['responses'])


def get_all_patterns_for_tag(tag):
    for intent in intents['intents']:
        if intent['tag'] == tag:
            return intent['patterns']
