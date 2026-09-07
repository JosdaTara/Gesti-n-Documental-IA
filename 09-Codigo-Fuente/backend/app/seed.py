"""Datos base: categorías, usuario administrador y (en modo demo) documentos de ejemplo."""

from datetime import datetime
from pathlib import Path

from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import ensure_storage
from app.core.security import hash_password
from app.models import Categoria, Documento, Usuario

CATEGORIAS = [
    ("factura", "Comprobante comercial de venta o cobro"),
    ("guia_despacho", "Documento que acompaña el envío físico de mercancía"),
    ("orden_compra", "Solicitud formal de compra de productos o servicios"),
    ("contrato", "Acuerdo legal entre dos o más partes"),
    ("acta_recepcion", "Constancia de entrega y recepción conforme"),
]

DOCUMENTOS_DEMO = [
    ("facturas-ejemplo.txt", "factura", "factura", 4123, "FACTURA FE-001\n"
     "NIT proveedor: 900.123.456-7\nProveedor: Alimentos del Valle S.A.\n"
     "Fecha: 12/03/2026\nSubtotal: 4,850,000 IVA: 921,500 Total a pagar: 5,771,500.\n"
     "Numero de factura: FACT-2026-0142"),
    ("facturas-ejemplo2.txt", "factura", "factura", 3890, "FACTURA FE-002\n"
     "NIT proveedor: 830.987.654-3\nProveedor: Papeles y Empaques Ltda.\n"
     "Fecha: 18/03/2026\nSubtotal: 1,230,000 IVA: 233,700 Total: 1,463,700.\n"
     "Numero de factura: FACT-2026-0158"),
    ("guias-despacho.txt", "guia_despacho", "guia_despacho", 2105, "GUIA DE DESPACHO GD-2041\n"
     "Remitente: Bodega Central Bogotá\nDestinatario: Sucursal Cali\n"
     "Transportadora: Envíos Andinos. Bultos: 12. Peso: 340 kg.\n"
     "Caso de despacho: DI-0987"),
    ("ordenes-compra.txt", "orden_compra", "orden_compra", 3341, "ORDEN DE COMPRA OC-552\n"
     "Proveedor: Ferreterías del Eje S.A.\nCantidad: 80 Precio unitario: 45,000\n"
     "Total orden: 3,600,000. Condiciones de entrega: 15 días.\n"
     "Cotización de referencia: COT-8871"),
    ("contrato-servicios.txt", "contrato", "contrato", 5560, "CONTRATO DE PRESTACIÓN DE SERVICIOS\n"
     "Entre Distribuidora Andina S.A.S. y Tecnología Documental S.A.\n"
     "Objeto: suministro e implementación de plataforma documental.\n"
     "Cláusula 1: vigencia 24 meses. Cláusula 3: obligaciones de las partes.\n"
     "Términos y condiciones de confidencialidad. Firmas y notaría 18."),
    ("actas-recepcion.txt", "acta_recepcion", "acta_recepcion", 1420, "ACTA DE RECEPCIÓN AR-778\n"
     "Entrega de mercancía: lote de empaques biodegradables.\n"
     "Se recibe a satisfacción la totalidad de los bienes relacionados.\n"
     "Recepción conforme. Conformidad del área de bodega."),
]


def crear_categorias(db: Session) -> None:
    if db.query(Categoria).count() == 0:
        for nombre, descripcion in CATEGORIAS:
            db.add(Categoria(nombre=nombre, descripcion=descripcion))
        db.commit()


def crear_admin(db: Session) -> None:
    if db.query(Usuario).filter(Usuario.email == "admin@sigad.co").first() is None:
        db.add(
            Usuario(
                nombre="Administrador SIGAD",
                email="admin@sigad.co",
                password_hash=hash_password("Admin123!"),
                rol="administrador",
            )
        )
        db.commit()


def crear_documentos_demo(db: Session) -> None:
    """Genera documentos de ejemplo ya procesados para la demo y sustentación."""
    from app.ia import engine
    from app.models import Chunk, MetadatoDocumento

    ensure_storage()
    if db.query(Documento).count() > 0:
        return

    categorias: dict[str, int] = {
        c.nombre: c.id for c in db.query(Categoria).all()
    }
    if not categorias:
        crear_categorias(db)
        categorias = {c.nombre: c.id for c in db.query(Categoria).all()}

    for nombre, categoria, carpeta, tamano, texto in DOCUMENTOS_DEMO:
        ruta = Path(settings.storage_path) / carpeta
        ruta.mkdir(parents=True, exist_ok=True)
        archivo = ruta / nombre
        archivo.write_text(texto, encoding="utf-8")

        documento = Documento(
            nombre_archivo=nombre,
            ruta_archivo=str(archivo),
            tipo_mime="text/plain",
            tamano_bytes=tamano,
            estado="procesado",
            categoria_id=categorias[categoria],
            confianza=0.94,
            resumen=engine.resumir(texto),
            texto_extraido=texto,
            cargado_en=datetime.utcnow(),
            procesado_en=datetime.utcnow(),
        )
        db.add(documento)
        db.flush()

        for indice, contenido in enumerate(engine.chunk_text(texto)):
            db.add(
                Chunk(
                    documento_id=documento.id,
                    indice=indice,
                    contenido=contenido[:1800],
                    embedding=engine.embed_json(contenido[:1200]),
                )
            )
        for clave, valor in engine.extract_metadatos(texto).items():
            db.add(MetadatoDocumento(documento_id=documento.id, clave=clave, valor=valor))

    db.commit()


def init_db(db: Session) -> None:
    crear_categorias(db)
    crear_admin(db)
    if settings.demo_mode:
        crear_documentos_demo(db)