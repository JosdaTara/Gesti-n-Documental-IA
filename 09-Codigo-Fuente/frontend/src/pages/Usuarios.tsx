import { useCallback, useEffect, useState, type FormEvent } from "react";
import { api, Usuario, errorMessage } from "../services/api";
import { useToast } from "../components/Toasts";
import Modal from "../components/Modal";
import { EmptyState, Skeleton } from "../components/Skeleton";
import { IconUsers } from "../components/Icons";

interface FormUser {
  nombre: string;
  email: string;
  password: string;
  rol: "administrador" | "analista";
}

const emptyForm: FormUser = { nombre: "", email: "", password: "", rol: "analista" };

export default function Usuarios() {
  const [usuarios, setUsuarios] = useState<Usuario[]>([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [form, setForm] = useState<FormUser>(emptyForm);
  const [submitting, setSubmitting] = useState(false);
  const { success, error } = useToast();

  const cargar = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get<Usuario[]>("/usuarios");
      setUsuarios(res.data);
    } catch (err) {
      error(errorMessage(err));
    } finally {
      setLoading(false);
    }
  }, [error]);

  useEffect(() => {
    cargar();
  }, [cargar]);

  const crear = async (e: FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    try {
      await api.post("/usuarios", form);
      success(`Usuario «${form.nombre}» creado`);
      setModalOpen(false);
      setForm(emptyForm);
      cargar();
    } catch (err) {
      error(errorMessage(err));
    } finally {
      setSubmitting(false);
    }
  };

  const toggleActivo = async (u: Usuario) => {
    try {
      await api.put(`/usuarios/${u.id}`, { activo: !u.activo });
      cargar();
    } catch (err) {
      error(errorMessage(err));
    }
  };

  return (
    <>
      <div className="page__head">
        <div>
          <h1 className="page__title">Usuarios</h1>
          <p className="page__sub">Gestiona los accesos y roles de la plataforma.</p>
        </div>
        <button className="btn btn-primary" onClick={() => setModalOpen(true)}>
          Nuevo usuario
        </button>
      </div>

      {loading ? (
        <div style={{ display: "grid", gap: "0.9rem", maxWidth: 720 }}>
          {[0, 1, 2].map((i) => (
            <Skeleton key={i} style={{ height: 64, borderRadius: 14 }} />
          ))}
        </div>
      ) : usuarios.length === 0 ? (
        <div className="card">
          <EmptyState mark={<IconUsers />} title="Sin usuarios registrados" />
        </div>
      ) : (
        <div className="table-wrap" style={{ maxWidth: 860 }}>
          <table className="table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Correo</th>
                <th>Rol</th>
                <th>Estado</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {usuarios.map((u) => (
                <tr key={u.id}>
                  <td style={{ fontWeight: 600 }}>{u.nombre}</td>
                  <td>{u.email}</td>
                  <td>
                    <span className={`badge ${u.rol === "administrador" ? "badge-primary" : "badge-info"}`}>
                      {u.rol}
                    </span>
                  </td>
                  <td>
                    <span className={`badge ${u.activo ? "badge-success" : "badge-neutral"}`}>
                      {u.activo ? "Activo" : "Inactivo"}
                    </span>
                  </td>
                  <td>
                    <button
                      className="btn btn-ghost btn-sm"
                      onClick={() => void toggleActivo(u)}
                      disabled={u.rol === "administrador" && usuarios.filter((x) => x.rol === "administrador" && x.activo).length === 1}
                      title={u.activo ? "Desactivar" : "Activar"}
                    >
                      {u.activo ? "Desactivar" : "Activar"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      {modalOpen && (
        <Modal title="Nuevo usuario" onClose={() => setModalOpen(false)}>
          <form onSubmit={crear}>
            <div className="field">
              <label className="label">Nombre completo</label>
              <input className="input" value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} required minLength={2} />
            </div>
            <div className="field">
              <label className="label">Correo</label>
              <input className="input" type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} required />
            </div>
            <div className="field">
              <label className="label">Contraseña (mín. 8 caracteres)</label>
              <input className="input" type="password" value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} required minLength={8} />
            </div>
            <div className="field">
              <label className="label">Rol</label>
              <select className="select" value={form.rol} onChange={(e) => setForm({ ...form, rol: e.target.value as FormUser["rol"] })}>
                <option value="analista">Analista</option>
                <option value="administrador">Administrador</option>
              </select>
            </div>
            <div style={{ display: "flex", gap: "0.6rem" }}>
              <button type="button" className="btn btn-outline btn-block" onClick={() => setModalOpen(false)}>
                Cancelar
              </button>
              <button type="submit" className="btn btn-primary btn-block" disabled={submitting}>
                {submitting ? "Guardando…" : "Crear usuario"}
              </button>
            </div>
          </form>
        </Modal>
      )}
    </>
  );
}