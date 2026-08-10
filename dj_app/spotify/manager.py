"""Spotify integration module"""

import os
from pathlib import Path
from typing import Optional, List, Dict
import json

try:
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth
except ImportError:
    spotipy = None
    SpotifyOAuth = None


class SpotifyManager:
    """Manager for Spotify interactions"""
    
    def __init__(self):
        """Initialize Spotify manager"""
        self.config_dir = Path.home() / ".dj-app"
        self.config_dir.mkdir(exist_ok=True)
        
        self.sp = None
        self.is_authenticated = False
        
        # Spotify API credentials (will be set by user)
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID', '')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET', '')
        self.redirect_uri = 'http://localhost:8888/callback'
    
    def authenticate(self) -> bool:
        """
        Authenticate with Spotify
        
        Returns:
            True if authenticated, False otherwise
        """
        if not spotipy:
            print("❌ Spotify library not installed. Install: pip install spotipy")
            return False
        
        if not self.client_id or not self.client_secret:
            print("❌ Spotify credentials not set. Set SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET")
            return False
        
        try:
            auth_manager = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope="playlist-read-private playlist-read-collaborative user-library-read"
            )
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            self.is_authenticated = True
            return True
        except Exception as e:
            print(f"❌ Authentication failed: {e}")
            return False
    
    def get_current_user(self) -> Optional[Dict]:
        """
        Get current user info
        
        Returns:
            User information dictionary
        """
        if not self.sp:
            return None
        
        try:
            return self.sp.current_user()
        except Exception as e:
            print(f"❌ Error getting user: {e}")
            return None
    
    def search_tracks(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Search for tracks
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of track dictionaries
        """
        if not self.sp:
            return []
        
        try:
            results = self.sp.search(q=query, type='track', limit=limit)
            tracks = []
            
            for item in results['tracks']['items']:
                track = {
                    'id': item['id'],
                    'name': item['name'],
                    'artist': ', '.join([artist['name'] for artist in item['artists']]),
                    'album': item['album']['name'],
                    'url': item['external_urls']['spotify'],
                    'preview_url': item['preview_url'],
                    'duration_ms': item['duration_ms'],
                }
                tracks.append(track)
            
            return tracks
        except Exception as e:
            print(f"❌ Error searching tracks: {e}")
            return []
    
    def search_artists(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Search for artists
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of artist dictionaries
        """
        if not self.sp:
            return []
        
        try:
            results = self.sp.search(q=query, type='artist', limit=limit)
            artists = []
            
            for item in results['artists']['items']:
                artist = {
                    'id': item['id'],
                    'name': item['name'],
                    'url': item['external_urls']['spotify'],
                    'genres': item.get('genres', []),
                    'followers': item['followers']['total'],
                }
                artists.append(artist)
            
            return artists
        except Exception as e:
            print(f"❌ Error searching artists: {e}")
            return []
    
    def get_playlists(self) -> List[Dict]:
        """
        Get user's playlists
        
        Returns:
            List of playlist dictionaries
        """
        if not self.sp:
            return []
        
        try:
            results = self.sp.current_user_playlists(limit=50)
            playlists = []
            
            for item in results['items']:
                playlist = {
                    'id': item['id'],
                    'name': item['name'],
                    'url': item['external_urls']['spotify'],
                    'tracks_count': item['tracks']['total'],
                }
                playlists.append(playlist)
            
            return playlists
        except Exception as e:
            print(f"❌ Error getting playlists: {e}")
            return []
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Dict]:
        """
        Get tracks from a playlist
        
        Args:
            playlist_id: Playlist ID
            
        Returns:
            List of track dictionaries
        """
        if not self.sp:
            return []
        
        try:
            results = self.sp.playlist_tracks(playlist_id)
            tracks = []
            
            for item in results['items']:
                track_info = item['track']
                if track_info:
                    track = {
                        'id': track_info['id'],
                        'name': track_info['name'],
                        'artist': ', '.join([artist['name'] for artist in track_info['artists']]),
                        'album': track_info['album']['name'],
                        'url': track_info['external_urls']['spotify'],
                        'preview_url': track_info['preview_url'],
                        'duration_ms': track_info['duration_ms'],
                    }
                    tracks.append(track)
            
            return tracks
        except Exception as e:
            print(f"❌ Error getting playlist tracks: {e}")
            return []
    
    def get_liked_tracks(self) -> List[Dict]:
        """
        Get user's liked tracks
        
        Returns:
            List of track dictionaries
        """
        if not self.sp:
            return []
        
        try:
            results = self.sp.current_user_saved_tracks(limit=50)
            tracks = []
            
            for item in results['items']:
                track_info = item['track']
                track = {
                    'id': track_info['id'],
                    'name': track_info['name'],
                    'artist': ', '.join([artist['name'] for artist in track_info['artists']]),
                    'album': track_info['album']['name'],
                    'url': track_info['external_urls']['spotify'],
                    'preview_url': track_info['preview_url'],
                    'duration_ms': track_info['duration_ms'],
                }
                tracks.append(track)
            
            return tracks
        except Exception as e:
            print(f"❌ Error getting liked tracks: {e}")
            return []
    
    def get_setup_instructions(self) -> str:
        """Get setup instructions"""
        return """
🎵 SPOTIFY SETUP INSTRUCTIONS
==============================

1. Go to: https://developer.spotify.com/dashboard
2. Create a new app
3. Get your Client ID and Client Secret
4. Set environment variables:
   export SPOTIFY_CLIENT_ID='your_client_id'
   export SPOTIFY_CLIENT_SECRET='your_client_secret'

5. Install spotipy:
   pip install spotipy

6. Then restart DJ App!

Done! ✅
"""
