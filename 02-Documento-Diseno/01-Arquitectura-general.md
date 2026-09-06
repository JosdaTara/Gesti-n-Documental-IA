# 1. Arquitectura general de la solución

Se seleccionó una **arquitectura cliente-servidor por capas (N-capas)** con componentes
desacoplados y despliegue por contenedores. No se usa microservicios completos porque el
proyecto es de mediana escala, prioriza simplicidad operativa y un solo equipo de desarrollo,
pero la separación en módulos permite evolucionar a microservicios si el volumen crece.

```
┌────────────────────────────────────────────────────────────────┐
│                    Cliente (navegador web)                     │
│                React 18 + TypeScript + Vite (SPA)              │
└──────────────────────────────┬─────────────────────────────────┘
                               │ HTTPS / REST (JSON)
┌──────────────────────────────▼─────────────────────────────────┐
│                       Capa de presentación API                 │
│                     FastAPI (Python 3.11)                      │
│          Autenticación JWT · roles · validación · auditoría    │
└───────────────┬───────────────────────────────┬────────────────┘
                │                               │
        ┌───────▼────────┐             ┌────────▼─────────┐
        │ Capa de datos   │             │  Capa de IA      │
        │ PostgreSQL 16   │             │  (módulo Python) │
        │ + pgvector      │             │  OCR · chunks ·  │
        │ (metadatos +    │             │  embeddings ·    │
        │  vectores)      │             │  RAG/LLM ·       │
        └─────────────────┘             │  resumen·clasif. │
                                        └─────────────────┘
        Almacenamiento de archivos:        Servicio de IA externo
        MinIO (S3) o carpeta local         (OpenAI / configuración)
```

**Justificación del estilo:**

- **N-capas:** separa presentación, lógica de negocio y datos; facilita pruebas unitarias
  y mantenimiento.
- **SPA React + API REST:** experiencia fluida y clara separación entre frontend y backend.
- **Contenedores Docker Compose:** reproducibilidad del ambiente en cualquier máquina de
  la UTS o del equipo, sin dependencias locales frágiles.
- **Servicio de IA como módulo interno:** encapsula OCR, embeddings y LLM tras una interfaz
  que se configura por variables de entorno, evitando acoplamiento con un proveedor específico.

Diagramas de despliegue y componentes: `02-Documento-Diseno/diagramas/`.