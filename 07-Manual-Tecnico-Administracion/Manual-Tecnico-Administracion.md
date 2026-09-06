# Manual Técnico / Administración

## 1. Arquitectura resumida (referencia a 02-Documento-Diseno)

- **Frontend:** React 18 + TypeScript + Vite (SPA).
- **Backend:** FastAPI (Python 3.11), JWT + BCrypt, RBAC, auditoría.
- **Datos:** PostgreSQL 16 + pgvector (metadatos, texto, vectores HNSW).
- **Almacenamiento:** MinIO (S3) o carpeta local según `STORAGE_BACKEND`.
- **IA:** módulo interno `ia/` — OCR (PaddleOCR/Tesseract), embeddings
  (`text-embedding-3-small`), LLM (`gpt-4o-mini`), RAG con pgvector.
- **Despliegue:** Docker Compose.

Detalle completo en:
- `02-Documento-Diseno/03-Modelo-datos-ER.md` (modelo de datos)
- `02-Documento-Diseno/05-Diseno-API-servicios.md` (endpoints)
- `03-Documento-Desarrollo/03-Estructura-codigo-fuente.md` (estructura)

## 2. Instalación y despliegue (referencia a 05-Documento-Implementacion-Despliegue)

```bash
git clone https://github.com/JosdaTara/Gesti-n-Documental-IA.git
cd 09-Codigo-Fuente
cp backend/.env.example backend/.env   # completar credenciales
docker compose up --build -d
```

Servicios: frontend `:5173`, API `:8000` (Swagger `/docs`), MinIO `:9001`.
Ver `05-Documento-Implementacion-Despliegue/06-Proceso-instalacion.md`.

## 3. Administración de usuarios y roles

Acceso: menú **Usuarios** (solo administrador).

| Acción | Procedimiento |
|---|---|
| Crear usuario | Usuarios → Nuevo → nombre, correo, contraseña, rol → Guardar |
| Editar rol | Usuarios → Editar → cambiar rol → Guardar |
| Desactivar | Usuarios → Editar → estado *inactivo* → Guardar |
| Reposicionar contraseña | Usuarios → Editar → nueva contraseña → Guardar |

Roles:
- `admin` — gestión total (usuarios, auditoría, dashboard).
- `gestor` — carga de documentos y corrección de clasificación.
- `consultor` — lectura, búsqueda, RAG y descarga.

Las contraseñas de demostración (`admin`, `gestor`, `consultor`) **deben cambiarse** antes de
cualquier uso productivo.

## 4. Monitoreo y logs de procesamiento

- **Logs de contenedores:**
  ```bash
  docker compose logs -f api
  docker compose logs -f db
  ```
- **Auditoría del sistema:** menú **Auditoría** (admin) — consulta por usuario, documento o
  período: fecha, usuario, acción y detalle.
- **Estados de documento:** en **Documentos** se filtra por estado; los errores muestran el
  motivo en el detalle de procesamiento.
- **Health básica:** consultar `GET /api/dashboard/estadisticas` para ver tasas de error y
  procesamiento.

## 5. Solución de problemas comunes

| Problema | Causa probable | Solución |
|---|---|---|
| No carga el frontend | Contenedor detenido o puerto en uso | `docker compose ps`; revisar puerto `5173` |
| API devuelve 500 en carga | Storage no disponible o BD caída | Verificar MinIO/`STORAGE_PATH` y `docker compose logs api` |
| OCR no procesa | Modelo de OCR no descargado | Revisar logs de `api`; reiniciar contenedor |
| Embeddings fallan | `OPENAI_API_KEY` inválida o sin créditos | Validar `.env` y el panel de OpenAI |
| Búsqueda semántica vacía | Vectores no generados o chunk muy grande la consulta | Reprocesar documentos; ajustar `CHUNK_SIZE`/`RAG_TOP_K` |
| Acceso denegado (403) | Rol sin permiso para la acción | Verificar el rol del usuario |

## 6. Contacto/soporte

- Incidencias técnicas: crear un issue en el repositorio
  `https://github.com/JosdaTara/Gesti-n-Documental-IA`.
- Soporte operativo: administrador del sistema del equipo SIGAD
  (facilitado por el docente Wilson Castaño Galviz — UTS).