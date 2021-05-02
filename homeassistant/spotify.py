from homeassistant.homeassistant import callService


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
