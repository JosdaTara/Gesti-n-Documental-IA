import { Link } from "react-router-dom";
import { IconArrowRight } from "../components/Icons";

export default function NotFound() {
  return (
    <div style={{ textAlign: "center", padding: "5rem 0" }}>
      <div style={{ fontSize: "6rem", fontWeight: 900, lineHeight: 1, background: "var(--gradient)", WebkitBackgroundClip: "text", backgroundClip: "text", color: "transparent" }}>
        404
      </div>
      <h1 style={{ margin: "0.5rem 0" }}>Página no encontrada</h1>
      <p className="muted" style={{ maxWidth: 420, margin: "0 auto 1.5rem" }}>
        La página que buscas no existe o fue movida. Verifica la dirección o vuelve al panel.
      </p>
      <Link to="/app/dashboard" className="btn btn-primary">
        Volver al panel
        <IconArrowRight width={17} height={17} />
      </Link>
    </div>
  );
}