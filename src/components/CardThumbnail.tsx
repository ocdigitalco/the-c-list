"use client";

import { useRef, useState, useEffect } from "react";
import { createPortal } from "react-dom";

const PREVIEW_WIDTH = 220;
const PREVIEW_GAP = 10;

export function CardThumbnail({ src, alt }: { src: string; alt: string }) {
  const wrapperRef = useRef<HTMLDivElement>(null);
  const [pos, setPos] = useState<{ x: number; y: number } | null>(null);
  const [visible, setVisible] = useState(false);
  const hideTimer = useRef<ReturnType<typeof setTimeout> | null>(null);
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    return () => {
      if (hideTimer.current) clearTimeout(hideTimer.current);
    };
  }, []);

  function handleMouseEnter() {
    // Skip on touch/pointer devices that don't support true hover
    if (!window.matchMedia("(hover: hover)").matches) return;
    if (hideTimer.current) clearTimeout(hideTimer.current);
    if (!wrapperRef.current) return;

    const rect = wrapperRef.current.getBoundingClientRect();
    // Card aspect ratio ~2.5:3.5 ≈ 1:1.4
    const previewHeight = Math.round(PREVIEW_WIDTH * 1.4);

    // Prefer right of thumbnail; flip left if not enough room
    let x = rect.right + PREVIEW_GAP;
    if (x + PREVIEW_WIDTH > window.innerWidth - 8) {
      x = rect.left - PREVIEW_WIDTH - PREVIEW_GAP;
    }
    x = Math.max(8, x);

    // Align to thumbnail top; shift up if too close to bottom
    let y = rect.top;
    if (y + previewHeight > window.innerHeight - 8) {
      y = window.innerHeight - previewHeight - 8;
    }
    y = Math.max(8, y);

    setPos({ x, y });
    setVisible(true);
  }

  function handleMouseLeave() {
    setVisible(false);
    // Keep pos briefly so the fade-out transition can play
    hideTimer.current = setTimeout(() => setPos(null), 200);
  }

  return (
    <>
      <div
        ref={wrapperRef}
        onMouseEnter={handleMouseEnter}
        onMouseLeave={handleMouseLeave}
        className="w-full h-full"
      >
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img
          src={src}
          alt={alt}
          className="w-full h-full object-cover object-center"
        />
      </div>

      {mounted && pos &&
        createPortal(
          <div
            style={{
              position: "fixed",
              left: pos.x,
              top: pos.y,
              width: PREVIEW_WIDTH,
              zIndex: 9999,
              pointerEvents: "none",
              opacity: visible ? 1 : 0,
              transform: visible ? "scale(1)" : "scale(0.97)",
              transition: "opacity 150ms ease, transform 150ms ease",
            }}
            className="rounded-lg overflow-hidden shadow-2xl border border-white/10 bg-zinc-900"
          >
            {/* eslint-disable-next-line @next/next/no-img-element */}
            <img
              src={src}
              alt=""
              style={{ width: "100%", height: "auto", display: "block" }}
            />
          </div>,
          document.body
        )}
    </>
  );
}
