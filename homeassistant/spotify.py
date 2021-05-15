import json

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
