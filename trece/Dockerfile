FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    libpq-dev \
    sqlite3 \
    git curl wget \
    vim nano htop tmux tree unzip ranger ncdu \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /trece

# Copiar todo el proyecto (tu manera)
COPY . .

# Instalar dependencias (simple, como tú tenías)
RUN pip install --upgrade pip setuptools wheel \
    && pip install -e .

SHELL ["/bin/bash", "-c"]