"use client";

import { createContext, useContext, useState, useEffect, useCallback, useRef } from "react";
import type { V2Theme } from "./types";

const STORAGE_KEY = "sets-v2-theme";
const DEFAULT_THEME: V2Theme = "light";

interface ThemeCtx {
  theme: V2Theme;
  toggle: () => void;
}

const Ctx = createContext<ThemeCtx>({ theme: DEFAULT_THEME, toggle: () => {} });

export function useV2Theme() {
  return useContext(Ctx);
}

export function V2ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<V2Theme>(DEFAULT_THEME);
  const prevThemeRef = useRef<string | null>(null);

  useEffect(() => {
    // Save whatever theme was active before entering v2
    prevThemeRef.current = document.documentElement.dataset.theme ?? "dark";
    // Read stored v2 preference
    const stored = localStorage.getItem(STORAGE_KEY) as V2Theme | null;
    const t = stored === "dark" || stored === "light" ? stored : DEFAULT_THEME;
    setTheme(t);
    document.documentElement.dataset.theme = t;

    return () => {
      // Restore previous theme on unmount
      if (prevThemeRef.current) {
        document.documentElement.dataset.theme = prevThemeRef.current;
      }
    };
  }, []);

  useEffect(() => {
    document.documentElement.dataset.theme = theme;
    localStorage.setItem(STORAGE_KEY, theme);
  }, [theme]);

  const toggle = useCallback(() => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  }, []);

  return <Ctx.Provider value={{ theme, toggle }}>{children}</Ctx.Provider>;
}
