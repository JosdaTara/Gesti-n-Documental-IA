# -*- coding: utf-8 -*-
"""Genera la presentación de sustentación de SIGAD (PPTX, 16:9).

Requisito: python-pptx instalado.

Uso:
    python generar_presentacion.py
"""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.util import Inches, Pt

OUT = "SIGAD-Sustentacion.pptx"

INDIGO = RGBColor(0x4F, 0x46, 0xE5)
INDIGO_D = RGBColor(0x31, 0x2E, 0x81)
CIELO = RGBColor(0x0E, 0xAA, 0xFF)
DARK = RGBColor(0x1E, 0x1B, 0x4B)
MUTED = RGBColor(0x5B, 0x5B, 0x7A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
SOFT = RGBColor(0xF2, 0xF3, 0xFD)
GREEN = RGBColor(0x10, 0xB9, 0x81)

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


def slide():
    return prs.slides.add_slide(BLANK)


def fondo(s, color=WHITE):
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = color


def caja(s, x, y, w, h, color, shape=MSO_SHAPE.RECTANGLE):
    sp = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    sp.fill.solid()
    sp.fill.fore_color.rgb = color
    sp.line.fill.background()
    return sp


def texto(s, x, y, w, h, runs, size=18, color=DARK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP):
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = anchor
    if isinstance(runs, str):
        runs = [[(runs, bold)]]
    first = True
    for para in runs:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = align
        p.space_after = Pt(6)
        if isinstance(para, str):
            para = [(para, bold)]
        for txt, b in para:
            r = p.add_run()
            r.text = txt
            r.font.size = Pt(size)
            r.font.bold = b
            r.font.color.rgb = color
            r.font.name = "Calibri"
    return tb


def header(s, titulo, sub=""):
    caja(s, 0, 0, 13.333, 1.15, INDIGO)
    caja(s, 0, 1.15, 13.333, 0.07, CIELO)
    texto(s, 0.7, 0.18, 12, 0.8, titulo, size=30, color=WHITE, bold=True)
    if sub:
        texto(s, 0.7, 0.72, 12, 0.4, sub, size=14, color=SOFT)


def bullets(s, items, x=0.9, y=1.6, w=11.6, size=20, gap=10):
    parrafos = []
    for item in items:
        if isinstance(item, tuple):
            txt, bold = item
        else:
            txt, bold = item, False
        parrafos.append([("•  ", bold), (txt, bold)])
    tb = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(6))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, para in enumerate(parrafos):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_after = Pt(gap)
        for t, b in para:
            r = p.add_run()
            r.text = t
            r.font.size = Pt(size)
            r.font.bold = b
            r.font.color.rgb = DARK
            r.font.name = "Calibri"


