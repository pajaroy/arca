---
type: "prompt"
fecha: "2025-08-21"
version: "0.1.0"
descripcion: "headers para trece.db"
---
# prompt:

te voy a pasar mis estructuras aver si se puede poner en sql. y si vamos a poder relacionar bien para hacer los retiros.

## concepts: para ventas y retiros

id,name,

## entities_type: lso tipos de entidades

id,name,

## entities: entidades qe forman la asociacion

id,name,entities_type_id,tel,mail,notes,

## expenses: gastos generales

id,date,amount,concept_id,entitie_id,caja_id,folio,description,notes

## genetics: tabla qe  marca las geneticas

id,name,description,tag,

## harvest_detail: detalle de las cosechas qe genetic tiene cada cosecha

id,harvest_id,genetic_id,grams

## harvest: cada cosecha individual

id,cut_date,module_id,description,notes,

## modules: marca los modulos de cultivo

id,name,description

## withdrawals: como tabla de retiros , qe deberiamos calcular el stock qe se va descontando.

id,date,entitie_id,genetic_id,harvest_id,grams,price,,status,paymethod_id,notes,created_at

## prices: tabla de precios

id,name,amount

## paymethods: metodos de pago transferencia y efectivo.

id,name,

# respuesta

Buenísimo 👌, gracias por pasar todas las estructuras. Esto se puede modelar muy bien en SQL. Te armo un **esquema relacional** con claves primarias y foráneas para que todo quede conectado y podás calcular stocks/retiros sin problemas.

---

## 📌 Propuesta de esquema SQL (SQLite/Postgres)

```sql
-- --------------------------
-- Tabla: concepts (ventas/retiros)
-- --------------------------
CREATE TABLE concepts (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- --------------------------
-- Tabla: entities_type
-- --------------------------
CREATE TABLE entities_type (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

-- --------------------------
-- Tabla: entities (socios/miembros)
-- --------------------------
CREATE TABLE entities (
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
CREATE TABLE expenses (
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
CREATE TABLE genetics (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    tag TEXT
);

-- --------------------------
-- Tabla: modules (módulos de cultivo)
-- --------------------------
CREATE TABLE modules (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT
);

-- --------------------------
-- Tabla: harvest (cosechas)
-- --------------------------
CREATE TABLE harvest (
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
CREATE TABLE harvest_detail (
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
CREATE TABLE withdrawals (
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
```

---

## 📊 Cómo se calcularía el stock

El **stock real** de una genética dentro de una cosecha sería:

```
stock = harvest_detail.grams - SUM(withdrawals.grams)
```

Ejemplo de consulta SQL para stock de cada `harvest`:

```sql
SELECT h.id AS harvest_id,
       g.name AS genetic,
       hd.grams AS total_cosechado,
       COALESCE(SUM(w.grams), 0) AS total_retirado,
       hd.grams - COALESCE(SUM(w.grams), 0) AS stock_actual
FROM harvest_detail hd
JOIN harvest h ON h.id = hd.harvest_id
JOIN genetics g ON g.id = hd.genetic_id
LEFT JOIN withdrawals w ON w.harvest_id = h.id AND w.genetic_id = g.id
GROUP BY h.id, g.name, hd.grams;
```

---

✅ Ventajas de este diseño:

* Todo queda **relacionado** por IDs (entities, harvest, genetics).
* Podés calcular **stocks por cosecha, genética, socio, etc.**
* Podés agregar más conceptos (ventas internas, externas, retiros personales).
* Escala fácil a más datos (con PostgreSQL, por ejemplo).

---

👉 Pregunta: ¿querés que te prepare directamente un **script en Python** que:

1. Importe tus CSV,
2. Cree la base SQLite con estas tablas,
3. Inserte los datos,
4. Y ya te permita consultar stocks y retiros?



