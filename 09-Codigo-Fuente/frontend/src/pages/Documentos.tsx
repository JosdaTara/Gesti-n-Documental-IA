import { useCallback, useEffect, useRef, useState, type ChangeEvent } from "react";
import { api, Categoria, Documento, EstadoDocumento, errorMessage } from "../services/api";
import { useToast } from "../components/Toasts";
import Modal from "../components/Modal";
import { DocumentoSkeleton, EmptyState } from "../components/Skeleton";
import {
  IconDocument,
  IconDownload,
  IconSearch,
  IconTrash,
  IconUpload,
} from "../components/Icons";

const ESTADOS_META: Record<string, { label: string; className: string }> = {
  procesado: { label: "Procesado", className: "badge-success" },
  requiere_revision: { label: "Requiere revisión", className: "badge-warning" },
  pendiente: { label: "Pendiente", className: "badge-neutral" },
  en_proceso: { label: "En proceso", className: "badge-info" },
  rechazado: { label: "Rechazado", className: "badge-danger" },
};

function formatBytes(bytes: number) {
  if (!bytes) return "0 B";
  const units = ["B", "KB", "MB", "GB"];
  let i = 0;
  let v = bytes;
  while (v >= 1024 && i < units.length - 1) {
    v /= 1024;
    i++;
  }
  return `${v.toFixed(v >= 10 || i === 0 ? 0 : 1)} ${units[i]}`;
}

