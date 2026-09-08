# 10. Base de Datos - Scripts

Scripts SQL de la base de datos **`gestion_documental_bd`** del sistema SIGAD.

## Contenido

| Archivo | Descripción |
|---|---|
| `01-Esquema-MySQL.sql` | DDL completo: tablas, índices, claves foráneas y creación de la BD en MySQL 8. |
| `02-Datos-Iniciales.sql` | Carga de las 5 categorías base (en mayúsculas) y del usuario administrador (`admin@sigad.co` / `Admin123!`). |
| `03-Consultas-Reportes.sql` | Consultas del tablero de control, auditoría y trazabilidad. |

## Estructura de datos

```
categorias 1─┐
             │           1 1                    1 1
usuarios 1───┤── documentos ── metadatos_documento    N
             │              │
             │              └── chunks (embedding JSON, 3072 dims)
             │
             ├── auditoria
             └── consultas
```

- **categorias**: clasificación documental (FACTURA, GUIA_DESPACHO, ORDEN_COMPRA, CONTRATO, ACTA_RECEPCION y las creadas por el administrador).
- **documentos**: expediente documental con estado (`pendiente`, `en_proceso`, `procesado`, `requiere_revision`, `rechazado`), confianza de la clasificación IA y texto extraído.
- **chunks**: fragmentos del texto (con `contenido`) y su **embedding** como vector JSON en `MEDIUMTEXT` (modelo `openai/text-embedding-3-large`, 3072 dimensiones, vía OpenRouter).
- **metadatos_documento**: datos clave extraídos por la IA (NIT, fechas, montos, números de documento…).
- **auditoria** y **consultas**: registro de acciones y del historial del asistente RAG.

## Cómo aplicar

1. Tener MySQL 8 corriendo (XAMPP: `C:\xampp\mysql\bin\mysql.exe -u root`).
2. Aplicar los scripts en orden:
   ```bash
   mysql -u root < 01-Esquema-MySQL.sql
   mysql -u root < 02-Datos-Iniciales.sql
   mysql -u root gestion_documental_bd < 03-Consultas-Reportes.sql
   ```
3. La aplicación puede crear la BD y los datos por su cuenta en el arranque
   (`init_db` en el backend). Este script es útil para aprovisionar o restablecer
   el entorno manualmente.

## Conexión de la aplicación

`backend/.env` (no se sube al repositorio):

```
DATABASE_URL=mysql+pymysql://root:@localhost:3306/gestion_documental_bd?charset=utf8mb4
```