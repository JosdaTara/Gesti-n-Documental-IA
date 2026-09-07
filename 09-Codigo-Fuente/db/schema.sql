-- SIGAD - Esquema de base de datos (PostgreSQL 16 + pgvector)
-- Usado por docker-compose (nombres de objetos en minusculas por compatibilidad).

CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS categorias (
    id          SERIAL PRIMARY KEY,
    nombre      VARCHAR(60)  NOT NULL UNIQUE,
    descripcion VARCHAR(200) NOT NULL DEFAULT '',
    activa      BOOLEAN      NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS usuarios (
    id             SERIAL PRIMARY KEY,
    nombre         VARCHAR(120) NOT NULL,
    email          VARCHAR(160) NOT NULL UNIQUE,
    password_hash  VARCHAR(256) NOT NULL,
    rol            VARCHAR(20)  NOT NULL DEFAULT 'analista',
    activo         BOOLEAN      NOT NULL DEFAULT TRUE,
    creado_en      TIMESTAMP    NOT NULL DEFAULT now(),
    ultimo_acceso  TIMESTAMP
);

CREATE TABLE IF NOT EXISTS documentos (
    id             SERIAL PRIMARY KEY,
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_archivo   VARCHAR(500) NOT NULL,
    tipo_mime      VARCHAR(120) NOT NULL DEFAULT 'application/octet-stream',
    tamano_bytes   INTEGER      NOT NULL DEFAULT 0,
    estado         VARCHAR(20)  NOT NULL DEFAULT 'pendiente',
    categoria_id   INTEGER REFERENCES categorias(id),
    confianza      NUMERIC(4, 3),
    resumen        TEXT,
    texto_extraido TEXT,
    cargado_por    INTEGER REFERENCES usuarios(id),
    cargado_en     TIMESTAMP    NOT NULL DEFAULT now(),
    procesado_en   TIMESTAMP
);
CREATE INDEX IF NOT EXISTS ix_documentos_estado ON documentos(estado);
CREATE INDEX IF NOT EXISTS ix_documentos_categoria ON documentos(categoria_id);

CREATE TABLE IF NOT EXISTS metadatos_documento (
    id           SERIAL PRIMARY KEY,
    documento_id INTEGER NOT NULL REFERENCES documentos(id) ON DELETE CASCADE,
    clave        VARCHAR(60)  NOT NULL,
    valor        VARCHAR(300) NOT NULL
);
CREATE INDEX IF NOT EXISTS ix_metadatos_documento ON metadatos_documento(documento_id);

CREATE TABLE IF NOT EXISTS chunks (
    id           SERIAL PRIMARY KEY,
    documento_id INTEGER NOT NULL REFERENCES documentos(id) ON DELETE CASCADE,
    indice       INTEGER NOT NULL DEFAULT 0,
    contenido    TEXT    NOT NULL,
    -- La aplicacion escribe el embedding como vector JSON y en produccion
    -- se indexa con pgvector (columna vector(384)) para busqueda HNSW.
    embedding    TEXT,
    activo       BOOLEAN NOT NULL DEFAULT TRUE
);
CREATE INDEX IF NOT EXISTS ix_chunks_documento ON chunks(documento_id);

CREATE TABLE IF NOT EXISTS auditoria (
    id         SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    accion     VARCHAR(60),
    detalle    TEXT,
    ip         VARCHAR(60),
    creado_en  TIMESTAMP NOT NULL DEFAULT now()
);

CREATE TABLE IF NOT EXISTS consultas (
    id         SERIAL PRIMARY KEY,
    usuario_id INTEGER REFERENCES usuarios(id),
    pregunta   TEXT NOT NULL,
    respuesta  TEXT NOT NULL,
    creado_en  TIMESTAMP NOT NULL DEFAULT now()
);