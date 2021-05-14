import asyncio
import json
import tempfile

from shazamio import Shazam

import clientUtils
import sentences

filename = tempfile.gettempdir() + '\\recorded_song.wav'


def recognise_song():
    clientUtils.ask_for_microphone_output(3, sentences.getRandomSentenceFromId('songRecognition'))

    loop = asyncio.get_event_loop()
    return loop.run_until_complete(get_shazam_song())


async def get_shazam_song():
    shazam = Shazam()
    out = await shazam.recognize_song(filename)
    json_out = json.loads(json.dumps(out))

    if len(json_out['matches']) > 0:
        title = json_out['track']['title']
        singer = json_out['track']['subtitle']
        spotify_track_id = json_out['track']['hub']['providers'][0]['actions'][0]['uri']

        return [title, singer, spotify_track_id]
    else:
        return []
