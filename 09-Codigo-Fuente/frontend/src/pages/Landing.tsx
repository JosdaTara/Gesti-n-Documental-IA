import { Link } from "react-router-dom";
import CtaScroll from "../components/CtaScroll";
import Reveal from "../components/Reveal";
import { useAuth } from "../context/AuthContext";
import {
  IconArrowRight,
  IconChat,
  IconDocument,
  IconSearch,
  IconShield,
  IconUpload,
} from "../components/Icons";

const CARACTERISTICAS = [
  {
    icon: <IconDocument />,
    title: "Clasificación automática",
    text: "Cada documento se clasifica en factura, guía de despacho, orden de compra, contrato o acta de recepción, con revisión humana cuando la confianza es baja.",
  },
  {
    icon: <IconSearch />,
    title: "Búsqueda semántica",
    text: "Busca por significado y no solo por palabras. Los embeddings junto con pgvector permiten encontrar documentos afines aunque no compartan términos exactos.",
  },
  {
    icon: <IconChat />,
    title: "Consulta conversacional",
    text: "Pregunta en lenguaje natural y obtén respuestas precisas que citan las fuentes documentales de la organización (RAG).",
  },
  {
    icon: <IconUpload />,
    title: "Extracción y OCR",
    text: "El sistema extrae el texto de PDF, Word e imágenes escaneadas para indexar todo el acervo, incluso archivos que no tienen capa de texto.",
  },
];

const PROCESO = [
  {
    num: "01",
    title: "Carga del documento",
    text: "Sube un archivo PDF, Word, TXT o imagen. El sistema valida formato y tamaño.",
  },
  {
    num: "02",
    title: "Extracción del contenido",
    text: "OCR e inteligencia artificial obtienen el texto, incluso de documentos escaneados.",
  },
  {
    num: "03",
    title: "Clasificación y análisis",
    text: "El motor identifica el tipo de documento, extrae metadatos y genera un resumen.",
  },
  {
    num: "04",
    title: "Búsqueda y consulta",
    text: "Buscá por palabras o pregunta en lenguaje natural. El sistema responde con sus fuentes.",
  },
];

const SEGURIDAD = [
  {
    title: "Autenticación JWT",
    text: "Sesiones seguras protegidas por tokens firmados y expiración controlada.",
  },
  {
    title: "Roles y permisos",
    text: "Administradores y analistas con permisos diferenciados sobre la información.",
  },
  {
    title: "Auditoría completa",
    text: "Cada acción relevante queda registrada con responsable, fecha e IP.",
  },
  {
    title: "Credenciales seguras",
    text: "Contraseñas con hash PBKDF2 y ninguna clave de IA versionada en el repositorio.",
  },
];

