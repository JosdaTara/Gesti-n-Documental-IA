"""Motor de IA de SIGAD.

Abstrae OCR, extracción, embeddings, RAG, clasificación y resumen.
Sin API key opera en modo demo determinístico: embeddings por hashing y
respuestas basadas en plantillas con los fragmentos más relevantes (sin
llamadas externas). Con GEMINI_API_KEY usa Gemini (text-embedding-004 y el
LLM configurado) y con OPENAI_API_KEY usa OpenAI como alternativa.
"""

import hashlib
import json
import logging
import re
from pathlib import Path

import numpy as np

from app.core.config import settings

logger = logging.getLogger("sigad.ia")

CATEGORIAS = {
    "factura": {
        "keywords": [
            "factura", "facturado", "nit proveedor", "caj 5000", "subtotal", "iva",
            "total a pagar", "numero de factura", "formato de factura",
        ]
    },
    "guia_despacho": {
        "keywords": [
            "guia de despacho", "guía de despacho", "despacho", "destinatario",
            "remitente", "caso de despacho", "transportadora", "kilo", "bultos",
        ]
    },
    "orden_compra": {
        "keywords": [
            "orden de compra", "órden de compra", "compra", "proveedor", "purchase order",
            "cotización", "cantidad", "precio unitario",
        ]
    },
    "contrato": {
        "keywords": [
            "contrato", "cláusula", "vigencia", "partes", "terminos y condiciones",
            "términos", "obligaciones", "firmas", "notaría", "resolución de contrato",
        ]
    },
    "acta_recepcion": {
        "keywords": [
            "acta de recepción", "acta de recibo", "recibo conforme", "recepción",
            "recibí a satisfacción", "conformidad", "entrega de",
        ]
    },
}

DEMO_DIM = 384


# ---------------------------------------------------------------- embeddings
def _demo_embed(text: str, dim: int = DEMO_DIM) -> np.ndarray:
    vector = np.zeros(dim, dtype=np.float32)
    tokens = re.findall(r"[a-záéíóúñü0-9]{2,}", text.lower())
    for token in tokens:
        h = hashlib.blake2b(token.encode("utf-8"), digest_size=8).digest()
        index = int.from_bytes(h[:4], "little") % dim
        sign = 1.0 if h[4] % 2 == 0 else -1.0
        vector[index] += sign
    norm = np.linalg.norm(vector)
    return vector / norm if norm > 0 else vector


_GEMINI_BASE = "https://generativelanguage.googleapis.com/v1beta"
_gemini_client = None


def _get_gemini_client():
    global _gemini_client
    if _gemini_client is None:
        import httpx

        _gemini_client = httpx.Client(timeout=90)
    return _gemini_client


def _gemini_embed(text: str) -> np.ndarray:
    url = (
        f"{_GEMINI_BASE}/models/{settings.gemini_embedding_model}:embedContent"
        f"?key={settings.gemini_api_key}"
    )
    resp = _get_gemini_client().post(
        url, json={"content": {"parts": [{"text": text}]}}
    )
    resp.raise_for_status()
    return np.asarray(resp.json()["embedding"]["values"], dtype=np.float32)


def _openai_embed(text: str) -> np.ndarray:
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    resp = client.embeddings.create(model=settings.openai_embedding_model, input=[text])
    return np.asarray(resp.data[0].embedding, dtype=np.float32)


def _make_embedding_fn():
    if settings.gemini_api_key:
        return _gemini_embed
    if settings.openai_api_key:
        return _openai_embed
    return _demo_embed


_EMBEDDING_FN = None


def get_embedding(text: str) -> np.ndarray:
    global _EMBEDDING_FN
    if _EMBEDDING_FN is None:
        _EMBEDDING_FN = _make_embedding_fn()
    try:
        return np.asarray(_EMBEDDING_FN(text), dtype=np.float32)
    except Exception as exc:  # API caída o sin red → demo determinístico
        logger.warning("Embedding real falló (%s); usando modo demo", exc)
        return _demo_embed(text)


def embed_json(text: str) -> str:
    return json.dumps(get_embedding(text).astype(float).tolist())


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    na = np.linalg.norm(a)
    nb = np.linalg.norm(b)
    if na == 0 or nb == 0:
        return 0.0
    return float(np.dot(a, b) / (na * nb))


