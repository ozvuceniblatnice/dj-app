"""Hlavní okno aplikace DJ App"""

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QSlider, QFileDialog,
    QListWidget, QListWidgetItem, QMessageBox,
    QTabWidget, QStatusBar, QDialog
)
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QIcon, QFont

from dj_app.gui.mixer_widget import MixerWidget
from dj_app.gui.player_widget import PlayerWidget
from dj_app.gui.effects_widget import EffectsWidget
from dj_app.gui.spotify_widget import SpotifyWidget
from dj_app.gui.youtube_widget import YouTubeWidget
from dj_app.audio.mixer import AudioMixer


class MainWindow(QMainWindow):
    """Hlavní okno aplikace"""
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DJ App - Linux DJ Mixer")
        self.setGeometry(100, 100, 1400, 900)
        
        # Audio mixer
        self.mixer = AudioMixer()
        
        # Inicializuj UI
        self.init_ui()
        
    def init_ui(self):
        """Inicializace uživatelského rozhraní"""
        
        # Hlavní widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Hlavní layout
        main_layout = QVBoxLayout(main_widget)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Titulky
        title_label = QLabel("🎵 DJ App - Linux DJ Mixer")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        main_layout.addWidget(title_label)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Player Tab
        player_tab = PlayerWidget(self.mixer)
        self.tabs.addTab(player_tab, "🎧 Přehrávač")
        
        # Mixer Tab
        mixer_tab = MixerWidget(self.mixer)
        self.tabs.addTab(mixer_tab, "🎚️ Mixer")
        
        # Effects Tab
        effects_tab = EffectsWidget(self.mixer)
        self.tabs.addTab(effects_tab, "✨ Efekty")
        
        # Spotify Tab
        spotify_tab = SpotifyWidget(self.mixer)
        self.tabs.addTab(spotify_tab, "🎵 Spotify")
        
        # YouTube Tab
        youtube_tab = YouTubeWidget(self.mixer)
        self.tabs.addTab(youtube_tab, "🎬 YouTube")
        
        main_layout.addWidget(self.tabs)
        
        # Kontrolní tlačítka dole
        controls_layout = QHBoxLayout()
        
        add_file_btn = QPushButton("➕ Přidat soubor (MP3, WAV)")
        add_file_btn.setMinimumHeight(40)
        add_file_btn.clicked.connect(self.add_audio_file)
        controls_layout.addWidget(add_file_btn)
        
        add_spotify_btn = QPushButton("🎵 Spotify")
        add_spotify_btn.setMinimumHeight(40)
        add_spotify_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(3))
        controls_layout.addWidget(add_spotify_btn)
        
        add_youtube_btn = QPushButton("🎬 YouTube")
        add_youtube_btn.setMinimumHeight(40)
        add_youtube_btn.clicked.connect(lambda: self.tabs.setCurrentIndex(4))
        controls_layout.addWidget(add_youtube_btn)
        
        main_layout.addLayout(controls_layout)
        
        # Status bar
        self.statusBar().showMessage("Připraveno | PipeWire: Připojeno | Spotify: Připraveno | YouTube: Připraveno")
        
    def add_audio_file(self):
        """Přidej audio soubor"""
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(
            self,
            "Vyber audio soubor",
            "",
            "Audio soubory (*.mp3 *.wav *.flac *.m4a);;Všechny soubory (*)"
        )
        
        if file_path:
            self.mixer.add_source("file", file_path)
            self.statusBar().showMessage(f"Přidáno: {file_path}")
            QMessageBox.information(self, "Úspěch", f"Soubor přidán: {file_path}")
    
    def closeEvent(self, event):
        """Zavření aplikace"""
        self.mixer.stop()
        event.accept()