# ---- Portada
s = slide()
fondo(s, INDIGO_D)
caja(s, 0, 6.75, 13.333, 0.75, CIELO)
texto(s, 1.2, 2.1, 11, 1.4, "SIGAD", size=66, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
texto(s, 1.2, 3.35, 11, 0.7, "Sistema de Gestión Documental con Inteligencia Artificial",
      size=26, color=SOFT, align=PP_ALIGN.CENTER)
texto(s, 1.2, 4.35, 11, 1.4,
      [[("Desarrollo de Aplicaciones Empresariales — 6° semestre\n", True)],
       [("Unidades Tecnológicas de Santander · 2026", False)]],
      size=17, color=WHITE, align=PP_ALIGN.CENTER)

# ---- Agenda
s = slide()
header(s, "Agenda", "Contenido de la sustentación")
items = ("El problema y la oportunidad", "Objetivos", "Alcance del sistema",
         "Arquitectura tecnológica", "Módulos funcionales", "Motor de IA (RAG)",
         "Seguridad y base de datos", "Resultados y pruebas", "Conclusiones")
for i, it in enumerate(items):
    col = i // 5
    fila = i % 5
    caja(s, 0.9 + col * 6.1, 1.6 + fila * 1.05, 5.7, 0.85, SOFT)
    texto(s, 1.15 + col * 6.1, 1.78 + fila * 1.05, 5.2, 0.6, f"{i+1}. {it}", size=18, bold=True, color=INDIGO_D)

# ---- Problema
s = slide()
header(s, "El problema", "Gestión documental manual y dispersa")
bullets(s, [
    ("Búsqueda lenta por nombre o carpeta, sin recuperación semántica.", True),
    ("Clasificación manual de documentos: costosa, inconsistente y propensa a error.", False),
    ("Sin acceso inmediato a respuestas: hay que abrir y leer cada archivo.", False),
    ("Sin trazabilidad ni auditoría de las acciones sobre los documentos.", False),
    ("Oportunidad: aplicar IA para clasificar, resumir y responder con fuentes.", True),
])

# ---- Objetivos
s = slide()
header(s, "Objetivos", "General y específicos")
caja(s, 0.9, 1.7, 5.7, 1.5, INDIGO)
texto(s, 1.2, 1.95, 5.1, 1.1, "Objetivo general", size=16, color=CIELO, bold=True)
texto(s, 1.2, 2.35, 5.1, 0.9, "Construir un sistema web de gestión documental con IA.",
      size=18, color=WHITE, bold=True, anchor=MSO_ANCHOR.TOP)
bullets(s, [
    ("Clasificar automáticamente documentos por categoría con confianza.", False),
    ("Extraer metadatos y resúmenes automáticos.", False),
    ("Buscar documentos por significado (búsqueda semántica).", False),
    ("Responder preguntas con RAG citando las fuentes.", False),
], x=7.0, w=5.6, y=1.8)

# ---- Alcance
s = slide()
header(s, "Alcance", "Qué incluye el sistema")
bullets(s, [
    ("Carga de documentos: PDF, DOCX, TXT, MD y JPG/PNG (máx. 15 MB).", True),
    ("Pipeline IA: extracción de texto → chunks → embeddings → clasificación → resumen → metadatos.", True),
    ("Análisis: tablero con KPIs y gráficos por categoría, estado y semana.", False),
    ("Búsqueda semántica + palabras clave y asistente conversacional RAG.", False),
    ("Administración: usuarios con roles, categorías y auditoría.", False),
    ("Exclusiones: firma electrónica, flujos de aprobación externos y OCR fotográfico complejo.", False),
])

# ---- Arquitectura
s = slide()
header(s, "Arquitectura tecnológica", "Frontend + Backend + BD + proveedor IA")
cajas = [
    ("React + Vite + TypeScript", "SPA con diseño responsive y tema claro/oscuro", 0.7, 2.4, 3.7, INDIGO),
    ("FastAPI (Python)", "API REST, JWT, motor de IA y pipeline documental", 4.8, 2.4, 3.7, INDIGO_D),
    ("MySQL 8", "Datos estructurados y embeddings como JSON (MEDIUMTEXT)", 8.9, 2.4, 3.7, INDIGO_D),
    ("OpenRouter (IA)", "Chat openrouter/auto + embeddings text-embedding-3-large", 2.75, 4.6, 7.8, CIELO),
]
for t, d, x, y, w, col in cajas:
    caja(s, x, y, w, 1.5, col)
    texto(s, x + 0.25, y + 0.15, w - 0.5, 0.6, t, size=18, color=WHITE, bold=True)
    texto(s, x + 0.25, y + 0.8, w - 0.5, 0.7, d, size=13, color=SOFT)

# ---- Módulos
s = slide()
header(s, "Módulos funcionales", "Alcance por módulo del sistema")
mods = [
    ("1. Autenticación", "Login JWT, roles: administrador y analista."),
    ("2. Tablero", "KPIs y gráficos del estado de la documentación."),
    ("3. Documentos", "Carga, clasificación, detalle, reclasificación y descarga."),
    ("4. Búsqueda", "Semántica (vectorial) y por palabras clave."),
    ("5. Asistente", "Chat con respuesta generada y fuentes citadas."),
    ("6. Admin", "Usuarios, categorías y auditoría de acciones."),
]
for i, (t, d) in enumerate(mods):
    col = i // 3
    fila = i % 3
    caja(s, 0.9 + col * 6.1, 1.7 + fila * 1.7, 5.7, 1.45, SOFT)
    texto(s, 1.15 + col * 6.1, 1.9 + fila * 1.7, 5.2, 0.6, t, size=19, color=INDIGO_D, bold=True)
    texto(s, 1.15 + col * 6.1, 2.5 + fila * 1.7, 5.2, 0.6, d, size=14, color=MUTED)

# ---- Motor IA
s = slide()
header(s, "Motor de IA", "RAG: recuperación aumentada por generación")
bullets(s, [
    ("Clasificación por palabras clave con % de confianza (umbral 70%).", True),
    ("Embeddings reales de 3072 dimensiones (text-embedding-3-large).", False),
    ("Chunking del texto y similitud coseno para recuperar fragmentos.", False),
    ("Prompt estructurado con citas obligatorias al final de la respuesta.", True),
    ("Fallback multi-proveedor: OpenRouter → Gemini → OpenAI y modo demo sin clave.", False),
    ("Resúmenes y metadatos automáticos por documento.", False),
])

# ---- Seguridad y BD
s = slide()
header(s, "Seguridad y base de datos", "Datos protegidos y trazables")
bullets(s, [
    ("Contraseñas con hash pbkdf2_sha256 y tokens JWT de acceso.", True),
    ("Roles: solo el administrador gestiona usuarios, categorías y auditoría.", False),
    ("7 entidades: categorias, usuarios, documentos, metadatos_documento, chunks, auditoria y consultas.", True),
    ("Embeddings almacenados como vector JSON (MEDIUMTEXT en MySQL).", False),
    ("Scripts SQL en la carpeta 10 para aprovisionar la base de datos.", False),
])

# ---- Resultados
s = slide()
header(s, "Resultados y pruebas", "Verificación del sistema")
bullets(s, [
    ("36 documentos de prueba en 5 categorías y 4 formatos (carpeta 11).", True),
    ("Clasificación automática con categorías en MAYÚSCULAS y % de confianza.", False),
    ("10 pruebas automatizadas del backend (pytest) superadas.", True),
    ("Respuestas del asistente con fuentes citadas desde la base documental.", False),
    ("Búsqueda semántica que recupera por significado, no solo palabra exacta.", False),
    ("Construcción de producción del frontend OK (112 módulos).", False),
])

# ---- Cierre
s = slide()
fondo(s, INDIGO_D)
caja(s, 0, 6.9, 13.333, 0.6, CIELO)
texto(s, 1.2, 1.6, 11, 1.2, "Conclusiones", size=40, color=WHITE, bold=True, align=PP_ALIGN.CENTER)
bullets(s, [
    ("SIGAD centraliza la documentación y reduce el trabajo manual de clasificación.", True),
    ("La búsqueda por significado y el asistente RAG aceleran la consulta de información.", True),
    ("La arquitectura es escalable (Docker, MySQL) y multinube para IA.", True),
    ("Se cumple el objetivo del curso: aplicación empresarial completa y desplegable.", True),
], x=1.5, y=3.0, w=10.3, size=20, gap=14)
texto(s, 1.2, 6.05, 11, 0.6, "¡Gracias!", size=22, color=SOFT, align=PP_ALIGN.CENTER)

prs.save(OUT)
print(f"Presentación guardada: {OUT} ({len(prs.slides)} diapositivas)")