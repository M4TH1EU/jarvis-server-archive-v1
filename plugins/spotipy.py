import os

import spotipy
from spotipy.oauth2 import SpotifyOAuth

scope = "user-read-playback-state, user-modify-playback-state, user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               client_id=os.getenv('SPOTIFY_CLIENT_ID'),
                                               client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
                                               redirect_uri='http://localhost:8888/callback/'))


def playSong(artist, song):
    track_uri = sp.search(q=("artist:" + artist + " track:" + song), limit=3)['tracks']['items'][0]['uri']
    sp.add_to_queue(uri=track_uri)
    sp.next_track()


def playSongWithoutArtist(song):
    track_uri = sp.search(q=("track:" + song), limit=3)['tracks']['items'][0]['uri']
    sp.add_to_queue(uri=track_uri)
    sp.next_track()
