"""Spotify integration module"""

import os
from pathlib import Path
from typing import Optional, List, Dict
import webbrowser
import json

import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyManager:
    """Manager for Spotify API interactions"""
    
    def __init__(self):
        """Initialize Spotify manager"""
        self.config_dir = Path.home() / ".dj-app"
        self.config_dir.mkdir(exist_ok=True)
        
        self.client_id = os.getenv("SPOTIFY_CLIENT_ID", "")
        self.client_secret = os.getenv("SPOTIFY_CLIENT_SECRET", "")
        self.redirect_uri = "http://localhost:8888/callback"
        
        self.sp = None
        self.is_authenticated = False
        
    def authenticate(self) -> bool:
        """
        Authenticate with Spotify
        Returns True if successful, False otherwise
        """
        if not self.client_id or not self.client_secret:
            return False
        
        try:
            auth_manager = SpotifyOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scope=[
                    "playlist-read-private",
                    "playlist-read-collaborative",
                    "user-library-read",
                    "user-read-playback-state",
                    "streaming"
                ],
                cache_path=str(self.config_dir / ".spotify_cache")
            )
            
            self.sp = spotipy.Spotify(auth_manager=auth_manager)
            
            # Test if authenticated
            user = self.sp.current_user()
            self.is_authenticated = True
            return True
            
        except Exception as e:
            print(f"❌ Spotify authentication failed: {e}")
            self.is_authenticated = False
            return False
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current authenticated user info"""
        if not self.is_authenticated or not self.sp:
            return None
        
        try:
            return self.sp.current_user()
        except Exception as e:
            print(f"Error getting current user: {e}")
            return None
    
    def search_tracks(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Search for tracks on Spotify
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of track dictionaries
        """
        if not self.is_authenticated or not self.sp:
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
                    'duration_ms': item['duration_ms'],
                    'uri': item['uri'],
                    'preview_url': item.get('preview_url'),
                    'image_url': item['album']['images'][0]['url'] if item['album']['images'] else None
                }
                tracks.append(track)
            
            return tracks
            
        except Exception as e:
            print(f"Error searching tracks: {e}")
            return []
    
    def search_artists(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Search for artists on Spotify
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of artist dictionaries
        """
        if not self.is_authenticated or not self.sp:
            return []
        
        try:
            results = self.sp.search(q=query, type='artist', limit=limit)
            artists = []
            
            for item in results['artists']['items']:
                artist = {
                    'id': item['id'],
                    'name': item['name'],
                    'genres': item['genres'],
                    'followers': item['followers']['total'],
                    'uri': item['uri'],
                    'image_url': item['images'][0]['url'] if item['images'] else None
                }
                artists.append(artist)
            
            return artists
            
        except Exception as e:
            print(f"Error searching artists: {e}")
            return []
    
    def get_artist_top_tracks(self, artist_id: str) -> List[Dict]:
        """
        Get top tracks for an artist
        
        Args:
            artist_id: Spotify artist ID
            
        Returns:
            List of track dictionaries
        """
        if not self.is_authenticated or not self.sp:
            return []
        
        try:
            results = self.sp.artist_top_tracks(artist_id)
            tracks = []
            
            for item in results['tracks']:
                track = {
                    'id': item['id'],
                    'name': item['name'],
                    'artist': ', '.join([artist['name'] for artist in item['artists']]),
                    'album': item['album']['name'],
                    'duration_ms': item['duration_ms'],
                    'uri': item['uri'],
                    'preview_url': item.get('preview_url'),
                    'image_url': item['album']['images'][0]['url'] if item['album']['images'] else None
                }
                tracks.append(track)
            
            return tracks
            
        except Exception as e:
            print(f"Error getting artist top tracks: {e}")
            return []
    
    def get_playlists(self) -> List[Dict]:
        """
        Get user's playlists
        
        Returns:
            List of playlist dictionaries
        """
        if not self.is_authenticated or not self.sp:
            return []
        
        try:
            results = self.sp.current_user_playlists(limit=50)
            playlists = []
            
            for item in results['items']:
                playlist = {
                    'id': item['id'],
                    'name': item['name'],
                    'uri': item['uri'],
                    'tracks_count': item['tracks']['total'],
                    'image_url': item['images'][0]['url'] if item['images'] else None
                }
                playlists.append(playlist)
            
            return playlists
            
        except Exception as e:
            print(f"Error getting playlists: {e}")
            return []
    
    def get_playlist_tracks(self, playlist_id: str) -> List[Dict]:
        """
        Get tracks from a playlist
        
        Args:
            playlist_id: Spotify playlist ID
            
        Returns:
            List of track dictionaries
        """
        if not self.is_authenticated or not self.sp:
            return []
        
        try:
            results = self.sp.playlist_tracks(playlist_id)
            tracks = []
            
            for item in results['items']:
                if item['track']:
                    track = {
                        'id': item['track']['id'],
                        'name': item['track']['name'],
                        'artist': ', '.join([artist['name'] for artist in item['track']['artists']]),
                        'album': item['track']['album']['name'],
                        'duration_ms': item['track']['duration_ms'],
                        'uri': item['track']['uri'],
                        'preview_url': item['track'].get('preview_url'),
                        'image_url': item['track']['album']['images'][0]['url'] if item['track']['album']['images'] else None
                    }
                    tracks.append(track)
            
            return tracks
            
        except Exception as e:
            print(f"Error getting playlist tracks: {e}")
            return []
    
    def get_liked_tracks(self) -> List[Dict]:
        """
        Get user's liked tracks
        
        Returns:
            List of track dictionaries
        """
        if not self.is_authenticated or not self.sp:
            return []
        
        try:
            results = self.sp.current_user_saved_tracks(limit=50)
            tracks = []
            
            for item in results['items']:
                track = {
                    'id': item['track']['id'],
                    'name': item['track']['name'],
                    'artist': ', '.join([artist['name'] for artist in item['track']['artists']]),
                    'album': item['track']['album']['name'],
                    'duration_ms': item['track']['duration_ms'],
                    'uri': item['track']['uri'],
                    'preview_url': item['track'].get('preview_url'),
                    'image_url': item['track']['album']['images'][0]['url'] if item['track']['album']['images'] else None
                }
                tracks.append(track)
            
            return tracks
            
        except Exception as e:
            print(f"Error getting liked tracks: {e}")
            return []
    
    def get_recommendations(self, seed_tracks: List[str] = None, 
                           seed_artists: List[str] = None,
                           limit: int = 20) -> List[Dict]:
        """
        Get track recommendations
        
        Args:
            seed_tracks: List of track IDs
            seed_artists: List of artist IDs
            limit: Maximum results
            
        Returns:
            List of track dictionaries
        """
        if not self.is_authenticated or not self.sp:
            return []
        
        try:
            results = self.sp.recommendations(
                seed_tracks=seed_tracks or [],
                seed_artists=seed_artists or [],
                limit=limit
            )
            tracks = []
            
            for item in results['tracks']:
                track = {
                    'id': item['id'],
                    'name': item['name'],
                    'artist': ', '.join([artist['name'] for artist in item['artists']]),
                    'album': item['album']['name'],
                    'duration_ms': item['duration_ms'],
                    'uri': item['uri'],
                    'preview_url': item.get('preview_url'),
                    'image_url': item['album']['images'][0]['url'] if item['album']['images'] else None
                }
                tracks.append(track)
            
            return tracks
            
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            return []
    
    def get_setup_instructions(self) -> str:
        """Get setup instructions for Spotify API"""
        return """
🎵 SPOTIFY SETUP INSTRUCTIONS
============================

1. Go to: https://developer.spotify.com/dashboard
2. Create a new app
3. Accept the terms and create

4. Copy your credentials:
   - Client ID
   - Client Secret

5. Add to ~/.dj-app/.env file:
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret

6. Set Redirect URI in Spotify dashboard to:
   http://localhost:8888/callback

7. Restart the application

Done! ✅
"""
