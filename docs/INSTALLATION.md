# DJ App - Instalační Průvodce

## Systémové Požadavky

- **OS:** Linux (Debian 11+, Ubuntu 22.04+)
- **Python:** 3.10+
- **RAM:** Minimálně 2GB (doporučeno 4GB+)
- **Disk:** 500MB volného místa
- **Audio:** PipeWire nebo JACK

## Kroková Instalace

### 1. Příprava Systému

Nejdřív aktualizuj systém:

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2. Klonování Repozitáře

```bash
git clone https://github.com/ozvuceniblatnice/dj-app.git
cd dj-app
```

### 3. Automatická Instalace (Doporučeno)

```bash
chmod +x install-debian.sh
sudo ./install-debian.sh
```

Skript nainstaluje všechny potřebné závislosti automaticky.

### 4. Manuální Instalace

Jestli preferuješ manuální instalaci:

#### Instalace Systémových Balíčků

```bash
# PipeWire a audio knihovny
sudo apt-get install -y pipewire pipewire-pulse pipewire-jack qpwgraph

# FFmpeg a audio nástroje
sudo apt-get install -y ffmpeg libavcodec-dev libavformat-dev

# Vývojové knihovny
sudo apt-get install -y build-essential python3.10 python3-dev

# Qt6 pro GUI
sudo apt-get install -y qt6-base-dev libqt6core6 libqt6gui6
```

#### Instalace Python Závislostí

```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## Ověření Instalace

### Kontrola PipeWire

```bash
# Spusť PipeWire (má běžet automaticky)
systemctl --user start pipewire
systemctl --user start pipewire-pulse

# Ověř status
systemctl --user status pipewire
```

### Kontrola Python Závislostí

```bash
python3 -c "import PyQt6; print('PyQt6: OK')"
python3 -c "import sounddevice; print('sounddevice: OK')"
```

## Spuštění Aplikace

### Přímý Start

```bash
python3 dj_app/main.py
```

### Pomocí Entry Point (po instalaci)

```bash
dj-app
```

### S Výstupem Diagnostiky

```bash
python3 -v dj_app/main.py
```

## Konfigurace

### Spotify Integration

1. Jdi na https://developer.spotify.com/dashboard
2. Vytvoř aplikaci
3. Zkopíruj Client ID a Client Secret
4. Vytvoř `~/.dj-app/spotify.conf`:

```ini
[spotify]
client_id = YOUR_CLIENT_ID
client_secret = YOUR_CLIENT_SECRET
redirect_uri = http://localhost:8888/callback
```

### Audio Konfigurace

Glavn konfigurační soubor: `~/.dj-app/config.json`

```json
{
  "audio": {
    "sample_rate": 44100,
    "buffer_size": 2048,
    "engine": "pipewire"
  },
  "gui": {
    "theme": "dark",
    "window_width": 1200,
    "window_height": 800
  }
}
```

## Docker

### Build

```bash
docker build -t dj-app .
```

### Run

```bash
docker run -it \
  --device /dev/snd \
  --device /dev/dri \
  -e DISPLAY=$DISPLAY \
  -v /tmp/.X11-unix:/tmp/.X11-unix \
  dj-app
```

## Řešení Problémů

### Chyba: "No module named 'PyQt6'"

```bash
pip3 install PyQt6 PyQt6-sip
```

### Chyba: "PipeWire not running"

```bash
systemctl --user start pipewire
systemctl --user enable pipewire
```

### Chyba: "Audio device not found"

```bash
# Zkontroluj dostupná zařízení
python3 -c "import sounddevice; print(sounddevice.query_devices())"
```

### Chyba: "Cannot open display"

Ujisti se, že X11 nebo Wayland běží:

```bash
echo $DISPLAY
```

## Optimalizace

### Zvyšování Performance

```bash
# Zvyš prioritu procesu
sudo nice -n -10 python3 dj_app/main.py
```

### Audio Latency

Sníž buffer size v `~/.dj-app/config.json`:

```json
{
  "audio": {
    "buffer_size": 512
  }
}
```

## Uninstall

```bash
# Odeber Python balíčky
pip3 uninstall dj-app -y

# Odeber konfiguraci
rm -rf ~/.dj-app

# Odeber repozitář
rm -rf ~/dj-app
```

## Další Nápověda

- [PipeWire Dokumentace](https://pipewire.org/)
- [PyQt6 Dokumentace](https://www.riverbankcomputing.com/static/Docs/PyQt6/)
- [FFmpeg Dokumentace](https://ffmpeg.org/)
