# 3. Configuración de base de datos y almacenamiento

## Base de datos

- **Motor:** PostgreSQL 16 con la extensión **pgvector** (incluida en la imagen
  `pgvector/pgvector:pg16`).
- **Base:** `sigad` — usuario `sigad` (valores por defecto solo para el ambiente de
  demostración; se configuran con `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD`).
- **Esquema:** se crea automáticamente en el primer arranque mediante
  `docker-entrypoint-initdb.d` que ejecuta `schema.sql` y `seed.sql`.
- **Índice vectorial:** `CREATE INDEX ... USING hnsw ((embedding vector_cosine_ops))` sobre
  `procesamiento.embedding` para búsqueda semántica eficiente.

`docker-compose.yml` (fragmento):

```yaml
db:
  image: pgvector/pgvector:pg16
  environment:
    POSTGRES_DB: ${DB_NAME}
    POSTGRES_USER: ${DB_USER}
    POSTGRES_PASSWORD: ${DB_PASSWORD}
  volumes:
    - pgdata:/var/lib/postgresql/data
    - ./db/schema.sql:/docker-entrypoint-initdb.d/01-schema.sql
    - ./db/seed.sql:/docker-entrypoint-initdb.d/02-seed.sql
  ports:
    - "5432:5432"
```

## Almacenamiento de archivos

- **Modo contenedor:** **MinIO** en `minio/minio`, bucket `sigad-docs`. Las credenciales se
  pasan por variables de entorno (`MINIO_ROOT_USER`, `MINIO_ROOT_PASSWORD`).
- **Modo desarrollo:** `STORAGE_BACKEND=local` guarda los archivos en `STORAGE_PATH`
  (por defecto `./storage`), que es un volumen del contenedor.

Los archivos originales nunca se modifican; el texto extraído, los vectores y los metadatos se
persisten en PostgreSQL.