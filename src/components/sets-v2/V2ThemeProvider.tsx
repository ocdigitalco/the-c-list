"use client";

import { createContext, useContext } from "react";
import type { V2Theme } from "./types";

interface ThemeCtx {
  theme: V2Theme;
  toggle: () => void;
}

const Ctx = createContext<ThemeCtx>({ theme: "light", toggle: () => {} });

export function useV2Theme() {
  return useContext(Ctx);
}

export function V2ThemeProvider({ children }: { children: React.ReactNode }) {
  return (
    <Ctx.Provider value={{ theme: "light", toggle: () => {} }}>
      {children}
    </Ctx.Provider>
  );
}
