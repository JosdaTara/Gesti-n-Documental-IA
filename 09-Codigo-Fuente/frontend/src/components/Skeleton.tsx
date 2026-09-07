import type { ReactNode } from "react";

export function Skeleton({ style, className = "" }: { style?: React.CSSProperties; className?: string }) {
  return <div className={`skeleton ${className}`} style={style} />;
}

export function CardSkeleton() {
  return (
    <div className="card" style={{ padding: "1.4rem 1.5rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between", marginBottom: "0.9rem" }}>
        <Skeleton style={{ width: 44, height: 44, borderRadius: 12 }} />
        <Skeleton style={{ width: 70, height: 20 }} />
      </div>
      <Skeleton style={{ width: "55%", height: 30, marginBottom: 8 }} />
      <Skeleton style={{ width: "70%", height: 16 }} />
    </div>
  );
}

export function DocumentoSkeleton() {
  return (
    <div className="card" style={{ padding: "1.1rem 1.3rem" }}>
      <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
        <div style={{ flex: 1 }}>
          <Skeleton style={{ width: "70%", height: 18, marginBottom: 8 }} />
          <Skeleton style={{ width: "45%", height: 14 }} />
        </div>
        <Skeleton style={{ width: 74, height: 24, borderRadius: 999 }} />
      </div>
    </div>
  );
}

export function ChatSkeleton() {
  return (
    <div className="chat-shell">
      <div className="chat-log">
        <Skeleton style={{ width: 200, height: 60, borderRadius: 18 }} />
        <Skeleton style={{ width: 260, height: 80, borderRadius: 18, marginLeft: "auto" }} />
        <Skeleton style={{ width: 180, height: 60, borderRadius: 18 }} />
        <Skeleton style={{ width: 240, height: 90, borderRadius: 18, marginLeft: "auto" }} />
      </div>
      <div style={{ padding: "1rem" }}>
        <Skeleton style={{ width: "100%", height: 50, borderRadius: 12 }} />
      </div>
    </div>
  );
}

export function PageLoader() {
  return (
    <div style={{ display: "grid", placeItems: "center", padding: "3rem 0" }}>
      <div className="spinner" role="status" aria-label="Cargando" />
    </div>
  );
}

export function EmptyState({
  mark,
  title,
  children,
}: {
  mark: ReactNode;
  title: string;
  children?: ReactNode;
}) {
  return (
    <div className="empty">
      <div className="empty__mark">{mark}</div>
      <h3>{title}</h3>
      {children && <p>{children}</p>}
    </div>
  );
}