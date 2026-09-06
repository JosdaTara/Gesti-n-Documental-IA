# 5. Manual técnico de instalación y ejecución

## Requisitos previos

- **Docker Desktop** (con WSL2 en Windows) o Docker Engine 24+ en Linux.
- Git.
- Una **API key de OpenAI** (para embeddings y LLM). Sin ella, el sistema funciona pero el
  procesamiento IA y la consulta RAG no estarán disponibles.
- 8 GB de RAM recomendados (el OCR y los contenedores consumen memoria).

## Pasos de instalación

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/JosdaTara/Gesti-n-Documental-IA.git
   cd 09-Codigo-Fuente
   ```
2. Crear el archivo `.env` a partir de la plantilla:
   ```bash
   cp backend/.env.example backend/.env
   # editar backend/.env y completar OPENAI_API_KEY y JWT_SECRET
   ```
3. Levantar el ambiente completo:
   ```bash
   docker compose up --build -d
   ```
   Esto inicia los contenedores: PostgreSQL (con pgvector), MinIO, API FastAPI y frontend.

4. Los contenedores ejecutan automáticamente los scripts de base de datos
   (`/db/schema.sql` y `/db/seed.sql`) en el primer arranque.

## Ejecución local

| Servicio | URL |
|---|---|
| Frontend (SPA) | http://localhost:5173 |
| API backend | http://localhost:8000 |
| Documentación API | http://localhost:8000/docs |
| MinIO consola | http://localhost:9001 |

### Credenciales iniciales (ambiente de demostración)

| Rol | Usuario | Contraseña |
|---|---|---|
| Administrador | admin | Cambiar en producción |
| Gestor documental | gestor | Cambiar en producción |
| Consultor | consultor | Cambiar en producción |

> Estas credenciales solo existen en el ambiente de desarrollo/demostración y deben
> cambiarse antes de cualquier despliegue real (ver 07-Manual-Tecnico-Administracion).

### Verificación rápida

1. Abrir http://localhost:5173 e iniciar sesión con el usuario gestor.
2. Cargar un documento de prueba del folder `11-Repositorio-Documentos-Prueba`.
3. En la lista de documentos, confirmar que el estado pasa a `procesado`.
4. Probar la búsqueda semántica y una pregunta en el chat RAG.