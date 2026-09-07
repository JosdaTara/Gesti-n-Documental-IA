import { useEffect, useState } from "react";
import { api, AuditoriaRow, errorMessage } from "../services/api";
import { useToast } from "../components/Toasts";
import { EmptyState, Skeleton } from "../components/Skeleton";
import { IconShield } from "../components/Icons";

const ACCIONES: Record<string, { label: string; className: string }> = {
  "documento.cargar": { label: "Carga de documento", className: "badge-info" },
  "documento.eliminar": { label: "Eliminación", className: "badge-danger" },
  "documento.clasificar": { label: "Clasificación", className: "badge-primary" },
};

export default function Auditoria() {
  const [rows, setRows] = useState<AuditoriaRow[]>([]);
  const [loading, setLoading] = useState(true);
  const [accion, setAccion] = useState("");
  const { error } = useToast();

  useEffect(() => {
    const cargar = async () => {
      setLoading(true);
      try {
        const params: Record<string, string> = {};
        if (accion) params.accion = accion;
        const res = await api.get<AuditoriaRow[]>("/auditoria", { params });
        setRows(res.data);
      } catch (err) {
        error(errorMessage(err));
      } finally {
        setLoading(false);
      }
    };
    void cargar();
  }, [accion, error]);

  return (
    <>
      <div className="page__head">
        <div>
          <h1 className="page__title">Auditoría</h1>
          <p className="page__sub">Registro de las acciones realizadas en la plataforma.</p>
        </div>
        <select className="select" style={{ width: "auto", minWidth: 200 }} value={accion} onChange={(e) => setAccion(e.target.value)}>
          <option value="">Todas las acciones</option>
          <option value="documento.cargar">Carga de documento</option>
          <option value="documento.eliminar">Eliminación</option>
          <option value="documento.clasificar">Clasificación</option>
        </select>
      </div>

      {loading ? (
        <div style={{ display: "grid", gap: "0.9rem", maxWidth: 900 }}>
          {[0, 1, 2].map((i) => (
            <Skeleton key={i} style={{ height: 56, borderRadius: 14 }} />
          ))}
        </div>
      ) : rows.length === 0 ? (
        <div className="card">
          <EmptyState mark={<IconShield />} title="Sin registros de auditoría">
            Las acciones relevantes quedarán registradas aquí.
          </EmptyState>
        </div>
      ) : (
        <div className="table-wrap">
          <table className="table">
            <thead>
              <tr>
                <th>Fecha</th>
                <th>Usuario</th>
                <th>Acción</th>
                <th>Detalle</th>
                <th>IP</th>
              </tr>
            </thead>
            <tbody>
              {rows.map((r) => {
                const meta = ACCIONES[r.accion] ?? { label: r.accion, className: "badge-neutral" };
                return (
                  <tr key={r.id}>
                    <td style={{ whiteSpace: "nowrap", color: "var(--text-2)", fontSize: "0.85rem" }}>
                      {r.creado_en ? new Date(r.creado_en).toLocaleString("es") : "—"}
                    </td>
                    <td style={{ fontWeight: 600 }}>{r.usuario ?? "—"}</td>
                    <td>
                      <span className={`badge ${meta.className}`}>{meta.label}</span>
                    </td>
                    <td style={{ color: "var(--text-2)" }}>{r.detalle ?? "—"}</td>
                    <td style={{ color: "var(--muted)", fontSize: "0.85rem" }}>{r.ip ?? "—"}</td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      )}
    </>
  );
}