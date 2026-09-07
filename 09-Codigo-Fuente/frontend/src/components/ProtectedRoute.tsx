import type { ReactNode } from "react";
import { Navigate, useLocation } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({ children }: { children: ReactNode }) {
  const { usuario, loading } = useAuth();
  const location = useLocation();

  if (loading) return null;

  if (!usuario) {
    return <Navigate to="/login" replace state={{ from: location.pathname }} />;
  }

  return <>{children}</>;
}

export function AdminRoute({ children }: { children: ReactNode }) {
  const { usuario } = useAuth();
  if (!usuario || usuario.rol !== "administrador") {
    return <Navigate to="/app/dashboard" replace />;
  }
  return <>{children}</>;
}