# 3. Modelo entidad-relación

_(Insertar diagrama ER — imagen o Mermaid)_

```mermaid
erDiagram
    ROLES {
        int id PK
        string nombre
    }
    USUARIOS {
        int id PK
        string nombre
        string email UNIQUE
        string password_hash
        int rol_id FK
        boolean activo
        timestamp creado_en
    }
    CATEGORIAS {
        int id PK
        string nombre
        string descripcion
        boolean activa
    }
    DOCUMENTOS {
        int id PK
        string nombre_archivo
        string tipo_mime
        int tamano_bytes
        string estado
        int categoria_id FK
        string ruta_archivo
        float confianza_clasificacion
        timestamp cargado_en
        int usuario_id FK
    }
    METADATOS {
        int id PK
        int documento_id FK
        string clave
        string valor
    }
    PROCESAMIENTO {
        int id PK
        int documento_id FK
        string texto_extraido
        vector embedding
        string resumen
        string modelo_uso
        int duracion_ms
        string estado
        string error
        timestamp procesado_en
    }
    CONSULTAS {
        int id PK
        int usuario_id FK
        string tipo
        string consulta
        string respuesta
        int documentos_recuperados
        timestamp realizada_en
    }
    AUDITORIA {
        int id PK
        int usuario_id FK
        string accion
        int documento_id FK
        string detalle
        timestamp realizada_en
    }

    ROLES ||--o{ USUARIOS : "asigna"
    USUARIOS ||--o{ DOCUMENTOS : "carga"
    CATEGORIAS ||--o{ DOCUMENTOS : "clasifica"
    DOCUMENTOS ||--|| PROCESAMIENTO : "posee"
    DOCUMENTOS ||--o{ METADATOS : "tiene"
    USUARIOS ||--o{ CONSULTAS : "realiza"
    USUARIOS ||--o{ AUDITORIA : "registra"
```

## Notas del modelo

- `DOCUMENTOS` guarda la referencia del archivo original; `PROCESAMIENTO` guarda el texto
  extraído, el vector y el resumen (relación 1:1).
- El vector de embeddings se almacena en `PROCESAMIENTO.embedding` (dim 1536) con pgvector.
- La auditoría registra cada acción sensible con referencia opcional al documento.
- Se aplica borrado lógico (campo `activo`) para preservar trazabilidad.