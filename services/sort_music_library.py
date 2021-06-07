import glob
import os
import re

import eyed3 as eyed3


def sortMusics(path):
    files = glob.glob(path + "\\*.mp3")

    for file in files:
        audio = eyed3.load(file)
        print("Title:", audio.tag.title)
        print("Artist:", audio.tag.artist)
        print("Album:", audio.tag.album)

        artist = replace_bad_chars(audio.tag.artist)
        title = replace_bad_chars(audio.tag.title)
        album = replace_bad_chars(audio.tag.album)

        if ',' in str(artist):
            artist = artist.split(',')[0]

        if title == album or album == " ":
            new_path = path + "\\" + artist + "\\"
        else:
            new_path = path + "\\" + artist + "\\" + album + "\\"

        os.makedirs(new_path, exist_ok=True)
        if not os.path.isfile(new_path + title + ".mp3"):
            os.rename(file, new_path + title + ".mp3")

    print("Done.")


def replace_bad_chars(string):
    """

    Parameters
    ----------
    string: str

    Returns
    -------

    """
    if not string:
        string = ""

    # a filename cannot contain : \ /  : * ? " < > |
    new_string = string.replace('\\', '')
    new_string = new_string.replace('/', '-')
    new_string = new_string.replace(':', '')
    new_string = new_string.replace('*', '')
    new_string = new_string.replace('?', '')
    new_string = new_string.replace('"', '')
    new_string = new_string.replace('<', '')
    new_string = new_string.replace('>', '')
    new_string = re.sub("[\(].*?[\)]", "", new_string)

    if " " in new_string:
        if new_string[-1] == " ":
            return new_string[:-1]

    return new_string


if __name__ == '__main__':
    sortMusics("C:\\Users\\Mathieu\\Music\\deemix Music mp3 320\\Happy Dance")
