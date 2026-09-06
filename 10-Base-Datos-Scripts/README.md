# Base de datos, scripts y estructura

- **Motor de base de datos:** PostgreSQL 16 con extensión **pgvector**.
- **Script de creación:** `09-Codigo-Fuente/db/schema.sql`
  - Crea las tablas: `roles`, `usuarios`, `categorias`, `documentos`, `metadatos`,
    `procesamiento`, `consultas`, `auditoria`.
  - Habilita `pgvector` y crea el índice HNSW sobre `procesamiento.embedding`.
- **Datos semilla (seed):** `09-Codigo-Fuente/db/seed.sql`
  - Roles: `admin`, `gestor`, `consultor`.
  - Categorías: factura de venta, guía de despacho, orden de compra, contrato, acta de recepción.
  - Usuarios iniciales de demostración (admin/gestor/consultor).
- **Instrucciones para reproducir la base de datos desde cero:**
  - Con Docker (recomendado): los scripts se ejecutan automáticamente en el primer arranque de
    los contenedores.
  - Manual:
    ```bash
    docker compose up -d db
    docker compose exec -T db psql -U sigad -d sigad < 09-Codigo-Fuente/db/schema.sql
    docker compose exec -T db psql -U sigad -d sigad < 09-Codigo-Fuente/db/seed.sql
    ```
- **Modelo y diccionario de datos:** `02-Documento-Diseno/03-Modelo-datos-ER.md` y `04-Diccionario-datos.md`.