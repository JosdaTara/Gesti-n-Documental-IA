# 3. Alcance y exclusiones

## Alcance (qué SÍ incluye el sistema)

- Registro, autenticación y gestión de usuarios con roles (administrador, gestor documental,
  consultor).
- Carga de documentos en formato PDF, DOCX, TXT, JPG y PNG, con validación de tipo y tamaño.
- Extracción de texto mediante OCR para documentos escaneados e imágenes.
- Clasificación automática en cinco categorías: facturas de venta, guías de despacho,
  órdenes de compra, contratos comerciales y actas de recepción.
- Extracción de metadatos clave por tipo de documento (número, fecha, proveedor, total, etc.).
- Generación de resúmenes automáticos de los documentos.
- Indexación vectorial (embeddings) y almacenamiento de los documentos y sus metadatos.
- Búsqueda por palabras clave y búsqueda semántica.
- Consulta conversacional en lenguaje natural sobre el contenido de los documentos (RAG),
  con indicación de las fuentes consultadas.
- Dashboard con estadísticas de documentos procesados, clasificaciones, consultas y errores.
- Registro de auditoría de las acciones de los usuarios.
- Despliegue local mediante contenedores Docker.

## Exclusiones (qué NO incluye)

- OCR de documentos manuscritos con caligrafía irregular sin revisión humana final.
- Firma electrónica/digital de documentos.
- Flujos de aprobación de documentos dentro del sistema.
- Correo electrónico automatizado (notificaciones externas).
- Migración automática de los sistemas legacy existentes (se realiza una carga masiva inicial
  guiada).
- Análisis de datos personales de sujetos reales sin autorización (se usan documentos de
  prueba anonimizados).
- Módulo de facturación electrónica o integración con DIAN.
- Aplicación móvil nativa (la interfaz web es responsive, pero no hay app móvil).