"""Widget for Spotify integration"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMessageBox,
    QProgressBar, QTabWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from dj_app.spotify.manager import SpotifyManager


class SpotifySearchThread(QThread):
    """Thread for Spotify searches"""
    
    results_ready = pyqtSignal(list)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, spotify_manager, search_type, query):
        super().__init__()
        self.spotify_manager = spotify_manager
        self.search_type = search_type
        self.query = query
    
    def run(self):
        try:
            if self.search_type == 'track':
                results = self.spotify_manager.search_tracks(self.query)
            elif self.search_type == 'artist':
                results = self.spotify_manager.search_artists(self.query)
            elif self.search_type == 'playlist':
                results = self.spotify_manager.get_playlists()
            else:
                results = []
            
            self.results_ready.emit(results)
        except Exception as e:
            self.error_occurred.emit(str(e))


class SpotifyWidget(QWidget):
    """Widget for Spotify integration"""
    
    def __init__(self, mixer):
        super().__init__()
        self.mixer = mixer
        self.spotify = SpotifyManager()
        self.is_authenticated = False
        self.init_ui()
        self.try_authenticate()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title = QLabel("🎵 Spotify")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Status
        self.status_label = QLabel("🔄 Připojuji se ke Spotify...")
        layout.addWidget(self.status_label)
        
        # Auth button
        self.auth_button = QPushButton("🔐 Připojit Spotify")
        self.auth_button.clicked.connect(self.authenticate)
        layout.addWidget(self.auth_button)
        
        # Tabs
        self.tabs = QTabWidget()
        
        # Search Tab
        search_widget = self.create_search_tab()
        self.tabs.addTab(search_widget, "🔍 Hledání")
        
        # Playlists Tab
        playlist_widget = self.create_playlists_tab()
        self.tabs.addTab(playlist_widget, "📋 Playlisty")
        
        # Liked Tracks Tab
        liked_widget = self.create_liked_tab()
        self.tabs.addTab(liked_widget, "❤️ Oblíbené")
        
        layout.addWidget(self.tabs)
        
        # Initially disable tabs
        self.tabs.setEnabled(False)
    
    def create_search_tab(self) -> QWidget:
        """Create search tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Search input
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Hledej skladby...")
        search_layout.addWidget(self.search_input)
        
        search_btn = QPushButton("🔍 Hledej")
        search_btn.clicked.connect(self.search_tracks)
        search_layout.addWidget(search_btn)
        
        layout.addLayout(search_layout)
        
        # Results
        self.search_results = QListWidget()
        self.search_results.itemDoubleClicked.connect(self.on_track_selected)
        layout.addWidget(self.search_results)
        
        return widget
    
    def create_playlists_tab(self) -> QWidget:
        """Create playlists tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Load playlists button
        load_btn = QPushButton("📋 Načíst mé playlisty")
        load_btn.clicked.connect(self.load_playlists)
        layout.addWidget(load_btn)
        
        # Playlists list
        self.playlists_list = QListWidget()
        self.playlists_list.itemDoubleClicked.connect(self.on_playlist_selected)
        layout.addWidget(self.playlists_list)
        
        # Playlist tracks
        self.playlist_tracks = QListWidget()
        self.playlist_tracks.itemDoubleClicked.connect(self.on_track_selected)
        layout.addWidget(self.playlist_tracks)
        
        return widget
    
    def create_liked_tab(self) -> QWidget:
        """Create liked tracks tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Load liked button
        load_btn = QPushButton("❤️ Načíst oblíbené skladby")
        load_btn.clicked.connect(self.load_liked_tracks)
        layout.addWidget(load_btn)
        
        # Liked tracks list
        self.liked_tracks = QListWidget()
        self.liked_tracks.itemDoubleClicked.connect(self.on_track_selected)
        layout.addWidget(self.liked_tracks)
        
        return widget
    
    def try_authenticate(self):
        """Try to authenticate with Spotify"""
        if self.spotify.authenticate():
            self.is_authenticated = True
            user = self.spotify.get_current_user()
            if user:
                self.status_label.setText(f"✅ Přihlášen jako: {user.get('display_name', 'User')}")
                self.auth_button.setText("✅ Spotify připojen")
                self.auth_button.setEnabled(False)
                self.tabs.setEnabled(True)
        else:
            self.status_label.setText("❌ Spotify není připojen")
    
    def authenticate(self):
        """Authenticate with Spotify"""
        if self.spotify.authenticate():
            self.is_authenticated = True
            self.try_authenticate()
        else:
            instructions = self.spotify.get_setup_instructions()
            QMessageBox.information(self, "Spotify Setup", instructions)
    
    def search_tracks(self):
        """Search for tracks"""
        if not self.is_authenticated:
            QMessageBox.warning(self, "Chyba", "Nejste připojeni ke Spotify")
            return
        
        query = self.search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Chyba", "Zadejte hledaný výraz")
            return
        
        self.search_results.clear()
        self.search_results.addItem("🔄 Hledám...")
        
        try:
            tracks = self.spotify.search_tracks(query)
            self.search_results.clear()
            
            for track in tracks:
                item_text = f"{track['name']} - {track['artist']}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, track)
                self.search_results.addItem(item)
        
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při hledání: {e}")
    
    def load_playlists(self):
        """Load user's playlists"""
        if not self.is_authenticated:
            QMessageBox.warning(self, "Chyba", "Nejste připojeni ke Spotify")
            return
        
        self.playlists_list.clear()
        self.playlists_list.addItem("🔄 Načítám playlisty...")
        
        try:
            playlists = self.spotify.get_playlists()
            self.playlists_list.clear()
            
            for playlist in playlists:
                item_text = f"{playlist['name']} ({playlist['tracks_count']} skladeb)"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, playlist)
                self.playlists_list.addItem(item)
        
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při načítání playlistů: {e}")
    
    def on_playlist_selected(self, item):
        """Load tracks from selected playlist"""
        playlist = item.data(Qt.UserRole)
        if not playlist:
            return
        
        self.playlist_tracks.clear()
        self.playlist_tracks.addItem("🔄 Načítám skladby...")
        
        try:
            tracks = self.spotify.get_playlist_tracks(playlist['id'])
            self.playlist_tracks.clear()
            
            for track in tracks:
                item_text = f"{track['name']} - {track['artist']}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, track)
                self.playlist_tracks.addItem(item)
        
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při načítání skladeb: {e}")
    
    def load_liked_tracks(self):
        """Load user's liked tracks"""
        if not self.is_authenticated:
            QMessageBox.warning(self, "Chyba", "Nejste připojeni ke Spotify")
            return
        
        self.liked_tracks.clear()
        self.liked_tracks.addItem("🔄 Načítám oblíbené skladby...")
        
        try:
            tracks = self.spotify.get_liked_tracks()
            self.liked_tracks.clear()
            
            for track in tracks:
                item_text = f"{track['name']} - {track['artist']}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, track)
                self.liked_tracks.addItem(item)
        
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při načítání oblíbených skladeb: {e}")
    
    def on_track_selected(self, item):
        """Handle track selection"""
        track = item.data(Qt.UserRole)
        if not track:
            return
        
        track_name = f"{track['name']} - {track['artist']}"
        self.mixer.add_source('spotify', track)
        
        QMessageBox.information(self, "✅ Přidáno", f"Skladba přidána: {track_name}")
