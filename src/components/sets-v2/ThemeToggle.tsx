"use client";

import { createContext, useContext, useState, useEffect, useCallback } from "react";
import type { V2Theme } from "./types";

const STORAGE_KEY = "sets-v2-theme";

interface ThemeCtx {
  theme: V2Theme;
  toggle: () => void;
}

const Ctx = createContext<ThemeCtx>({ theme: "light", toggle: () => {} });

export function useV2ThemeCtx() {
  return useContext(Ctx);
}

export function V2ThemeWrapper({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<V2Theme>("light");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    const stored = localStorage.getItem(STORAGE_KEY) as V2Theme | null;
    if (stored === "dark" || stored === "light") setTheme(stored);
    setMounted(true);
  }, []);

  useEffect(() => {
    if (mounted) localStorage.setItem(STORAGE_KEY, theme);
  }, [theme, mounted]);

  const toggle = useCallback(() => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  }, []);

  return (
    <Ctx.Provider value={{ theme, toggle }}>
      <div data-v2-theme={theme} className="v2-root">
        <style>{`
          .v2-root {
            --v2-page-bg: #F4F6F9;
            --v2-card-bg: #FFFFFF;
            --v2-sidebar-bg: #FFFFFF;
            --v2-border: #E5E7EB;
            --v2-text-primary: #111827;
            --v2-text-secondary: #6B7280;
            --v2-accent: #6366F1;
            --v2-accent-light: #EEF2FF;
            --v2-success: #10B981;
            --v2-badge-bg: #F3F4F6;
            --v2-row-alt: #F9FAFB;
            --v2-hover-shadow: 0 2px 8px rgba(0,0,0,0.06);
            --v2-card-shadow: 0 1px 3px rgba(0,0,0,0.04);
          }
          .v2-root[data-v2-theme="dark"] {
            --v2-page-bg: #0F172A;
            --v2-card-bg: #1E293B;
            --v2-sidebar-bg: #1E293B;
            --v2-border: #334155;
            --v2-text-primary: #F1F5F9;
            --v2-text-secondary: #94A3B8;
            --v2-accent: #818CF8;
            --v2-accent-light: #1E1B4B;
            --v2-success: #34D399;
            --v2-badge-bg: #334155;
            --v2-row-alt: #1E293B;
            --v2-hover-shadow: 0 2px 8px rgba(0,0,0,0.3);
            --v2-card-shadow: 0 1px 3px rgba(0,0,0,0.2);
          }
          .v2-root {
            background: var(--v2-page-bg);
            color: var(--v2-text-primary);
            min-height: 100%;
          }
        `}</style>
        {children}
      </div>
    </Ctx.Provider>
  );
}

export function ThemeToggle() {
  const { theme, toggle } = useV2ThemeCtx();

  return (
    <button
      onClick={toggle}
      className="flex items-center gap-2 text-[13px] font-medium transition-colors cursor-pointer"
      style={{ color: "var(--v2-text-secondary)" }}
    >
      {theme === "light" ? (
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M21.752 15.002A9.72 9.72 0 0118 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 003 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 009.002-5.998z" />
        </svg>
      ) : (
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386l-1.591 1.591M21 12h-2.25m-.386 6.364l-1.591-1.591M12 18.75V21m-4.773-4.227l-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 11-7.5 0 3.75 3.75 0 017.5 0z" />
        </svg>
      )}
      <span>Appearance</span>
    </button>
  );
}
