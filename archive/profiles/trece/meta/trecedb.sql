-- --------------------------
-- Tabla: concepts (ventas/retiros)
-- --------------------------
CREATE TABLE IF NOT EXISTS concepts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- --------------------------
-- Tabla: entities_type
-- --------------------------
CREATE TABLE IF NOT EXISTS entities_type (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- --------------------------
-- Tabla: entities (socios/miembros)
-- --------------------------
CREATE TABLE IF NOT EXISTS entities (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    entities_type_id INTEGER,
    tel TEXT,
    mail TEXT,
    notes TEXT,
    FOREIGN KEY (entities_type_id) REFERENCES entities_type(id)
);

-- --------------------------
-- Tabla: expenses (gastos generales)
-- --------------------------
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    amount REAL NOT NULL,
    concept_id INTEGER,
    entitie_id INTEGER,
    caja_id INTEGER,
    folio TEXT,
    description TEXT,
    notes TEXT,
    FOREIGN KEY (concept_id) REFERENCES concepts(id),
    FOREIGN KEY (entitie_id) REFERENCES entities(id)
);

-- --------------------------
-- Tabla: genetics (variedades genéticas)
-- --------------------------
CREATE TABLE IF NOT EXISTS genetics (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    tag TEXT
);

-- --------------------------
-- Tabla: modules (módulos de cultivo)
-- --------------------------
CREATE TABLE IF NOT EXISTS modules (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

-- --------------------------
-- Tabla: harvest (cosechas)
-- --------------------------
CREATE TABLE IF NOT EXISTS harvest (
    id INTEGER PRIMARY KEY,
    cut_date DATE NOT NULL,
    module_id INTEGER,
    description TEXT,
    notes TEXT,
    FOREIGN KEY (module_id) REFERENCES modules(id)
);

-- --------------------------
-- Tabla: harvest_detail (detalle por genética de cada cosecha)
-- --------------------------
CREATE TABLE IF NOT EXISTS harvest_detail (
    id INTEGER PRIMARY KEY,
    harvest_id INTEGER NOT NULL,
    genetic_id INTEGER NOT NULL,
    grams REAL NOT NULL,
    FOREIGN KEY (harvest_id) REFERENCES harvest(id),
    FOREIGN KEY (genetic_id) REFERENCES genetics(id)
);

-- --------------------------
-- Tabla: withdrawals (retiros, ventas, consumos)
-- --------------------------
CREATE TABLE IF NOT EXISTS withdrawals (
    id INTEGER PRIMARY KEY,
    date DATE NOT NULL,
    entitie_id INTEGER,
    genetic_id INTEGER,
    harvest_id INTEGER,
    grams REAL NOT NULL,
    price REAL,
    status TEXT,
    paymethod_id INTEGER,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entitie_id) REFERENCES entities(id),
    FOREIGN KEY (genetic_id) REFERENCES genetics(id),
    FOREIGN KEY (harvest_id) REFERENCES harvest(id)
);
