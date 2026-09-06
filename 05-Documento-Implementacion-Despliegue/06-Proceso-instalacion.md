# 6. Proceso de instalación

## Paso 1 — Prerrequisitos
- Confirmar Docker Desktop y Git instalados (ver `02-Requisitos-hw-sw`).
- Contar con una API key de OpenAI.

## Paso 2 — Clonar el repositorio
```bash
git clone https://github.com/JosdaTara/Gesti-n-Documental-IA.git
cd 09-Codigo-Fuente
```

## Paso 3 — Configurar variables de entorno
```bash
cp backend/.env.example backend/.env
# Editar backend/.env: OPENAI_API_KEY, JWT_SECRET, contraseñas de BD/MinIO
```

## Paso 4 — Levantar el ambiente
```bash
docker compose up --build -d
```

## Paso 5 — Verificar servicios
```bash
docker compose ps
# Esperar que todos los contenedores estén "healthy"/"running"
```
- API: http://localhost:8000/docs
- Frontend: http://localhost:5173
- MinIO consola: http://localhost:9001

## Paso 6 — Carga inicial de evidencias
- Ingresar con un usuario gestor.
- Cargar los documentos del folder `11-Repositorio-Documentos-Prueba` (30 documentos,
  5 categorías).
- Confirmar que pasan a estado `procesado`.

## Paso 7 — Prueba de humo
- Ejecutar una búsqueda por palabra clave.
- Ejecutar una búsqueda semántica.
- Hacer una pregunta en el chat RAG y verificar las fuentes citadas.

## Solución de problemas comunes de instalación
| Síntoma | Causa probable | Acción |
|---|---|---|
| Puerto 8000/5432 en uso | Otra aplicación ocupándolo | Cambiar de puerto en `docker-compose.yml` |
| OCR lento o falla | Modelo no descargado / RAM insuficiente | Revisar `docker compose logs backend`; aumentar RAM de Docker |
| Embeddings fallan | API key inválida o sin créditos | Validar `OPENAI_API_KEY` en `.env` y reiniciar |