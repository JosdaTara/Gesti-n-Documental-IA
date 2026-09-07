import axios from "axios";

export const TOKEN_KEY = "sigad_token";
export const USER_KEY = "sigad_user";

export type Rol = "administrador" | "analista";
export type EstadoDocumento =
  | "pendiente"
  | "en_proceso"
  | "procesado"
  | "requiere_revision"
  | "rechazado";

export interface Usuario {
  id: number;
  nombre: string;
  email: string;
  rol: Rol;
  activo: boolean;
  creado_en?: string | null;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  usuario: Usuario;
}

export interface Categoria {
  id: number;
  nombre: string;
  descripcion: string;
  activa: boolean;
}

export interface Metadato {
  clave: string;
  valor: string;
}

export interface Documento {
  id: number;
  nombre_archivo: string;
  tipo_mime: string;
  tamano_bytes: number;
  estado: EstadoDocumento;
  categoria: string | null;
  confianza: number | null;
  resumen: string | null;
  cargado_en: string | null;
  procesado_en: string | null;
  metadatos?: Metadato[];
}

export interface ResultadoBusqueda {
  id: number;
  documento: string;
  estado: string;
  categoria: string | null;
  fragmento: string;
  puntaje: number;
  confianza: number | null;
}

export interface Fuente {
  documento_id: number;
  documento: string;
  fragmento: string;
  pagina: number | null;
}

export interface RespuestaRag {
  respuesta: string;
  fuentes: Fuente[];
}

export interface Estadisticas {
  total_documentos: number;
  total_procesados: number;
  pendientes: number;
  revision: number;
  total_consultas: number;
  por_categoria: { categoria: string; cantidad: number }[];
  por_estado: { estado: EstadoDocumento; cantidad: number }[];
  por_semana: { fecha: string; cantidad: number }[];
}

export interface AuditoriaRow {
  id: number;
  usuario: string | null;
  accion: string;
  detalle: string | null;
  ip: string | null;
  creado_en: string | null;
}

export const api = axios.create({ baseURL: "/api" });

api.interceptors.request.use((config) => {
  const token = window.localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      window.localStorage.removeItem(TOKEN_KEY);
      window.localStorage.removeItem(USER_KEY);
      if (!window.location.pathname.startsWith("/login")) {
        window.location.assign("/login");
      }
    }
    return Promise.reject(error);
  }
);

export async function loginApi(email: string, password: string): Promise<LoginResponse> {
  const { data } = await api.post<LoginResponse>("/auth/login", { email, password });
  return data;
}

export class ApiError extends Error {
  status: number;

  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

export function errorMessage(error: unknown): string {
  if (axios.isAxiosError(error)) {
    const detail = ((error.response?.data ?? {}) as { detail?: unknown }).detail;
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail) && detail.length > 0) {
      const first = detail[0] as { msg?: string };
      if (first?.msg) return first.msg;
    }
    if (!error.response) return "No se pudo conectar con el servidor.";
    if (error.response.status === 401) return "Credenciales incorrectas o sesión expirada.";
    if (error.response.status === 413) return "El archivo supera el tamaño máximo permitido.";
    if (error.response.status === 415) return "El formato del archivo no está permitido.";
    return "Ocurrió un error al comunicarse con el servidor.";
  }
  return "Ocurrió un error inesperado.";
}