# ---------------------------------------------------------------- extracción
def extract_text(path: str | Path, mime: str) -> str:
    path = Path(path)
    if mime == "application/pdf" and path.suffix.lower() == ".pdf":
        return _extract_pdf(path)
    if mime.startswith("text/") or path.suffix.lower() in (".txt", ".md", ".csv", ".log"):
        return path.read_text(encoding="utf-8", errors="replace")
    if mime in ("application/vnd.openxmlformats-officedocument.wordprocessingml.document",):
        return _extract_docx(path)
    if mime.startswith("image/"):
        return _extract_image_ocr(path)
    return f"Formato sin extractor instalado: {mime}. Nombre: {path.name}"


def _extract_pdf(path: Path) -> str:
    try:
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        parts = [f"[PAGINA {i + 1}] {page.extract_text() or ''}" for i, page in enumerate(reader.pages)]
        return "\n".join(parts)
    except Exception:  # pypdf ausente o archivo dañado
        return f"[PDF sin texto extraído — OCR no disponible para: {path.name}]"


def _extract_docx(path: Path) -> str:
    try:
        from docx import Document

        doc = Document(str(path))
        return "\n".join(p.text for p in doc.paragraphs if p.text.strip())
    except Exception:
        return f"[DOCX sin texto extraído: {path.name}]"


def _extract_image_ocr(path: Path) -> str:
    try:
        import pytesseract
        from PIL import Image

        return pytesseract.image_to_string(Image.open(path), lang="spa")
    except Exception:
        return f"[Imagen sin OCR disponible: {path.name}]"


