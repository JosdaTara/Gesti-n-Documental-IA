# Matriz de Trazabilidad General

| Requisito | Historia de Usuario | Caso de Uso | Componente diseño | Módulo código | Caso de prueba | Estado |
|---|---|---|---|---|---|---|
| RF-01 | HU-01 | CU-01 | 02-09 Diseño seguridad (JWT) | backend/app/security | CP-01, CP-02 | Implementado |
| RF-02 | HU-02 | CU-02 | 02-09 RBAC / 02-05 API usuarios | backend/app/services/usuarios + routes | CP-14 | Implementado |
| RF-03 | HU-03 | CU-03 | 02-06 Flujo documental | backend/app/services/carga | CP-03 | Implementado |
| RF-04 | HU-03 | CU-03 | 02-09 Validación archivos | backend/app/security/validacion | CP-04, CP-05 | Implementado |
| RF-05 | HU-04 | CU-04 | 02-07 Integración IA (OCR) | backend/ia/ocr.py + chunking.py | CP-06 | Implementado |
| RF-06 | HU-04 | CU-04 | 02-07 Clasificación | backend/ia/clasificador.py | CP-07 | Implementado |
| RF-07 | HU-05 | CU-04 | 02-07 Metadatos | backend/ia/metadatos.py | CP-09 | Implementado |
| RF-08 | HU-05 | CU-05 | 02-05 API clasificación | backend/app/services/correccion | CP-08 | Implementado |
| RF-09 | HU-09 | CU-08 | 02-07 Resumen | backend/ia/resumen.py | CP-13 | Implementado |
| RF-10 | HU-04 | CU-04 | 02-02 Capa de datos (pgvector) | db/schema.sql + ia/embeddings.py | CP-06, CP-15 | Implementado |
| RF-11 | HU-06 | CU-06 | 02-05 API búsqueda | backend/app/services/busqueda | CP-10 | Implementado |
| RF-12 | HU-07 | CU-06 | 02-07 Búsqueda semántica | backend/app/services/busqueda + pgvector | CP-11 | Implementado |
| RF-13 | HU-08 | CU-07 | 02-07 RAG | backend/ia/rag.py | CP-12 | Implementado |
| RF-14 | HU-06 | CU-06 | 02-05 API descarga | backend/app/services/archivos | CP-10 | Implementado |
| RF-15 | HU-11 | CU-10 | 02-02 Auditoría | backend/app/services/auditoria | CP-14 | Implementado |
| RF-16 | HU-10 | CU-09 | 02-05 API dashboard | backend/app/repositories/dashboard | CP-16 | Implementado |

> Versión en Excel: `08-Matriz-Trazabilidad/Matriz-Trazabilidad-General.xlsx` (opcional,
> misma información para facilitar el llenado).