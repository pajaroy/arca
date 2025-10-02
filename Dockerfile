FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Instalar utilidades y compiladores necesarios
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpq-dev \
    gcc \
    gfortran \
    vim wget git curl htop tmux tree unzip direnv \
    sqlite3 nano ranger ncdu \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /arca

# Copiar todo el proyecto
COPY . /arca

# Upgrade pip e instalar proyecto editable
RUN pip install --no-cache-dir --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -e .

SHELL ["/bin/bash", "-c"]   