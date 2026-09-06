# 8. Historias de usuario con criterios de aceptación

## HU-01
**Como** gestor documental **quiero** iniciar sesión de forma segura en el sistema **para** acceder al módulo de carga y procesamiento.

**Criterios de aceptación:**
- Dado que ingreso credenciales correctas, cuando presiono "Iniciar sesión", entonces accedo al sistema y recibo un token de sesión.
- Dado que ingreso credenciales incorrectas, cuando intento ingresar, entonces el sistema muestra "Usuario o contraseña inválidos" y no accedo.
- Dado que mi sesión expiró, cuando realizo una acción, entonces el sistema me solicita autenticarme nuevamente.

## HU-02
**Como** administrador **quiero** gestionar usuarios y roles **para** controlar quién accede al sistema y qué puede hacer.

**Criterios de aceptación:**
- Dado que soy administrador, cuando creo un usuario y le asigno un rol, entonces el usuario puede iniciar sesión con su rol asignado.
- Dado que desactivo un usuario, cuando este intenta ingresar, entonces el sistema lo rechaza.
- Dado que un usuario con rol consultor intenta modificar roles, entonces el sistema le niega el acceso (403).

## HU-03
**Como** gestor documental **quiero** cargar documentos en varios formatos **para** digitalizar el acervo documental.

**Criterios de aceptación:**
- Dado que selecciono un archivo válido (PDF, DOCX, TXT, JPG, PNG) de menos de 25 MB, cuando lo cargo, entonces el sistema lo acepta y lo encola para procesamiento.
- Dado que selecciono un archivo no permitido o mayor a 25 MB, cuando lo cargo, entonces el sistema lo rechaza con un mensaje claro.

## HU-04
**Como** gestor documental **quiero** ver el estado del procesamiento de cada documento **para** saber qué documentos están listos para consulta.

**Criterios de aceptación:**
- Dado que cargo varios documentos, cuando reviso la lista, entonces cada uno muestra su estado: pendiente, procesando, procesado, error.
- Dado que el procesamiento falla, cuando reviso el detalle, entonces el sistema muestra el motivo del error.

## HU-05
**Como** gestor documental **quiero** corregir la clasificación automática **para** garantizar que los documentos queden en la categoría correcta.

**Criterios de aceptación:**
- Dado que un documento fue clasificado erróneamente, cuando lo edito, entonces puedo cambiar su categoría y guardar los cambios.
- Dado que un documento tiene confianza de clasificación < 70%, cuando se listan los documentos, entonces aparece marcado como "requiere revisión".

## HU-06
**Como** consultor **quiero** buscar documentos por palabras clave **para** localizarlos rápidamente.

**Criterios de aceptación:**
- Dado que digito una palabra clave, cuando ejecuto la búsqueda, entonces el sistema devuelve los documentos que la contienen en el texto o metadatos, ordenados por relevancia.
- Dado que no hay resultados, cuando busco, entonces el sistema muestra un mensaje "Sin resultados".

## HU-07
**Como** consultor **quiero** buscar por concepto o significado (búsqueda semántica) **para** encontrar documentos aunque no use las palabras exactas.

**Criterios de aceptación:**
- Dado que busco por un concepto equivalente ("acuerdos de pago"), cuando ejecuto la búsqueda, entonces el sistema encuentra contratos con cláusulas de pago aunque no contengan esa frase exacta.

## HU-08
**Como** consultor **quiero** hacer preguntas en lenguaje natural sobre los documentos **para** obtener respuestas con sus fuentes.

**Criterios de aceptación:**
- Dado que pregunto "¿cuál es el plazo de pago del contrato con Proveedor X?", cuando envío la pregunta, entonces el sistema responde citando el contrato del que obtuvo la información.
- Dado que no hay información en la base documental, cuando pregunto, entonces el sistema indica que no encontró información en los documentos.

## HU-09
**Como** consultor **quiero** ver un resumen automático de un documento **para** entender su contenido sin leerlo completo.

**Criterios de aceptación:**
- Dado que abro un documento procesado, cuando solicito el resumen, entonces el sistema muestra un resumen de máximo 150 palabras.

## HU-10
**Como** gerente **quiero** ver un dashboard con estadísticas **para** monitorear la operación documental.

**Criterios de aceptación:**
- Dado que ingreso al dashboard, cuando lo abro, entonces veo totales de documentos, categorías, documentos procesados por semana y consultas realizadas.

## HU-11
**Como** administrador **quiero** consultar el log de auditoría **para** verificar qué usuario realizó cada acción.

**Criterios de aceptación:**
- Dado que reviso la auditoría, cuando filtro por usuario o por documento, entonces veo fecha, usuario, acción y detalle de cada evento.