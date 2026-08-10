"""Widget for YouTube integration"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QLineEdit, QListWidget, QListWidgetItem, QMessageBox,
    QProgressBar, QTabWidget
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QFont

from dj_app.youtube.manager import YouTubeManager


class YouTubeDownloadThread(QThread):
    """Thread for YouTube downloads"""
    
    download_complete = pyqtSignal(str)
    download_progress = pyqtSignal(str)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, youtube_manager, url):
        super().__init__()
        self.youtube_manager = youtube_manager
        self.url = url
    
    def run(self):
        try:
            path = self.youtube_manager.download_audio(
                self.url,
                progress_callback=self.download_progress.emit
            )
            if path:
                self.download_complete.emit(path)
            else:
                self.error_occurred.emit("Selhalo stažení")
        except Exception as e:
            self.error_occurred.emit(str(e))


class YouTubeWidget(QWidget):
    """Widget for YouTube integration"""
    
    def __init__(self, mixer):
        super().__init__()
        self.mixer = mixer
        self.youtube = YouTubeManager()
        self.download_thread = None
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)
        
        # Title
        title = QLabel("🎬 YouTube")
        title_font = QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)
        
        # Tabs
        tabs = QTabWidget()
        
        # Video Search Tab
        video_tab = self.create_video_search_tab()
        tabs.addTab(video_tab, "🎥 Videa")
        
        # URL Download Tab
        url_tab = self.create_url_download_tab()
        tabs.addTab(url_tab, "🔗 URL")
        
        # Playlist Tab
        playlist_tab = self.create_playlist_tab()
        tabs.addTab(playlist_tab, "📋 Playlisty")
        
        layout.addWidget(tabs)
    
    def create_video_search_tab(self) -> QWidget:
        """Create video search tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Search input
        search_layout = QHBoxLayout()
        self.video_search_input = QLineEdit()
        self.video_search_input.setPlaceholderText("Hledej videa na YouTube...")
        search_layout.addWidget(self.video_search_input)
        
        search_btn = QPushButton("🔍 Hledej")
        search_btn.clicked.connect(self.search_videos)
        search_layout.addWidget(search_btn)
        
        layout.addLayout(search_layout)
        
        # Results
        self.video_results = QListWidget()
        self.video_results.itemDoubleClicked.connect(self.on_video_selected)
        layout.addWidget(self.video_results)
        
        # Download button
        download_btn = QPushButton("⬇️ Stáhnout a přidat")
        download_btn.clicked.connect(self.download_selected_video)
        layout.addWidget(download_btn)
        
        # Progress bar
        self.video_progress = QProgressBar()
        self.video_progress.setVisible(False)
        layout.addWidget(self.video_progress)
        
        return widget
    
    def create_url_download_tab(self) -> QWidget:
        """Create URL download tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # URL input
        url_layout = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Vlož YouTube URL...")
        url_layout.addWidget(self.url_input)
        
        layout.addLayout(url_layout)
        
        # Video info
        self.video_info_label = QLabel("")
        layout.addWidget(self.video_info_label)
        
        # Get info button
        info_btn = QPushButton("ℹ️ Načíst informace")
        info_btn.clicked.connect(self.get_video_info)
        layout.addWidget(info_btn)
        
        # Download button
        download_btn = QPushButton("⬇️ Stáhnout audio")
        download_btn.clicked.connect(self.download_url_video)
        layout.addWidget(download_btn)
        
        # Progress bar
        self.url_progress = QProgressBar()
        self.url_progress.setVisible(False)
        layout.addWidget(self.url_progress)
        
        layout.addStretch()
        
        return widget
    
    def create_playlist_tab(self) -> QWidget:
        """Create playlist tab"""
        widget = QWidget()
        layout = QVBoxLayout(widget)
        
        # Playlist URL input
        url_layout = QHBoxLayout()
        self.playlist_url_input = QLineEdit()
        self.playlist_url_input.setPlaceholderText("Vlož YouTube Playlist URL...")
        url_layout.addWidget(self.playlist_url_input)
        
        load_btn = QPushButton("📋 Načíst playlist")
        load_btn.clicked.connect(self.load_playlist)
        url_layout.addWidget(load_btn)
        
        layout.addLayout(url_layout)
        
        # Playlist items
        self.playlist_items = QListWidget()
        self.playlist_items.itemDoubleClicked.connect(self.on_playlist_item_selected)
        layout.addWidget(self.playlist_items)
        
        # Download all button
        download_all_btn = QPushButton("⬇️ Stáhnout všechny")
        download_all_btn.clicked.connect(self.download_all_playlist)
        layout.addWidget(download_all_btn)
        
        return widget
    
    def search_videos(self):
        """Search for videos"""
        query = self.video_search_input.text().strip()
        if not query:
            QMessageBox.warning(self, "Chyba", "Zadejte hledaný výraz")
            return
        
        self.video_results.clear()
        self.video_results.addItem("🔄 Hledám...")
        
        try:
            videos = self.youtube.search_videos(query)
            self.video_results.clear()
            
            for video in videos:
                duration = f"({video['duration']}s)" if video['duration'] else ""
                item_text = f"{video['title']} {duration}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, video)
                self.video_results.addItem(item)
            
            if not videos:
                self.video_results.addItem("Žádná videa nenalezena")
        
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při hledání: {e}")
    
    def on_video_selected(self, item):
        """Handle video selection"""
        video = item.data(Qt.UserRole)
        if video:
            print(f"Vybrané video: {video['title']}")
    
    def download_selected_video(self):
        """Download selected video"""
        current_item = self.video_results.currentItem()
        if not current_item:
            QMessageBox.warning(self, "Chyba", "Vyberte video")
            return
        
        video = current_item.data(Qt.UserRole)
        if not video:
            return
        
        url = video['url']
        self.start_download(url)
    
    def get_video_info(self):
        """Get info about video from URL"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Chyba", "Zadejte YouTube URL")
            return
        
        self.video_info_label.setText("🔄 Načítám...")
        
        try:
            video = self.youtube.get_video_info(url)
            if video:
                duration = f"{video['duration'] // 60}:{video['duration'] % 60:02d}" if video['duration'] else "?"
                views = f"{video['views']:,}" if video['views'] else "?"
                info_text = f"""
                📺 {video['title']}
                👤 {video['channel']}
                ⏱️  {duration}
                👁️  {views} zhlédnutí
                """
                self.video_info_label.setText(info_text)
            else:
                self.video_info_label.setText("❌ Nepodařilo se načíst informace")
        
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba: {e}")
    
    def download_url_video(self):
        """Download video from URL"""
        url = self.url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Chyba", "Zadejte YouTube URL")
            return
        
        self.start_download(url)
    
    def start_download(self, url: str):
        """Start download thread"""
        self.url_progress.setVisible(True)
        self.url_progress.setValue(0)
        
        self.download_thread = YouTubeDownloadThread(self.youtube, url)
        self.download_thread.download_complete.connect(self.on_download_complete)
        self.download_thread.download_progress.connect(self.on_download_progress)
        self.download_thread.error_occurred.connect(self.on_download_error)
        self.download_thread.start()
    
    def on_download_progress(self, progress: str):
        """Update download progress"""
        self.url_progress.setFormat(f"Stažení: {progress}")
    
    def on_download_complete(self, file_path: str):
        """Handle download completion"""
        self.url_progress.setVisible(False)
        self.mixer.add_source('youtube', file_path)
        QMessageBox.information(self, "✅ Staženo", f"Audio přidáno do playlistu!")
    
    def on_download_error(self, error: str):
        """Handle download error"""
        self.url_progress.setVisible(False)
        QMessageBox.critical(self, "Chyba", f"Chyba při stahování: {error}")
    
    def load_playlist(self):
        """Load playlist from URL"""
        url = self.playlist_url_input.text().strip()
        if not url:
            QMessageBox.warning(self, "Chyba", "Zadejte Playlist URL")
            return
        
        self.playlist_items.clear()
        self.playlist_items.addItem("🔄 Načítám playlist...")
        
        try:
            videos = self.youtube.get_playlist_videos(url)
            self.playlist_items.clear()
            
            for video in videos:
                item_text = f"{video['title']}"
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, video)
                self.playlist_items.addItem(item)
            
            if not videos:
                self.playlist_items.addItem("Žádná videa v playlistu")
        
        except Exception as e:
            QMessageBox.critical(self, "Chyba", f"Chyba při načítání: {e}")
    
    def on_playlist_item_selected(self, item):
        """Download selected playlist item"""
        video = item.data(Qt.UserRole)
        if video:
            url = video['url']
            self.start_download(url)
    
    def download_all_playlist(self):
        """Download all videos from playlist"""
        QMessageBox.information(
            self,
            "Hromadné stahování",
            "Tato funkce bude implementována v příští verzi.\n\nPro teď stahujte videa jednotlivě." 
        )
