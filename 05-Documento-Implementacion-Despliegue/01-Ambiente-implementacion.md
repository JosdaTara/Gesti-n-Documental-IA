# 1. Descripción del ambiente de implementación

El ambiente de implementación es **contenedorizado y local** mediante Docker Compose, lo que
garantiza reproducibilidad para la demostración y la sustentación en la universidad.

- **PostgreSQL 16 + pgvector:** base de datos relacional y vectorial.
- **MinIO:** almacenamiento de archivos compatible con S3 (opcional; en desarrollo puede usarse
  carpeta local vía `STORAGE_BACKEND=local`).
- **API FastAPI (Python 3.11):** backend y módulo de IA.
- **Frontend React + Vite:** interfaz web servida como SPA.
- **Red interna Docker:** los servicios se comunican a través de una red propia definida en
  `docker-compose.yml`.

| Servicio | Imagen/Base | Puerto |
|---|---|---|
| Frontend | node:20-alpine (build) + nginx | 5173 |
| Backend/API | python:3.11-slim | 8000 |
| PostgreSQL | postgres:16 + pgvector | 5432 |
| MinIO | minio/minio | 9000 (API) / 9001 (consola) |

El ambiente no requiere nube externa ni IP pública; toda la operación se ejecuta en la máquina
del equipo. La única dependencia externa opcional es la API de OpenAI (embeddings y LLM).