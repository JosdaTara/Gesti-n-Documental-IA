# 7. Diseño de la integración con IA

## Modelo/API/servicio utilizado

- **Embeddings:** `text-embedding-3-small` de OpenAI (vector de 1536 dimensiones).
- **LLM generativo:** `gpt-4o-mini` de OpenAI (eficiente en costo y latencia).
- **OCR:** PaddleOCR (precisión en español) con Tesseract 5 como respaldo.
- Todo se consume a través de un **módulo interno propio** (`ia/`) que abstrae al proveedor;
  el modelo, el endpoint y la API key se configuran por variables de entorno.

## Técnica (RAG, embeddings, búsqueda semántica, NLP, OCR…)

1. **OCR + normalización:** los documentos escaneados se convierten a texto utilizable.
2. **Chunking:** división del texto en fragmentos (~512 tokens, solapamiento 64).
3. **Embeddings:** cada fragmento se vectoriza y se indexa en pgvector (HNSW).
4. **Búsqueda semántica:** la consulta se vectoriza y se recuperan los fragmentos más similares
   por similitud coseno, con filtros por categoría (búsqueda híbrida con ILIKE).
5. **RAG:** los fragmentos recuperados se inyectan en el prompt del LLM junto con la pregunta;
   el modelo responde **exclusivamente** con base en ese contexto y cita las fuentes.
6. **NLP:** la clasificación, extracción de metadatos y resumen se resuelven con prompting
   estructurado del LLM sobre el texto extraído.

## Justificación técnica

- **RAG** resuelve el reto de negocio porque la empresa necesita respuestas confiables sobre
  sus propios documentos (contratos, facturas) sin "alucinaciones": el modelo solo razona sobre
  fragmentos reales recuperados de la base documental, y cada respuesta es trazable a su fuente.
- **Embeddings** permiten recuperar información **por concepto**, no solo por coincidencia de
  palabras (p. ej. "condiciones de pago" → contratos con cláusulas de pago), lo cual es el
  problema central de la búsqueda manual actual.
- **OCR** es imprescindible porque gran parte del acervo llega escaneado (guías de despacho),
  y sin texto no hay indexación viable.
- **gpt-4o-mini + text-embedding-3-small** ofrecen una relación costo/latencia/calidad adecuada
  para el volumen del caso (30+ documentos) con margen de crecimiento.