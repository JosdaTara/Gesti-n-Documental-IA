# Presentación y sustentación

Checklist de la sustentación (todos los integrantes deben poder explicar):

- [x] **Requisitos:** problema de negocio, actores, RF/RNF, historias de usuario y casos de uso
  (consultar `01-Documento-Analisis`).
- [x] **Arquitectura:** N-capas, componentes, modelo ER, API e integración IA
  (consultar `02-Documento-Diseno`).
- [x] **Código:** estructura del repositorio y módulos implementados
  (consultar `03-Documento-Desarrollo` y `09-Codigo-Fuente`).
- [x] **Integración de IA:** OCR → embeddings → RAG; justificación de la técnica y del modelo
  (consultar `02-Documento-Diseno/07-Diseno-integracion-IA.md`).
- [x] **Pruebas:** plan, 16 casos de prueba, defectos y conclusiones
  (consultar `04-Plan-Evidencias-Pruebas`).
- [x] **Despliegue:** ambiente contenedor, variables de entorno, instalación y respaldo
  (consultar `05-Documento-Implementacion-Despliegue`).

## Sugerencias para la sustentación

- Distribuir módulos entre los integrantes (cada uno sustenta una parte del flujo completo:
  carga → OCR → clasificación → búsqueda/RAG → dashboard).
- Tener lista una demostración en vivo con los 30 documentos de prueba.
- Preparar respuesta clara a: *¿por qué RAG y embeddings?* (cita a las fuentes y búsqueda por
  concepto), y a *¿cómo se protegen las credenciales?* (variables de entorno, `.gitignore`).

## Enlace a la presentación

- **Presentación:** `13-Presentacion-Sustentacion/presentacion-final.pdf`
- _(completar con los archivos finales: diapositivas y guion de la demo)_