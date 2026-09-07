import { useEffect, useState, type FormEvent } from "react";
import { api, Categoria, ResultadoBusqueda, errorMessage } from "../services/api";
import { useToast } from "../components/Toasts";
import { EmptyState } from "../components/Skeleton";
import { IconDocument, IconSearch } from "../components/Icons";

type TipoBusqueda = "semantica" | "keyword";

export default function Busqueda() {
  const [q, setQ] = useState("");
  const [tipo, setTipo] = useState<TipoBusqueda>("semantica");
  const [categoria, setCategoria] = useState("");
  const [categorias, setCategorias] = useState<Categoria[]>([]);
  const [resultados, setResultados] = useState<ResultadoBusqueda[]>([]);
  const [loading, setLoading] = useState(false);
  const [buscado, setBuscado] = useState(false);
  const { error } = useToast();

  useEffect(() => {
    api.get<Categoria[]>("/categorias").then((res) => setCategorias(res.data)).catch(() => undefined);
  }, []);

  const buscar = async (e?: FormEvent) => {
    e?.preventDefault();
    if (q.trim().length < 2) return;
    setLoading(true);
    setBuscado(true);
    try {
      const params: Record<string, string> = { q: q.trim(), tipo };
      if (categoria) params.categoria = categoria;
      const res = await api.get<ResultadoBusqueda[]>("/busqueda", { params });
      setResultados(res.data);
    } catch (err) {
      error(errorMessage(err));
      setResultados([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="page__head">
        <div>
          <h1 className="page__title">Búsqueda semántica</h1>
          <p className="page__sub">
            Encuentra documentos por significado, no solo por palabras exactas.
          </p>
        </div>
      </div>

      <div className="search-panel">
        <form className="search-row" onSubmit={buscar}>
          <input
            className="input"
            placeholder="¿Qué documento necesitas encontrar?…"
            value={q}
            onChange={(e) => setQ(e.target.value)}
          />
          <button className="btn btn-primary" type="submit" disabled={loading} style={{ whiteSpace: "nowrap" }}>
            {loading ? <span className="spin" /> : <IconSearch width={17} height={17} />}
            {loading ? "Buscando…" : "Buscar"}
          </button>
        </form>
        <div style={{ display: "flex", gap: "0.7rem", flexWrap: "wrap" }}>
          <div style={{ display: "inline-flex", gap: "0.25rem" }}>
            {(["semantica", "keyword"] as TipoBusqueda[]).map((t) => (
              <button
                key={t}
                type="button"
                className={`btn ${tipo === t ? "btn-primary" : "btn-outline"} btn-sm`}
                onClick={() => setTipo(t)}
              >
                {t === "semantica" ? "Semántica" : "Palabras clave"}
              </button>
            ))}
          </div>
          <select className="select" style={{ width: "auto", minWidth: 170 }} value={categoria} onChange={(e) => setCategoria(e.target.value)}>
            <option value="">Todas las categorías</option>
            {categorias.map((c) => (
              <option key={c.id} value={c.nombre}>{c.nombre}</option>
            ))}
          </select>
        </div>
      </div>

      <div style={{ height: 20 }} />

      {loading ? (
        <div className="search-panel" style={{ gap: "1rem" }}>
          {[0, 1, 2, 3].map((i) => (
            <div key={i}>
              <div className="skeleton" style={{ width: "40%", height: 18, marginBottom: 10 }} />
              <div className="skeleton" style={{ width: "90%", height: 14 }} />
            </div>
          ))}
        </div>
      ) : !buscado ? (
        <div className="card">
          <EmptyState mark={<IconSearch />} title="Comienza una búsqueda">
            Escribe una consulta o una frase de ejemplo. La búsqueda semántica recupera los
            documentos más relevantes según su significado.
          </EmptyState>
        </div>
      ) : resultados.length === 0 ? (
        <div className="card">
          <EmptyState mark={<IconDocument />} title="Sin resultados">
            No se encontraron documentos relacionados con tu consulta.
          </EmptyState>
        </div>
      ) : (
        <div style={{ display: "grid", gap: "0.9rem" }}>
          <div className="metric-pill">
            <b>{resultados.length}</b>
            <span>resultado{resultados.length !== 1 ? "s" : ""}</span>
          </div>
          {resultados.map((r) => (
            <div className="card card-hover result-item" key={`${r.id}-${r.fragmento}`}>
              <div className="result-item__head">
                <div>
                  <strong>{r.documento}</strong>
                  <div style={{ display: "flex", gap: "0.5rem", marginTop: "0.25rem" }}>
                    {r.categoria && <span className="badge badge-info">{r.categoria}</span>}
                    <span className="badge badge-neutral">{r.estado}</span>
                  </div>
                </div>
                <div style={{ textAlign: "right" }}>
                  <div className="result-item__score">{Math.round(r.puntaje * 100)}%</div>
                  <div className="muted" style={{ fontSize: "0.72rem" }}>coincidencia</div>
                </div>
              </div>
              <p className="result-item__frag">{r.fragmento}</p>
            </div>
          ))}
        </div>
      )}
    </>
  );
}