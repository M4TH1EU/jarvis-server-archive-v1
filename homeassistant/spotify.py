import json

from homeassistant.homeassistant import callService, getState


def nextTrack(entity_id):
    """
    Play the next track

    Parameters
    ----------
    entity_id : str
    """

    callService('{"entity_id": "' + entity_id + '" }', "media_player/media_next_track")


def previousTrack(entity_id):
    """
    Play the next track

    Parameters
    ----------
    entity_id : str
    """

    callService('{"entity_id": "' + entity_id + '" }', "media_player/media_previous_track")


def pause(entity_id):
    """
    Pause the song

    Parameters
    ----------
    entity_id : str
    """

    callService('{"entity_id": "' + entity_id + '" }', "media_player/media_pause")


def play(entity_id):
    """
    Resume the song

    Parameters
    ----------
    entity_id : str
    """

    callService('{"entity_id": "' + entity_id + '" }', "media_player/media_play")


def turnUpVolume(entity_id):
    """
    Turn the volume up

    Parameters
    ----------
    entity_id : str
    """

    # calling it twice to really see a volume difference
    callService('{"entity_id": "' + entity_id + '" }', "media_player/volume_up")
    callService('{"entity_id": "' + entity_id + '" }', "media_player/volume_up")


def turnDownVolume(entity_id):
    """
    Turn the volume down

    Parameters
    ----------
    entity_id : str
    """

    # calling it twice to really see a volume difference
    callService('{"entity_id": "' + entity_id + '" }', "media_player/volume_down")
    callService('{"entity_id": "' + entity_id + '" }', "media_player/volume_down")


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
    return json.loads(getState(entity_id))['state'] == 'playing'


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

    song_info = json.loads(getState(entity_id))['attributes']
    artist = song_info['media_artist']
    song = song_info['media_title']

    return [song, artist]
