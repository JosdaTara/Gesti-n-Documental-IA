# 13. Presentación de Sustentación

Presentación utilizada en la sustentación final del proyecto **SIGAD**.

## Archivos

| Archivo | Descripción |
|---|---|
| `SIGAD-Sustentacion.pptx` | Presentación de 11 diapositivas en formato 16:9 (editable en PowerPoint/LibreOffice). |
| `generar_presentacion.py` | Script Python que genera la presentación (requiere `python-pptx`). |

## Contenido de las diapositivas

1. Portada (nombre del proyecto, materia, institución).
2. Agenda.
3. El problema y la oportunidad.
4. Objetivos (general y específicos).
5. Alcance del sistema.
6. Arquitectura tecnológica (React · FastAPI · MySQL · OpenRouter).
7. Módulos funcionales.
8. Motor de IA (RAG).
9. Seguridad y base de datos.
10. Resultados y pruebas.
11. Conclusiones y cierre.

## Editar y regenerar

```bash
pip install python-pptx
python generar_presentacion.py
```

Para ajustar textos o colores, editar las listas y constantes del script y
volver a ejecutarlo.