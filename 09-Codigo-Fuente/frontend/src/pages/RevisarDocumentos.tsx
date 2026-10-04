import { useCallback, useEffect, useState } from "react";
import { api } from "../services/api";
import {
  Documento,
  Categoria,
  revisarDocumento,
  errorMessage,
  DecisionRevision,
} from "../services/api";
import { useToast } from "../components/Toasts";
import { EmptyState, Skeleton } from "../components/Skeleton";
import { IconCheck, IconClose, IconDocument, IconSettings } from "../components/Icons";

export default function RevisarDocumentos() {
  const [documentos, setDocumentos] = useState<Documento[]>([]);
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [loading, setLoading] = useState(true);
  const [procesandoId, setProcesandoId] = useState<number | null>(null);
  const [comentarios, setComentarios] = useState<Record<number, string>>({});
  const [correcciones, setCorrecciones] = useState<Record<number, number>>({});
  const { success, error } = useToast();

  const cargar = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get<Documento[]>("/documentos", { params: { estado: "requiere_revision" } });
      setDocumentos(res.data);
    } catch (err) {
      error(errorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [error]);

  useEffect(() => {
    cargar();
  }, [cargar]);

  useEffect(() => {
    api.get<Categoria[]>("/categorias").then((res) => setCategorias(res.data)).catch(() => undefined);
  }, []);

  const enviarRevision = async (doc: Documento, decision: DecisionRevision) => {
    setProcesandoId(doc.id);
    try {
      const body: { decision: DecisionRevision; comentario?: string; categoria_final_id?: number } = {
        decision,
        comentario: comentarios[doc.id]?.trim() || undefined,
      };
      if (decision === "CORREGIR") {
        body.categoria_final_id = correcciones[doc.id];
        if (!body.categoria_final_id) {
          error("Selecciona una categoría para corregir.");
          setProcesandoId(null);
          return;
        }
      }
      await revisarDocumento(doc.id, body);
      const etiqueta =
        decision === "APROBAR" ? "aprobado" : decision === "CORREGIR" ? "corregido" : "rechazado";
      success(`«${doc.nombre_archivo}» ${etiqueta}`);
      setComentarios((prev) => {
        const next = { ...prev };
        delete next[doc.id];
        return next;
      });
      cargar();
    } catch (err) {
      error(errorMessage(err));
    } finally {
      setProcesandoId(null);
    }
  };

  return (
    <>
      <div className="page__head">
        <div>
          <h1 className="page__title">Revisión de clasificación</h1>
          <p className="page__sub">
            La IA dudó (confianza menor al 70%) y necesita tu decisión para indexar el documento.
          </p>
        </div>
        <span className="badge badge-warning" style={{ alignSelf: "flex-start" }}>
          {documentos.length} pendiente{documentos.length === 1 ? "" : "s"}
        </span>
      </div>

      {loading ? (
        <div style={{ display: "grid", gap: "0.9rem", maxWidth: 900 }}>
          {[0, 1].map((i) => (
            <Skeleton key={i} style={{ height: 130, borderRadius: 14 }} />
          ))}
        </div>
      ) : documentos.length === 0 ? (
        <div className="card">
          <EmptyState mark={<IconCheck />} title="Sin revisiones pendientes">
            Los documentos con baja confianza de la IA aparecerán aquí para que los apruebes,
            corrijas o rechaces.
          </EmptyState>
        </div>
      ) : (
        <div style={{ display: "grid", gap: "1rem", maxWidth: 900 }}>
          {documentos.map((doc) => (
            <div className="card" key={doc.id} style={{ padding: "1.2rem 1.3rem" }}>
              <div style={{ display: "flex", justifyContent: "space-between", gap: "0.8rem", flexWrap: "wrap" }}>
                <div>
                  <h3 style={{ fontSize: "1rem", wordBreak: "break-word" }}>
                    <IconDocument width={17} height={17} style={{ verticalAlign: "-3px", marginRight: 6, color: "var(--primary)" }} />
                    {doc.nombre_archivo}
                  </h3>
                  <div style={{ display: "flex", gap: "0.5rem", flexWrap: "wrap", marginTop: "0.5rem" }}>
                    <span className="badge badge-warning">requiere_revision</span>
                    {doc.categoria ? <span className="badge badge-info">{doc.categoria}</span> : null}
                    {doc.confianza != null && (
                      <span className="badge badge-primary">{Math.round(doc.confianza * 100)}% de confianza</span>
                    )}
                  </div>
                </div>
                <span className="muted" style={{ fontSize: "0.8rem" }}>
                  {doc.cargado_en ? new Date(doc.cargado_en).toLocaleString("es") : "—"}
                </span>
              </div>

              {doc.resumen && (
                <p className="muted" style={{ margin: "0.7rem 0 0.9rem", fontSize: "0.9rem" }}>
                  <strong>Resumen IA:</strong> {doc.resumen}
                </p>
              )}

              <div style={{ display: "grid", gap: "0.6rem", marginTop: "0.4rem" }}>
                <input
                  className="input"
                  placeholder="Comentario de la revisión (opcional)"
                  value={comentarios[doc.id] ?? ""}
                  onChange={(e) => setComentarios((prev) => ({ ...prev, [doc.id]: e.target.value }))}
                />
                <div style={{ display: "flex", gap: "0.6rem", flexWrap: "wrap", alignItems: "center" }}>
                  <select
                    className="select"
                    style={{ width: "auto", flex: 1, minWidth: 200 }}
                    value={correcciones[doc.id] ?? ""}
                    onChange={(e) =>
                      setCorrecciones((prev) => ({ ...prev, [doc.id]: Number(e.target.value) }))
                    }
                  >
                    <option value="">Corregir a…</option>
                    {categorias.map((c) => (
                      <option key={c.id} value={c.id}>
                        {c.nombre}
                      </option>
                    ))}
                  </select>
                  <button className="btn btn-primary" disabled={procesandoId === doc.id} onClick={() => void enviarRevision(doc, "APROBAR")}>
                    <IconCheck width={16} height={16} />
                    Aprobar
                  </button>
                  <button className="btn btn-outline" disabled={procesandoId === doc.id} onClick={() => void enviarRevision(doc, "CORREGIR")}>
                    <IconSettings width={16} height={16} />
                    Corregir
                  </button>
                  <button className="btn btn-danger-ghost" disabled={procesandoId === doc.id} onClick={() => void enviarRevision(doc, "RECHAZAR")}>
                    <IconClose width={16} height={16} />
                    Rechazar
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </>
  );
}