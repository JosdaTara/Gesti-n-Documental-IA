# 1. Descripción del problema y contexto empresarial

## 1.1 Contexto empresarial

**Distribuidora Andina S.A.S.** es una empresa colombiana de distribución y logística de
productos de consumo masivo, con operación en Bogotá y Cundinamarca. Cuenta con 45
colaboradores y genera mensualmente cerca de 2.000 documentos operativos y comerciales.
Su operación documental incluye facturas de venta, guías de despacho, órdenes de compra,
contratos comerciales y actas de recepción.

## 1.2 Descripción del problema

Actualmente la empresa administra sus documentos de las siguientes formas:

- **Dispersión:** Los documentos se almacenan en carpetas de red, correos corporativos y
  dispositivos locales sin un orden unificado.
- **Búsqueda lenta:** La búsqueda de un documento puede tomar entre 15 y 40 minutos, pues
  requiere revisar manualmente carpetas y nombres de archivo.
- **Documentos sin texto digital:** Muchas guías de despacho y facturas se reciben escaneadas
  como imágenes (JPG/PNG/PDF sin capa de texto), lo que impide buscar su contenido.
- **Información no aprovechable:** No es posible hacer preguntas sobre los contratos ni
  obtener resúmenes automáticos del contenido de los documentos.
- **Riesgo de pérdida y reprocesos:** Sin un inventario indexado, se duplican documentos y se
  incurre en reprocesos administrativos que afectan la productividad.

## 1.3 Identificación de la necesidad y oportunidad de negocio

Se identificó la necesidad de un **Sistema Inteligente de Gestión y Análisis Documental (SIGAD)**
que automatice el flujo: archivo → extracción de contenido (OCR) → procesamiento con IA →
análisis → almacenamiento → búsqueda/consulta → respuesta.

La oportunidad de negocio se resume en:

- Reducción del tiempo de búsqueda de 15-40 minutos a menos de 5 segundos.
- Recuperación del valor de los documentos escaneados mediante OCR.
- Respuestas a preguntas sobre el contenido de los documentos con base en sus propios datos
  (técnica RAG — Retrieval-Augmented Generation).
- Control, trazabilidad y auditoría sobre los documentos y las acciones de los usuarios.