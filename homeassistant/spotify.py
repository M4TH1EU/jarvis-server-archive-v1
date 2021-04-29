from homeassistant.homeassistant import callApiPost


def nextTrack(entity_id):
    """
    Play the next track

    Parameters
    ----------
    entity_id : str
    """

    callApiPost('{"entity_id": "' + entity_id + '" }', "media_player/media_next_track")


def previousTrack(entity_id):
    """
    Play the next track

    Parameters
    ----------
    entity_id : str
    """

    callApiPost('{"entity_id": "' + entity_id + '" }', "media_player/media_previous_track")


def pause(entity_id):
    """
    Pause the song

    Parameters
    ----------
    entity_id : str
    """

    callApiPost('{"entity_id": "' + entity_id + '" }', "media_player/media_pause")


def play(entity_id):
    """
    Resume the song

    Parameters
    ----------
    entity_id : str
    """

    callApiPost('{"entity_id": "' + entity_id + '" }', "media_player/media_play")