export default function Landing() {
  const { usuario } = useAuth();

  return (
    <div>
      {/* HERO */}
      <section className="hero" id="inicio">
        <div className="hero__bg" />
        <div className="hero__grid" />
        <div className="hero__blob-a" />
        <div className="hero__blob-b" />

        <div className="container hero__inner">
          <div>
            <div className="hero__eyebrow">
              <span style={{ width: 8, height: 8, borderRadius: 99, background: "var(--success)", display: "inline-block" }} />
              Sistema Inteligente · Despliegue empresarial
            </div>
            <h1 className="hero__title">
              Gestión y análisis documental con{" "}
              <span className="gradient-text">inteligencia artificial</span>
            </h1>
            <p className="hero__sub">
              SIGAD automatiza el ciclo completo de la documentación: extracción de contenido,
              clasificación automática, búsqueda semántica y consulta conversacional, garantizando
              trazabilidad y seguridad en cada operación.
            </p>
            <div className="hero__cta">
              <Link to={usuario ? "/app/dashboard" : "/login"} className="btn btn-primary">
                Explorar el sistema
                <IconArrowRight width={18} height={18} />
              </Link>
              <a href="#caracteristicas" className="btn btn-outline">
                Conocer más
              </a>
            </div>
            <div className="hero__trust">
              <div>
                <strong>+5</strong> <span>categorías</span>
              </div>
              <div>
                <strong>30+</strong> <span>documentos de prueba</span>
              </div>
              <div>
                <strong>100%</strong> <span>respaldado en la nube</span>
              </div>
            </div>
          </div>

          <div className="hero__visual">
            <div className="hero__card">
              <div className="hero__card-head">
                <span>Procesamiento documental</span>
                <span className="pill-group">
                  <span className="pill">IA</span>
                  <span className="pill pill-a">RAG</span>
                  <span className="pill pill-b">OCR</span>
                </span>
              </div>
              <div className="hero__line grad" />
              <div className="hero__line m" />
              <div className="hero__line s" />
              <div className="hero__line m" />
              <div style={{ height: 14 }} />
              <div style={{ display: "flex", gap: 8 }}>
                <span className="badge badge-success">Clasificado</span>
                <span className="badge badge-info">Embeddings</span>
              </div>
            </div>
            <div className="hero__mini-card hero__mini-a">
              <span className="badge badge-primary">Búsqueda semántica</span>
            </div>
            <div className="hero__mini-card hero__mini-b">
              <span className="badge badge-success">97% precisión</span>
            </div>
          </div>
        </div>
      </section>

      {/* CARACTERÍSTICAS */}
      <section className="section" id="caracteristicas">
        <div className="container">
          <Reveal className="section__head">
            <span className="section__tag">Características</span>
            <h2>Tecnología pensada para el volumen documental real</h2>
            <p className="muted">
              Disponible para resolver el problema de los documentos dispersos y no
              accesibles que enfrentan las empresas.
            </p>
          </Reveal>
          <div className="features">
            {CARACTERISTICAS.map((f, i) => (
              <Reveal key={f.title} delay={i * 90}>
                <article className="card card-hover feature">
                  <div className="feature__chip">{f.icon}</div>
                  <h3>{f.title}</h3>
                  <p>{f.text}</p>
                </article>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* PROCESO */}
      <section className="section" id="proceso" style={{ background: "var(--surface)" }}>
        <div className="container">
          <Reveal className="section__head">
            <span className="section__tag">Proceso</span>
            <h2>El flujo completo, en cuatro pasos</h2>
            <p className="muted">
              Desde el archivo original hasta la respuesta con fuente verificable.
            </p>
          </Reveal>
          <div className="steps">
            {PROCESO.map((p, i) => (
              <Reveal key={p.num} delay={i * 90}>
                <div className="card card-hover step" style={{ height: "100%" }}>
                  <div className="step__num">{p.num}</div>
                  <h3>{p.title}</h3>
                  <p>{p.text}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* SEGURIDAD */}
      <section className="section" id="seguridad">
        <div className="container">
          <Reveal className="section__head">
            <span className="section__tag">Seguridad</span>
            <h2>Confidencialidad y trazabilidad por diseño</h2>
            <p className="muted">
              La información de la organización está protegida en cada etapa del flujo.
            </p>
          </Reveal>
          <div className="features">
            {SEGURIDAD.map((s, i) => (
              <Reveal key={s.title} delay={i * 90}>
                <article className="card card-hover feature">
                  <div className="feature__chip" style={{ background: "color-mix(in srgb, var(--success) 85%, transparent)" }}>
                    <IconShield width={24} height={24} />
                  </div>
                  <h3>{s.title}</h3>
                  <p>{s.text}</p>
                </article>
              </Reveal>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="section" id="cta">
        <div className="container">
          <Reveal>
            <div className="cta-band">
              <h2>¿Listo para poner la documentación a trabajar?</h2>
              <p style={{ maxWidth: 560, margin: "0 auto 1.6rem", opacity: 0.9 }}>
                Accede al panel de demostración y comprueba la rapidez de la búsqueda semántica
                y el asistente conversacional.
              </p>
              <div className="hero__cta" style={{ justifyContent: "center" }}>
                <Link to={usuario ? "/app/dashboard" : "/login"} className="btn btn-primary">
                  Ir al sistema
                  <IconArrowRight width={18} height={18} />
                </Link>
                <a href="#caracteristicas" className="btn btn-outline">
                  Ver características
                </a>
              </div>
            </div>
          </Reveal>
        </div>
      </section>

      {/* FOOTER */}
      <footer className="footer">
        <div className="container footer__inner">
          <div>
            <strong>SIGAD</strong> · Sistema Inteligente de Gestión y Análisis Documental
          </div>
          <div>UTS · Desarrollo de Aplicaciones Empresariales · VI semestre</div>
        </div>
      </footer>

      <CtaScroll />
    </div>
  );
}