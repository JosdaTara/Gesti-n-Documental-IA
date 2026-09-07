import { useId } from "react";

export default function Logo({ size = 28, className = "" }: { size?: number; className?: string }) {
  const uid = useId().replace(/[^a-zA-Z0-9]/g, "");
  const gid = `sigad-${uid}`;

  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 64 64"
      fill="none"
      className={className}
      role="img"
      aria-label="SIGAD"
    >
      <defs>
        <linearGradient id={gid} x1="0" y1="0" x2="64" y2="64" gradientUnits="userSpaceOnUse">
          <stop stopColor="#4f46e5" />
          <stop offset="1" stopColor="#0ea5e9" />
        </linearGradient>
      </defs>
      <rect x="2" y="2" width="60" height="60" rx="15" fill={`url(#${gid})`} />
      <rect x="2" y="2" width="60" height="60" rx="15" fill="none" stroke="rgba(255,255,255,0.18)" strokeWidth="1.5" />
      <path
        d="M22 19h14l9 9v15a5 5 0 0 1-5 5H22a5 5 0 0 1-5-5V24a5 5 0 0 1 5-5z"
        fill="rgba(255,255,255,0.12)"
        stroke="#fff"
        strokeWidth="3.5"
        strokeLinejoin="round"
      />
      <path d="M36 19v9h9" fill="none" stroke="#fff" strokeWidth="3.5" strokeLinejoin="round" />
      <path d="M23 36h18M23 43h11" stroke="#fff" strokeWidth="3.5" strokeLinecap="round" />
      <circle cx="47" cy="47" r="5" fill="#fff" />
      <path
        d="M47 43.4l1.1 2.55 2.55 1.1-2.55 1.1-1.1 2.55-1.1-2.55-2.55-1.1 2.55-1.1z"
        fill="#4f46e5"
      />
    </svg>
  );
}