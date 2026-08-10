"""YouTube integration module"""

import os
from pathlib import Path
from typing import Optional, List, Dict
import subprocess
import json

try:
    from yt_dlp import YoutubeDL
except ImportError:
    YoutubeDL = None


class YouTubeManager:
    """Manager for YouTube interactions"""
    
    def __init__(self):
        """Initialize YouTube manager"""
        self.config_dir = Path.home() / ".dj-app"
        self.config_dir.mkdir(exist_ok=True)
        
        self.download_dir = self.config_dir / "downloads"
        self.download_dir.mkdir(exist_ok=True)
        
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'outtmpl': str(self.download_dir / '%(title)s.%(ext)s'),
            'quiet': False,
            'no_warnings': False,
            'extract_audio': True,
            'audio_format': 'mp3',
            'audio_quality': '192',
        }
    
    def search_videos(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Search for videos on YouTube
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of video dictionaries
        """
        if not YoutubeDL:
            print("❌ yt-dlp not installed. Install: pip install yt-dlp")
            return []
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                search_query = f"ytsearch{limit}:{query}"
                results = ydl.extract_info(search_query, download=False)
                
                videos = []
                for item in results.get('entries', []):
                    video = {
                        'id': item.get('id'),
                        'title': item.get('title'),
                        'duration': item.get('duration'),
                        'channel': item.get('uploader'),
                        'views': item.get('view_count'),
                        'url': item.get('webpage_url'),
                        'thumbnail': item.get('thumbnail'),
                        'description': item.get('description', ''),
                    }
                    videos.append(video)
                
                return videos
                
        except Exception as e:
            print(f"❌ Error searching YouTube: {e}")
            return []
    
    def get_video_info(self, url: str) -> Optional[Dict]:
        """
        Get information about a video
        
        Args:
            url: YouTube video URL
            
        Returns:
            Video information dictionary
        """
        if not YoutubeDL:
            return None
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                video = {
                    'id': info.get('id'),
                    'title': info.get('title'),
                    'duration': info.get('duration'),
                    'channel': info.get('uploader'),
                    'views': info.get('view_count'),
                    'url': info.get('webpage_url'),
                    'thumbnail': info.get('thumbnail'),
                    'description': info.get('description', ''),
                    'upload_date': info.get('upload_date'),
                }
                
                return video
                
        except Exception as e:
            print(f"❌ Error getting video info: {e}")
            return None
    
    def download_audio(self, url: str, progress_callback=None) -> Optional[str]:
        """
        Download audio from YouTube video
        
        Args:
            url: YouTube video URL
            progress_callback: Callback function for progress updates
            
        Returns:
            Path to downloaded audio file
        """
        if not YoutubeDL:
            return None
        
        try:
            video_info = self.get_video_info(url)
            if not video_info:
                return None
            
            print(f"⬇️  Stahuji: {video_info['title']}...")
            
            ydl_opts = self.ydl_opts.copy()
            
            if progress_callback:
                def progress_hook(d):
                    if d['status'] == 'downloading':
                        progress_callback(d.get('_percent_str', ''))
                    elif d['status'] == 'finished':
                        progress_callback('Konvertuji na MP3...')
                
                ydl_opts['progress_hooks'] = [progress_hook]
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                mp3_path = str(self.download_dir / f"{info.get('title')}.mp3")
                
                print(f"✅ Staženo: {filename}")
                return mp3_path
                
        except Exception as e:
            print(f"❌ Error downloading audio: {e}")
            return None
    
    def search_playlists(self, query: str, limit: int = 10) -> List[Dict]:
        """
        Search for playlists on YouTube
        
        Args:
            query: Search query
            limit: Maximum results
            
        Returns:
            List of playlist dictionaries
        """
        if not YoutubeDL:
            return []
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                search_query = f"ytsearchall:{query}"
                results = ydl.extract_info(search_query, download=False)
                
                playlists = []
                count = 0
                
                for item in results.get('entries', []):
                    if 'entries' in item and count < limit:
                        playlist = {
                            'id': item.get('id'),
                            'title': item.get('title'),
                            'channel': item.get('uploader'),
                            'url': item.get('webpage_url'),
                            'video_count': len(item.get('entries', [])),
                        }
                        playlists.append(playlist)
                        count += 1
                
                return playlists
                
        except Exception as e:
            print(f"❌ Error searching playlists: {e}")
            return []
    
    def get_playlist_videos(self, playlist_url: str) -> List[Dict]:
        """
        Get videos from a playlist
        
        Args:
            playlist_url: YouTube playlist URL
            
        Returns:
            List of video dictionaries
        """
        if not YoutubeDL:
            return []
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
            }
            
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(playlist_url, download=False)
                
                videos = []
                for entry in info.get('entries', []):
                    video = {
                        'id': entry.get('id'),
                        'title': entry.get('title'),
                        'duration': entry.get('duration'),
                        'channel': entry.get('uploader'),
                        'url': entry.get('webpage_url'),
                        'thumbnail': entry.get('thumbnail'),
                    }
                    videos.append(video)
                
                return videos
                
        except Exception as e:
            print(f"❌ Error getting playlist videos: {e}")
            return []
    
    def get_download_directory(self) -> Path:
        """Get downloads directory"""
        return self.download_dir
    
    def get_setup_instructions(self) -> str:
        """Get setup instructions"""
        return """
🎬 YOUTUBE SETUP INSTRUCTIONS
=============================

YouTube integration is ready to use!

1. YouTube videos will be downloaded as MP3 audio
2. Search for videos or playlists
3. Downloaded files are saved to:
   ~/.dj-app/downloads/

Install dependencies:
  pip install yt-dlp

Note: Ensure ffmpeg is installed:
  Ubuntu/Debian: sudo apt-get install ffmpeg
  MacOS: brew install ffmpeg
  Windows: Download from ffmpeg.org

Done! ✅
"""
