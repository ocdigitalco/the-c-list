"use client";

import { useState, useEffect, useRef, useCallback } from "react";

const GAP = 12;

type Orientation = "portrait" | "landscape";

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
  const [orientations, setOrientations] = useState<Orientation[]>(
    () => slides.map(() => "portrait")
  );
  const [containerWidth, setContainerWidth] = useState(0);
  const [isMobile, setIsMobile] = useState(false);
  const [failedSet, setFailedSet] = useState<Set<number>>(() => new Set());
  const containerRef = useRef<HTMLDivElement>(null);

  // Measure container and detect mobile
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

  const getSlideWidth = useCallback(
    (idx: number): number => {
      if (isMobile || containerWidth === 0) return containerWidth;
      return orientations[idx] === "landscape"
        ? containerWidth
        : (containerWidth - GAP) / 2;
    },
    [orientations, containerWidth, isMobile]
  );

  const getOffsetForSlide = useCallback(
    (idx: number): number => {
      let offset = 0;
      for (let i = 0; i < idx; i++) {
        offset += getSlideWidth(i) + GAP;
      }
      return offset;
    },
    [getSlideWidth]
  );

  const safeIdx = Math.min(currentIdx, slides.length - 1);
  const offset = containerWidth > 0 ? getOffsetForSlide(safeIdx) : 0;

  const prev = () => setCurrentIdx((i) => Math.max(0, i - 1));
  const next = () => setCurrentIdx((i) => Math.min(slides.length - 1, i + 1));

  const handleLoad = (idx: number, e: React.SyntheticEvent<HTMLImageElement>) => {
    const img = e.currentTarget;
    const isLandscape = img.naturalWidth > img.naturalHeight;
    setOrientations((prev) => {
      const next = [...prev];
      next[idx] = isLandscape ? "landscape" : "portrait";
      return next;
    });
  };

  const handleError = (idx: number, src: string) => {
    console.error(`[ArticleCarousel] Failed to load: ${src}`);
    setFailedSet((prev) => {
      const next = new Set(prev);
      next.add(idx);
      return next;
    });
  };

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
              transform: `translateX(-${offset}px)`,
              gap: `${GAP}px`,
            }}
          >
            {slides.map((slide, i) => (
              <div
                key={i}
                style={{
                  width: containerWidth > 0 ? `${getSlideWidth(i)}px` : "50%",
                  flexShrink: 0,
                  transition: "width 0.2s ease",
                }}
              >
                <div
                  className="rounded-lg overflow-hidden bg-[#2C2C2A]"
                  style={{
                    aspectRatio:
                      orientations[i] === "landscape" ? "4/3" : "3/4",
                  }}
                >
                  {failedSet.has(i) ? (
                    <div className="w-full h-full flex items-center justify-center px-4">
                      <p className="text-xs text-zinc-400 text-center">
                        {slide.caption}
                      </p>
                    </div>
                  ) : (
                    <img
                      src={slide.src}
                      alt={slide.caption}
                      className="w-full h-full object-cover"
                      onLoad={(e) => handleLoad(i, e)}
                      onError={() => handleError(i, slide.src)}
                    />
                  )}
                </div>
                <p className="text-xs text-zinc-400 mt-2 text-center">
                  {slide.caption}
                </p>
                {slide.subcaption && (
                  <p className="text-[11px] text-zinc-600 text-center">
                    {slide.subcaption}
                  </p>
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
      {/* Dot indicators — one per slide */}
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
