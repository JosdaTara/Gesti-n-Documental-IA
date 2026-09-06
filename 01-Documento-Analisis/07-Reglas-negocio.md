# 7. Reglas de negocio

| ID | Regla |
|---|---|
| RN-01 | Los únicos formatos aceptados para la carga son PDF, DOCX, TXT, JPG y PNG. |
| RN-02 | El tamaño máximo de un archivo es de 25 MB. |
| RN-03 | Cada documento debe pertenecer a una única categoría; las categorías de fábrica son: factura de venta, guía de despacho, orden de compra, contrato y acta de recepción. |
| RN-04 | No se permite almacenar documentos con datos personales reales de terceros sin autorización expresa (Ley 1581 de 2012). |
| RN-05 | Los documentos comerciales deben conservarse al menos 5 años desde su fecha de emisión. |
| RN-06 | Un documento ya procesado e indexado no se procesa nuevamente, salvo que se cargue una nueva versión. |
| RN-07 | Solo los usuarios con rol 'gestor documental' o 'administrador' pueden corregir clasificaciones y metadatos. |
| RN-08 | Toda acción sensible (carga, edición, descarga, eliminación) debe quedar registrada en el log de auditoría. |
| RN-09 | La clasificación automática que tenga una confianza baja (< 70%) debe marcarse como "requiere revisión" para el gestor. |
| RN-10 | Las respuestas del módulo conversacional deben citar al menos una fuente (documento) extraída de la base documental. |