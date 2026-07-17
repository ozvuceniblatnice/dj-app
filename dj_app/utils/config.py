"""Konfigurační soubory"""

import json
from pathlib import Path


class Config:
    """Správce konfigurace DJ App"""
    
    CONFIG_DIR = Path.home() / ".dj-app"
    CONFIG_FILE = CONFIG_DIR / "config.json"
    
    DEFAULT_CONFIG = {
        "audio": {
            "sample_rate": 44100,
            "buffer_size": 2048,
            "engine": "pipewire"
        },
        "gui": {
            "theme": "dark",
            "window_width": 1200,
            "window_height": 800
        },
        "spotify": {
            "enabled": False,
            "client_id": "",
            "client_secret": ""
        },
        "youtube": {
            "enabled": True
        }
    }
    
    @classmethod
    def create_default_config(cls):
        """Vytvoř default konfiguraci"""
        cls.CONFIG_DIR.mkdir(exist_ok=True)
        
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(cls.DEFAULT_CONFIG, f, indent=2)
        
        print(f"✅ Konfigurační soubor vytvořen: {cls.CONFIG_FILE}")
    
    @classmethod
    def load_config(cls):
        """Načti konfiguraci"""
        if not cls.CONFIG_FILE.exists():
            cls.create_default_config()
        
        with open(cls.CONFIG_FILE, 'r') as f:
            config = json.load(f)
        
        return config
    
    @classmethod
    def save_config(cls, config):
        """Ulož konfiguraci"""
        cls.CONFIG_DIR.mkdir(exist_ok=True)
        
        with open(cls.CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
        
        print(f"✅ Konfigurační soubor uložen")
