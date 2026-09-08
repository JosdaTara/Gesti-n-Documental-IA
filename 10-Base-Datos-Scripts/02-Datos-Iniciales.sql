-- =====================================================================
-- SIGAD - 10. Base de Datos - Scripts
-- 02-Datos-Iniciales.sql
-- Carga las categorías base y el usuario administrador por defecto.
-- El password_hash corresponde a la clave "Admin123!" (pbkdf2_sha256).
-- =====================================================================

USE gestion_documental_bd;

INSERT INTO categorias (nombre, descripcion, activa) VALUES
    ('FACTURA',        'Comprobante comercial de venta o cobro', 1),
    ('GUIA_DESPACHO',  'Documento que acompaña el envío físico de mercancía', 1),
    ('ORDEN_COMPRA',   'Solicitud formal de compra de productos o servicios', 1),
    ('CONTRATO',       'Acuerdo legal entre dos o más partes', 1),
    ('ACTA_RECEPCION', 'Constancia de entrega y recepción conforme', 1)
ON DUPLICATE KEY UPDATE descripcion = VALUES(descripcion);

INSERT INTO usuarios (nombre, email, password_hash, rol, activo) VALUES
    ('Administrador SIGAD',
     'admin@sigad.co',
     'pbkdf2_sha256$DbQz6A76ud5q0K0pG3kuPQ$9e9OA0mhsAF4kUsKSbqK-okPN2DrAJoGrkM2t5L2ZRw',
     'administrador',
     1)
ON DUPLICATE KEY UPDATE rol = VALUES(rol), activo = VALUES(activo);