# ---------------------------------------------------------------- chunking
def chunk_text(text: str, size: int = 900, overlap: int = 120) -> list[str]:
    texto = re.sub(r"\s+", " ", text).strip()
    if not texto:
        return []
    chunks: list[str] = []
    start = 0
    total = len(texto)
    while start < total:
        end = min(start + size, total)
        if end < total:
            boundary = re.search(r"[\n.]\s|\n|\. ", texto[start + size - 200 :])
            if boundary:
                boundary_pos = start + size - 200 + boundary.start() + (0 if boundary.group(0) == "\n" else 1)
                end = max(start + 1, min(boundary_pos + 1, total))
        chunk = texto[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= total:
            break
        start = max(0, end - overlap)
    return chunks


# ---------------------------------------------------------------- metadatos
def extract_metadatos(text: str) -> dict[str, str]:
    metadatos: dict[str, str] = {}
    patterns = {
        "numero": r"(?:numero\s*(?:de\s*)?(?:documento|factura|orden)\s*)?[:#]?\s*([A-Z]{2,3}-\d{3,})",
        "valor_total": r"(?:total|valor\s*total|valor\s*a\s*pagar)[:$\s]*([\d.,]+)",
        "fecha": r"(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})",
        "proveedor": r"(?:proveedor|cliente|vendedor)[:\s]+([A-Za-zÁÉÍÓÚÑ .]{4,40})",
        "cuit_nit": r"(?:nit|cuit|cc)[:\s]*([\d-]{5,20})",
    }
    for clave, pattern in patterns.items():
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            if clave == "fecha":
                metadatos[clave] = "-".join(match.groups())
            elif clave in ("valor_total", "proveedor"):
                metadatos[clave] = match.group(1).strip()
            else:
                metadatos[clave] = match.group(1)
    return metadatos


# ---------------------------------------------------------------- clasificación
def clasificar(text: str) -> tuple[str | None, float]:
    lower = text.lower()
    scores: dict[str, int] = {}
    for categoria, spec in CATEGORIAS.items():
        hits = sum(1 for kw in spec["keywords"] if kw in lower)
        scores[categoria] = hits
    best = max(scores, key=scores.get)
    max_hits = scores[best]
    if max_hits == 0:
        return None, 0.0
    confianza = min(0.5 + max_hits * 0.12, 0.98)
    return best, confianza


# ---------------------------------------------------------------- resumen
def resumir(text: str, max_chars: int = 420) -> str:
    oraciones = re.split(r"(?<=[.!?])\s+", text.replace("\n", " ").strip())
    oraciones = [o.strip() for o in oraciones if len(o.strip()) > 20]
    if not oraciones:
        return text[:max_chars].strip()
    base = " ".join(oraciones[:3])
    return base[:max_chars].rstrip() + ("…" if len(base) > max_chars else "")


# ---------------------------------------------------------------- generación LLM
_demo_cache: dict[str, str] = {}

CITA_INSTRUCT = (
    "Responde en español usando exclusivamente el contexto proporcionado. "
    "Cita al final las fuentes entre paréntesis con el nombre del documento. "
    "Si el contexto no responde la pregunta, indícalo con claridad."
)


def generar_respuesta(pregunta: str, fuentes: list[dict]) -> str:
    """Genera una respuesta a partir de los fragmentos recuperados."""
    if settings.gemini_api_key:
        try:
            return _generar_respuesta_gemini(pregunta, fuentes)
        except Exception:
            logger.warning("Gemini falló en generación; intentando OpenAI/demo", exc_info=True)
    if settings.openai_api_key:
        try:
            return _generar_respuesta_llm(pregunta, fuentes)
        except Exception:
            logger.warning("OpenAI falló en generación; usando demo", exc_info=True)
    return _generar_respuesta_demo(pregunta, fuentes)


def _generar_respuesta_gemini(pregunta: str, fuentes: list[dict]) -> str:
    url = (
        f"{_GEMINI_BASE}/models/{settings.gemini_llm_model}:generateContent"
        f"?key={settings.gemini_api_key}"
    )
    contexto = "\n\n".join(
        f"Documento: {f['documento']}\n{f['fragmento']}" for f in fuentes[:5]
    )
    payload = {
        "system_instruction": {"parts": [{"text": CITA_INSTRUCT}]},
        "contents": [{"parts": [{"text": f"Contexto:\n{contexto}\n\nPregunta: {pregunta}"}]}],
        "generationConfig": {"temperature": 0.3, "maxOutputTokens": 600},
    }
    resp = _get_gemini_client().post(url, json=payload)
    resp.raise_for_status()
    data = resp.json()
    return data["candidates"][0]["content"]["parts"][0]["text"].strip()


def _generar_respuesta_llm(pregunta: str, fuentes: list[dict]) -> str:
    from openai import OpenAI

    client = OpenAI(api_key=settings.openai_api_key)
    contexto = "\n\n".join(
        f"Documento: {f['documento']}\n{f['fragmento']}" for f in fuentes[:5]
    )
    messages = [
        {"role": "system", "content": CITA_INSTRUCT},
        {"role": "user", "content": f"Contexto:\n{contexto}\n\nPregunta: {pregunta}"},
    ]
    resp = client.chat.completions.create(
        model=settings.openai_llm_model, messages=messages, temperature=0.3, max_tokens=600
    )
    return resp.choices[0].message.content.strip()


def _generar_respuesta_demo(pregunta: str, fuentes: list[dict]) -> str:
    clave = pregunta.lower().strip()
    if clave in _demo_cache:
        return _demo_cache[clave]

    tema = _inferir_tema(pregunta)
    if not fuentes:
        texto = (
            f"No encontré documentos relacionados con tu consulta sobre {tema}. "
            "Verifica que existan documentos procesados en la base documental o reformula la pregunta."
        )
        _demo_cache[clave] = texto
        return texto

    mejor = fuentes[0]
    refs = ", ".join(f"«{f['documento']}»" for f in fuentes[:3])
    texto = (
        f"Según la información de la base documental, {tema} se describe en {mejor['documento']}: "
        f"{mejor['fragmento'][:380]}"
    )
    if len(fuentes) > 1:
        texto += f" También encontré referencias en {refs}."
    texto += (
        "\n\nEsta respuesta fue generada en modo demo (sin LLM externo). "
        "Configura GEMINI_API_KEY u OPENAI_API_KEY para respuestas sintetizadas."
    )
    _demo_cache[clave] = texto
    return texto


def _inferir_tema(pregunta: str) -> str:
    preguntas_clave = [
        ("proveedor", ["proveedor", "vendedor", "cliente"]),
        ("factura", ["factura", "facturado", "facturas", "monto", "pagar"]),
        ("contrato", ["contrato", "cláusula", "vigencia"]),
        ("despacho", ["guía", "guia", "despacho", "envío", "envio"]),
        ("orden de compra", ["orden", "compra", "pedido"]),
    ]
    lower = pregunta.lower()
    for etiqueta, sinonimias in preguntas_clave:
        if any(s in lower for s in sinonimias):
            return etiqueta
    return "el contenido documental"