"""Widget pro přehrávač"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QLabel, QSlider, QListWidget, QListWidgetItem,
    QProgressBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont


class PlayerWidget(QWidget):
    """Widget pro přehrávání audio"""
    
    def __init__(self, mixer):
        super().__init__()
        self.mixer = mixer
        self.is_playing = False
        self.init_ui()
    
    def init_ui(self):
        """Inicializace UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Título
        title = QLabel("🎧 Přehrávač")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Playlist
        playlist_label = QLabel("Playlist:")
        layout.addWidget(playlist_label)
        
        self.playlist = QListWidget()
        self.playlist.itemClicked.connect(self.on_track_selected)
        layout.addWidget(self.playlist)
        
        # Progress
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(100)
        layout.addWidget(self.progress_bar)
        
        # Time labels
        time_layout = QHBoxLayout()
        self.time_current = QLabel("00:00")
        self.time_total = QLabel("00:00")
        time_layout.addWidget(self.time_current)
        time_layout.addStretch()
        time_layout.addWidget(self.time_total)
        layout.addLayout(time_layout)
        
        # Playback controls
        controls_layout = QHBoxLayout()
        
        prev_btn = QPushButton("⏮️ Předchozí")
        prev_btn.clicked.connect(self.previous_track)
        controls_layout.addWidget(prev_btn)
        
        self.play_btn = QPushButton("▶️ Přehrávat")
        self.play_btn.clicked.connect(self.toggle_playback)
        controls_layout.addWidget(self.play_btn)
        
        pause_btn = QPushButton("⏸️ Pauza")
        pause_btn.clicked.connect(self.pause_playback)
        controls_layout.addWidget(pause_btn)
        
        stop_btn = QPushButton("⏹️ Zastavit")
        stop_btn.clicked.connect(self.stop_playback)
        controls_layout.addWidget(stop_btn)
        
        next_btn = QPushButton("⏭️ Další")
        next_btn.clicked.connect(self.next_track)
        controls_layout.addWidget(next_btn)
        
        layout.addLayout(controls_layout)
        
        # Speed control
        speed_layout = QHBoxLayout()
        speed_label = QLabel("Rychlost (tempo):")
        speed_layout.addWidget(speed_label)
        
        speed_slider = QSlider(Qt.Orientation.Horizontal)
        speed_slider.setMinimum(50)
        speed_slider.setMaximum(150)
        speed_slider.setValue(100)
        speed_slider.setMinimumWidth(300)
        speed_layout.addWidget(speed_slider)
        
        speed_value = QLabel("100%")
        speed_layout.addWidget(speed_value)
        
        layout.addLayout(speed_layout)
        
        layout.addStretch()
    
    def on_track_selected(self, item):
        """Vybrani skladby"""
        print(f"Vybrána skladba: {item.text()}")
    
    def toggle_playback(self):
        """Přehrávat/Pozastavit"""
        if self.is_playing:
            self.pause_playback()
        else:
            self.play_track()
    
    def play_track(self):
        """Přehrávej skladbu"""
        self.is_playing = True
        self.play_btn.setText("⏸️ Pozastavit")
        print("Přehrávání...")
    
    def pause_playback(self):
        """Pozastavit přehrávání"""
        self.is_playing = False
        self.play_btn.setText("▶️ Přehrávat")
        print("Pozastaveno")
    
    def stop_playback(self):
        """Zastavit přehrávání"""
        self.is_playing = False
        self.play_btn.setText("▶️ Přehrávat")
        self.progress_bar.setValue(0)
        self.time_current.setText("00:00")
        print("Zastaveno")
    
    def previous_track(self):
        """Předchozí skladba"""
        print("Předchozí skladba")
    
    def next_track(self):
        """Další skladba"""
        print("Další skladba")
