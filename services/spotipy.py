# NOT TO BE MISTAKEN WITH "media_player.py" from homeassistant folder, this is for the spotiPy library (used for searching titles and playing songs, homeassistant cannot find spotify track id or search songs/artists)
import random

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import config
import intents.intents
from sentences import get_person_in_sentence, get_sentence_without_patterns_words

scope = "user-read-playback-state, user-modify-playback-state, user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               client_id=config.get_in_config("SPOTIFY_CLIENT_ID"),
                                               client_secret=config.get_in_config("SPOTIFY_CLIENT_SECRET"),
                                               redirect_uri='http://localhost:8888/callback/'))


def play_song(artist, song):
    songs_found = sp.search(q=("artist:" + artist + " track:" + song), limit=3, type='track')['tracks']['items']
    if len(songs_found) > 0:
        track_uri = songs_found[0]['uri']
        sp.add_to_queue(uri=track_uri)
        sp.next_track()
        return intents.intents.get_random_response_for_tag('done_sir')
    else:
        return intents.intents.get_random_from_list_for_tag('play_song', 'responses_fail')


def play_artist(artist):
    songs_found = sp.search(q=("artist:" + artist), limit=10, type='track')['tracks']['items']
    if len(songs_found) > 0:
        track_uri = songs_found[random.randint(0, len(songs_found))][
            'uri']
        sp.add_to_queue(uri=track_uri)
        sp.next_track()
        return intents.intents.get_random_response_for_tag('done_sir')

    else:
        return intents.intents.get_random_from_list_for_tag('play_song', 'responses_fail')


def play_song_without_artist(song):
    songs_found = sp.search(q=("track:" + song), limit=3, type='track')['tracks']['items']
    if len(songs_found) > 0:
        track_uri = songs_found[0]['uri']
        sp.add_to_queue(uri=track_uri)
        sp.next_track()
        return intents.intents.get_random_response_for_tag('done_sir')
    else:
        return intents.intents.get_random_from_list_for_tag('play_song', 'responses_fail')


def is_music_playing():
    return sp.current_user_playing_track()['is_playing']


def get_infos_playing_song():
    song_info = sp.current_user_playing_track()
    artist = song_info['item']['artists'][0]['name']
    song = song_info['item']['name']

    return [song, artist]


def play_a_song(data):
    """
    Retrieve the author and the title from a sentence and play it
    Parameters
    ----------
    data: dict

    Returns
    -------

    """
    if 'sentence' in data:
        sentence = data.get('sentence')

        singer = get_person_in_sentence(sentence, play_song=True)
        print("singer : " + singer)

        song_name = get_sentence_without_patterns_words(sentence, 'play_song').replace(singer, '')
        print("song name : " + song_name)

        song_name = song_name.replace('\'', '')

        if singer != 'none' and song_name:
            return play_song(singer, song_name)
        elif singer != 'none' and not song_name:
            return play_artist(singer)
        elif singer == 'none' and song_name:
            return play_song_without_artist(song_name)
    else:
        raise Exception("spotipy.play_song need a sentence in data")
