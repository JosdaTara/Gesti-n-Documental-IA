# 9. Plan básico de mantenimiento

## Tareas periódicas

| Frecuencia | Tarea | Responsable |
|---|---|---|
| Diaria | Revisar contenedores (`docker compose ps`) y logs del backend | Administrador |
| Diaria | Verificar procesamiento de documentos (colas sin acumular errores) | Administrador |
| Semanal | Respaldo de BD y almacenamiento (ver `08-Estrategia-respaldo-recuperacion`) | Administrador |
| Semanal | Revisión de auditoría: acciones sospechosas o accesos atípicos | Administrador |
| Mensual | Revisar consumo/costos de la API de IA y ajustar límites | Administrador |
| Mensual | Actualizar dependencias de seguridad (imágenes Docker, paquetes) | Equipo de desarrollo |
| Trimestral | Pruebas de humo completas (login, carga, OCR, búsqueda, RAG, dashboard) | Equipo de desarrollo |
| Trimestral | Revisión de categorías y calidad de clasificación de documentos nuevos | Gestor documental |

## Procedimiento de actualización de versión
1. Realizar respaldo antes de actualizar.
2. `git pull origin main`.
3. `docker compose up --build -d`.
4. Ejecutar migraciones de BD si existen en `db/`.
5. Pruebas de humo post-actualización.

## Operación de rutina
- Carga y revisión de documentos: rol gestor documental.
- Solución de incidencias operativas: rol administrador.
- Reportes y consultas: rol consultor / gerencia.

## Indicadores de salud
- Porcentaje de documentos con estado `error` (objetivo < 2%).
- Tiempo promedio de procesamiento por documento (< 30 s).
- Tiempo de respuesta de búsqueda (< 5 s) y de consulta RAG (< 20 s).
- Disponibilidad del ambiente (objetivo ≥ 99,5%).

## Soporte y escalamiento
- Incidencias técnicas: abrir issue en el repositorio del equipo.
- Escalamiento futuro: separar el módulo de IA en un servicio independiente y agrupar el
  backend en réplicas si el volumen crece (> 5.000 documentos).