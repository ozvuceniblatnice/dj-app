"""Audio efekty"""

import numpy as np
from scipy import signal


class AudioEffects:
    """Třída pro audio efekty"""
    
    def __init__(self, sample_rate=44100):
        self.sample_rate = sample_rate
    
    def apply_eq(self, audio, bass=0, mid=0, treble=0):
        """Aplikuj 3-band ekvalizér
        
        Args:
            audio: numpy array s audio daty
            bass: -12 až 12 dB
            mid: -12 až 12 dB
            treble: -12 až 12 dB
        
        Returns:
            numpy array s aplikovaným EQ
        """
        # Konvertuj dB na lineární
        bass_gain = 10 ** (bass / 20)
        mid_gain = 10 ** (mid / 20)
        treble_gain = 10 ** (treble / 20)
        
        # Vytvoř filtry
        nyquist = self.sample_rate / 2
        
        # Bass filter (low-pass)
        bass_order = 4
        bass_cutoff = 200 / nyquist
        bass_b, bass_a = signal.butter(bass_order, bass_cutoff, btype='low')
        
        # Mid filter (band-pass)
        mid_low = 200 / nyquist
        mid_high = 4000 / nyquist
        mid_b, mid_a = signal.butter(4, [mid_low, mid_high], btype='band')
        
        # Treble filter (high-pass)
        treble_cutoff = 4000 / nyquist
        treble_b, treble_a = signal.butter(bass_order, treble_cutoff, btype='high')
        
        # Aplikuj filtry
        bass_filtered = signal.filtfilt(bass_b, bass_a, audio) * bass_gain
        mid_filtered = signal.filtfilt(mid_b, mid_a, audio) * mid_gain
        treble_filtered = signal.filtfilt(treble_b, treble_a, audio) * treble_gain
        
        # Mix
        output = bass_filtered + mid_filtered + treble_filtered
        
        return output
    
    def apply_delay(self, audio, delay_ms=500, feedback=0.5):
        """Aplikuj delay efekt
        
        Args:
            audio: numpy array s audio daty
            delay_ms: delay v milisekundách
            feedback: feedback (0-1)
        
        Returns:
            numpy array s aplikovaným delay
        """
        delay_samples = int(delay_ms * self.sample_rate / 1000)
        
        # Vytvoř delay buffer
        delay_buffer = np.zeros(delay_samples)
        output = np.copy(audio)
        
        for i in range(len(audio)):
            # Přičti delay signál
            output[i] += delay_buffer[i % delay_samples] * feedback
            # Ulož do buffer
            delay_buffer[i % delay_samples] = output[i]
        
        return output
    
    def apply_reverb(self, audio, room_size=0.5):
        """Aplikuj reverb efekt
        
        Args:
            audio: numpy array s audio daty
            room_size: velikost místnosti (0-1)
        
        Returns:
            numpy array s aplikovaným reverb
        """
        # Zjednodušený reverb pomocí více delays
        delays = [50, 125, 200, 350]  # ms
        output = np.copy(audio)
        
        for delay_ms in delays:
            delayed = self.apply_delay(audio, delay_ms, room_size * 0.4)
            output += delayed * 0.25
        
        return output
    
    def apply_low_pass_filter(self, audio, cutoff_hz=5000):
        """Aplikuj low-pass filtr
        
        Args:
            audio: numpy array s audio daty
            cutoff_hz: cut-off frekvence v Hz
        
        Returns:
            numpy array s aplikovaným filtrem
        """
        nyquist = self.sample_rate / 2
        normalized_cutoff = cutoff_hz / nyquist
        
        b, a = signal.butter(4, normalized_cutoff, btype='low')
        output = signal.filtfilt(b, a, audio)
        
        return output
