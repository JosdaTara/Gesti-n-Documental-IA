# 4. Diccionario de datos

| Tabla | Campo | Tipo | Descripción | Restricciones |
|---|---|---|---|---|
| roles | id | SERIAL PK | Identificador del rol | Único |
| roles | nombre | VARCHAR(50) | Nombre del rol (admin, gestor, consultor) | Único, NOT NULL |
| usuarios | id | SERIAL PK | Identificador del usuario | Único |
| usuarios | nombre | VARCHAR(120) | Nombre completo del usuario | NOT NULL |
| usuarios | email | VARCHAR(150) | Correo de acceso | Único, formato email |
| usuarios | password_hash | VARCHAR(255) | Hash BCrypt de la contraseña | NOT NULL |
| usuarios | rol_id | INT FK → roles.id | Rol asignado | NOT NULL |
| usuarios | activo | BOOLEAN | Habilitado para ingresar | Default TRUE |
| usuarios | creado_en | TIMESTAMP | Fecha de creación | Default now() |
| categorias | id | SERIAL PK | Identificador de la categoría | Único |
| categorias | nombre | VARCHAR(80) | Nombre (factura, guía, orden, contrato, acta) | Único, NOT NULL |
| categorias | activa | BOOLEAN | Categoría disponible | Default TRUE |
| documentos | id | SERIAL PK | Identificador del documento | Único |
| documentos | nombre_archivo | VARCHAR(255) | Nombre original del archivo | NOT NULL |
| documentos | tipo_mime | VARCHAR(100) | Tipo MIME validado | NOT NULL |
| documentos | tamano_bytes | BIGINT | Tamaño en bytes | 1–25.000.000 |
| documentos | estado | VARCHAR(20) | pendiente, procesando, procesado, error | NOT NULL |
| documentos | categoria_id | INT FK → categorias.id | Categoría asignada | Nulo si requiere revisión |
| documentos | ruta_archivo | VARCHAR(500) | Ubicación en MinIO/carpeta | NOT NULL |
| documentos | confianza_clasificacion | NUMERIC(5,4) | Confianza 0–1 de la clasificación automática | 0–1 |
| documentos | cargado_en | TIMESTAMP | Fecha de carga | Default now() |
| documentos | usuario_id | INT FK → usuarios.id | Quién cargó | NOT NULL |
| metadatos | id | SERIAL PK | Identificador | Único |
| metadatos | documento_id | INT FK → documentos.id | Documento asociado | NOT NULL, borrado en cascada |
| metadatos | clave | VARCHAR(60) | Nombre del metadato (numero, fecha, total…) | NOT NULL |
| metadatos | valor | VARCHAR(255) | Valor del metadato | NOT NULL |
| procesamiento | id | SERIAL PK | Identificador | Único |
| procesamiento | documento_id | INT FK → documentos.id | Documento procesado | Único |
| procesamiento | texto_extraido | TEXT | Texto completo extraído/OCR | NOT NULL |
| procesamiento | embedding | VECTOR(1536) | Vector semántico pgvector | Indizado HNSW |
| procesamiento | resumen | TEXT | Resumen generado | Nullable |
| procesamiento | modelo_uso | VARCHAR(80) | Modelo usado (embeddings/LLM) | Nullable |
| procesamiento | duracion_ms | INT | Tiempo total del procesamiento | Nullable |
| procesamiento | estado | VARCHAR(20) | exitoso, error | NOT NULL |
| procesamiento | error | TEXT | Motivo del error | Nullable |
| procesamiento | procesado_en | TIMESTAMP | Fecha de finalización | Nullable |
| consultas | id | SERIAL PK | Identificador | Único |
| consultas | usuario_id | INT FK → usuarios.id | Quién consultó | NOT NULL |
| consultas | tipo | VARCHAR(20) | keyword, semantica, rag | NOT NULL |
| consultas | consulta | TEXT | Texto de la consulta | NOT NULL |
| consultas | respuesta | TEXT | Respuesta (RAG) o resultado | Nullable |
| consultas | documentos_recuperados | INT | Cantidad de fuentes encontradas | Default 0 |
| consultas | realizada_en | TIMESTAMP | Fecha de la consulta | Default now() |
| auditoria | id | SERIAL PK | Identificador | Único |
| auditoria | usuario_id | INT FK → usuarios.id | Usuario que actuó | NOT NULL |
| auditoria | accion | VARCHAR(50) | LOGIN, CARGAR, EDITAR, DESCARGAR, ELIMINAR… | NOT NULL |
| auditoria | documento_id | INT FK → documentos.id | Documento afectado | Nullable |
| auditoria | detalle | TEXT | Descripción del evento | Nullable |
| auditoria | realizada_en | TIMESTAMP | Fecha del evento | Default now() |