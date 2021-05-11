import os
import random

import spotipy
from spotipy.oauth2 import SpotifyOAuth

import sentences

scope = "user-read-playback-state, user-modify-playback-state, user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                               client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                                               redirect_uri='http://localhost:8888/callback/'))


def playSong(artist, song):
    songs_found = sp.search(q=("artist:" + artist + " track:" + song), limit=3, type='track')['tracks']['items']
    if len(songs_found) > 0:
        track_uri = songs_found[0]['uri']
        sp.add_to_queue(uri=track_uri)
        sp.next_track()
        return sentences.getRandomSentenceFromId('doneSir')
    else:
        return sentences.getRandomSentenceFromId('songNotFound')


def playArtist(artist):
    songs_found = sp.search(q=("artist:" + artist), limit=10, type='track')['tracks']['items']
    if len(songs_found) > 0:
        track_uri = songs_found[random.randint(0, len(songs_found))][
            'uri']
        sp.add_to_queue(uri=track_uri)
        sp.next_track()
        return sentences.getRandomSentenceFromId('doneSir')
    else:
        return sentences.getRandomSentenceFromId('songNotFound')


def playSongWithoutArtist(song):
    songs_found = sp.search(q=("track:" + song), limit=3, type='track')['tracks']['items']
    if len(songs_found) > 0:
        track_uri = songs_found[0]['uri']
        sp.add_to_queue(uri=track_uri)
        sp.next_track()
        return sentences.getRandomSentenceFromId('doneSir')
    else:
        return sentences.getRandomSentenceFromId('songNotFound')


def is_music_playing():
    return sp.current_user_playing_track()['is_playing']


def get_infos_playing_song():
    song_info = sp.current_user_playing_track()
    artist = song_info['item']['artists'][0]['name']
    song = song_info['item']['name']

    return [song, artist]
