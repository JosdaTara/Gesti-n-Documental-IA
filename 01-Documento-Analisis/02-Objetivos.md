# 2. Objetivo general y objetivos específicos

## Objetivo general

Desarrollar un Sistema Inteligente de Gestión y Análisis Documental (SIGAD) para
Distribuidora Andina S.A.S. que permita digitalizar, indexar, clasificar y consultar los
documentos de la organización mediante técnicas de IA (OCR, embeddings, búsqueda semántica
y RAG), reduciendo los tiempos de búsqueda y aprovechando la información contenida en los
documentos.

## Objetivos específicos

1. Implementar un módulo de carga y validación de documentos en múltiples formatos
   (PDF, DOCX, TXT, imágenes JPG/PNG) con validación de tipo y tamaño.
2. Integrar un servicio de extracción de texto mediante OCR para documentos escaneados
   e imágenes, garantizando que todo el contenido quede textualizado e indexable.
3. Implementar la clasificación automática de documentos por categoría
   (factura, guía de despacho, orden de compra, contrato, acta) y la extracción de
   metadatos relevantes de cada documento.
4. Diseñar e implementar la indexación vectorial (embeddings) de los documentos y un
   motor de búsqueda híbrida: por palabras clave y por similitud semántica.
5. Implementar un módulo de consulta conversacional (RAG) que responda preguntas en
   lenguaje natural sobre los documentos, citando las fuentes utilizadas.
6. Proveer un dashboard con estadísticas de uso, procesamiento y clasificación para la
   toma de decisiones gerenciales.