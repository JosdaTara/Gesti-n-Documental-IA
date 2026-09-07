import {
  createContext,
  useCallback,
  useContext,
  useRef,
  useState,
  type ReactNode,
} from "react";
import { IconCheck, IconClose } from "./Icons";

type ToastKind = "success" | "error" | "info";

interface Toast {
  id: number;
  kind: ToastKind;
  message: string;
  leaving?: boolean;
}

interface ToastContextValue {
  push: (kind: ToastKind, message: string) => void;
  success: (message: string) => void;
  error: (message: string) => void;
  info: (message: string) => void;
}

const ToastContext = createContext<ToastContextValue>({
  push: () => undefined,
  success: () => undefined,
  error: () => undefined,
  info: () => undefined,
});

let nextId = 1;

export function ToastProvider({ children }: { children: ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);
  const timers = useRef<Map<number, number>>(new Map());

  const dismiss = useCallback((id: number) => {
    setToasts((prev) => prev.map((t) => (t.id === id ? { ...t, leaving: true } : t)));
    window.setTimeout(() => {
      setToasts((prev) => prev.filter((t) => t.id !== id));
      timers.current.delete(id);
    }, 320);
  }, []);

  const push = useCallback(
    (kind: ToastKind, message: string) => {
      const id = nextId++;
      setToasts((prev) => [...prev.slice(-3), { id, kind, message }]);
      const t = window.setTimeout(() => dismiss(id), 4200);
      timers.current.set(id, t);
    },
    [dismiss]
  );

  const value: ToastContextValue = {
    push,
    success: (m) => push("success", m),
    error: (m) => push("error", m),
    info: (m) => push("info", m),
  };

  return (
    <ToastContext.Provider value={value}>
      {children}
      <div className="toast-region">
        {toasts.map((toast) => (
          <div
            key={toast.id}
            className={`toast toast--${toast.kind}${toast.leaving ? " is-leaving" : ""}`}
            role="status"
          >
            <span style={{ color: `var(--${toast.kind})`, marginTop: 2 }}>
              {toast.kind === "success" ? (
                <IconCheck width={16} height={16} />
              ) : (
                <IconClose width={16} height={16} />
              )}
            </span>
            <span style={{ flex: 1 }}>{toast.message}</span>
            <button
              type="button"
              className="icon-btn"
              style={{ width: 28, height: 28, borderRadius: 8 }}
              onClick={() => dismiss(toast.id)}
              aria-label="Cerrar notificación"
            >
              <IconClose width={14} height={14} />
            </button>
          </div>
        ))}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  return useContext(ToastContext);
}