import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api, Estadisticas } from "../services/api";
import { CardSkeleton, EmptyState } from "../components/Skeleton";
import { useToast } from "../components/Toasts";
import { errorMessage } from "../context/AuthContext";
import { useAuth } from "../context/AuthContext";
import {
  IconChat,
  IconDocument,
  IconSearch,
  IconShield,
} from "../components/Icons";

const ESTADOS_META: Record<string, { label: string; className: string }> = {
  procesado: { label: "Procesado", className: "badge-success" },
  requiere_revision: { label: "Requiere revisión", className: "badge-warning" },
  pendiente: { label: "Pendiente", className: "badge-neutral" },
  en_proceso: { label: "En proceso", className: "badge-info" },
  rechazado: { label: "Rechazado", className: "badge-danger" },
};

export default function Dashboard() {
  const [data, setData] = useState<Estadisticas | null>(null);
  const [loading, setLoading] = useState(true);
  const { usuario } = useAuth();
  const { error } = useToast();
  const navigate = useNavigate();

  useEffect(() => {
    api
      .get<Estadisticas>("/dashboard/estadisticas")
      .then((res) => setData(res.data))
      .catch((err) => error(errorMessage(err)))
      .finally(() => setLoading(false));
  }, [error]);

  if (loading) {
    return (
      <>
        <div className="page-grid">
          <div className="span-4"><CardSkeleton /></div>
          <div className="span-4"><CardSkeleton /></div>
          <div className="span-4"><CardSkeleton /></div>
          <div className="span-8"><CardSkeleton /></div>
          <div className="span-4"><CardSkeleton /></div>
        </div>
      </>
    );
  }

  const maxCategoria = Math.max(1, ...(data?.por_categoria.map((c) => c.cantidad) ?? [1]));
  const maxSemana = Math.max(1, ...(data?.por_semana.map((d) => d.cantidad) ?? [1]));

  const stats = [
    {
      icon: <IconDocument width={20} height={20} />,
      gradient: "linear-gradient(120deg,#4f46e5,#0ea5e9)",
      num: data?.total_documentos ?? 0,
      label: "Documentos totales",
    },
    {
      icon: <IconSearch width={20} height={20} />,
      gradient: "linear-gradient(120deg,#0ea5e9,#10b981)",
      num: data?.total_procesados ?? 0,
      label: "Procesados",
    },
    {
      icon: <IconChat width={20} height={20} />,
      gradient: "linear-gradient(120deg,#f59e0b,#ef4444)",
      num: data?.total_consultas ?? 0,
      label: "Consultas IA",
    },
    {
      icon: <IconShield width={20} height={20} />,
      gradient: "linear-gradient(120deg,#8b5cf6,#6366f1)",
      num: data?.revision ?? 0,
      label: "Por revisar",
    },
  ];

  return (
    <>
      <div className="page__head">
        <div>
          <h1 className="page__title">Panel de control</h1>
          <p className="page__sub">
            Hola, {usuario?.nombre.split(" ")[0]} — resumen del estado de la documentación.
          </p>
        </div>
        <button className="btn btn-primary" onClick={() => navigate("/app/documentos")}>
          <IconDocument width={17} height={17} />
          Gestionar documentos
        </button>
      </div>

      <div className="page-grid">
        {stats.map((s) => (
          <div key={s.label} className="card stat span-4">
            <div className="stat__top">
              <div className="stat__chip" style={{ background: s.gradient, color: "#fff" }}>
                {s.icon}
              </div>
            </div>
            <div className="stat__num">{s.num}</div>
            <div className="stat__label">{s.label}</div>
          </div>
        ))}

        <div className="card span-8" style={{ padding: "1.4rem 1.5rem" }}>
          <h3>Documentos por categoría</h3>
          <p className="muted" style={{ fontSize: "0.88rem", marginBottom: "1.2rem" }}>
            Distribución de documentos procesados según la clasificación automática.
          </p>
          {data?.por_categoria.length ? (
            data.por_categoria.map((c) => (
              <div className="bar-row" key={c.categoria}>
                <span>{c.categoria}</span>
                <div className="bar-row__track">
                  <div
                    className="bar-row__fill"
                    style={{ width: `${(c.cantidad / maxCategoria) * 100}%` }}
                  />
                </div>
                <span className="bar-row__val">{c.cantidad}</span>
              </div>
            ))
          ) : (
            <EmptyState mark={<IconDocument />} title="Sin documentos procesados" />
          )}
        </div>

        <div className="card span-4" style={{ padding: "1.4rem 1.5rem" }}>
          <h3>Estado general</h3>
          <p className="muted" style={{ fontSize: "0.88rem", marginBottom: "1.2rem" }}>
            Procesamiento de la base documental.
          </p>
          {data?.por_estado
            .filter((e) => e.cantidad > 0)
            .map((e) => {
              const meta = ESTADOS_META[e.estado] ?? { label: e.estado, className: "badge-neutral" };
              return (
                <div
                  key={e.estado}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    alignItems: "center",
                    padding: "0.5rem 0",
                    borderBottom: "1px solid var(--line)",
                  }}
                >
                  <span className={`badge ${meta.className}`}>{meta.label}</span>
                  <strong>{e.cantidad}</strong>
                </div>
              );
            })}
          {!(data?.por_estado.some((e) => e.cantidad > 0)) && <p className="muted">Sin datos</p>}
        </div>

        <div className="card span-12" style={{ padding: "1.4rem 1.5rem" }}>
          <h3>Documentos cargados — últimos 7 días</h3>
          <div className="chart-week">
            {data?.por_semana.map((d) => (
              <div className="chart-week__col" key={d.fecha}>
                <div
                  className="chart-week__bar"
                  style={{ height: `${Math.max(4, (d.cantidad / maxSemana) * 100)}%` }}
                />
                <span className="chart-week__label">
                  {new Date(d.fecha + "T00:00:00").toLocaleDateString("es", { weekday: "short" })}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </>
  );
}