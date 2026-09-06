# 9. Casos de uso y especificaciones

## Diagrama general de casos de uso

El diagrama general se encuentra en `02-Documento-Diseno/diagramas/diagrama-casos-uso.png`.
Lo representa el actor "Usuario" según su rol: administrador, gestor documental, consultor y
gerencia interactúan con los casos de uso descritos abajo.

## CU-01: Iniciar sesión
- **Actor principal:** Usuario (todas las personas).
- **Precondiciones:** El usuario existe y está activo en el sistema.
- **Flujo principal:**
  1. El usuario ingresa usuario y contraseña.
  2. El sistema valida las credenciales.
  3. El sistema emite un token JWT y muestra la interfaz según el rol.
- **Flujos alternativos:** Credenciales inválidas → mensaje de error; usuario desactivado → acceso denegado.
- **Postcondiciones:** El usuario posee una sesión activa con su rol.

## CU-02: Gestionar usuarios
- **Actor principal:** Administrador.
- **Precondiciones:** Sesión iniciada con rol administrador.
- **Flujo principal:**
  1. El administrador consulta la lista de usuarios.
  2. Crea, edita o desactiva un usuario y asigna rol.
  3. El sistema valida y guarda los cambios.
- **Flujos alternativos:** Email duplicado → error de validación.
- **Postcondiciones:** Los cambios de usuario quedan registrados y auditados.

## CU-03: Cargar documento
- **Actor principal:** Gestor documental.
- **Precondiciones:** Sesión iniciada con rol gestor o administrador.
- **Flujo principal:**
  1. El gestor selecciona uno o varios archivos.
  2. El sistema valida formato y tamaño.
  3. El sistema crea el registro y encola el documento para procesamiento.
- **Flujos alternativos:** Archivo no permitido o >25 MB → rechazo con mensaje.
- **Postcondiciones:** El documento queda en estado "pendiente".

## CU-04: Procesar documento (OCR + IA)
- **Actor principal:** Motor IA (iniciado automáticamente).
- **Precondiciones:** Documento en estado "pendiente".
- **Flujo principal:**
  1. El motor extrae el texto (OCR si es imagen/escaneado).
  2. Normaliza el texto (limpieza, chunking).
  3. Clasifica el documento y extrae metadatos.
  4. Genera el resumen y el embedding.
  5. Persiste resultados y cambia el estado a "procesado".
- **Flujos alternativos:** Error de OCR → estado "error" con motivo.
- **Postcondiciones:** El documento está indexado y consultable.

## CU-05: Corregir clasificación
- **Actor principal:** Gestor documental.
- **Precondiciones:** Documento procesado y sesión con permiso para editar.
- **Flujo principal:**
  1. El gestor abre el documento "requiere revisión".
  2. Cambia la categoría o metadatos.
  3. Guarda; el sistema actualiza la información.
- **Flujos alternativos:** Usuario sin permiso → acceso denegado 403.
- **Postcondiciones:** Los metadatos y la búsqueda usan la información corregida.

## CU-06: Buscar documentos
- **Actor principal:** Consultor.
- **Precondiciones:** Sesión iniciada.
- **Flujo principal:**
  1. El usuario ingresa una consulta (palabra clave o frase conceptual).
  2. El sistema ejecuta búsqueda textual y/o semántica con filtros de categoría.
  3. Muestra resultados ordenados por relevancia con opción de descarga.
- **Flujos alternativos:** Sin resultados → mensaje "Sin resultados".
- **Postcondiciones:** El usuario visualiza y puede abrir documentos.

## CU-07: Consultar documentos en lenguaje natural (RAG)
- **Actor principal:** Consultor.
- **Precondiciones:** Hay documentos indexados.
- **Flujo principal:**
  1. El usuario escribe una pregunta en lenguaje natural.
  2. El sistema recupera fragmentos relevantes por embeddings.
  3. El LLM genera una respuesta basada solo en esos fragmentos.
  4. El sistema muestra la respuesta con las fuentes citadas.
- **Flujos alternativos:** Sin información suficiente → el sistema lo indica.
- **Postcondiciones:** El usuario obtiene una respuesta con trazabilidad a las fuentes.

## CU-08: Generar resumen
- **Actor principal:** Consultor.
- **Precondiciones:** Documento procesado.
- **Flujo principal:**
  1. El usuario solicita el resumen de un documento.
  2. El LLM sintetiza el contenido.
  3. El sistema muestra el resumen.
- **Postcondiciones:** El usuario puede copiar o descargar el resumen.

## CU-09: Ver dashboard
- **Actor principal:** Gerencia / Administrador.
- **Precondiciones:** Sesión con permiso de reportes.
- **Flujo principal:**
  1. El usuario ingresa al dashboard.
  2. El sistema calcula estadísticas de documentos, categorías y consultas.
  3. Muestra gráficas y totales.
- **Postcondiciones:** El usuario visualiza indicadores actualizados.

## CU-10: Auditar acciones
- **Actor principal:** Administrador.
- **Precondiciones:** Sesión con rol administrador.
- **Flujo principal:**
  1. El administrador abre el módulo de auditoría.
  2. Filtra por usuario, documento o período.
  3. El sistema muestra el detalle de cada evento.
- **Postcondiciones:** Se dispone de trazabilidad completa de las acciones.