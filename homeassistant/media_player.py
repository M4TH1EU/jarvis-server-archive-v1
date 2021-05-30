import json

import homeassistant
import intents.intents
import services.shazam
from homeassistant.homeassistant import call_service, get_state


def media_next_track(entity_id):
    """
    Play the next track

    Parameters
    ----------
    entity_id : str
    """
    homeassistant.homeassistant.call_api("media_player", "media_next_track", {'entity_id': entity_id})


def media_previous_track(entity_id):
    """
    Play the next track

    Parameters
    ----------
    entity_id : str
    """
    homeassistant.homeassistant.call_api("media_player", "media_previous_track", {'entity_id': entity_id})



def media_pause(entity_id):
    """
    Pause the song

    Parameters
    ----------
    entity_id : str
    """

    homeassistant.homeassistant.call_api("media_player", "media_pause", {'entity_id': entity_id})


def media_play(entity_id):
    """
    Resume the song

    Parameters
    ----------
    entity_id : str
    """

    homeassistant.homeassistant.call_api("media_player", "media_play", {'entity_id': entity_id})


def volume_up(entity_id):
    """
    Turn the volume up

    Parameters
    ----------
    entity_id : str
    """

    # calling it twice to really see a volume difference
    homeassistant.homeassistant.call_api("media_player", "volume_up", {'entity_id': entity_id})
    homeassistant.homeassistant.call_api("media_player", "volume_up", {'entity_id': entity_id})


def volume_down(entity_id):
    """
    Turn the volume down

    Parameters
    ----------
    entity_id : str
    """

    # calling it twice to really see a volume difference
    homeassistant.homeassistant.call_api("media_player", "volume_down", {'entity_id': entity_id})
    homeassistant.homeassistant.call_api("media_player", "volume_down", {'entity_id': entity_id})


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
    return homeassistant.homeassistant.get_state(entity_id).state == 'playing'


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

    song_info = homeassistant.homeassistant.get_state(entity_id).attributes
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
