-- Tabla de tipos de entidades (socio, proveedor, etc.)
CREATE TABLE IF NOT EXISTS entity_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla principal de entidades (socios, proveedores)
CREATE TABLE IF NOT EXISTS entities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    entity_type_id INTEGER NOT NULL,
    email TEXT,
    phone TEXT,
    address TEXT,
    membership_number TEXT UNIQUE,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entity_type_id) REFERENCES entity_types(id),
    UNIQUE(name, entity_type_id)
);

-- Tabla de genéticas
CREATE TABLE IF NOT EXISTS genetics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    thc_range TEXT,
    cbd_range TEXT,
    flowering_days INTEGER,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de módulos de cultivo
CREATE TABLE IF NOT EXISTS modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    capacity_plants INTEGER,
    capacity_grams INTEGER,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de conceptos para gastos
CREATE TABLE IF NOT EXISTS concepts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    category TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla de métodos de pago
CREATE TABLE IF NOT EXISTS paymethods (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    description TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Modificar la tabla prices
CREATE TABLE IF NOT EXISTS prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genetic_id INTEGER NOT NULL,
    price_per_gram DECIMAL(10,2) NOT NULL,
    price_type TEXT NOT NULL DEFAULT 'retail', 
    start_date DATE NOT NULL,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (genetic_id) REFERENCES genetics(id),
    UNIQUE(genetic_id, price_type, start_date)  
);

-- Tabla de cajas (control de efectivo)
CREATE TABLE IF NOT EXISTS cajas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE,
    balance DECIMAL(15,2) DEFAULT 0.00,
    description TEXT,
    status TEXT DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabla principal de cosechas
CREATE TABLE IF NOT EXISTS harvests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    harvest_date DATE NOT NULL,
    total_grams DECIMAL(10,2) NOT NULL,
    notes TEXT,
    status TEXT DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (module_id) REFERENCES modules(id)
);

-- Tabla de items de cosecha (por genética)
CREATE TABLE IF NOT EXISTS harvest_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    harvest_id INTEGER NOT NULL,
    genetic_id INTEGER NOT NULL,
    grams DECIMAL(10,2) NOT NULL,
    quality_notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (harvest_id) REFERENCES harvests(id),
    FOREIGN KEY (genetic_id) REFERENCES genetics(id)
);

-- Tabla de detalles de cosecha (opcional, para tracking detallado)
CREATE TABLE IF NOT EXISTS harvest_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    harvest_item_id INTEGER NOT NULL,
    detail_type TEXT NOT NULL,
    value TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (harvest_item_id) REFERENCES harvest_items(id)
);

-- Tabla de retiros (ventas a socios)
CREATE TABLE IF NOT EXISTS withdrawals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER NOT NULL,
    genetic_id INTEGER NOT NULL,
    grams DECIMAL(10,2) NOT NULL,
    price_per_gram DECIMAL(10,2) NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    withdrawal_date DATE NOT NULL,
    status TEXT DEFAULT 'completed',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entity_id) REFERENCES entities(id),
    FOREIGN KEY (genetic_id) REFERENCES genetics(id)
);

-- Tabla de gastos
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    entity_id INTEGER NOT NULL,
    concept_id INTEGER NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    expense_date DATE NOT NULL,
    folio TEXT,
    paymethod_id INTEGER,
    notes TEXT,
    status TEXT DEFAULT 'completed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (entity_id) REFERENCES entities(id),
    FOREIGN KEY (concept_id) REFERENCES concepts(id),
    FOREIGN KEY (paymethod_id) REFERENCES paymethods(id)
);

-- Tabla de movimientos de stock
CREATE TABLE IF NOT EXISTS stock_movements (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    genetic_id INTEGER NOT NULL,
    movement_type TEXT NOT NULL, -- 'in' (cosecha), 'out' (retiro), 'adjustment'
    quantity DECIMAL(10,2) NOT NULL,
    reference_table TEXT NOT NULL, -- 'harvest_items', 'withdrawals'
    reference_id INTEGER NOT NULL,
    movement_date DATE NOT NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (genetic_id) REFERENCES genetics(id)
);

-- Índices para mejor performance
CREATE INDEX IF NOT EXISTS idx_stock_movements_genetic_date ON stock_movements(genetic_id, movement_date);
CREATE INDEX IF NOT EXISTS idx_withdrawals_entity_date ON withdrawals(entity_id, withdrawal_date);
CREATE INDEX IF NOT EXISTS idx_expenses_entity_date ON expenses(entity_id, expense_date);
CREATE INDEX IF NOT EXISTS idx_harvests_date ON harvests(harvest_date);

-- Datos iniciales
INSERT OR IGNORE INTO entity_types (name, description) VALUES 
    ('socio', 'Miembro del cannabis club'),
    ('proveedor', 'Proveedor de insumos o servicios'),
    ('empleado', 'Personal de la organización'),
    ('mayorista', 'Cliente mayorista');

INSERT OR IGNORE INTO concepts (name, description, category) VALUES 
    ('fertilizantes', 'Insumos para nutrición de plantas', 'cultivo'),
    ('electricidad', 'Consumo eléctrico', 'operacion'),
    ('agua', 'Consumo de agua', 'operacion'),
    ('sustratos', 'Sustratos y tierras', 'cultivo'),
    ('mantenimiento', 'Mantenimiento de equipos', 'operacion');

INSERT OR IGNORE INTO paymethods (name, description) VALUES 
    ('efectivo', 'Pago en efectivo'),
    ('transferencia', 'Transferencia bancaria'),
    ('tarjeta', 'Pago con tarjeta');

INSERT OR IGNORE INTO cajas (name, description) VALUES 
    ('caja_principal', 'Caja principal de efectivo');