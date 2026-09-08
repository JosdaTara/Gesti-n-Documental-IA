# 11. Repositorio de Documentos de Prueba

Conjunto de documentos sintéticos en español para validar el sistema SIGAD:
clasificación automática por IA, extracción de metadatos, búsqueda semántica
(RAG) y el asistente documental.

## Cumplimiento del objetivo

> Repositorio de **mínimo 30 documentos** de prueba distribuidos en al menos
> **3 categorías** y en diferentes formatos.

| Indicador | Valor |
|---|---|
| Total de documentos | **36** |
| Categorías | **5** (FACTURA, GUIA_DESPACHO, ORDEN_COMPRA, CONTRATO, ACTA_RECEPCION) |
| Formatos | **4** (`.txt`, `.md`, `.pdf`, `.docx`) |

## Distribución

| Categoría | Cantidad | Prefijo de archivo |
|---|---|---|
| FACTURA | 8 | `FACTURA-FE-001…008` |
| GUIA_DESPACHO | 7 | `GUIA-DESPACHO-GD-001…007` |
| ORDEN_COMPRA | 7 | `ORDEN-COMPRA-OC-001…007` |
| CONTRATO | 7 | `CONTRATO-CT-001…007` |
| ACTA_RECEPCION | 7 | `ACTA-RECEPCION-AR-001…007` |

Los documentos contienen datos empresariales realistas (NIT de proveedores,
fechas, montos en pesos colombianos, CIUDADES, transportadoras, cláusulas
contractuales, etc.), lo que permite:

- Probar la **clasificación IA** según las palabras clave de cada categoría.
- Verificar la **extracción de metadatos** (proveedores, montos, números de documento).
- Consultar el **asistente** con preguntas del tipo "¿qué facturas hay?", "resumen de las órdenes de compra", "¿qué contratos están vigentes?".

## Cómo cargarlos en SIGAD

Opción A — vía interfaz (recomendado para la demostración):
1. Iniciar sesión con el usuario administrador.
2. Ir a **Documentos → Subir documento** y arrastrar los archivos.
3. El motor IA los clasifica, extrae el texto y genera los embeddings automáticamente.

Opción B — vía API:
```bash
curl -X POST http://127.0.0.1:8000/api/documentos \
  -H "Authorization: Bearer <token>" \
  -F "archivo=@FACTURA/FACTURA-FE-001.pdf"
```

## Regenerar los documentos

El script `generar_documentos_prueba.py` recrea los 36 documentos (necesita
`fpdf2` y `python-docx`):

```bash
pip install fpdf2 python-docx
python generar_documentos_prueba.py
```