#!/usr/bin/env python3
"""
DJ App - Hlavní aplikace
Desktopová DJ aplikace pro Linux Debian
"""

import sys
import os
from pathlib import Path

from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import Qt

from dj_app.gui.main_window import MainWindow
from dj_app.utils.config import Config


def setup_config():
    """
    Inicializace konfigurační složky a souborů
    """
    config_dir = Path.home() / ".dj-app"
    config_dir.mkdir(exist_ok=True)
    
    # Vytvoř default konfiguraci pokud neexistuje
    config_file = config_dir / "config.json"
    if not config_file.exists():
        Config.create_default_config()


def main():
    """
    Hlavní funkce aplikace
    """
    print("="*50)
    print("🎵 DJ App - Linux DJ Mixer")
    print("="*50)
    print()
    
    # Inicializace konfigurace
    setup_config()
    print("✅ Konfigurace inicializována")
    
    # Vytvoř Qt aplikaci
    app = QApplication(sys.argv)
    app.setApplicationName("DJ App")
    app.setApplicationVersion("0.1.0")
    app.setStyle("Fusion")
    
    # Vytvoř hlavní okno
    print("🖼️  Otevírám hlavní okno...")
    main_window = MainWindow()
    main_window.show()
    
    print("✅ Aplikace je připravena!")
    print()
    print("Tipy:")
    print("  - Vlož audiosoubory (MP3, WAV) pomocí 'Přidat zdroj'")
    print("  - Otevři Qpwgraph pro pokročilý audio routing")
    print("  - Zkontroluj PipeWire status: systemctl --user status pipewire")
    print()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
