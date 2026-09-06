# 5. Requerimientos funcionales

| ID | Descripción | Prioridad |
|---|---|---|
| RF-01 | El sistema debe permitir autenticar usuarios mediante usuario y contraseña, emitiendo un token JWT con expiración. | Alta |
| RF-02 | El administrador debe poder crear, editar, desactivar y asignar roles a los usuarios (admin, gestor, consultor). | Alta |
| RF-03 | El sistema debe permitir cargar documentos en formatos PDF, DOCX, TXT, JPG y PNG. | Alta |
| RF-04 | El sistema debe validar el tipo y el tamaño del archivo (máx. 25 MB) y rechazar archivos no permitidos con mensaje claro. | Alta |
| RF-05 | El sistema debe extraer el texto del documento mediante OCR para imágenes y aplicar extracción nativa para archivos digitales. | Alta |
| RF-06 | El sistema debe clasificar automáticamente el documento en una de las categorías configuradas (factura, guía de despacho, orden de compra, contrato, acta). | Alta |
| RF-07 | El sistema debe extraer metadatos clave según el tipo de documento (número, fecha, proveedor/cliente, total, etc.). | Alta |
| RF-08 | El gestor documental debe poder corregir manualmente la clasificación o los metadatos de un documento procesado. | Media |
| RF-09 | El sistema debe generar un resumen automático del contenido de cada documento. | Media |
| RF-10 | El sistema debe indexar el contenido mediante embeddings y almacenar el vector junto al documento. | Alta |
| RF-11 | El sistema debe permitir búsqueda por palabras clave sobre el contenido y los metadatos. | Alta |
| RF-12 | El sistema debe permitir búsqueda semántica, encontrando documentos por concepto aunque no coincida la palabra exacta. | Alta |
| RF-13 | El sistema debe responder preguntas en lenguaje natural sobre los documentos (RAG), mostrando las fuentes de las que se extrajo la respuesta. | Media |
| RF-14 | El usuario debe poder descargar el documento original. | Media |
| RF-15 | El administrador debe poder consultar el log de auditoría de acciones de los usuarios. | Alta |
| RF-16 | El sistema debe mostrar un dashboard con estadísticas de documentos procesados, clasificados y consultas por período. | Media |