# 4. Conclusiones de las pruebas

- **Cobertura:** se ejecutaron **16 casos de prueba** (mínimo exigido: 10) cubriendo
  autenticación, validación de archivos, procesamiento de IA, clasificación, extracción,
  búsqueda, preguntas en lenguaje natural, seguridad y casos límite. **15 de 16 resultaron
  aprobados** y el caso pendiente (CP-15, duplicados) quedó aprobado tras la corrección DEF-04,
  completando así el 100% de los casos críticos.
- **Procesamiento de IA:** el OCR resolvió la textualización de documentos escaneados y la
  búsqueda semántica encontró documentos por concepto (p. ej., "condiciones de pago" → contratos),
  cumpliendo el objetivo central del proyecto.
- **RAG:** las respuestas en lenguaje natural estuvieron respaldadas por fuentes citadas de la
  base documental, reduciendo el riesgo de respuestas sin soporte.
- **Seguridad:** la autenticación JWT y el control de roles funcionaron correctamente; los
  accesos no autorizados devolvieron 403 y quedaron auditarse.
- **Rendimiento:** las búsquedas respondieron en menos de 5 segundos y el procesamiento por
  documento se mantuvo por debajo de 30 segundos (RNF-01/RNF-02).
- **Estado global:** el sistema cumple con los criterios de aceptación definidos en el plan de
  pruebas y queda listo para la demostración y sustentación final.