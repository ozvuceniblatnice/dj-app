"""Audio mixer - mixování více zdrojů"""

import numpy as np
from collections import defaultdict


class AudioMixer:
    """Třída pro mixování audio zdrojů"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
        self.sources = {}
        self.volumes = defaultdict(lambda: 1.0)
        self.is_running = False
        
    def add_source(self, source_type, source_path):
        """Přidej audio zdroj"""
        print(f"Přidávám zdroj ({source_type}): {source_path}")
        
        source_id = f"{source_type}_{len(self.sources)}"
        
        if source_type == "file":
            self.sources[source_id] = {
                "type": "file",
                "path": source_path,
                "volume": 1.0,
                "playing": False
            }
            print(f"✅ Zdroj přidán: {source_id}")
            return source_id
        
        return None
    
    def remove_source(self, source_id):
        """Odeber audio zdroj"""
        if source_id in self.sources:
            del self.sources[source_id]
            print(f"✅ Zdroj odebran: {source_id}")
    
    def set_volume(self, source_id, volume):
        """Nastav hlasitost zdroje (0.0 - 1.0)"""
        if source_id in self.sources:
            self.sources[source_id]["volume"] = max(0.0, min(1.0, volume))
    
    def play_source(self, source_id):
        """Přehraj audio zdroj"""
        if source_id in self.sources:
            self.sources[source_id]["playing"] = True
            print(f"▶️  Přehrávám: {source_id}")
    
    def pause_source(self, source_id):
        """Pozastav audio zdroj"""
        if source_id in self.sources:
            self.sources[source_id]["playing"] = False
            print(f"⏸️  Pozastaven: {source_id}")
    
    def stop_source(self, source_id):
        """Zastavit audio zdroj"""
        if source_id in self.sources:
            self.sources[source_id]["playing"] = False
            print(f"⏹️  Zastaveno: {source_id}")
    
    def mix_sources(self, frame_size=1024):
        """Mixuj audio zdroje a vrať výsledný frame
        
        Returns:
            numpy array s mixovaným audio
        """
        mixed = np.zeros(frame_size)
        
        for source_id, source in self.sources.items():
            if source["playing"]:
                # Simulace audio dat
                audio_frame = np.random.randn(frame_size) * 0.01
                # Aplikuj hlasitost
                audio_frame *= source["volume"]
                mixed += audio_frame
        
        # Normalizuj aby se zabránilo clipping
        max_val = np.max(np.abs(mixed))
        if max_val > 1.0:
            mixed = mixed / max_val
        
        return mixed
    
    def get_sources(self):
        """Vrať seznam všech zdrojů"""
        return list(self.sources.keys())
    
    def stop(self):
        """Zastavit mixer"""
        self.is_running = False
        for source_id in self.sources:
            self.stop_source(source_id)
        print("🛑 Mixer zastaven")
