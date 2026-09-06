# 3. Estructura del código fuente

```
09-Codigo-Fuente/
├── README.md
├── docker-compose.yml
├── /backend
│   ├── main.py                 # Punto de entrada FastAPI
│   ├── .env.example            # Plantilla de variables de entorno
│   ├── requirements.txt
│   ├── /app
│   │   ├── /routes             # Endpoints (auth, usuarios, documentos, busqueda, rag, dashboard, auditoria)
│   │   ├── /services           # Lógica de negocio (carga, procesamiento, clasificación, resumen, RAG)
│   │   ├── /repositories       # Acceso a datos (SQLAlchemy)
│   │   ├── /models             # Modelos ORM (Usuario, Documento, Categoria, Procesamiento, Auditoria)
│   │   ├── /schemas            # Esquemas Pydantic
│   │   ├── /security           # JWT, BCrypt, RBAC, validación de archivos
│   │   └── /core               # Configuración y lectura de variables de entorno
│   │
│   └── /ia                      # Módulo de IA
│       ├── ocr.py              # PaddleOCR / Tesseract / extracción nativa
│       ├── chunking.py         # División de texto en fragmentos
│       ├── embeddings.py       # Generación y búsqueda de vectores (pgvector)
│       ├── rag.py              # Recuperación + generación con fuentes
│       ├── clasificador.py     # Clasificación por categoría + confianza
│       ├── metadatos.py        # Extracción de campos clave
│       └── resumen.py          # Resumen automático
│
├── /frontend
│   ├── package.json
│   ├── vite.config.ts
│   ├── /src
│   │   ├── /pages              # Login, Usuarios, Carga, Documentos, Detalle, Busqueda, Chat, Dashboard
│   │   ├── /components         # Componentes reutilizables
│   │   ├── /services           # Cliente Axios con interceptor JWT
│   │   ├── /hooks              # Hooks de autenticación y datos
│   │   ├── /router             # Rutas protegidas por rol
│   │   └── /context            # Contexto de sesión
│
├── /db
│   ├── schema.sql              # Creación de tablas + extensión pgvector
│   ├── seed.sql                # Roles, categorías y usuarios iniciales
│   └── README.md
│
└── /docs_ia
    ├── flujo_procesamiento.md
    └── prompts.md              # Prompts de clasificación, metadatos, resumen y RAG
```

## Explicación de las carpetas

| Carpeta | Propósito |
|---|---|
| `backend/app/` | API y lógica de negocio, separada en rutas, servicios, repositorios y modelos. |
| `backend/ia/` | Encapsula toda la funcionalidad de IA (OCR, embeddings, RAG, clasificación). |
| `frontend/src/` | SPA React con páginas por módulo y protección de rutas por rol. |
| `db/` | Scripts SQL de creación y datos semilla del esquema relacional + vectorial. |
| `docker-compose.yml` | Orquesta backend, frontend, PostgreSQL, MinIO y la cola de procesamiento. |
| `docs_ia/` | Documentación técnica del flujo de IA y los prompts utilizados. |