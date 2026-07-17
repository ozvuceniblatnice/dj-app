FROM debian:bookworm

# Nastav locale
ENV DEBIAN_FRONTEND=noninteractive
ENV LANG=cs_CZ.UTF-8

# Instalace základních balíčků
RUN apt-get update && apt-get install -y \
    python3.11 \
    python3-pip \
    python3-dev \
    build-essential \
    git \
    pipewire \
    pipewire-pulse \
    pipewire-jack \
    pipewire-alsa \
    libpipewire-0.3-dev \
    wireplumber \
    qpwgraph \
    ffmpeg \
    libavcodec-dev \
    libavformat-dev \
    libavdevice-dev \
    libswresample-dev \
    libsndfile1 \
    sox \
    libssl-dev \
    libffi-dev \
    qt6-base-dev \
    libqt6core6 \
    libqt6gui6 \
    libqt6multimedia6 \
    && rm -rf /var/lib/apt/lists/*

# Pracovní adresář
WORKDIR /app

# Kopíruj projekt
COPY . /app

# Instalace Python závislostí
RUN pip3 install --upgrade pip setuptools wheel && \
    pip3 install -r requirements.txt

# Vytvoř konfigurační složku
RUN mkdir -p ~/.dj-app

# Spustit aplikaci
CMD ["python3", "dj_app/main.py"]
