import { useEffect, useState } from "react";
import { IconArrowRight } from "./Icons";

export default function CtaScroll() {
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const handle = () => {
      const y = window.scrollY;
      const hero = document.getElementById("inicio");
      const heroBottom = hero ? hero.offsetHeight * 0.7 : 700;
      setVisible(y > heroBottom && y < (document.body.scrollHeight - window.innerHeight - 300));
    };
    handle();
    window.addEventListener("scroll", handle, { passive: true });
    return () => window.removeEventListener("scroll", handle);
  }, []);

  return (
    <a
      href="#inicio"
      className={`cta-scroll ${visible ? "is-visible" : ""}`}
      aria-hidden={!visible}
    >
      Conoce el sistema
      <IconArrowRight width={16} height={16} />
    </a>
  );
}