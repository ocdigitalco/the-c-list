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
            --v2-page-bg: #FAFAF7;
            --v2-card-bg: #FFFFFF;
            --v2-sidebar-bg: #FFFFFF;
            --v2-border: #EDEAE0;
            --v2-text-primary: #0F0F0E;
            --v2-text-secondary: #6B6757;
            --v2-text-muted: #8A8677;
            --v2-text-disabled: #B7B2A3;
            --v2-text-rare: #9A2B14;
            --v2-accent: #0F0F0E;
            --v2-accent-light: #F1EFE9;
            --v2-success: #0E8A4F;
            --v2-badge-bg: #F1EFE9;
            --v2-row-alt: #FAFAF7;
            --v2-border-subtle: #F4F1E8;
            --v2-border-chip: #E6E3D9;
            --v2-hover-shadow: 0 2px 8px rgba(0,0,0,0.06);
            --v2-card-shadow: 0 1px 3px rgba(0,0,0,0.04);
            --v2-break-sheet-bg: #0F0F0E;
            --v2-break-sheet-hover-bg: #1A1A19;
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
