import json
import os
import sys
import tempfile
import threading

import flask
from flask import Flask, jsonify, request

import automations
import chatbot.train
import config
import intents.intents
import sentences

path = os.getcwd()
# elevate.elevate()

app = Flask(__name__)


def check_api_key(actual_request):
    token = actual_request.headers.get('Authorization')
    if token != config.get_in_config("API_KEY"):
        flask.abort(401)


def get_sentence_in_body(name):
    data = json.loads(str(request.data.decode('utf8')).replace('"', '\"').replace("\'", "'"))
    if not isinstance(data, dict):
        data = json.loads(data)

    data = str(data[name])
    return data


def get_body(name):
    data = json.loads(request.data.decode('utf8'))
    if not isinstance(data, dict):
        data = json.loads(data)

    data = str(data[name])
    return data


@app.route("/sentence/get_by_id", methods=['POST'])
def get_by_id():
    sentence_id = get_body("sentenceId")
    return jsonify(intents.intents.get_random_response_for_tag(sentence_id))


@app.route("/send_record", methods=['POST'])
def get_recorded_song():
    check_api_key(request)

    filename = tempfile.gettempdir() + '/received_song.wav'

    received_bytes = request.data

    # Open file in binary write mode
    binary_file = open(filename, 'wb+')

    # Write bytes to file
    binary_file.write(received_bytes)

    # Close file
    binary_file.close()
    print("Created file")
    return jsonify("OK")


@app.route("/send", methods=['POST'])
def send():
    check_api_key(request)
    data = get_sentence_in_body('sentence')
    print(data)

    # add support for multiples actions in one sentence (two actions here)
    if " et " in data:
        phrases = data.split(" et ")

        response = sentences.recogniseSentence(phrases[0]) + " et " + sentences.recogniseSentence(
            phrases[1])
        return jsonify(response)
    else:
        return jsonify(sentences.recogniseSentence(data))


if __name__ == '__main__':
    if 'train' in sys.argv:
        chatbot.train.train()
        exit(0)

    if config.get_in_config("TRAIN_ON_START"):
        chatbot.train.train()

    threading.Thread(target=sentences.load_nlp)
    automations.register()

    app.config['JSON_AS_ASCII'] = False
    app.run(port=config.get_in_config("PORT"), debug=False, host='0.0.0.0', threaded=True)
