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
            --v2-break-sheet-bg: #111827;
            --v2-break-sheet-hover-bg: #1F2937;
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
