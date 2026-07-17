# DJ App - Debian Linux

DJ aplikace pro Linux Debian s možností remixování audio zdrojů (Spotify, YouTube, MP3, WAV).

## 🎵 Funkce

- ✅ Přehrávání 2+ audio zdrojů současně
- ✅ Podpora MP3, WAV, FLAC formátů
- ✅ YouTube integrace
- ✅ Spotify integrace
- ✅ Mixování s crossfaderem
- ✅ Volume controlů
- ✅ EQ/Bass/Treble efekty
- ✅ Qpwgraph audio routing integrace
- ✅ PipeWire/JACK backend

## 📋 Požadavky

- Linux Debian 11+
- Python 3.10+
- PipeWire nebo JACK
- Qpwgraph (volitelné, pro vizuální routing)

## 🚀 Instalace

### 1. Klonování repozitáře

```bash
git clone https://github.com/ozvuceniblatnice/dj-app.git
cd dj-app
```

### 2. Automatická instalace (Debian)

```bash
chmod +x install-debian.sh
sudo ./install-debian.sh
```

### 3. Manuální instalace

```bash
# Instalace systémových závislostí
sudo apt-get update
sudo apt-get install -y \
    python3.10 \
    python3-pip \
    python3-dev \
    libpipewire-0.3-dev \
    pipewire \
    pipewire-pulse \
    qpwgraph \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev

# Instalace Python závislostí
pip3 install -r requirements.txt
```

## 📦 Python závislosti

- `PyQt6` - desktopové GUI
- `sounddevice` - audio I/O
- `numpy` - audio processing
- `scipy` - DSP filtry
- `pydub` - audio manipulace
- `yt-dlp` - stahování z YouTube
- `spotipy` - Spotify API

## 🎮 Spuštění aplikace

```bash
python3 dj_app/main.py
```

## 📁 Struktura projektu

```
dj-app/
├── dj_app/
│   ├── __init__.py
│   ├── main.py                 # Hlavní aplikace
│   ├── gui/
│   │   ├── __init__.py
│   │   ├── main_window.py      # Hlavní okno
│   │   ├── mixer_widget.py     # Mixer UI
│   │   ├── player_widget.py    # Player UI
│   │   └── effects_widget.py   # Effects UI
│   ├── audio/
│   │   ├── __init__.py
│   │   ├── player.py           # Audio přehrávač
│   │   ├── mixer.py            # Audio mixer
│   │   ├── effects.py          # Audio efekty
│   │   └── pipewire.py         # PipeWire integrace
│   ├── sources/
│   │   ├── __init__.py
│   │   ├── local_source.py     # Lokální soubory
│   │   ├── youtube_source.py   # YouTube integrace
│   │   └── spotify_source.py   # Spotify integrace
│   └── utils/
│       ├── __init__.py
│       └── config.py           # Konfigurační soubory
├── requirements.txt
├── setup.py
├── install-debian.sh
├── Dockerfile
└── README.md
```

## 🔧 Konfigurace

### Spotify API

1. Jdi na https://developer.spotify.com
2. Vytvoř aplikaci a získej `Client ID` a `Client Secret`
3. Vytvoř soubor `~/.dj-app/spotify.conf`:

```ini
[spotify]
client_id = YOUR_CLIENT_ID
client_secret = YOUR_CLIENT_SECRET
redirect_uri = http://localhost:8888/callback
```

### PipeWire/JACK

Aplikace automaticky detekuje dostupný audio engine (PipeWire nebo JACK).

Pro manuální konfiguraci PipeWire:

```bash
systemctl --user start pipewire
systemctl --user start pipewire-pulse
```

## 🐳 Docker

```bash
docker build -t dj-app .
docker run -it --device /dev/snd --device /dev/dri -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix dj-app
```

## 📖 Dokumentace

Více informací najdeš v `docs/` složce:
- `INSTALLATION.md` - Detailní instalace
- `USAGE.md` - Návod na použití
- `API.md` - API dokumentace
- `TROUBLESHOOTING.md` - Řešení problémů

## 🐛 Hlášení chyb

Prosím hlásit chyby na: https://github.com/ozvuceniblatnice/dj-app/issues

## 📝 Licence

MIT License - viz LICENSE soubor

## 👨‍💻 Autor

DJ App - Created for Linux audio enthusiasts

---

**Pozn:** Aplikace je v beta stadiu. Hlášení chyb a Pull Requests jsou vítány!
