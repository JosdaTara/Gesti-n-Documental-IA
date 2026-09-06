# Código fuente

El código fuente del sistema SIGAD vive en el repositorio Git del equipo:

- **URL del repositorio:** https://github.com/JosdaTara/Gesti-n-Documental-IA.git
- **Rama principal:** `main`
- **Ubicación dentro del repo:** folder `09-Codigo-Fuente/`
- **Instrucciones de clonado y ejecución:** ver `03-Documento-Desarrollo/05-Manual-tecnico-instalacion.md`

## Estructura resumida

```
09-Codigo-Fuente/
├── docker-compose.yml
├── backend/       # API FastAPI + módulo de IA (ia/)
├── frontend/      # SPA React 18 + TypeScript + Vite
├── db/            # schema.sql, seed.sql (PostgreSQL + pgvector)
└── docs_ia/       # flujo IA y prompts
```

## Notas de seguridad

- Las credenciales y API keys viven solo en variables de entorno (`.env`, excluido del repo).
- Nunca se suben claves, contraseñas o `OPENAI_API_KEY` al repositorio.
- Documentación funcional y técnica completa en las carpetas `01` a `08` del proyecto.