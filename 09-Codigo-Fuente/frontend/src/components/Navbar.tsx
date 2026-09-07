import { useEffect, useState } from "react";
import { Link, NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import ThemeToggle from "./ThemeToggle";
import { IconLogout, IconArrowRight } from "./Icons";

export default function Navbar() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);
  const { usuario, logout } = useAuth();

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    onScroll();
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  const logo = (
    <Link to="/" className="brand" onClick={() => setOpen(false)}>
      <span className="brand__mark">SIG</span>
      <span>
        SIGAD
        <span className="muted" style={{ fontWeight: 600, fontSize: "0.82rem", marginLeft: 8 }}>
          Gestión Documental
        </span>
      </span>
    </Link>
  );

  const navItems = usuario
    ? [
        { to: "/app/dashboard", label: "Dashboard" },
        { to: "/app/documentos", label: "Documentos" },
        { to: "/app/busqueda", label: "Búsqueda" },
        { to: "/app/chat", label: "Asistente IA" },
        ...(usuario.rol === "administrador"
          ? [
              { to: "/app/usuarios", label: "Usuarios" },
              { to: "/app/auditoria", label: "Auditoría" },
            ]
          : []),
      ]
    : [
        { to: "/#caracteristicas", label: "Características" },
        { to: "/#proceso", label: "Proceso" },
        { to: "/#seguridad", label: "Seguridad" },
      ];

  const handleLogout = () => {
    setOpen(false);
    logout();
  };

  return (
    <>
      <header className={`nav ${scrolled || scrolled ? "is-scrolled" : ""}`}>
        <div className="container nav__inner">
          {logo}

          <nav className="nav__links" aria-label="Navegación principal">
            {navItems.map((item) => (
              <NavLink
                key={item.label}
                to={item.to}
                end={item.to === "/app/dashboard"}
                className={({ isActive }) => `nav__link ${isActive ? "is-active" : ""}`}
              >
                {item.label}
              </NavLink>
            ))}
          </nav>

          <div className="nav__actions">
            <ThemeToggle />
            {usuario ? (
              <button
                type="button"
                className="btn btn-outline btn-sm nav__inline-cta"
                onClick={handleLogout}
              >
                <IconLogout width={16} height={16} />
                Salir
              </button>
            ) : (
              <>
                <NavLink to="/login" className="btn btn-primary btn-sm nav__inline-cta">
                  Iniciar sesión
                  <IconArrowRight width={16} height={16} />
                </NavLink>
              </>
            )}

            <button
              type="button"
              className={`nav__burger ${open ? "is-open" : ""}`}
              onClick={() => setOpen((v) => !v)}
              aria-label="Abrir menú"
              aria-expanded={open}
            >
              <span />
              <span />
              <span />
            </button>
          </div>
        </div>
      </header>

      <div className={`nav__menu ${open ? "is-open" : ""}`}>
        <div className="container" style={{ display: "flex", flexDirection: "column", gap: "0.2rem" }}>
          {navItems.map((item) => (
            <NavLink
              key={item.label}
              to={item.to}
              className={({ isActive }) => `nav__link ${isActive ? "is-active" : ""}`}
              onClick={() => setOpen(false)}
            >
              {item.label}
            </NavLink>
          ))}
          <div style={{ height: 12 }} />
          {usuario ? (
            <button type="button" className="btn btn-outline" onClick={handleLogout}>
              <IconLogout width={16} height={16} />
              Cerrar sesión
            </button>
          ) : (
            <NavLink to="/login" className="btn btn-primary" onClick={() => setOpen(false)}>
              Iniciar sesión
              <IconArrowRight width={16} height={16} />
            </NavLink>
          )}
        </div>
      </div>
    </>
  );
}
