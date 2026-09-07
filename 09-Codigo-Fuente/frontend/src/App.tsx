import { useEffect } from "react";
import { Routes, Route, Navigate, Outlet, useLocation } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { ThemeProvider } from "./context/ThemeContext";
import { ToastProvider } from "./components/Toasts";
import Navbar from "./components/Navbar";
import BackToTop from "./components/BackToTop";
import ProtectedRoute, { AdminRoute } from "./components/ProtectedRoute";
import { PageLoader } from "./components/Skeleton";
import Landing from "./pages/Landing";
import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Documentos from "./pages/Documentos";
import Busqueda from "./pages/Busqueda";
import Chat from "./pages/Chat";
import Usuarios from "./pages/Usuarios";
import Auditoria from "./pages/Auditoria";
import NotFound from "./pages/NotFound";

function AppLayout() {
  const { loading } = useAuth();
  if (loading) {
    return (
      <div style={{ paddingTop: "140px" }}>
        <PageLoader />
      </div>
    );
  }
  return (
    <>
      <Navbar />
      <main className="page">
        <div className="container">
          <Outlet />
        </div>
      </main>
      <BackToTop />
    </>
  );
}

function PublicLayout() {
  return (
    <>
      <Navbar />
      <Outlet />
      <BackToTop />
    </>
  );
}

function LandingRedirect() {
  const { usuario } = useAuth();
  return usuario ? <Navigate to="/app/dashboard" replace /> : <Landing />;
}

export default function App() {
  return (
    <ThemeProvider>
      <ToastProvider>
        <AuthProvider>
          <ScrollToTop />
          <Routes>
            <Route element={<PublicLayout />}>
              <Route path="/" element={<LandingRedirect />} />
              <Route path="/login" element={<Login />} />
            </Route>
            <Route
              path="/app"
              element={
                <ProtectedRoute>
                  <AppLayout />
                </ProtectedRoute>
              }
            >
              <Route index element={<Navigate to="/app/dashboard" replace />} />
              <Route path="dashboard" element={<Dashboard />} />
              <Route path="documentos" element={<Documentos />} />
              <Route path="busqueda" element={<Busqueda />} />
              <Route path="chat" element={<Chat />} />
              <Route
                path="usuarios"
                element={
                  <AdminRoute>
                    <Usuarios />
                  </AdminRoute>
                }
              />
              <Route
                path="auditoria"
                element={
                  <AdminRoute>
                    <Auditoria />
                  </AdminRoute>
                }
              />
            </Route>
            <Route
              path="*"
              element={
                <div className="page">
                  <div className="container">
                    <NotFound />
                  </div>
                </div>
              }
            />
          </Routes>
        </AuthProvider>
      </ToastProvider>
    </ThemeProvider>
  );
}

function ScrollToTop() {
  const { pathname } = useLocation();
  useEffect(() => {
    window.scrollTo({ top: 0, behavior: "instant" as ScrollBehavior });
  }, [pathname]);
  return null;
}