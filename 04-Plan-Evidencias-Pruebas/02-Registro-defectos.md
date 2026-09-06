# 2. Registro de defectos y correcciones

| ID | Descripción del defecto | Severidad | Estado | Corrección aplicada |
|---|---|---|---|---|
| DEF-01 | La carga de un PDF con nombre de extensión .jpg se aceptaba por extensión pero el contenido era rechazado por magic bytes; el mensaje de error no era claro. | Media | Resuelto | Se mejoró la validación (extensión + MIME + magic bytes) y el mensaje de rechazo en español. |
| DEF-02 | La búsqueda semántica devolvía documentos con similitud muy baja por fragmentos demasiado pequeños. | Alta | Resuelto | Se ajustó el tamaño del chunk a 512 tokens con solapamiento de 64. |
| DEF-03 | La clasificación automática fallaba al devolver una categoría no existente (formato JSON inconsistente del LLM). | Alta | Resuelto | Se agregó parseo tolerante a JSON y validación contra la lista de categorías del sistema. |
| DEF-04 | Al cargar un archivo duplicado se reprocesaba el documento y se duplicaba el vector. | Media | Resuelto | Se implementó la regla RN-06: verificación por hash del archivo antes de encolar. |
| DEF-05 | La respuesta del chat RAG no siempre mostraba las fuentes cuando recuperaba múltiples fragmentos del mismo documento. | Media | Resuelto | Se deduplican y agrupan las fuentes por documento en la respuesta. |
| DEF-06 | En el dashboard, los conteos por semana no consideraban el huso horario del servidor. | Baja | Resuelto | Se normalizaron las fechas a la zona horaria de Bogotá (UTC-5) para los reportes. |