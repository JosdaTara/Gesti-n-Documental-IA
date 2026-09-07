import { useTheme } from "../context/ThemeContext";
import { IconMoon, IconSun } from "./Icons";

export default function ThemeToggle() {
  const { theme, toggle } = useTheme();
  return (
    <button
      type="button"
      className="icon-btn"
      onClick={toggle}
      aria-label={theme === "dark" ? "Cambiar a modo claro" : "Cambiar a modo oscuro"}
      title={theme === "dark" ? "Modo claro" : "Modo oscuro"}
    >
      {theme === "dark" ? <IconSun width={19} height={19} /> : <IconMoon width={19} height={19} />}
    </button>
  );
}