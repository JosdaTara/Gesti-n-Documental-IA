# 4. Configuración de servicios de IA

Los servicios de IA se ejecutan dentro del backend y se configuran por variables de entorno:

```env
AI_PROVIDER=openai
OPENAI_API_KEY=<tu_api_key>
AI_MODEL_EMBEDDING=text-embedding-3-small
AI_MODEL_LLM=gpt-4o-mini
EMBEDDING_DIM=1536
CHUNK_SIZE=512
CHUNK_OVERLAP=64
RAG_TOP_K=5
OCR_ENGINE=paddle          # paddle | tesseract
```

## Componentes configurados

1. **OCR**
   - `OCR_ENGINE=paddle` → PaddleOCR (mejor precisión en español y facturas).
   - `OCR_ENGINE=tesseract` → Tesseract 5 como respaldo.
   - Los modelos de OCR se descargan en el primer uso y se almacenan en un volumen interno.
2. **Embeddings**
   - Modelo `text-embedding-3-small` (1536 dimensiones).
   - La dimensión del vector debe coincidir con `EMBEDDING_DIM` usado en `schema.sql`.
3. **LLM generativo**
   - `gpt-4o-mini` para clasificación, metadatos, resumen y respuestas RAG.
   - Prompts en `docs_ia/prompts.md`; todos exigen salida estructurada (JSON) para
     clasificación/metadatos.
4. **RAG**
   - `RAG_TOP_K=5` fragmentos recuperados por consulta; respuesta con citas de fuentes.

## Control de uso y costos

- Se recomienda un límite de consumo en el panel de OpenAI (por usuario/proyecto).
- Los embeddings se generan una sola vez por documento (cache por `documento_id`); si el texto
  no cambia no se regeneran (regla RN-06).