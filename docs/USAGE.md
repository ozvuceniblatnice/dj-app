# DJ App - Návod na Použití

## Spuštění Aplikace

```bash
python3 dj_app/main.py
```

## Uživatelské Rozhraní

### Hlavní Okno

Aplikace se skládá ze 3 hlavních sekcí:

1. **🎧 Přehrávač** - Správa skladeb a přehrávání
2. **🎚️ Mixer** - Mixování audio kanálů
3. **✨ Efekty** - Audio efekty a EQ

## Přidávání Audio Zdrojů

### Lokální Soubory (MP3, WAV)

1. Klikni na **"➕ Přidat soubor (MP3, WAV)"**
2. Vyber audio soubor z disku
3. Soubor se přidá do playlistu

### Z YouTube

1. Klikni na **"🎬 Přidat z YouTube"**
2. Vloži YouTube URL
3. Aplikace stáhne audio

### Ze Spotify

1. Klikni na **"🎵 Přidat ze Spotify"**
2. Přihlas se svým účtem
3. Vyber skladbu nebo playlist

## Přehrávání

### Ovládání Playlistu

- **▶️ Přehrávat** - Spustí vybranou skladbu
- **⏸️ Pauza** - Pozastaví přehrávání
- **⏹️ Zastavit** - Zastaví přehrávání
- **⏮️ Předchozí** - Přejdi na předchozí skladbu
- **⏭️ Další** - Přejdi na další skladbu

### Posun v Čase

Posuň progress bar na hodnotu kam chceš skočit.

## Mixer

### Crossfader

Pomáhá vytvářet smooth mix mezi dvěma kanály:

- **Vlevo** - Pouze kanál 1
- **Uprostřed** - Oba kanály stejně
- **Vpravo** - Pouze kanál 2

### Volume Kontroly

- **Volume Ch. 1** - Hlasitost kanálu 1
- **Volume Ch. 2** - Hlasitost kanálu 2
- **Master Volume** - Hlavní hlasitost výstupu

## Efekty

### Ekvalizér (3-band EQ)

- **Bass (60Hz)** - Nízké frekvence
- **Mid (1kHz)** - Střední frekvence
- **Treble (10kHz)** - Vysoké frekvence

Rozsah: -12dB až +12dB

### Echo/Delay

1. Zaškrtni **"Echo/Delay"**
2. Nastav čas v milisekundách
3. Efekt se aplikuje na výstup

### Reverb

1. Zaškrtni **"Reverb"**
2. Vyber typ místnosti:
   - Malá místnost
   - Velká místnost
   - Hala
   - Katedrála

### Low-Pass Filtr

1. Zaškrtni **"Filtr (Low-Pass)"**
2. Nastav frekvenci
3. Filtr propustí pouze nižší frekvence

## Pokročilá Práce - Qpwgraph

Pro vizuální routing audio signálů:

```bash
qpwgraph
```

V Qpwgraph můžeš:
- Vidět všechny audio aplikace a zařízení
- Propojit aplikace podle potřeby
- Vytvořit komplexní audio grafy
- Ukládat routingy

## Tipy a Triky

### Pro Začátečníky

1. Začni s jedním zdrojem (YouTube nebo lokal soubor)
2. Nauč se používat mixer a crossfader
3. Vyzkoušej efekty jeden po jednom
4. Postupně přidávaj další zdroje

### Pro Pokročilé

1. Kombinuj více efektů dohromady
2. Vytvářej loops pomocí delay efektu
3. Používej Qpwgraph pro detailní kontrolu
4. Nahrávej výstup do WAV souboru

### Nahrávání Mixu

```bash
# Nahrávej PipeWire výstup do souboru
pw-record --format=F32 output.wav
```

## Klávesové Zkratky

| Zkratka | Funkce |
|---------|--------|
| `Space` | Play/Pause |
| `→` | Příští skladba |
| `←` | Předchozí skladba |
| `Q` | Zavřít aplikaci |

## Základní DJ Techniky

### Beat Matching

1. Nastav tempo obou skladeb na stejnou hodnotu
2. Sluchu poslechni oba beaty
3. Jestli se liší, uprav tempo

### Mixing

1. Spusť první skladbu
2. Druhá skladba nech naslouchnou (na headphonech)
3. Když je ready, použij crossfader pro plynulý mix
4. Postupně přechází mezi skladbami

### EQ Mixing

1. Na konci první skladby stlum bass nové skladby
2. Pomalu zvyš bass při mixování
3. Vytvoří to plynulejší transition

## Řešení Problémů

### Žádný zvuk

1. Zkontroluj Master Volume
2. Zkontroluj hlasitost svého zařízení
3. Zkontroluj PipeWire status

### Trhavý zvuk

1. Zvyš buffer size v konfiguraci
2. Zavři ostatní aplikace
3. Zvyš prioritu procesu

### Skladba se nepřehrává

1. Zkontroluj formát souboru (MP3, WAV, FLAC)
2. Zkontroluj oprávnění k souboru
3. Ověř že soubor není poškozený
