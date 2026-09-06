# 6. Flujo de procesamiento documental

Flujo completo solicitado: **archivo → extracción de contenido → procesamiento IA → análisis
→ almacenamiento de resultados → búsqueda/consulta → respuesta**.

## Paso 1 — Carga y validación (archivo)
- Entrada: PDF, DOCX, TXT, JPG, PNG (máx. 25 MB).
- Se valida extensión, tipo MIME y magic bytes. Se elimina cualquier riesgo de ejecutables.
- Evento: `auditoria: CARGAR`.

## Paso 2 — Extracción de contenido (OCR)
- Entrada: archivo validado.
- PDF digital → texto nativo con PyMuPDF/pdfplumber.
- DOCX → texto con python-docx.
- TXT → lectura directa UTF-8.
- JPG/PNG/PDF escaneado → OCR con PaddleOCR (precisión en español); Tesseract como respaldo.
- Salida: `texto_extraido` (texto plano normalizado: límites de línea, espacios múltiples,
  caracteres no imprimibles removidos).

## Paso 3 — Procesamiento IA (chunking + embeddings)
- El texto se divide en fragmentos de ~512 tokens con solapamiento de 64 para conservar contexto.
- Cada fragmento se convierte en un vector con `text-embedding-3-small` (dim 1536).
- Salida: `embedding` listo para pgvector.

## Paso 4 — Análisis (clasificación, metadatos, resumen)
- **Clasificación:** prompting del LLM sobre el texto → categoría (factura, guía, orden,
  contrato, acta) + nivel de confianza.
- **Metadatos:** extracción de campos clave según la categoría (número, fecha, proveedor/cliente,
  total, plazo).
- **Resumen:** síntesis de hasta 150 palabras.
- Salida: `categoria_id`, `confianza_clasificacion`, tabla `metadatos`, `resumen`.

## Paso 5 — Almacenamiento de resultados
- Transacción en PostgreSQL: documento → estado `procesado`; `procesamiento` → texto + vector +
  resumen; índice HNSW actualizado.
- Si la confianza < 70% → estado `procesado` con marca "requiere revisión".
- Si falla → estado `error` con motivo en `procesamiento.error`.

## Paso 6 — Búsqueda / consulta
- **Por palabra clave:** `ILIKE` sobre texto/metadatos, ordenado por relevancia.
- **Semántica:** embedding de la consulta + similitud coseno sobre pgvector (top-k) con filtro
  por categoría opcional.
- **RAG:** recuperación de fragmentos relevantes + prompt al LLM para responder citando fuentes.

## Paso 7 — Respuesta
- El usuario ve los resultados con enlace al documento original.
- En RAG, la respuesta incluye la lista de documentos fuente consultados.