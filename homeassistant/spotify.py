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

