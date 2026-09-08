-- =====================================================================
-- SIGAD - 10. Base de Datos - Scripts
-- 03-Consultas-Reportes.sql
-- Consultas para el tablero de control, auditoría y trazabilidad.
-- =====================================================================

USE gestion_documental_bd;

-- 1) Documentos por estado
SELECT estado, COUNT(*) AS cantidad
FROM documentos
GROUP BY estado
ORDER BY cantidad DESC;

-- 2) Documentos por categoría (solo procesados)
SELECT c.nombre AS categoria, COUNT(d.id) AS cantidad
FROM categorias c
LEFT JOIN documentos d
       ON d.categoria_id = c.id AND d.estado = 'procesado'
WHERE c.activa = 1
GROUP BY c.id, c.nombre
ORDER BY c.id;

-- 3) Totales del tablero
SELECT
    COUNT(*)                                             AS total_documentos,
    SUM(estado = 'procesado')                            AS total_procesados,
    SUM(estado = 'pendiente')                            AS pendientes,
    SUM(estado = 'requiere_revision')                    AS revision,
    (SELECT COUNT(*) FROM consultas)                     AS total_consultas;

-- 4) Documentos cargados por semana
SELECT DATE_FORMAT(cargado_en, '%x-%v') AS semana, COUNT(*) AS cantidad
FROM documentos
GROUP BY DATE_FORMAT(cargado_en, '%x-%v')
ORDER BY semana DESC;

-- 5) Documentos con clasificación automática de baja confianza
--    (los que deben revisarse manualmente)
SELECT id, nombre_archivo, estado, confianza
FROM documentos
WHERE estado = 'requiere_revision'
ORDER BY confianza ASC;

-- 6) Auditoría reciente (últimas 50 acciones)
SELECT a.id, u.email AS usuario, a.accion, a.detalle, a.ip, a.creado_en
FROM auditoria a
LEFT JOIN usuarios u ON u.id = a.usuario_id
ORDER BY a.id DESC
LIMIT 50;

-- 7) Consultas más frecuentes del asistente
SELECT TRIM(pregunta) AS pregunta, COUNT(*) AS veces
FROM consultas
GROUP BY TRIM(pregunta)
ORDER BY veces DESC
LIMIT 20;

-- 8) Porcentaje de procesados vs pendientes (trazabilidad)
SELECT
    SUM(estado = 'procesado') / COUNT(*) * 100 AS pct_procesados,
    SUM(estado = 'requiere_revision') / COUNT(*) * 100 AS pct_revision
FROM documentos;

-- 9) Metadatos extraídos más frecuentes
SELECT clave, COUNT(DISTINCT documento_id) AS documentos
FROM metadatos_documento
GROUP BY clave
ORDER BY documentos DESC
LIMIT 20;