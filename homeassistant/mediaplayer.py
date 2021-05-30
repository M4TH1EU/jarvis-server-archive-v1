import json

import intents.intents
import services.shazam
from homeassistant.homeassistant import call_service, get_state


def next_track(entity_id):
    """
    Play the next track

    Parameters
    ----------
    entity_id : str
    """

    call_service('{"entity_id": "' + entity_id + '" }', "media_player/media_next_track")


def previous_track(entity_id):
    """
    Play the next track

    Parameters
    ----------
    entity_id : str
    """

    call_service('{"entity_id": "' + entity_id + '" }', "media_player/media_previous_track")


def pause(entity_id):
    """
    Pause the song

    Parameters
    ----------
    entity_id : str
    """

    call_service('{"entity_id": "' + entity_id + '" }', "media_player/media_pause")


def play(entity_id):
    """
    Resume the song

    Parameters
    ----------
    entity_id : str
    """

    call_service('{"entity_id": "' + entity_id + '" }', "media_player/media_play")


def turn_up_volume(entity_id):
    """
    Turn the volume up

    Parameters
    ----------
    entity_id : str
    """

    # calling it twice to really see a volume difference
    call_service('{"entity_id": "' + entity_id + '" }', "media_player/volume_up")
    call_service('{"entity_id": "' + entity_id + '" }', "media_player/volume_up")


def turn_down_volume(entity_id):
    """
    Turn the volume down

    Parameters
    ----------
    entity_id : str
    """

    # calling it twice to really see a volume difference
    call_service('{"entity_id": "' + entity_id + '" }', "media_player/volume_down")
    call_service('{"entity_id": "' + entity_id + '" }', "media_player/volume_down")


def is_music_playing(entity_id):
    """
    Return true if spotify is playing a song

    Parameters
    ----------
    entity_id : str

    Returns
    ----------
    bool
    """
    return json.loads(get_state(entity_id))['state'] == 'playing'


def get_infos_playing_song(entity_id):
    """
    Return the song name and artist when spotify is playing

    Parameters
    ----------
    entity_id : str

    Returns
    ----------
    dict
    """

    song_info = json.loads(get_state(entity_id))['attributes']
    artist = song_info['media_artist']
    song = song_info['media_title']

    return [song, artist]


def song_recognition(entity_id):
    """
    Return the name of a song using either shazam or homeassistant media_player entity (if entity_id set)
    Parameters
    ----------
    entity_id

    Returns
    -------
    str
    """

    title = ""
    singer = ""

    def shazam():
        song = services.shazam.recognise_song()
        if len(song) > 0:
            title = song[0]
            singer = song[1]
            # track_id = song[2]
            return [title, singer]
        else:
            return intents.intents.get_random_from_list_for_tag('song_recognition', 'responses_fail')

    if entity_id:
        # if entity is playing return the playing song with entity_id
        if is_music_playing(entity_id):
            song_info = get_infos_playing_song(entity_id)
            title = song_info[0]
            singer = song_info[1]
        # if entity_id is not playing then shazam
        else:
            title, singer = shazam()

    # if no entity_id is specified then shazam
    else:
        title, singer = shazam()

    # if the title or the singer are empty return fail response (can happend when a microphone error occurs and no audio is send from the client)
    if not title or not singer:
        return intents.intents.get_random_from_list_for_tag('song_recognition', 'responses_fail')

    answer_sentence = intents.intents.get_random_response_for_tag('song_recognition')
    answer_sentence = answer_sentence.replace("%title", title)
    answer_sentence = answer_sentence.replace("%singer", singer)
    return answer_sentence
