# 4. Actores, usuarios y perfiles

## Actores del sistema

| Actor | Rol | Descripción |
|---|---|---|
| Administrador | Admin | Gestiona usuarios, roles, categorías y revisa la auditoría del sistema. |
| Gestor documental | Operativo | Carga documentos, supervisa el procesamiento y corrige clasificaciones automáticas. |
| Consultor | Consulta | Busca, consulta y hace preguntas sobre los documentos. |
| Gerencia | Reportes | Revisa el dashboard con estadísticas para la toma de decisiones. |
| Motor IA | Sistema | Componente automatizado (OCR, embeddings, RAG, LLM) que procesa y responde. |

## Perfiles de usuario (personas)

### Persona 1: Carlos Méndez — Gestor documental
- Objetivos: Digitalizar rápido los documentos que llegan a la oficina y encontrar convenientemente los que necesita.
- Frustraciones: Buscar en carpetas por nombres de archivo inconsistentes; reprocesar documentos porque no los encuentra.
- Nivel técnico: Básico; requiere una interfaz simple, clara y con mensajes en español.

### Persona 2: Laura Torres — Consultor / analista comercial
- Objetivos: Localizar contratos y condiciones de pago y hacer preguntas sobre los documentos para responder a clientes y proveedores.
- Frustraciones: No poder buscar por concepto; depender de otras personas para encontrar documentos.
- Nivel técnico: Medio; confía en búsqueda semántica y consultas conversacionales con IA.

### Persona 3: Andrés Ramírez — Administrador del sistema
- Objetivos: Controlar accesos, revisar auditoría y garantizar la estabilidad del sistema.
- Frustraciones: Procesos manuales de alta de usuarios; falta de trazabilidad sobre quién modifica qué.
- Nivel técnico: Alto; administra configuraciones, variables de entorno y monitoreo.

### Persona 4: Diana Ospina — Gerencia / toma de decisiones
- Objetivos: Conocer cuántos documentos se procesan, su clasificación y las consultas más frecuentes.
- Frustraciones: No tener métricas sobre la operación documental.
- Nivel técnico: Básico; consulta el dashboard y reportes predefinidos.