# Casos de prueba (mínimo 10)

| ID | Tipo | Descripción | Pasos | Resultado esperado | Resultado obtenido | Estado |
|---|---|---|---|---|---|---|
| CP-01 | Funcional | Inicio de sesión exitoso con credenciales válidas | 1) Abrir login; 2) Ingresar usuario gestor y contraseña válida; 3) Aceptar | Acceso al sistema con menú según rol | Acceso correcto al módulo de carga | Aprobado |
| CP-02 | Seguridad | Inicio de sesión con credenciales inválidas | 1) Ingresar usuario/contraseña incorrectos; 2) Aceptar | Mensaje "Usuario o contraseña inválidos"; sin acceso | Mensaje mostrado; sin sesión | Aprobado |
| CP-03 | Validación archivos | Carga de un PDF digital válido | 1) Ir a carga; 2) Seleccionar factura PDF; 3) Confirmar | Documento aceptado y encolado en estado pendiente | Aceptado y procesado | Aprobado |
| CP-04 | Validación archivos | Rechazo de archivo no permitido (.exe) | 1) Intentar cargar archivo .exe | Rechazo con mensaje de formato no permitido; no se almacena | Rechazado con mensaje claro | Aprobado |
| CP-05 | Caso límite | Rechazo de archivo mayor a 25 MB | 1) Intentar cargar archivo de 30 MB | Rechazo con mensaje de tamaño máximo | Rechazado correctamente | Aprobado |
| CP-06 | Procesamiento IA | OCR de un PDF escaneado (imagen) | 1) Cargar guía de despacho escaneada; 2) Esperar procesamiento | Texto extraído y documento indexado con estado procesado | Texto extraído correctamente | Aprobado |
| CP-07 | Clasificación | Clasificación automática de una factura | 1) Cargar factura de venta; 2) Revisar categoría asignada | Categoría "factura" con confianza ≥ 70% | Categoría correcta | Aprobado |
| CP-08 | Clasificación | Corrección manual de clasificación | 1) Abrir documento "requiere revisión"; 2) Cambiar categoría; 3) Guardar | Categoría y metadatos actualizados | Actualización correcta | Aprobado |
| CP-09 | Extracción | Extracción de metadatos de una factura | 1) Abrir factura procesada; 2) Revisar metadatos | Número, fecha, proveedor y total extraídos | Campos extraídos correctamente | Aprobado |
| CP-10 | Búsqueda | Búsqueda por palabra clave | 1) Buscar "contrato"; 2) Revisar resultados | Documentos con la palabra en texto/metadatos, ordenados por relevancia | Resultados correctos < 5 s | Aprobado |
| CP-11 | Búsqueda | Búsqueda semántica por concepto | 1) Buscar "condiciones de pago"; 2) Revisar resultados | Contratos con cláusulas de pago recuperados por similitud | Recuperación semántica correcta | Aprobado |
| CP-12 | Preguntas NL | Pregunta en lenguaje natural con fuentes | 1) Abrir chat RAG; 2) Preguntar plazo de pago de un proveedor; 3) Revisar respuesta | Respuesta basada en los documentos con fuentes citadas | Respuesta correcta con fuentes | Aprobado |
| CP-13 | Preguntas/sumario | Generación de resumen del documento | 1) Abrir documento; 2) Solicitar resumen | Resumen de hasta 150 palabras | Resumen generado | Aprobado |
| CP-14 | Seguridad | Acceso denegado a rol consultor para gestión de usuarios | 1) Ingresar como consultor; 2) Intentar abrir gestión de usuarios | Acceso denegado (403) | Petición rechazada (403) | Aprobado |
| CP-15 | Caso límite | Carga de documento duplicado | 1) Cargar un documento ya subido; 2) Confirmar | El sistema no reprocesa (RN-06) e informa que ya existe | Duplicado rechazado, sin reproceso | Aprobado |
| CP-16 | Funcional | Dashboard con estadísticas | 1) Ingresar al dashboard; 2) Revisar gráficas | Totales de documentos, categorías y consultas por semana | Datos visualizados correctamente | Aprobado |