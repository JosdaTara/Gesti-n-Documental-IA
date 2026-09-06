# Manual de Usuario

## 1. Introducción

SIGAD es el **Sistema Inteligente de Gestión y Análisis Documental** de Distribuidora Andina
S.A.S. Permite cargar documentos (facturas, guías de despacho, órdenes de compra, contratos y
actas), procesarlos con IA (OCR, clasificación, resumen) y consultarlos mediante búsqueda
textual, búsqueda semántica y preguntas en lenguaje natural.

## 2. Requisitos para usar el sistema

- Navegador web actual (Chrome, Edge o Firefox).
- Credenciales de acceso entregadas por el administrador.
- Acceso a la URL del sistema: `http://localhost:5173` (ambiente local).

## 3. Registro e inicio de sesión

1. Abrir la URL del sistema.
2. Digitar **usuario** y **contraseña** y pulsar **Ingresar**.
3. Al ingresar, el menú se ajusta a tu rol:
   - **Consultor:** búsqueda, consultas y descarga.
   - **Gestor documental:** además, carga de documentos y corrección de clasificación.
   - **Administrador:** además, usuarios, auditoría y dashboard.

> El registro directo no está habilitado: los usuarios son creados por el administrador.

## 4. Gestión de repositorios/carpetas

Los documentos se organizan por **categoría** (configuradas por el administrador):

| Categoría | Ejemplos |
|---|---|
| Factura | Facturas de venta emitidas |
| Guía de despacho | Guías de transporte de mercancía |
| Orden de compra | Órdenes emitidas a proveedores |
| Contrato | Contratos comerciales con clientes/proveedores |
| Acta | Actas de recepción y reunión |

Los documentos quedan asignados automáticamente a una categoría durante el procesamiento.

## 5. Carga y consulta de documentos

**Cargar (rol gestor/admin):**
1. Ir a **Carga de documentos**.
2. Seleccionar uno o varios archivos (PDF, DOCX, TXT, JPG, PNG; máx. 25 MB).
3. Pulsar **Subir**.
4. El estado avanza: `pendiente → procesando → procesado` (o `error`).

**Consultar lista:**
- En **Documentos** se filtra por estado y categoría.
- Cada documento muestra su categoría, confianza de clasificación y acciones
  (ver texto/resumen, corregir, descargar).

## 6. Uso de funciones de IA (clasificación, resumen, búsqueda, preguntas)

- **Clasificación automática:** el sistema asigna la categoría y la marca como
  "requiere revisión" si la confianza es baja (< 70%). El gestor puede corregirla abriendo el
  documento y guardando la categoría correcta.
- **Metadatos y resumen:** al abrir un documento procesado se muestra su texto, los campos
  extraídos (número, fecha, proveedor, total, etc.) y un **resumen automático** de hasta
  150 palabras.
- **Búsqueda por palabra clave:** ingresa términos en **Buscar** (modo *palabra clave*).
- **Búsqueda semántica:** cambia el modo a *semántico*. Encuentra documentos **por concepto**,
  aunque no contengan la palabra exacta (ej.: "condiciones de pago" → contratos con cláusulas
  de pago).
- **Preguntas al sistema (RAG):** en el **chat**, escribe preguntas en lenguaje natural sobre
  los documentos (ej.: "¿Cuál es el plazo de pago del contrato con Proveedor X?"). El sistema
  responde citando las fuentes de las que obtuvo la información.

## 7. Dashboard

Disponible para administrador y gerencia:
- Total de documentos y por categoría.
- Documentos procesados por semana.
- Consultas realizadas.
- Porcentaje de errores de procesamiento.

## 8. Preguntas frecuentes

**¿Qué hago si un documento queda en error?**
Comunícalo al administrador; el error queda registrado con su motivo y puede reprocesarse.

**¿Puedo subir cualquier formato?**
No. Solo PDF, DOCX, TXT, JPG y PNG, con un máximo de 25 MB por archivo.

**¿Puedo consultar sin saber la palabra exacta?**
Sí, usa la **búsqueda semántica** o el **chat** con lenguaje natural.

**¿El sistema guarda mis datos personales?**
No. Solo se procesan los documentos de la base corporativa (validados para no incluir datos
personales reales sin autorización).