import clientUtils


def play_sound(data):
    """

    Parameters
    ----------
    data: dict

    Returns
    -------

    """
    if 'sound_name' in data:
        clientUtils.sound(data.get('sound_name'))
        return ""

    return "Je ne trouve pas le son demandé"
