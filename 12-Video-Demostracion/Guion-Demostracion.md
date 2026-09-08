# 12. Video Demostración - Guion

Video de demostración funcional del sistema **SIGAD** para la sustentación.
Duración sugerida: **6 a 8 minutos**. Grabación en `SIGAD-Demostracion.mp4`
(en esta carpeta) y/o publicado en YouTube (enlace en el README).

> Registro sugerido con OBS Studio o la grabadora del sistema (Windows: Win+G)
> en **Full HD (1920×1080)**, 25-30 fps, con audio explicativo en español.

---

## Guion paso a paso (por módulo)

### 1. Presentación (0:00 – 0:40)
- Nombre del proyecto: **SIGAD – Sistema de Gestión Documental con IA**.
- Objetivo: cargar, clasificar y consultar documentos empresariales mediante IA.
- Tecnologías: FastAPI + React + MySQL + modelos de IA vía OpenRouter.

### 2. Acceso seguro (0:40 – 1:10)
- Abrir `http://localhost:5173`.
- Iniciar sesión con el **administrador** (`admin@sigad.co`).
- Mencionar el control de acceso por token (JWT) y los roles (administrador/analista).

### 3. Tablero de control (1:10 – 1:50)
- Mostrar KPIs: total de documentos, procesados, pendientes, revisiones y consultas.
- Gráficos: documentos por categoría, por estado y por semana.

### 4. Carga y clasificación automática (1:50 – 3:20)
- Ir a **Documentos → Subir documento**.
- Arrastrar un PDF de prueba de la carpeta `11-Repositorio-Documentos-Prueba/FACTURA`.
- Mostrar los estados: `pendiente` → `en_proceso` → `procesado`.
- Abrir **Detalle**: explicar la **categoría asignada en MAYÚSCULAS**,
  el **% de confianza**, el **resumen IA** y los **metadatos extraídos**.
- Reclasificar manualmente un documento con el selector de categoría.

### 5. Búsqueda semántica (3:20 – 4:10)
- Buscar algo *no textual*: "¿qué proveedores de alimentos aparecen?".
- Enfatizar que encuentra por **significado**, no solo por palabra exacta.
- Mostrar el puntaje de coincidencia y alternar a búsqueda por palabras clave.

### 6. Asistente documental con RAG (4:10 – 5:40)
- Hacer 2-3 preguntas reales al chat:
  - "¿Qué facturas se han registrado?"
  - "Resumen de las órdenes de compra"
  - "¿Qué contratos están vigentes?"
- Señalar que responde **con fuentes citadas** (desplegar "Fuentes: N documentos").

### 7. Administración (5:40 – 6:30)
- Crear una **nueva categoría** (botón "Nueva categoría", solo admin).
- Mostrar el registro de usuarios y la **auditoría** de acciones recientes.

### 8. Cierre (6:30 – 7:00)
- Ideas fuerza: clasificación y resúmenes automáticos, búsqueda por significado,
  respuestas con fuentes, auditoría, escalabilidad (Docker, MySQL, multi-proveedor IA).
- Agradecimiento.