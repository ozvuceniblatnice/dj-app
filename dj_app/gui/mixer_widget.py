"""Widget pro mixer"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QSlider,
    QLabel, QSpinBox, QDoubleSpinBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


class MixerWidget(QWidget):
    """Widget pro kontrolu mixeru"""
    
    def __init__(self, mixer):
        super().__init__()
        self.mixer = mixer
        self.init_ui()
    
    def init_ui(self):
        """Inicializace UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título
        title = QLabel("🎚️ Audio Mixer - Crossfader & Volume")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Crossfader
        crossfader_layout = QHBoxLayout()
        crossfader_label = QLabel("Crossfader:")
        crossfader_label.setMinimumWidth(100)
        crossfader_layout.addWidget(crossfader_label)
        
        crossfader_slider = QSlider(Qt.Orientation.Horizontal)
        crossfader_slider.setMinimum(0)
        crossfader_slider.setMaximum(100)
        crossfader_slider.setValue(50)
        crossfader_slider.setMinimumWidth(300)
        crossfader_slider.sliderMoved.connect(self.on_crossfader_changed)
        crossfader_layout.addWidget(crossfader_slider)
        
        crossfader_value = QLabel("50%")
        crossfader_value.setMinimumWidth(50)
        crossfader_layout.addWidget(crossfader_value)
        
        layout.addLayout(crossfader_layout)
        
        # Volume Channel 1
        vol1_layout = QHBoxLayout()
        vol1_label = QLabel("Volume Ch. 1:")
        vol1_label.setMinimumWidth(100)
        vol1_layout.addWidget(vol1_label)
        
        vol1_slider = QSlider(Qt.Orientation.Horizontal)
        vol1_slider.setMinimum(0)
        vol1_slider.setMaximum(100)
        vol1_slider.setValue(70)
        vol1_slider.setMinimumWidth(300)
        vol1_slider.sliderMoved.connect(self.on_volume_ch1_changed)
        vol1_layout.addWidget(vol1_slider)
        
        vol1_value = QLabel("70%")
        vol1_value.setMinimumWidth(50)
        vol1_layout.addWidget(vol1_value)
        
        layout.addLayout(vol1_layout)
        
        # Volume Channel 2
        vol2_layout = QHBoxLayout()
        vol2_label = QLabel("Volume Ch. 2:")
        vol2_label.setMinimumWidth(100)
        vol2_layout.addWidget(vol2_label)
        
        vol2_slider = QSlider(Qt.Orientation.Horizontal)
        vol2_slider.setMinimum(0)
        vol2_slider.setMaximum(100)
        vol2_slider.setValue(70)
        vol2_slider.setMinimumWidth(300)
        vol2_slider.sliderMoved.connect(self.on_volume_ch2_changed)
        vol2_layout.addWidget(vol2_slider)
        
        vol2_value = QLabel("70%")
        vol2_value.setMinimumWidth(50)
        vol2_layout.addWidget(vol2_value)
        
        layout.addLayout(vol2_layout)
        
        # Master Volume
        master_layout = QHBoxLayout()
        master_label = QLabel("Master Volume:")
        master_label.setMinimumWidth(100)
        master_layout.addWidget(master_label)
        
        master_slider = QSlider(Qt.Orientation.Horizontal)
        master_slider.setMinimum(0)
        master_slider.setMaximum(100)
        master_slider.setValue(80)
        master_slider.setMinimumWidth(300)
        master_slider.sliderMoved.connect(self.on_master_changed)
        master_layout.addWidget(master_slider)
        
        master_value = QLabel("80%")
        master_value.setMinimumWidth(50)
        master_layout.addWidget(master_value)
        
        layout.addLayout(master_layout)
        
        layout.addStretch()
        
    def on_crossfader_changed(self, value):
        """Změna crossfaderu"""
        print(f"Crossfader: {value}%")
    
    def on_volume_ch1_changed(self, value):
        """Změna volume channel 1"""
        print(f"Volume Ch.1: {value}%")
    
    def on_volume_ch2_changed(self, value):
        """Změna volume channel 2"""
        print(f"Volume Ch.2: {value}%")
    
    def on_master_changed(self, value):
        """Změna master volume"""
        print(f"Master Volume: {value}%")
