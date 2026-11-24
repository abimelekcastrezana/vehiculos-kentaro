CREATE TABLE IF NOT EXISTS usuarios (
    id       INTEGER PRIMARY KEY,
    nombre   TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS marcas (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS tipos (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS lotes (
    id     INTEGER PRIMARY KEY,
    nombre TEXT NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS vehiculos (
    id          INTEGER PRIMARY KEY,
    marca_id    INTEGER NOT NULL REFERENCES marcas(id),
    tipo_id     INTEGER NOT NULL REFERENCES tipos(id),
    lote_id     INTEGER NOT NULL REFERENCES lotes(id),
    modelo      TEXT NOT NULL,
    anio        INTEGER NOT NULL,
    precio      REAL NOT NULL,
    descripcion TEXT NOT NULL,
    imagen_url  TEXT
);

-- Datos iniciales para los selects
INSERT OR IGNORE INTO marcas (nombre) VALUES ('Nissan'), ('Toyota'), ('Ford'), ('Chevrolet');
INSERT OR IGNORE INTO tipos  (nombre) VALUES ('Sedán'), ('SUV'), ('Pickup'), ('Hatchback');
INSERT OR IGNORE INTO lotes  (nombre) VALUES ('Lote A'), ('Lote B'), ('Lote C');
