"use client";

import { useEffect } from "react";

interface Props {
  onClose: () => void;
  children: React.ReactNode;
}

export function V2SidebarDrawer({ onClose, children }: Props) {
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") onClose();
    }
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  return (
    <div className="fixed inset-0 z-40 md:hidden">
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/60" onClick={onClose} />
      {/* Panel */}
      <div className="relative w-72 h-full bg-zinc-900 border-r border-zinc-800 shadow-2xl animate-slide-in-left">
        {children}
      </div>
      <style jsx>{`
        @keyframes slideInLeft {
          from { transform: translateX(-100%); }
          to { transform: translateX(0); }
        }
        .animate-slide-in-left {
          animation: slideInLeft 200ms ease-out;
        }
      `}</style>
    </div>
  );
}
