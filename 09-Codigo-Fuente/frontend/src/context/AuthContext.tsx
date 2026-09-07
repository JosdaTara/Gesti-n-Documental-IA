import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import {
  TOKEN_KEY,
  USER_KEY,
  Usuario,
  api,
  errorMessage,
  loginApi,
} from "../services/api";

interface AuthContextValue {
  usuario: Usuario | null;
  loading: boolean;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue>({
  usuario: null,
  loading: true,
  login: async () => undefined,
  logout: () => undefined,
});

function readUsuario(): Usuario | null {
  try {
    const raw = window.localStorage.getItem(USER_KEY);
    return raw ? (JSON.parse(raw) as Usuario) : null;
  } catch {
    return null;
  }
}

export function AuthProvider({ children }: { children: ReactNode }) {
  const [usuario, setUsuario] = useState<Usuario | null>(readUsuario);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = window.localStorage.getItem(TOKEN_KEY);
    if (!token) {
      setLoading(false);
      return;
    }
    apiGetMe()
      .then((data) => {
        setUsuario(data);
        window.localStorage.setItem(USER_KEY, JSON.stringify(data));
      })
      .catch(() => {
        setUsuario(null);
      })
      .finally(() => setLoading(false));
  }, []);

  const login = async (email: string, password: string) => {
    const response = await loginApi(email, password);
    window.localStorage.setItem(TOKEN_KEY, response.access_token);
    window.localStorage.setItem(USER_KEY, JSON.stringify(response.usuario));
    setUsuario(response.usuario);
  };

  const logout = () => {
    window.localStorage.removeItem(TOKEN_KEY);
    window.localStorage.removeItem(USER_KEY);
    setUsuario(null);
    window.location.assign("/");
  };

  return (
    <AuthContext.Provider value={{ usuario, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

async function apiGetMe(): Promise<Usuario> {
  const { data } = await api.get<Usuario>("/auth/me");
  return data;
}

export function useAuth() {
  return useContext(AuthContext);
}

export { errorMessage };