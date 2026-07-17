"""Widget pro efekty"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSlider,
    QLabel, QCheckBox, QComboBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class EffectsWidget(QWidget):
    """Widget pro audio efekty"""
    
    def __init__(self, mixer):
        super().__init__()
        self.mixer = mixer
        self.init_ui()
    
    def init_ui(self):
        """Inicializace UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título
        title = QLabel("✨ Audio Efekty")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # EQ Section
        eq_label = QLabel("🎛️ Ekvalizér (3-band EQ)")
        eq_font = QFont()
        eq_font.setBold(True)
        eq_label.setFont(eq_font)
        layout.addWidget(eq_label)
        
        # Bass
        bass_layout = QHBoxLayout()
        bass_label = QLabel("Bass (60Hz):")
        bass_label.setMinimumWidth(120)
        bass_layout.addWidget(bass_label)
        
        bass_slider = QSlider(Qt.Orientation.Horizontal)
        bass_slider.setMinimum(-12)
        bass_slider.setMaximum(12)
        bass_slider.setValue(0)
        bass_slider.setMinimumWidth(300)
        bass_layout.addWidget(bass_slider)
        
        bass_value = QLabel("0 dB")
        bass_layout.addWidget(bass_value)
        
        layout.addLayout(bass_layout)
        
        # Mid
        mid_layout = QHBoxLayout()
        mid_label = QLabel("Mid (1kHz):")
        mid_label.setMinimumWidth(120)
        mid_layout.addWidget(mid_label)
        
        mid_slider = QSlider(Qt.Orientation.Horizontal)
        mid_slider.setMinimum(-12)
        mid_slider.setMaximum(12)
        mid_slider.setValue(0)
        mid_slider.setMinimumWidth(300)
        mid_layout.addWidget(mid_slider)
        
        mid_value = QLabel("0 dB")
        mid_layout.addWidget(mid_value)
        
        layout.addLayout(mid_layout)
        
        # Treble
        treble_layout = QHBoxLayout()
        treble_label = QLabel("Treble (10kHz):")
        treble_label.setMinimumWidth(120)
        treble_layout.addWidget(treble_label)
        
        treble_slider = QSlider(Qt.Orientation.Horizontal)
        treble_slider.setMinimum(-12)
        treble_slider.setMaximum(12)
        treble_slider.setValue(0)
        treble_slider.setMinimumWidth(300)
        treble_layout.addWidget(treble_slider)
        
        treble_value = QLabel("0 dB")
        treble_layout.addWidget(treble_value)
        
        layout.addLayout(treble_layout)
        
        # Effects Section
        effects_label = QLabel("🎨 Efekty")
        effects_font = QFont()
        effects_font.setBold(True)
        effects_label.setFont(effects_font)
        layout.addWidget(effects_label)
        
        # Echo/Delay
        echo_layout = QHBoxLayout()
        echo_checkbox = QCheckBox("Echo/Delay")
        echo_layout.addWidget(echo_checkbox)
        
        echo_time_label = QLabel("Čas (ms):")
        echo_layout.addWidget(echo_time_label)
        
        echo_slider = QSlider(Qt.Orientation.Horizontal)
        echo_slider.setMinimum(0)
        echo_slider.setMaximum(1000)
        echo_slider.setValue(500)
        echo_slider.setMaximumWidth(150)
        echo_layout.addWidget(echo_slider)
        
        echo_value = QLabel("500")
        echo_layout.addWidget(echo_value)
        echo_layout.addStretch()
        
        layout.addLayout(echo_layout)
        
        # Reverb
        reverb_layout = QHBoxLayout()
        reverb_checkbox = QCheckBox("Reverb")
        reverb_layout.addWidget(reverb_checkbox)
        
        reverb_type_label = QLabel("Typ:")
        reverb_layout.addWidget(reverb_type_label)
        
        reverb_combo = QComboBox()
        reverb_combo.addItems(["Malá místnost", "Velká místnost", "Hala", "Katedrála"])
        reverb_combo.setMaximumWidth(150)
        reverb_layout.addWidget(reverb_combo)
        reverb_layout.addStretch()
        
        layout.addLayout(reverb_layout)
        
        # Filter
        filter_layout = QHBoxLayout()
        filter_checkbox = QCheckBox("Filtr (Low-Pass)")
        filter_layout.addWidget(filter_checkbox)
        
        filter_freq_label = QLabel("Frekvence (Hz):")
        filter_layout.addWidget(filter_freq_label)
        
        filter_slider = QSlider(Qt.Orientation.Horizontal)
        filter_slider.setMinimum(100)
        filter_slider.setMaximum(20000)
        filter_slider.setValue(20000)
        filter_slider.setMaximumWidth(150)
        filter_layout.addWidget(filter_slider)
        
        filter_value = QLabel("20k")
        filter_layout.addWidget(filter_value)
        filter_layout.addStretch()
        
        layout.addLayout(filter_layout)
        
        layout.addStretch()
