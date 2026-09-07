import { useState, type FormEvent } from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useToast } from "../components/Toasts";
import { errorMessage } from "../context/AuthContext";

export default function Login() {
  const [email, setEmail] = useState("admin@sigad.co");
  const [password, setPassword] = useState("Admin123!");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const { success } = useToast();
  const navigate = useNavigate();
  const location = useLocation();

  const from = (location.state as { from?: string })?.from ?? "/app/dashboard";

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email.trim(), password);
      success("Sesión iniciada correctamente");
      navigate(from, { replace: true });
    } catch (err) {
      setError(errorMessage(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth">
      <aside className="auth__side">
        <Link to="/" className="brand">
          <span className="brand__mark">SIG</span>
          <span>SIGAD</span>
        </Link>
        <div className="auth__side-quote gradient-text">
          La documentación de tu organización, disponible, clasificada y segura en
          segundos.
        </div>
        <div className="auth__side-foot">
          Proyecto integrador · UTS · VI semestre
        </div>
      </aside>

      <main className="auth__main">
        <div className="auth__card">
          <h1>Iniciar sesión</h1>
          <p className="muted">Accede al panel de gestión documental.</p>

          {error && <div className="alert alert-error">{error}</div>}

          <form onSubmit={handleSubmit}>
            <div className="field">
              <label className="label" htmlFor="email">
                Correo institucional
              </label>
              <input
                id="email"
                type="email"
                className="input"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
                autoComplete="email"
                placeholder="usuario@dominio.com"
              />
            </div>
            <div className="field">
              <label className="label" htmlFor="password">
                Contraseña
              </label>
              <input
                id="password"
                type="password"
                className="input"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                autoComplete="current-password"
                placeholder="••••••••"
              />
            </div>
            <button type="submit" className="btn btn-primary btn-block" disabled={loading}>
              {loading && <span className="spin" />}
              {loading ? "Ingresando…" : "Ingresar al sistema"}
            </button>
          </form>

          <div className="demo-hint">
            <strong>Acceso de demostración</strong> — correo <code>admin@sigad.co</code> y
            contraseña <code>Admin123!</code>
          </div>
        </div>
      </main>
    </div>
  );
}