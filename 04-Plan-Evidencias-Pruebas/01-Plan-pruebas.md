# 1. Plan de pruebas

## Estrategia y tipos de pruebas aplicadas

La estrategia es **funcional, orientada a escenarios del negocio**, ejecutada sobre el
ambiente Docker local con los datos de prueba del folder `11-Repositorio-Documentos-Prueba`
(30 documentos, 5 categorías).

Se aplicaron los siguientes tipos de pruebas:

- **Funcionales:** verificación de los casos de uso principales (login, carga, búsqueda,
  consulta RAG, descarga).
- **Validación de archivos:** aceptación/rechazo de formatos, tamaños y archivos maliciosos
  (magic bytes).
- **Procesamiento de IA:** OCR sobre documentos escaneados, generación de embeddings y resumen.
- **Clasificación y extracción:** acierto de la categoría asignada y campos clave extraídos.
- **Búsqueda y preguntas sobre documentos:** búsqueda por palabra clave, semántica y preguntas
  en lenguaje natural con verificación de fuentes.
- **Seguridad básica:** autenticación, control de roles (RBAC) y manejo de tokens.
- **Errores y casos límite:** archivos duplicados, archivos sin contenido, consultas sin
  resultados, accesos no autorizados.

## Alcance y responsables

**Alcance:** todas las funcionalidades desarrolladas en la entrega (frontend, backend y módulo
de IA) en el ambiente de demostración.

**Responsables:** el equipo de desarrollo ejecuta las pruebas; el gestor documental y el
consultor (usuarios tipo) participan como evaluadores de usabilidad y resultados de negocio.

**Criterio de aceptación de la entrega:** 100% de casos críticos aprobados (CP-01 a CP-08,
CP-14) y, en general, al menos el 90% de todos los casos de prueba con estado "Aprobado".