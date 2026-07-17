"""Audio přehrávač"""

import threading
from pathlib import Path


class AudioPlayer:
    """Třída pro přehrávání audio souborů"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.is_playing = False
        self.current_file = None
        self.playback_thread = None
    
    def load_file(self, file_path):
        """Načti audio soubor"""
        file_path = Path(file_path)
        
        if not file_path.exists():
            raise FileNotFoundError(f"Soubor nenalezen: {file_path}")
        
        if file_path.suffix.lower() not in ['.mp3', '.wav', '.flac', '.m4a']:
            raise ValueError(f"Nepodporovaný formát: {file_path.suffix}")
        
        self.current_file = str(file_path)
        print(f"✅ Soubor načten: {self.current_file}")
    
    def play(self):
        """Přehraj audio"""
        if not self.current_file:
            raise RuntimeError("Žádný soubor nebyl načten")
        
        self.is_playing = True
        print(f"▶️  Přehrávám: {self.current_file}")
    
    def pause(self):
        """Pozastav přehrávání"""
        self.is_playing = False
        print("⏸️  Pozastaveno")
    
    def stop(self):
        """Zastavit přehrávání"""
        self.is_playing = False
        self.current_file = None
        print("⏹️  Zastaveno")
