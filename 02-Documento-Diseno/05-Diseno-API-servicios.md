# 5. Diseño de API / servicios

| Método | Endpoint | Descripción | Auth |
|---|---|---|---|
| POST | /api/auth/login | Autenticación, devuelve token JWT | No |
| POST | /api/auth/refresh | Renueva el token | Sí |
| GET | /api/usuarios | Lista usuarios (admin) | Sí (admin) |
| POST | /api/usuarios | Crea usuario con rol | Sí (admin) |
| PUT | /api/usuarios/{id} | Edita usuario / rol / estado | Sí (admin) |
| GET | /api/categorias | Lista categorías | Sí |
| POST | /api/documentos | Sube documento(s), encola procesamiento | Sí (gestor/admin) |
| GET | /api/documentos | Lista documentos con filtros (estado, categoría, texto) | Sí |
| GET | /api/documentos/{id} | Detalle del documento, texto y resumen | Sí |
| PUT | /api/documentos/{id}/clasificacion | Corrige clasificación y metadatos | Sí (gestor/admin) |
| GET | /api/documentos/{id}/archivo | Descarga el documento original | Sí |
| GET | /api/documentos/{id}/resumen | Devuelve el resumen generado | Sí |
| GET | /api/busqueda?q=&tipo=keyword | Búsqueda por palabra clave | Sí |
| GET | /api/busqueda?q=&tipo=semantica | Búsqueda semántica (embeddings) | Sí |
| POST | /api/rag/consultar | Pregunta en lenguaje natural → respuesta con fuentes | Sí |
| GET | /api/dashboard/estadisticas | Indicadores para el dashboard | Sí (gerente/admin) |
| GET | /api/auditoria | Log de auditoría con filtros | Sí (admin) |

## Notas de diseño

- Todas las respuestas usan JSON; los errores siguen el contrato `{ "detalle": "mensaje" }`.
- Los endpoints protegidos exigen el header `Authorization: Bearer <token>`.
- Los códigos de estado: 200/201 éxito, 400 validación, 401 no autenticado, 403 sin permiso,
  404 no encontrado, 422 datos inválidos, 500 error interno.
- El contrato OpenAPI se genera automáticamente en `/docs` (Swagger).