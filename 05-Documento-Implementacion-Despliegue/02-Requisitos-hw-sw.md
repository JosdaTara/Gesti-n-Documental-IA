# 2. Requisitos de hardware/software

## Hardware (mínimo recomendado)

| Recurso | Requisito mínimo | Recomendado |
|---|---|---|
| Procesador | 2 núcleos x64 | 4 núcleos |
| Memoria RAM | 8 GB | 16 GB |
| Disco | 20 GB libres (incluye 30+ documentos de prueba) | 40 GB SSD |
| Red | Conexión a Internet (solo para la API de IA) | Banda ancha estable |

## Software

| Componente | Versión | Observaciones |
|---|---|---|
| Sistema operativo | Windows 10/11, macOS o Linux | WSL2 recomendado en Windows |
| Docker Desktop | 4.x+ | Con WSL2 habilitado |
| Git | 2.40+ | Para clonar el repositorio |
| Navegador | Chrome/Edge/Firefox actuales | Para el frontend |
| (Opcional) API key de OpenAI | — | Para embeddings y LLM |
| (Opcional) pgAdmin / DBeaver | — | Administración de la BD |

## Verificación de prerequisitos

```bash
docker --version
docker compose version
git --version
```