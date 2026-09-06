# 8. Decisiones tecnológicas y su justificación

| Decisión | Alternativas consideradas | Justificación |
|---|---|---|
| Stack backend | FastAPI vs Django vs Flask (Node.js Express) | FastAPI: alto rendimiento async, tipado con Pydantic, documentación Swagger automática, ecosistema Python natural para IA/OCR. |
| Stack frontend | React + Vite vs Angular vs Vue | React 18 + TypeScript + Vite: ciclo de desarrollo rápido, tipado seguro y amplia comunidad; SPA adecuada para una aplicación interna. |
| Base de datos | PostgreSQL 16 + pgvector vs MySQL vs MongoDB vs Chroma | PostgreSQL relacional + pgvector: integra metadatos estructurados, texto y vectores en un solo motor con índices HNSW; evita bases vectoriales dispersas. |
| Servicio de IA | OpenAI (embeddings + gpt-4o-mini) vs Gemini vs LLM local (Ollama) | OpenAI: calidad y velocidad consistentes, instalación cero en el contenedor, adecuado para la sustentación; el módulo interno permite cambiar a LLM local por variables de entorno. |
| OCR | PaddleOCR vs Tesseract vs Cloud OCR | PaddleOCR: mejor precisión en documentos en español y facturas; se complementa con Tesseract como respaldo sin costo adicional. |
| Almacenamiento de archivos | MinIO (S3) vs carpeta local vs AWS S3 | MinIO: estándar S3 local, dockerizable, sin depender de nube externa en la demostración; configurable por variable de entorno. |
| Despliegue | Docker Compose vs instalación manual vs PaaS | Docker Compose: reproduce el entorno completo (BD + API + front + IA) en cualquier máquina de forma confiable para la entrega. |
| Autenticación | JWT vs sesiones vs OAuth | JWT stateless: simple, escalable y suficiente para el alcance; compatible con la SPA. |
| Búsqueda | pgvector + ILIKE híbrida vs Elasticsearch vs BM25 puro | pgvector + ILIKE: búsqueda semántica + textual en el mismo motor, sin infraestructura adicional para el volumen del caso. |