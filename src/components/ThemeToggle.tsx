"use client";

import { useEffect, useState } from "react";

type Theme = "dark" | "light";

function getStoredTheme(): Theme | null {
  try {
    const v = localStorage.getItem("theme");
    return v === "dark" || v === "light" ? v : null;
  } catch {
    return null;
  }
}

function getSystemTheme(): Theme {
  return window.matchMedia("(prefers-color-scheme: light)").matches
    ? "light"
    : "dark";
}

function applyTheme(t: Theme) {
  document.documentElement.dataset.theme = t;
}

export function ThemeToggle() {
  const [theme, setTheme] = useState<Theme>("dark");
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // Resolve the correct theme: localStorage → system preference
    const t = getStoredTheme() ?? getSystemTheme();

    // Always apply to <html data-theme="…"> on mount.
    // This is the belt-and-suspenders: the FOUC script in <head> covers the
    // initial paint, but React hydration can sometimes clear client-set
    // attributes. Reapplying here guarantees correctness.
    applyTheme(t);
    setTheme(t);
    setMounted(true);

    // Enable transitions only after the initial theme is painted.
    // Putting it in rAF means transitions won't fire during first render.
    requestAnimationFrame(() => {
      document.documentElement.classList.add("theme-ready");
    });
  }, []);

  function toggle() {
    const next: Theme = theme === "dark" ? "light" : "dark";
    applyTheme(next);
    setTheme(next);
    try {
      localStorage.setItem("theme", next);
    } catch {
      // Private browsing / storage blocked — visual toggle still works
    }
  }

  // Render a size-matched placeholder until mounted to prevent layout shift.
  // We can't render the button during SSR because we don't know the user's
  // theme preference server-side.
  if (!mounted) {
    return <div className="w-7 h-7" aria-hidden />;
  }

  return (
    <button
      onClick={toggle}
      className="p-1.5 rounded-md text-zinc-400 hover:text-zinc-200 hover:bg-zinc-800/40 transition-colors"
      aria-label={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
    >
      {theme === "dark" ? (
        /* Sun — visible in dark mode, click to go light */
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M12 3v2.25m6.364.386-1.591 1.591M21 12h-2.25m-.386 6.364-1.591-1.591M12 18.75V21m-4.773-4.227-1.591 1.591M5.25 12H3m4.227-4.773L5.636 5.636M15.75 12a3.75 3.75 0 1 1-7.5 0 3.75 3.75 0 0 1 7.5 0z" />
        </svg>
      ) : (
        /* Moon — visible in light mode, click to go dark */
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M21.752 15.002A9.718 9.718 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998z" />
        </svg>
      )}
    </button>
  );
}
