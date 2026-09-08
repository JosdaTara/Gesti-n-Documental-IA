-- =====================================================================
-- SIGAD - Sistema de Gestión Documental con IA
-- 10. Base de Datos - Scripts
-- 01-Esquema-MySQL.sql
-- Motor: MySQL 8.x (XAMPP / MySQL Server)
-- BD:   gestion_documental_bd
-- Nota: los nombres de tablas/columnas coinciden con SQLAlchemy (models.py)
--       y responden a la lógica de la aplicación.
-- =====================================================================

CREATE DATABASE IF NOT EXISTS gestion_documental_bd
  DEFAULT CHARACTER SET utf8mb4
  DEFAULT COLLATE utf8mb4_spanish_ci;

USE gestion_documental_bd;

-- ---------------------------------------------------------------------
-- CATEGORIAS: clasificación documental (se almacenan en mayúsculas)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS categorias (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre      VARCHAR(60)  NOT NULL,
    descripcion VARCHAR(200) NOT NULL DEFAULT '',
    activa      TINYINT(1)   NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    UNIQUE KEY uq_categorias_nombre (nombre)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- ---------------------------------------------------------------------
-- USUARIOS: acceso al sistema (roles administrador | analista)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS usuarios (
    id             INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre         VARCHAR(120) NOT NULL,
    email          VARCHAR(160) NOT NULL,
    password_hash  VARCHAR(256) NOT NULL,
    rol            VARCHAR(20)  NOT NULL DEFAULT 'analista',
    activo         TINYINT(1)   NOT NULL DEFAULT 1,
    creado_en      DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultimo_acceso  DATETIME     NULL,
    PRIMARY KEY (id),
    UNIQUE KEY uq_usuarios_email (email),
    KEY ix_usuarios_email (email)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- ---------------------------------------------------------------------
-- DOCUMENTOS: expediente documental gestionado por el sistema
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS documentos (
    id             INT UNSIGNED NOT NULL AUTO_INCREMENT,
    nombre_archivo VARCHAR(255) NOT NULL,
    ruta_archivo   VARCHAR(500) NOT NULL,
    tipo_mime      VARCHAR(120) NOT NULL DEFAULT 'application/octet-stream',
    tamano_bytes   INT          NOT NULL DEFAULT 0,
    estado         VARCHAR(20)  NOT NULL DEFAULT 'pendiente',
    categoria_id   INT UNSIGNED NULL,
    confianza      DECIMAL(4, 3)     NULL,
    resumen        TEXT         NULL,
    texto_extraido TEXT         NULL,
    cargado_por    INT UNSIGNED NULL,
    cargado_en     DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    procesado_en   DATETIME     NULL,
    PRIMARY KEY (id),
    KEY ix_documentos_estado (estado),
    KEY ix_documentos_categoria (categoria_id),
    KEY ix_documentos_cargado_por (cargado_por),
    CONSTRAINT fk_documentos_categoria FOREIGN KEY (categoria_id)
        REFERENCES categorias (id),
    CONSTRAINT fk_documentos_usuario FOREIGN KEY (cargado_por)
        REFERENCES usuarios (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- ---------------------------------------------------------------------
-- METADATOS_DOCUMENTO: datos extraídos por la IA (fechas, montos, NIT...)
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS metadatos_documento (
    id           INT UNSIGNED NOT NULL AUTO_INCREMENT,
    documento_id INT UNSIGNED NOT NULL,
    clave        VARCHAR(60)  NOT NULL,
    valor        VARCHAR(300) NOT NULL,
    PRIMARY KEY (id),
    KEY ix_metadatos_documento (documento_id),
    CONSTRAINT fk_metadatos_documento FOREIGN KEY (documento_id)
        REFERENCES documentos (id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- ---------------------------------------------------------------------
-- CHUNKS: fragmentos del texto extraído con su vector de embedding.
--  - embedding: vector JSON (MEDIUMTEXT). En la app se usa el modelo
--    openai/text-embedding-3-large (3072 dimensiones) vía OpenRouter.
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS chunks (
    id           INT UNSIGNED NOT NULL AUTO_INCREMENT,
    documento_id INT UNSIGNED NOT NULL,
    indice       INT          NOT NULL DEFAULT 0,
    contenido    TEXT         NOT NULL,
    embedding    MEDIUMTEXT   NULL,
    activo       TINYINT(1)   NOT NULL DEFAULT 1,
    PRIMARY KEY (id),
    KEY ix_chunks_documento (documento_id),
    CONSTRAINT fk_chunks_documento FOREIGN KEY (documento_id)
        REFERENCES documentos (id) ON DELETE CASCADE
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- ---------------------------------------------------------------------
-- AUDITORIA: registro de acciones de los usuarios
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS auditoria (
    id         INT UNSIGNED NOT NULL AUTO_INCREMENT,
    usuario_id INT UNSIGNED NULL,
    accion     VARCHAR(60)  NOT NULL,
    detalle    TEXT         NULL,
    ip         VARCHAR(60)  NULL,
    creado_en  DATETIME     NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_auditoria_usuario (usuario_id),
    CONSTRAINT fk_auditoria_usuario FOREIGN KEY (usuario_id)
        REFERENCES usuarios (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

-- ---------------------------------------------------------------------
-- CONSULTAS: historial de preguntas/respuestas del asistente RAG
-- ---------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS consultas (
    id         INT UNSIGNED NOT NULL AUTO_INCREMENT,
    usuario_id INT UNSIGNED NULL,
    pregunta   TEXT NOT NULL,
    respuesta  TEXT NOT NULL,
    creado_en  DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ix_consultas_usuario (usuario_id),
    CONSTRAINT fk_consultas_usuario FOREIGN KEY (usuario_id)
        REFERENCES usuarios (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;