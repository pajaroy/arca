-- Script de creación de la base de datos
CREATE TABLE IF NOT EXISTS archivos (
    -- Identificación básica
    ruta TEXT NOT NULL,
    nombre TEXT NOT NULL,
    tipo TEXT NOT NULL,
    
    -- Metadatos técnicos
    tamano_bytes INTEGER CHECK (tamano_bytes >= 0),
    fecha_mod TEXT CHECK (datetime(fecha_mod) IS NOT NULL),
    hash_blake3 TEXT UNIQUE,
    
    -- Contenido y análisis
    contenido TEXT,
    palabras_limpias TEXT,  -- JSON array
    entidades TEXT,         -- JSON: {"personas": [], ...}
    
    -- Relaciones y metadatos extendidos
    linked_to TEXT,         -- JSON: {"parent": "hash", "tipo": "derivado"}
    metadata TEXT,          -- JSON crudo
    
    -- Índices
    INDEX idx_hash (hash_blake3),
    INDEX idx_tipo (tipo),
    INDEX idx_fecha (fecha_mod),
    INDEX idx_entidades (entidades)
);

-- Configuración de rendimiento (opcional pero recomendado)
PRAGMA journal_mode = WAL;
PRAGMA synchronous = NORMAL;