export default function Documentos() {
  const [documentos, setDocumentos] = useState<Documento[]>([]);
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [dragActive, setDragActive] = useState(false);
  const [filtroEstado, setFiltroEstado] = useState<EstadoDocumento | "">("");
  const [filtroCategoria, setFiltroCategoria] = useState("");
  const [q, setQ] = useState("");
  const [detalle, setDetalle] = useState<Documento | null>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const { success, error } = useToast();

  const cargar = useCallback(async () => {
    setLoading(true);
    try {
      const params: Record<string, string> = {};
      if (filtroEstado) params.estado = filtroEstado;
      if (filtroCategoria) params.categoria = filtroCategoria;
      if (q) params.q = q;
      const res = await api.get<Documento[]>("/documentos", { params });
      setDocumentos(res.data);
    } catch (err) {
      error(errorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [filtroEstado, filtroCategoria, q, error]);

  useEffect(() => {
    cargar();
  }, [cargar]);

  useEffect(() => {
    api.get<Categoria[]>("/categorias").then((res) => setCategorias(res.data)).catch(() => undefined);
  }, []);

  const handleFile = async (file: File) => {
    setUploading(true);
    try {
      const form = new FormData();
      form.append("archivo", file);
      await api.post("/documentos", form);
      success(`«${file.name}» procesado correctamente`);
      setFiltroEstado("");
      setFiltroCategoria("");
      setQ("");
      cargar();
    } catch (err) {
      error(errorMessage(err));
    } finally {
      setUploading(false);
    }
  };

  const onUpload = (e: ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) void handleFile(file);
    e.target.value = "";
  };

  const onDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setDragActive(false);
    const file = e.dataTransfer.files?.[0];
    if (file) void handleFile(file);
  };

  const reclasificar = async (documentoId: number, categoriaId: number) => {
    try {
      await api.put(`/documentos/${documentoId}/clasificacion`, { categoria_id: categoriaId });
      success("Clasificación actualizada");
      if (detalle && detalle.id === documentoId) await abrirDetalle(documentoId);
      cargar();
    } catch (err) {
      error(errorMessage(err));
    }
  };

  const abrirDetalle = async (documentoId: number) => {
    try {
      const res = await api.get<Documento>(`/documentos/${documentoId}`);
      setDetalle(res.data);
    } catch (err) {
      error(errorMessage(err));
    }
  };

  const eliminar = async (documentoId: number) => {
    if (!window.confirm("¿Eliminar este documento de forma permanente?")) return;
    try {
      await api.delete(`/documentos/${documentoId}`);
      success("Documento eliminado");
      setDetalle(null);
      cargar();
    } catch (err) {
      error(errorMessage(err));
    }
  };

  const descargar = (documentoId: number) => {
    window.open(`/api/documentos/${documentoId}/archivo`, "_blank");
  };

  const hayFiltros = Boolean(filtroEstado || filtroCategoria || q);

  return (
    <>
      <div className="page__head">
        <div>
          <h1 className="page__title">Documentos</h1>
          <p className="page__sub">Carga, clasifica y gestiona la base documental.</p>
        </div>
        <button className="btn btn-primary" onClick={() => inputRef.current?.click()}>
          <IconUpload width={17} height={17} />
          Subir documento
        </button>
        <input
          ref={inputRef}
          type="file"
          style={{ display: "none" }}
          accept=".pdf,.docx,.txt,.md,.jpg,.jpeg,.png"
          onChange={onUpload}
        />
      </div>

      <div
        className={`doc-upload ${dragActive ? "is-dragging" : ""}`}
        onDragOver={(e) => {
          e.preventDefault();
          setDragActive(true);
        }}
        onDragLeave={() => setDragActive(false)}
        onDrop={onDrop}
        onClick={() => inputRef.current?.click()}
      >
        <span className="feature__chip" style={{ margin: "0 auto 0.8rem" }}>
          <IconUpload />
        </span>
        {uploading ? (
          <>
            <div className="spinner" style={{ margin: "0 auto 0.8rem" }} />
            <strong>Procesando documento…</strong>
            <div className="doc-upload__hint">El motor IA está extrayendo y clasificando el contenido.</div>
          </>
        ) : (
          <>
            <strong>Arrastra tu archivo aquí o haz clic para elegir</strong>
            <div className="doc-upload__hint">PDF, DOCX, TXT, MD, JPG o PNG · máx. 15 MB</div>
          </>
        )}
      </div>

      <div style={{ height: 20 }} />

      <div className="search-panel">
        <div className="search-row">
          <span className="icon-btn" style={{ color: "var(--muted)", pointerEvents: "none", border: "none", background: "transparent" }}>
            <IconSearch width={18} height={18} />
          </span>
          <input
            className="input"
            placeholder="Buscar por nombre de archivo…"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
        </div>
        <div style={{ display: "flex", gap: "0.7rem", flexWrap: "wrap" }}>
          <select className="select" style={{ width: "auto", flex: 1, minWidth: 170 }} value={filtroEstado} onChange={(e) => setFiltroEstado(e.target.value as EstadoDocumento | "")}>
            <option value="">Todos los estados</option>
            <option value="procesado">Procesados</option>
            <option value="requiere_revision">Requiere revisión</option>
            <option value="pendiente">Pendientes</option>
            <option value="en_proceso">En proceso</option>
            <option value="rechazado">Rechazados</option>
          </select>
          <select className="select" style={{ width: "auto", flex: 1, minWidth: 170 }} value={filtroCategoria} onChange={(e) => setFiltroCategoria(e.target.value)}>
            <option value="">Todas las categorías</option>
            {categorias.map((c) => (
              <option key={c.id} value={c.nombre}>{c.nombre}</option>
            ))}
          </select>
          {hayFiltros && (
            <button
              className="btn btn-ghost btn-sm"
              onClick={() => {
                setFiltroEstado("");
                setFiltroCategoria("");
                setQ("");
              }}
            >
              Limpiar
            </button>
          )}
        </div>
      </div>

      <div style={{ height: 20 }} />

      {loading ? (
        <div className="page-grid">
          <div className="span-12" style={{ display: "grid", gap: "0.9rem" }}>
            {[0, 1, 2, 3].map((i) => (
              <DocumentoSkeleton key={i} />
            ))}
          </div>
        </div>
      ) : documentos.length === 0 ? (
        <div className="card">
          <EmptyState mark={<IconDocument />} title="No hay documentos que coincidan">
            {hayFiltros
              ? "Ajusta los filtros o limpia la búsqueda."
              : "Sube un documento para comenzar a construir la base documental."}
          </EmptyState>
        </div>
      ) : (
        <div className="page-grid">
          {documentos.map((doc) => {
            const meta = ESTADOS_META[doc.estado] ?? { label: doc.estado, className: "badge-neutral" };
            return (
              <div className="card card-hover span-4" key={doc.id} style={{ padding: "1.2rem 1.3rem" }}>
                <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.6rem" }}>
                  <span className={`badge ${meta.className}`}>{meta.label}</span>
                  {doc.confianza != null && (
                    <span className="badge badge-primary">{Math.round(doc.confianza * 100)}% conf.</span>
                  )}
                </div>
                <h3 style={{ fontSize: "0.98rem", marginBottom: "0.4rem", wordBreak: "break-word" }}>
                  {doc.nombre_archivo}
                </h3>
                <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginBottom: "0.5rem" }}>
                  {doc.categoria ? (
                    <span className="badge badge-info">{doc.categoria}</span>
                  ) : (
                    <span className="badge badge-neutral">Sin clasificar</span>
                  )}
                  <span className="muted" style={{ fontSize: "0.8rem" }}>{formatBytes(doc.tamano_bytes)}</span>
                </div>
                <div style={{ display: "flex", gap: "0.5rem" }}>
                  <button className="btn btn-outline btn-sm" onClick={() => void abrirDetalle(doc.id)}>
                    Detalle
                  </button>
                  <button className="btn btn-ghost btn-sm" onClick={() => descargar(doc.id)}>
                    <IconDownload width={15} height={15} />
                  </button>
                  <button className="btn btn-danger-ghost btn-sm" onClick={() => void eliminar(doc.id)}>
                    <IconTrash width={15} height={15} />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {detalle && (
        <Modal title="Detalle del documento" onClose={() => setDetalle(null)}>
          <div style={{ marginBottom: "1rem" }}>
            <h3 style={{ fontSize: "1.05rem", wordBreak: "break-word" }}>{detalle.nombre_archivo}</h3>
            <p className="muted" style={{ fontSize: "0.85rem" }}>
              {formatBytes(detalle.tamano_bytes)} · {detalle.tipo_mime}
            </p>
          </div>

          <div className="field">
            <label className="label">Categoría asignada</label>
            <select
              className="select"
              value={detalle.categoria ?? ""}
              onChange={(e) => {
                const cat = categorias.find((c) => c.nombre === e.target.value);
                if (cat) void reclasificar(detalle.id, cat.id);
                else setDetalle({ ...detalle, categoria: e.target.value });
              }}
            >
              <option value="">Sin categoría</option>
              {categorias.map((c) => (
                <option key={c.id} value={c.nombre}>{c.nombre}</option>
              ))}
            </select>
          </div>

          {detalle.resumen && (
            <div className="alert alert-info" style={{ marginBottom: "1rem" }}>
              <strong>Resumen IA:</strong> {detalle.resumen}
            </div>
          )}

          {detalle.metadatos && detalle.metadatos.length > 0 && (
            <div style={{ marginBottom: "1rem" }}>
              <h4 style={{ fontSize: "0.9rem", marginBottom: "0.5rem" }}>Metadatos extraídos</h4>
              <div className="table-wrap">
                <table className="table" style={{ minWidth: 0 }}>
                  <tbody>
                    {detalle.metadatos.slice(0, 6).map((m) => (
                      <tr key={m.clave}>
                        <td style={{ width: "42%", color: "var(--text-2)" }}>{m.clave}</td>
                        <td style={{ fontWeight: 600 }}>{m.valor}</td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}

          <div style={{ display: "flex", gap: "0.6rem", marginTop: "0.4rem" }}>
            <button className="btn btn-outline btn-block" onClick={() => descargar(detalle.id)}>
              <IconDownload width={16} height={16} />
              Descargar
            </button>
            <button className="btn btn-danger-ghost" style={{ border: "1px solid var(--danger)" }} onClick={() => void eliminar(detalle.id)}>
              <IconTrash width={16} height={16} />
            </button>
          </div>
        </Modal>
      )}
    </>
  );
}