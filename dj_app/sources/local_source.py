"""Zdroj - Lokální audio soubory"""

from pathlib import Path


class LocalAudioSource:
    """Zdroj pro lokální audio soubory (MP3, WAV, FLAC)"""
    
    SUPPORTED_FORMATS = [".mp3", ".wav", ".flac", ".m4a", ".ogg"]
    
    def __init__(self, file_path):
        self.file_path = Path(file_path)
        self.validate()
    
    def validate(self):
        """Ověř že soubor existuje a má podporovaný formát"""
        if not self.file_path.exists():
            raise FileNotFoundError(f"Soubor nenalezen: {self.file_path}")
        
        if self.file_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Nepodporovaný formát: {self.file_path.suffix}")
    
    def get_metadata(self):
        """Vrať metadata o souboru"""
        return {
            "path": str(self.file_path),
            "name": self.file_path.name,
            "format": self.file_path.suffix.lower(),
            "size_mb": self.file_path.stat().st_size / (1024 * 1024)
        }
