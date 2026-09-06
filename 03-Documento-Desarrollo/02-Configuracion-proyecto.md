# 2. Configuración del proyecto

## Clonar el repositorio

```bash
git clone https://github.com/JosdaTara/Gesti-n-Documental-IA.git
cd 09-Codigo-Fuente
```

## Instalar dependencias

```bash
# Backend
cd backend
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
```

> Nota: si se usa Docker Compose (recomendado), no es necesario instalar dependencias
> localmente; el arranque se hace con `docker compose up --build`.

## Variables de entorno necesarias

Se debe crear un archivo `.env` en la raíz de `backend/` a partir de la plantilla
`env.example`. **No se suben valores reales al repositorio.**

```env
DATABASE_URL=postgresql://sigad:sigad@localhost:5432/sigad
JWT_SECRET=<clave_secreta_aleatoria>
JWT_EXPIRATION_MINUTES=30
STORAGE_PATH=./storage
STORAGE_BACKEND=local            # local | minio
AI_MODEL_EMBEDDING=text-embedding-3-small
AI_MODEL_LLM=gpt-4o-mini
OPENAI_API_KEY=<tu_api_key>
EMBEDDING_DIM=1536
CHUNK_SIZE=512
CHUNK_OVERLAP=64
```

## Configurar la base de datos

```bash
cd ../db
psql -U sigad -d sigad -f schema.sql
psql -U sigad -d sigad -f seed.sql
```

## Ejecutar en modo desarrollo

```bash
# Backend (API en http://localhost:8000)
cd backend
uvicorn main:app --reload

# Frontend (SPA en http://localhost:5173)
cd frontend
npm run dev
```