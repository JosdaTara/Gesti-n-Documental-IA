-- SIGAD - Datos base de la base de datos.
-- El password_hash corresponde a la clave por defecto "Admin123!".

INSERT INTO categorias (nombre, descripcion, activa) VALUES
    ('factura',        'Comprobante comercial de venta o cobro', TRUE),
    ('guia_despacho',  'Documento que acompaña el envío físico de mercancía', TRUE),
    ('orden_compra',   'Solicitud formal de compra de productos o servicios', TRUE),
    ('contrato',       'Acuerdo legal entre dos o más partes', TRUE),
    ('acta_recepcion', 'Constancia de entrega y recepción conforme', TRUE)
ON CONFLICT (nombre) DO NOTHING;

INSERT INTO usuarios (nombre, email, password_hash, rol, activo) VALUES
    ('Administrador SIGAD',
     'admin@sigad.co',
     'pbkdf2_sha256$DbQz6A76ud5q0K0pG3kuPQ$9e9OA0mhsAF4kUsKSbqK-okPN2DrAJoGrkM2t5L2ZRw',
     'administrador',
     TRUE)
ON CONFLICT (email) DO NOTHING;