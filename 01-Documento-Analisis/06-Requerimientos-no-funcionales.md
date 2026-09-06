# 6. Requerimientos no funcionales

| ID | Categoría | Descripción |
|---|---|---|
| RNF-01 | Rendimiento | La búsqueda por palabra clave y la búsqueda semántica deben responder en menos de 5 segundos para una base de hasta 5.000 documentos. |
| RNF-02 | Rendimiento | El procesamiento (OCR + clasificación + indexación) de un documento no debe superar los 30 segundos en promedio. |
| RNF-03 | Rendimiento | La respuesta conversacional (RAG) debe generarse en menos de 20 segundos, incluyendo la recuperación de contexto. |
| RNF-04 | Seguridad | Las contraseñas deben almacenarse cifradas con BCrypt y el acceso mediante JWT con expiración (30 minutos) y renovación. |
| RNF-05 | Seguridad | Las API keys y credenciales deben manejarse mediante variables de entorno y nunca quedar en el repositorio. |
| RNF-06 | Seguridad | El sistema debe implementar control de acceso por roles (RBAC) y registrar auditoría de acciones sensibles. |
| RNF-07 | Seguridad | Los archivos subidos deben validarse por extensión, tipo MIME y "magic bytes" para evitar ejecutables o contenido malicioso. |
| RNF-08 | Usabilidad | La interfaz debe ser web responsive, en español, usable en los navegadores modernos (Chrome, Edge, Firefox). |
| RNF-09 | Escalabilidad | La arquitectura debe soportar el crecimiento desde 30 documentos de prueba hasta miles sin cambios estructurales. |
| RNF-10 | Portabilidad | El sistema debe poder desplegarse localmente mediante Docker Compose sin dependencias específicas del equipo de desarrollo. |
| RNF-11 | Disponibilidad | El sistema debe ofrecer una disponibilidad mínima del 99,5% en el ambiente de demostración. |
| RNF-12 | Cumplimiento | No se deben almacenar datos personales reales sin autorización; cumplimiento de la Ley 1581 de 2012 en el manejo de información. |
| RNF-13 | Mantenibilidad | El código debe ser modular, comentado y seguir convenciones; cada módulo debe tener responsabilidad única. |
| RNF-14 | Compatibilidad | Los documentos generados (resúmenes, respuestas) deben exportarse en texto plano, descargable en formatos comunes. |