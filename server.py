import json
import tempfile

import elevate
import flask
from flask import Flask, jsonify, request

import automations
import sentences

elevate.elevate()

app = Flask(__name__)
hotword = 'jarvis'
token = 'B*TyX&y7bDd5xLXYNw5iaN6X7%QAiqTQ#9nvtgMX3X2risrD64ew!*Q9*ky3PRvrSWYE6euykHycNzQqmViKo%XfoyTCSrJTFSUK*ycP2P$!Psn55iJT4@b4tdxw*XA!'  # test token (nothing private)


def check_api_key(request):
    token = request.headers.get('Authorization')
    if token != token:
        flask.abort(401)


def get_sentence_in_body(name):
    data = json.loads(str(request.data.decode('utf8')).replace('"', '\"').replace("\'", "'"))
    if not isinstance(data, dict):
        data = json.loads(data)

    data = str(data[name]).lower()
    return data


def get_body(name):
    data = json.loads(request.data.decode('utf8'))
    if not isinstance(data, dict):
        data = json.loads(data)

    data = str(data[name])
    return data


@app.route("/hotword", methods=['GET'])
def get_hotword():
    check_api_key(request)
    return jsonify(hotword)


@app.route("/send_record", methods=['POST'])
def get_recorded_song():
    check_api_key(request)

    filename = tempfile.gettempdir() + '\\received_song.wav'

    received_bytes = request.data

    # Open file in binary write mode
    binary_file = open(filename, 'wb+')

    # Write bytes to file
    binary_file.write(received_bytes)

    # Close file
    binary_file.close()
    print("Created file")
    return jsonify("OK")


@app.route("/sentence/contains", methods=['POST'])
def contains_sentence():
    sentence = get_body("sentence")
    return jsonify(sentences.contains_sentence(sentence))


@app.route("/sentence/get_by_id", methods=['POST'])
def get_by_id():
    sentence_id = get_body("sentenceId")
    return jsonify(sentences.getRandomSentenceFromId(sentence_id))


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
    sentences.registerSentences()
    automations.register()

    app.run(port=5000, debug=False, host='0.0.0.0', threaded=True)
