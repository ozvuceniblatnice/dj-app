# DJ App - Troubleshooting & FAQ

## Časté Problémy

### 1. "ModuleNotFoundError: No module named 'PyQt6'"

**Příčina:** PyQt6 není nainstalován

**Řešení:**
```bash
pip3 install PyQt6 PyQt6-sip
```

### 2. "PipeWire is not running"

**Příčina:** Audio engine není spuštěn

**Řešení:**
```bash
systemctl --user start pipewire
systemctl --user start pipewire-pulse

# Ověř
systemctl --user status pipewire
```

### 3. "Cannot open audio device"

**Příčina:** Audio zařízení není dostupné

**Řešení:**
```bash
# Zkontroluj dostupná zařízení
python3 -c "import sounddevice; print(sounddevice.query_devices())"

# Zkontroluj PipeWire zařízení
pwctl status
```

### 4. "No sound output"

**Příčina:** Problém s audio routingem

**Řešení:**
```bash
# Otevři Qpwgraph pro vizuální routing
qpwgraph

# Zkontroluj zda je aplikace připojená k výstupu
```

### 5. "GUI doesn't appear"

**Příčina:** Problém s X11/Wayland

**Řešení:**
```bash
# Zkontroluj DISPLAY
echo $DISPLAY

# Případně nastav
export DISPLAY=:0
```

### 6. "Audio buffer underrun / crackles"

**Příčina:** Příliš nízký buffer size nebo vysoká CPU zátěž

**Řešení:**
```json
// ~/.dj-app/config.json
{
  "audio": {
    "buffer_size": 2048  // Zvyš z 512 na 2048
  }
}
```

Nebo:
```bash
# Zvyš prioritu procesu
sudo nice -n -10 python3 dj_app/main.py

# Zavři ostatní aplikace
killall firefox chromium spotify
```

### 7. "YouTube download fails"

**Příčina:** yt-dlp není nainstalován nebo nefunguje

**Řešení:**
```bash
pip3 install --upgrade yt-dlp

# Zkontroluj
yt-dlp --version
```

### 8. "Spotify authentication error"

**Příčina:** Chybné credentials

**Řešení:**
1. Jdi na https://developer.spotify.com/dashboard
2. Ověř Client ID a Client Secret
3. Aktualizuj `~/.dj-app/spotify.conf`

## FAQ

### Q: Jaký je minimální požadavek?

**A:** 
- Debian/Ubuntu Linux
- Python 3.10+
- 2GB RAM
- PipeWire nebo JACK

### Q: Můžu použít JACK místo PipeWire?

**A:** Ano! JACK je také podporován. Stačí instalovat `jack2` místo `pipewire`.

```bash
sudo apt-get install jack2 qjackctl
```

### Q: Jak nahraju výstup?

**A:** Pomocí `pw-record` nebo `ffmpeg`:

```bash
# Metoda 1: PipeWire record
pw-record --format=F32 mix.wav

# Metoda 2: FFmpeg
ffmpeg -f pulse -i default output.mp3
```

### Q: Jaká je latence?

**A:** Závisí na buffer size:
- Buffer 512: ~12ms latency
- Buffer 1024: ~24ms latency
- Buffer 2048: ~48ms latency

### Q: Mohu udělat livestream?

**A:** Ano! Můžeš streamovat přes OBS:

```bash
# V OBS: Audio Input = ALSA/PipeWire výstup aplikace
```

### Q: Jaké formáty jsou podporované?

**A:** 
- MP3
- WAV
- FLAC
- M4A
- OGG

### Q: Mohu mixit 3+ skladby?

**A:** V základní verzi 2 kanály. Pro 3+ kanály:
- Rozšiř `mixer.py` a přidej více kanálů
- Nebo použij Qpwgraph pro komplexní routingy

### Q: Je volný software?

**A:** Ano! MIT License - můžeš ho používat a modifikovat volně.

## Diagnostika

### Kompletní diagnostika

```bash
echo "=== System Info ==="
uname -a
echo ""
echo "=== Python ==="
python3 --version
echo ""
echo "=== PipeWire ==="
systemctl --user status pipewire
echo ""
echo "=== Audio Devices ==="
python3 -c "import sounddevice; print(sounddevice.query_devices())"
echo ""
echo "=== Python Modules ==="
python3 -c "import PyQt6; print('PyQt6 OK')"
python3 -c "import sounddevice; print('sounddevice OK')"
python3 -c "import numpy; print('numpy OK')"
```

## Kontakt a Podpora

- **GitHub Issues:** https://github.com/ozvuceniblatnice/dj-app/issues
- **Dokumentace:** Viz `docs/` složka
- **Source Code:** https://github.com/ozvuceniblatnice/dj-app
