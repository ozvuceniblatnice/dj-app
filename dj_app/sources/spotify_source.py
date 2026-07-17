"""Zdroj - Spotify skladby"""

class SpotifyAudioSource:
    """Zdroj pro audio ze Spotify"""
    
    def __init__(self, spotify_track_uri):
        self.track_uri = spotify_track_uri
        self.title = None
        self.artist = None
        self.duration = None
    
    def authenticate(self, client_id, client_secret):
        """Autentizuj se se Spotify API"""
        # TODO: Implementace pomocí spotipy
        print("Autentizuji se se Spotify...")
    
    def get_stream_url(self):
        """Vrať stream URL skladby"""
        # TODO: Implementace
        return None
