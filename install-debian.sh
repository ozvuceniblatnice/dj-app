#!/bin/bash

# DJ App - Instalační skript pro Debian
# Spuštění: sudo ./install-debian.sh

set -e

echo "========================================"
echo "DJ App - Instalace na Debian"
echo "========================================"
echo ""

# Kontrola root práv
if [[ $EUID -ne 0 ]]; then
   echo "❌ Tento skript musí běžet s sudo právy!"
   echo "   Spusť: sudo ./install-debian.sh"
   exit 1
fi

echo "📦 Aktualizace balíčků..."
apt-get update
apt-get upgrade -y

echo ""
echo "📦 Instalace Python 3.10+..."
apt-get install -y python3.10 python3-pip python3-dev python3-venv

echo ""
echo "🔊 Instalace PipeWire a audio knihoven..."
apt-get install -y \
    pipewire \
    pipewire-pulse \
    pipewire-jack \
    pipewire-alsa \
    libpipewire-0.3-dev \
    wireplumber \
    qpwgraph

echo ""
echo "🎬 Instalace FFmpeg a audio nástrojů..."
apt-get install -y \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libavdevice-dev \
    libswresample-dev \
    libsndfile1 \
    sox

echo ""
echo "📚 Instalace vývojových knihoven..."
apt-get install -y \
    libssl-dev \
    libffi-dev \
    build-essential \
    git

echo ""
echo "🎨 Instalace Qt6 knihoven (pro GUI)..."
apt-get install -y \
    qt6-base-dev \
    libqt6core6 \
    libqt6gui6 \
    libqt6multimedia6

echo ""
echo "📂 Instalace Python závislostí z requirements.txt..."
pip3 install --upgrade pip setuptools wheel
pip3 install -r requirements.txt

echo ""
echo "✅ Instalace dokončena!"
echo ""
echo "========================================"
echo "Jak spustit aplikaci:"
echo "========================================"
echo ""
echo "1. Jdi do složky:"
echo "   cd $(pwd)"
echo ""
echo "2. Spusť aplikaci:"
echo "   python3 dj_app/main.py"
echo ""
echo "3. Nebo použij příkaz (pokud je instalován):"
echo "   dj-app"
echo ""
echo "========================================"
echo "⚠️  POZNÁMKY:"
echo "========================================"
echo ""
echo "- Ujisti se, že PipeWire běží:"
echo "  systemctl --user status pipewire"
echo ""
echo "- Pro Spotify API, vytvoř soubor ~/.dj-app/spotify.conf"
echo "  [spotify]"
echo "  client_id = YOUR_CLIENT_ID"
echo "  client_secret = YOUR_CLIENT_SECRET"
echo ""
echo "- Pro vizuální audio routing otevři Qpwgraph:"
echo "  qpwgraph"
echo ""
