# 8. Estrategia básica de respaldo y recuperación

## Qué se respalda
1. **Base de datos PostgreSQL** (`sigad`): metadatos, texto extraído, vectores, auditoría.
2. **Almacenamiento de archivos** (MinIO bucket `sigad-docs` o `STORAGE_PATH` local): los
   documentos originales.
3. **Variables de entorno** (`.env`): copia cifrada fuera del repositorio (no se versiona).

## Frecuencia y método
- **Respaldo diario** programado; en el ambiente de demostración puede ejecutarse manualmente
  antes de cada prueba o sustentación.
- Base de datos:
  ```bash
  docker compose exec db pg_dump -U sigad sigad > backup_sigad_$(date +%F).sql
  ```
- Archivos:
  ```bash
  docker compose exec minio mc mirror local/sigad-docs ./backups/minio/
  ```
  (o copia de la carpeta `STORAGE_PATH` en modo local).

## Retención
- Conservar los últimos 7 respaldos diarios y 4 respaldos semanales.
- Guardar una copia externa (USB/nube) fuera del equipo para la sustentación.

## Recuperación
- Restaurar la base de datos:
  ```bash
  docker compose exec -T db psql -U sigad sigad < backup_sigad_YYYY-MM-DD.sql
  ```
- Restaurar archivos: volcar el bucket/carpeta respaldada al contenedor correspondiente.
- Verificación: tras restaurar, ejecutar una búsqueda y una consulta RAG para confirmar que los
  índices vectoriales y el texto están íntegros.

## RTO / RPO (referencial)
- RPO: pérdida máxima de 24 horas (respaldo diario).
- RTO: tiempo de recuperación estimado ≤ 30 minutos en el ambiente de demostración.