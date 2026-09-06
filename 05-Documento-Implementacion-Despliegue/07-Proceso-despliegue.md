# 7. Proceso de despliegue

## Modalidad de despliegue

Despliegue **local mediante Docker Compose** (ambiente de demostración/sustentación). Permite
ejecutar el sistema completo en la máquina del equipo sin infraestructura externa.

```bash
# Construir y publicar los servicios
docker compose up --build -d

# Ver estado
docker compose ps

# Logs del backend
docker compose logs -f api
```

## URL o mecanismo de acceso

| Servicio | URL | Acceso |
|---|---|---|
| Frontend (SPA) | http://localhost:5173 | Navegador |
| API (Swagger) | http://localhost:8000/docs | Interfaz interactiva |
| MinIO consola | http://localhost:9001 | Credenciales de `MINIO_ROOT_USER/PASSWORD` |

Usuarios iniciales de demostración: `admin`, `gestor`, `consultor` (ver
03-Documento-Desarrollo/05-Manual-tecnico-instalacion.md para las credenciales por defecto).

## Procedimiento de actualización
```bash
git pull origin main
docker compose up --build -d
```
Si el esquema de BD cambió, ejecutar las migraciones correspondientes en `db/`.

## Consideraciones para un despliegue productivo futuro
- Cambiar todas las credenciales de demostración.
- Usar HTTPS y secretos gestionados.
- Reemplazar MinIO/local por almacenamiento gestionado si se requiere alta disponibilidad.
- Configurar respaldos automáticos (ver `08-Estrategia-respaldo-recuperacion`).