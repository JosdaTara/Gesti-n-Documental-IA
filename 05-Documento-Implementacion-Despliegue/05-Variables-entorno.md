# 5. Variables de entorno y configuración segura

Plantilla `backend/.env.example` — **NUNCA valores reales en el repositorio**:

```
# --- Aplicación ---
APP_NAME=SIGAD
APP_ENV=development
APP_SECRET=                                   # JWT secret (generar aleatorio)
JWT_EXPIRATION_MINUTES=30

# --- Base de datos ---
DB_HOST=db
DB_PORT=5432
DB_NAME=sigad
DB_USER=sigad
DB_PASSWORD=                                  # solo dev/demo
DATABASE_URL=postgresql://sigad:password@db:5432/sigad

# --- Almacenamiento ---
STORAGE_BACKEND=local                         # local | minio
STORAGE_PATH=./storage
MINIO_ENDPOINT=minio:9000
MINIO_ROOT_USER=minioadmin
MINIO_ROOT_PASSWORD=                          # solo dev/demo
MINIO_BUCKET=sigad-docs

# --- Servicios de IA ---
AI_PROVIDER=openai
OPENAI_API_KEY=                               # <tu_api_key> — nunca subir
AI_MODEL_EMBEDDING=text-embedding-3-small
AI_MODEL_LLM=gpt-4o-mini
EMBEDDING_DIM=1536
CHUNK_SIZE=512
CHUNK_OVERLAP=64
RAG_TOP_K=5
OCR_ENGINE=paddle
```

## Buenas prácticas aplicadas

- El archivo `.env` está incluido en `.gitignore`; no se rastrea ni se sube.
- Se publica únicamente `env.example` con nombres de variables vacíos.
- El `JWT_SECRET` y la `OPENAI_API_KEY` solo existen en el ambiente de ejecución.
- En producción se deben rotar credenciales, usar secretos gestionados y evitar contraseñas
  de demostración.