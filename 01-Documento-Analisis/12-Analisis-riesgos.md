# 12. Análisis de riesgos del proyecto

| Riesgo | Probabilidad | Impacto | Plan de mitigación |
|---|---|---|---|
| Errores de OCR en documentos escaneados de baja calidad | Media | Alto | Usar preprocesamiento de imagen (escala, binarización) y marcar clasificaciones de baja confianza para revisión humana. |
| Costo elevado del consumo de la API de IA (embeddings + LLM) durante el desarrollo | Media | Medio | Configurar modelo eficiente (gpt-4o-mini), cache de embeddings y límites de uso; documentar control de consumo. |
| Fuga o almacenamiento de datos personales reales | Baja | Alto | Validación de contenido, uso exclusivo de documentos de prueba anonimizados y cumplimiento de la Ley 1581 de 2012. |
| Baja calidad de la búsqueda semántica con documentos muy cortos | Media | Medio | Ajustar tamaño de fragmentos (chunk), solapamiento y usar búsqueda híbrida (textual + vectorial). |
| Dependencia del proveedor externo de IA (caídas o cambios de API) | Media | Medio | Abstraer el servicio de IA tras una interfaz propia y permitir configurar el endpoint/modelo por variables de entorno. |
| Latencia en la respuesta conversacional | Media | Medio | Recuperar contexto con top-k acotado, generar con modelo rápido y medir tiempos con RNF-03. |
| Pérdida de datos por falta de respaldo | Baja | Alto | Estrategia de respaldos diarios de base de datos y almacenamiento en el ambiente de implementación. |
| Baja adopción por resistencia al cambio del personal | Media | Medio | Capacitación mediante el manual de usuario y demostración del valor (menos tiempos de búsqueda). |
| Corrupción o manejo incorrecto de archivos subidos | Baja | Medio | Validación por magic bytes, cuarentena de errores y log de procesamiento de cada documento. |