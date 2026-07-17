"""Zdroj - YouTube videa a audio"""

class YouTubeAudioSource:
    """Zdroj pro audio z YouTube videí"""
    
    def __init__(self, youtube_url):
        self.youtube_url = youtube_url
        self.title = None
        self.duration = None
    
    def fetch_info(self):
        """Stáhni informace o videu"""
        # TODO: Implementace pomocí yt-dlp
        print(f"Načítám: {self.youtube_url}")
    
    def download_audio(self, output_path):
        """Stáhni audio z YouTube"""
        # TODO: Implementace pomocí yt-dlp
        print(f"Stahuju audio z: {self.youtube_url}")
