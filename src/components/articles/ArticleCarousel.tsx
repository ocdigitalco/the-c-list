"use client";

import { useState, useEffect, useRef } from "react";

const GAP = 12;

export function ArticleCarousel({
  slides,
}: {
  slides: Array<{
    src: string;
    caption: string;
    subcaption?: string;
  }>;
}) {
  const [currentIdx, setCurrentIdx] = useState(0);
  const [containerWidth, setContainerWidth] = useState(0);
  const [isMobile, setIsMobile] = useState(false);
  const [failedSet, setFailedSet] = useState<Set<number>>(() => new Set());
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function measure() {
      if (containerRef.current) {
        setContainerWidth(containerRef.current.clientWidth);
      }
      setIsMobile(window.innerWidth < 640);
    }
    measure();
    window.addEventListener("resize", measure);
    return () => window.removeEventListener("resize", measure);
  }, []);

  const slideWidth = isMobile
    ? containerWidth
    : (containerWidth - GAP) / 2;
  const offset = currentIdx * (slideWidth + GAP);
  const safeIdx = Math.min(currentIdx, slides.length - 1);

  const prev = () => setCurrentIdx((i) => Math.max(0, i - 1));
  const next = () => setCurrentIdx((i) => Math.min(slides.length - 1, i + 1));

  return (
    <div className="mb-6">
      <div className="relative">
        <div
          ref={containerRef}
          className="overflow-hidden rounded-lg border border-zinc-800"
        >
          <div
            className="flex transition-transform duration-300 ease-out"
            style={{
              transform: containerWidth > 0 ? `translateX(-${offset}px)` : undefined,
              gap: `${GAP}px`,
            }}
          >
            {slides.map((slide, i) => (
              <div
                key={i}
                style={{
                  width: containerWidth > 0 ? `${slideWidth}px` : "50%",
                  flexShrink: 0,
                }}
              >
                <div className="rounded-lg overflow-hidden bg-[#2C2C2A]" style={{ aspectRatio: "2/3" }}>
                  {failedSet.has(i) ? (
                    <div className="w-full h-full flex items-center justify-center px-4">
                      <p className="text-xs text-zinc-400 text-center">{slide.caption}</p>
                    </div>
                  ) : (
                    <img
                      src={slide.src}
                      alt={slide.caption}
                      className="w-full h-full object-cover"
                      onError={() => {
                        console.error(`[ArticleCarousel] Failed to load: ${slide.src}`);
                        setFailedSet((prev) => new Set(prev).add(i));
                      }}
                    />
                  )}
                </div>
                <p className="text-xs text-zinc-400 mt-2 text-center">{slide.caption}</p>
                {slide.subcaption && (
                  <p className="text-[11px] text-zinc-600 text-center">{slide.subcaption}</p>
                )}
              </div>
            ))}
          </div>
        </div>
        {safeIdx > 0 && (
          <button
            onClick={prev}
            className="absolute left-2 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-zinc-900/80 border border-zinc-700 flex items-center justify-center text-zinc-300 hover:bg-zinc-800 transition-colors"
            aria-label="Previous"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M15 19l-7-7 7-7" />
            </svg>
          </button>
        )}
        {safeIdx < slides.length - 1 && (
          <button
            onClick={next}
            className="absolute right-2 top-1/2 -translate-y-1/2 w-8 h-8 rounded-full bg-zinc-900/80 border border-zinc-700 flex items-center justify-center text-zinc-300 hover:bg-zinc-800 transition-colors"
            aria-label="Next"
          >
            <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
            </svg>
          </button>
        )}
      </div>
      <div className="flex justify-center gap-1.5 mt-3">
        {slides.map((_, i) => (
          <button
            key={i}
            onClick={() => setCurrentIdx(i)}
            className={`w-1.5 h-1.5 rounded-full transition-colors ${
              i === safeIdx ? "bg-zinc-300" : "bg-zinc-700"
            }`}
            aria-label={`Go to slide ${i + 1}`}
          />
        ))}
      </div>
    </div>
  );
}
