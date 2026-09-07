import { useEffect, useRef, useState, type FormEvent, type KeyboardEvent } from "react";
import { api, RespuestaRag, errorMessage } from "../services/api";
import { useToast } from "../components/Toasts";
import { ChatSkeleton } from "../components/Skeleton";
import Logo from "../components/Logo";
import { IconArrowRight } from "../components/Icons";

interface Mensaje {
  id: number;
  role: "user" | "assistant";
  content: string;
  fuentes?: { documento_id: number; documento: string }[];
}

const SUGERENCIAS = [
  "¿Qué facturas se han registrado?",
  "¿Qué contratos están vigentes?",
  "Resumen de las órdenes de compra",
  "¿Qué documentos hablan sobre facturación?",
];

const FASES_PENSANDO = [
  "Recuperando documentos…",
  "Analizando el contexto…",
  "Redactando la respuesta…",
];

let msgId = 1;

export default function Chat() {
  const [mensajes, setMensajes] = useState<Mensaje[]>([]);
  const [input, setInput] = useState("");
  const [cargando, setCargando] = useState(false);
  const logRef = useRef<HTMLDivElement>(null);
  const { error } = useToast();

  useEffect(() => {
    logRef.current?.scrollTo({ top: logRef.current.scrollHeight, behavior: "smooth" });
  }, [mensajes, cargando]);

  const enviar = async (texto: string) => {
    const pregunta = texto.trim();
    if (!pregunta || cargando) return;
    setInput("");
    setMensajes((prev) => [...prev, { id: msgId++, role: "user", content: pregunta }]);
    setCargando(true);
    try {
      const res = await api.post<RespuestaRag>("/rag/consultar", { pregunta });
      setMensajes((prev) => [
        ...prev,
        {
          id: msgId++,
          role: "assistant",
          content: res.data.respuesta,
          fuentes: res.data.fuentes.map((f) => ({ documento_id: f.documento_id, documento: f.documento })),
        },
      ]);
    } catch (err) {
      error(errorMessage(err));
    } finally {
      setCargando(false);
    }
  };

  const onSubmit = (e: FormEvent) => {
    e.preventDefault();
    void enviar(input);
  };

  const onKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      void enviar(input);
    }
  };

  return (
    <>
      <div className="page__head">
        <div>
          <h1 className="page__title">Asistente documental</h1>
          <p className="page__sub">
            Haz preguntas en lenguaje natural y obtén respuestas con sus fuentes.
          </p>
        </div>
      </div>

      {mensajes.length === 0 && !cargando ? (
        <div style={{ maxWidth: 720, margin: "0 auto" }}>
          <div className="card" style={{ padding: "1.4rem", marginBottom: "1rem", textAlign: "center" }}>
            <div className="feature__chip" style={{ margin: "0 auto 0.9rem" }}>
              <IconChatInline />
            </div>
            <h2 style={{ fontSize: "1.3rem" }}>Pregunta sobre tu base documental</h2>
            <p className="muted" style={{ maxWidth: 460, margin: "0 auto 1.2rem" }}>
              El asistente combina búsqueda semántica con generación aumentada por recuperación
              (RAG) para responder citando los documentos.
            </p>
            <div className="chips" style={{ justifyContent: "center", padding: 0 }}>
              {SUGERENCIAS.map((s) => (
                <button key={s} type="button" className="chip" onClick={() => void enviar(s)}>
                  {s}
                </button>
              ))}
            </div>
          </div>
          <div className="chat-shell" style={{ minHeight: 320 }}>
            <div className="chat-log" ref={logRef}>
              <div className="chat-bubble chat-bubble--ai">
                Hola, soy el asistente documental de SIGAD. Puedo responder consultas sobre
                las facturas, guías, órdenes de compra, contratos y actas de tu organización.
                Escribe tu pregunta para comenzar.
              </div>
            </div>
            <ChatInput value={input} onChange={setInput} onSubmit={onSubmit} onKeyDown={onKeyDown} cargando={cargando} />
          </div>
        </div>
      ) : (
        <div className="chat-shell">
          {mensajes.length === 0 ? (
            <ChatSkeleton />
          ) : (
            <>
              <div className="chat-log" ref={logRef}>
                {mensajes.map((m) => (
                  <div key={m.id} className={`chat-bubble chat-bubble--${m.role}`}>
                    {m.content}
                    {m.fuentes && m.fuentes.length > 0 && (
                      <details className="chat-sources">
                        <summary>
                          Fuentes: {m.fuentes.length} documento{m.fuentes.length !== 1 ? "s" : ""}
                        </summary>
                        <ul>
                          {m.fuentes.map((f, i) => (
                            <li key={i}>{f.documento}</li>
                          ))}
                        </ul>
                      </details>
                    )}
                  </div>
                ))}
                {cargando && (
                  <div className="chat-bubble chat-bubble--ai">
                    <AiThinking />
                  </div>
                )}
              </div>
              <ChatInput value={input} onChange={setInput} onSubmit={onSubmit} onKeyDown={onKeyDown} cargando={cargando} />
            </>
          )}
        </div>
      )}
    </>
  );
}

function IconChatInline() {
  return (
    <svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" />
      <path d="M8 9h8M8 13h5" />
    </svg>
  );
}

function AiThinking() {
  const [fase, setFase] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => setFase((f) => (f + 1) % FASES_PENSANDO.length), 2200);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="chat-thinking" role="status" aria-live="polite">
      <span className="ai-orbit" aria-hidden="true">
        <i />
        <Logo size={20} />
      </span>
      <span className="ai-status" key={fase}>
        {FASES_PENSANDO[fase]}
      </span>
      <span className="typing" aria-hidden="true">
        <span />
        <span />
        <span />
      </span>
    </div>
  );
}

interface ChatInputProps {
  value: string;
  onChange: (v: string) => void;
  onSubmit: (e: FormEvent) => void;
  onKeyDown: (e: KeyboardEvent<HTMLTextAreaElement>) => void;
  cargando: boolean;
}

function ChatInput({ value, onChange, onSubmit, onKeyDown, cargando }: ChatInputProps) {
  return (
    <div>
      <form className="chat-input" onSubmit={onSubmit}>
        <textarea
          className="input textarea"
          rows={1}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          onKeyDown={onKeyDown}
          placeholder="Escribe tu pregunta… (Enter para enviar)"
          disabled={cargando}
        />
        <button className="btn btn-primary" type="submit" disabled={cargando || !value.trim()} aria-label="Enviar pregunta">
          {cargando ? <span className="spin" /> : <IconArrowRight width={18} height={18} />}
        </button>
      </form>
    </div>
  );
}