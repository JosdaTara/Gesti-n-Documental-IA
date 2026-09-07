# SIGAD — Código Fuente

Repositorio oficial del código fuente del **Sistema Inteligente de Gestión y Análisis
Documental** (SIGAD). Implementa el flujo: archivo → extracción (OCR) → procesamiento IA →
análisis → almacenamiento → búsqueda/consulta → respuesta.

## Componentes

| Carpeta | Descripción |
|---|---|
| `backend/` | API REST en Python 3.11 + FastAPI (auth JWT, documentos, búsqueda, RAG, dashboard, auditoría) |
| `frontend/` | SPA en React 18 + TypeScript + Vite (responsive, modo oscuro, animaciones) |
| `db/` | `schema.sql` (PostgreSQL 16 + pgvector) y `seed.sql` (datos base) |
| `docker-compose.yml` | Ambiente completo reproducible (db + back + front) |

## Inicio rápido (Docker)

```bash
cp backend/.env.example backend/.env   # completar OPENAI_API_KEY y SECRET_KEY
docker compose up --build -d
```

| Servicio | URL |
|---|---|
| Frontend | http://localhost:5173 |
| API (Swagger) | http://localhost:8000/docs |
| MinIO consola | http://localhost:9001 |

## Inicio rápido (desarrollo sin Docker)

Backend usa SQLite por defecto y modo demo de IA (no requiere API key ni PostgreSQL):

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:

```bash
cd frontend
npm install
npm run dev
```

Credenciales demo: `admin@sigad.co` / `Admin123!`

## Variables de entorno clave (backend/.env)

- `SECRET_KEY` — clave de firma JWT
- `DATABASE_URL` — por defecto `sqlite:///./sigad.db`; en producción usar PostgreSQL (`postgresql+psycopg://...`)
- `STORAGE_PATH` — carpeta donde se guardan los documentos subidos
- `OPENAI_API_KEY` — si se configura, el motor IA usa embeddings y LLM reales; si no, usa modo demo determinístico
- `DEMO_MODE` — si `true`, al iniciar crea documentos de ejemplo clasificados para la demo y la sustentación

## Documentación técnica

- Instalación completa: `03-Documento-Desarrollo/05-Manual-tecnico-instalacion`
- Despliegue: `05-Documento-Implementacion-Despliegue/06-Proceso-instalacion` y `07-Proceso-despliegue`
- API y servicios: `02-Documento-Diseno/05-Diseno-API-servicios`
- Integración IA: `02-Documento-Diseno/07-Diseno-integracion-IA`