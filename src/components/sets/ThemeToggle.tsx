"use client";

import { createContext, useContext } from "react";
import type { V2Theme } from "./types";

interface ThemeCtx {
  theme: V2Theme;
  toggle: () => void;
}

const Ctx = createContext<ThemeCtx>({ theme: "light", toggle: () => {} });

export function useV2ThemeCtx() {
  return useContext(Ctx);
}

export function V2ThemeWrapper({ children }: { children: React.ReactNode }) {
  return (
    <Ctx.Provider value={{ theme: "light", toggle: () => {} }}>
      <div className="v2-root">
        <style>{`
          .v2-root {
            --v2-page-bg: var(--brand-page);
            --v2-card-bg: var(--brand-card);
            --v2-sidebar-bg: var(--brand-card);
            --v2-border: var(--brand-line);
            --v2-text-primary: var(--brand-ink);
            --v2-text-secondary: var(--brand-slate);
            --v2-text-muted: var(--brand-slate);
            --v2-text-disabled: var(--brand-fog);
            --v2-text-rare: var(--brand-accent-deep);
            --v2-accent: var(--brand-ink);
            --v2-accent-light: var(--brand-track);
            --v2-success: var(--brand-ok);
            --v2-badge-bg: var(--brand-track);
            --v2-row-alt: var(--brand-page);
            --v2-border-subtle: var(--brand-line);
            --v2-border-chip: var(--brand-line);
            --v2-hover-shadow: 0 2px 8px rgba(0,0,0,0.06);
            --v2-card-shadow: 0 1px 3px rgba(0,0,0,0.04);
            --v2-break-sheet-bg: var(--brand-ink);
            --v2-break-sheet-hover-bg: var(--brand-ink);
            background: var(--v2-page-bg);
            color: var(--v2-text-primary);
            height: 100%;
            overflow-y: auto;
          }
        `}</style>
        {children}
      </div>
    </Ctx.Provider>
  );
}

export function ThemeToggle() {
  return null;
}
