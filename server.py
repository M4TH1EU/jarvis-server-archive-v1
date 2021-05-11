import json

import flask
from flask import Flask, jsonify, request

import automations
import sentences

app = Flask(__name__)
hotword = 'jarvis'
token = 'B*TyX&y7bDd5xLXYNw5iaN6X7%QAiqTQ#9nvtgMX3X2risrD64ew!*Q9*ky3PRvrSWYE6euykHycNzQqmViKo%XfoyTCSrJTFSUK*ycP2P$!Psn55iJT4@b4tdxw*XA!'  # test token (nothing private)


def check_api_key(request):
    token = request.headers.get('Authorization')
    if token != token:
        flask.abort(401)


def get_sentence(request):
    data = json.loads(request.data.decode('utf8').replace("'", '"'))
    data = str(data['sentence']).lower()
    return data


def get_body(request, name):
    data = json.loads(request.data.decode('utf8').replace("'", '"'))
    data = str(data[name])
    return data


@app.route("/hotword", methods=['GET'])
def get_hotword():
    check_api_key(request)
    return jsonify(hotword)


@app.route("/sentence/contains", methods=['POST'])
def contains_sentence():
    sentence = get_body(request, "sentence")
    return jsonify(sentences.contains_sentence(sentence))


@app.route("/sentence/get_by_id", methods=['POST'])
def get_by_id():
    sentence_id = get_body(request, "sentenceId")
    return jsonify(sentences.getRandomSentenceFromId(sentence_id))


@app.route("/send", methods=['POST'])
def send():
    check_api_key(request)
    data = get_sentence(request)
    print(data)

    # add support for multiples actions in one sentence (two actions here)
    if " et " in data:
        phrases = data.split(" et ")

        response = sentences.recogniseSentence(phrases[0]) + "et" + sentences.recogniseSentence(
            phrases[1])
        return jsonify(response)
    else:
        return jsonify(sentences.recogniseSentence(data))


if __name__ == '__main__':
    sentences.registerSentences()
    automations.register()
    app.run(port=5000, debug=False, host='0.0.0.0', threaded=True)
