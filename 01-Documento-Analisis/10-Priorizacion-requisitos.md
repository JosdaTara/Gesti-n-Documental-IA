# 10. Priorización de requisitos

| ID | Requisito | Prioridad (MoSCoW) | Justificación |
|---|---|---|---|
| RF-01 | Autenticación con JWT | MUST | Sin acceso seguro ningún usuario puede operar el sistema. |
| RF-02 | Gestión de usuarios y roles | MUST | El control de accesos es requisito de seguridad y cumplimiento. |
| RF-03 | Carga de documentos | MUST | Es la entrada principal del flujo documental. |
| RF-04 | Validación de archivos | MUST | Evita archivos maliciosos o inválidos; requisito de seguridad. |
| RF-05 | Extracción de texto/OCR | MUST | Sin texto no hay indexación ni análisis; es el corazón del sistema. |
| RF-06 | Clasificación automática | MUST | Organiza la información para la búsqueda por categoría. |
| RF-07 | Extracción de metadatos | SHOULD | Enriquece la búsqueda y los reportes sin ser indispensable en v1. |
| RF-08 | Corrección manual de clasificación | SHOULD | Asegura calidad; el algoritmo no es infalible. |
| RF-09 | Resumen automático | SHOULD | Alto valor para el usuario sin afectar el flujo crítico. |
| RF-10 | Indexación vectorial | MUST | Base del RAG y de la búsqueda semántica (objetivo del proyecto). |
| RF-11 | Búsqueda por palabra clave | MUST | Funcionalidad básica de recuperación de información. |
| RF-12 | Búsqueda semántica | MUST | Diferenciador solicitado en el enunciado (embeddings + similitud). |
| RF-13 | Consulta conversacional RAG | MUST | Entregable central: preguntas sobre documentos con fuentes. |
| RF-14 | Descarga del documento original | SHOULD | Necesario para uso operativo, no crítico para el MVP de IA. |
| RF-15 | Log de auditoría | MUST | Trazabilidad exigida por reglas de negocio y seguridad. |
| RF-16 | Dashboard | SHOULD | Facilita la toma de decisiones gerenciales. |