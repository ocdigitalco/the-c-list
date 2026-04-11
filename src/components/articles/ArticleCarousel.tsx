"use client";

import { useState, useEffect, useCallback } from "react";

function Slide({
  slide,
}: {
  slide: { src: string; caption: string; subcaption?: string };
}) {
  const [failed, setFailed] = useState(false);

  return (
    <div>
      <div className="aspect-[3/4] rounded-lg overflow-hidden bg-[#2C2C2A]">
        {failed ? (
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
              setFailed(true);
            }}
          />
        )}
      </div>
      <p className="text-xs text-zinc-400 mt-2 text-center">{slide.caption}</p>
      {slide.subcaption && (
        <p className="text-[11px] text-zinc-600 text-center">
          {slide.subcaption}
        </p>
      )}
    </div>
  );
}

export function ArticleCarousel({
  slides,
}: {
  slides: Array<{
    src: string;
    caption: string;
    subcaption?: string;
  }>;
}) {
  const [page, setPage] = useState(0);
  const [perPage, setPerPage] = useState(2);

  useEffect(() => {
    function update() {
      setPerPage(window.innerWidth >= 640 ? 2 : 1);
    }
    update();
    window.addEventListener("resize", update);
    return () => window.removeEventListener("resize", update);
  }, []);

  const pageCount = Math.ceil(slides.length / perPage);
  const safePage = Math.min(page, pageCount - 1);

  const prev = useCallback(
    () => setPage((p) => Math.max(0, p - 1)),
    []
  );
  const next = useCallback(
    () => setPage((p) => Math.min(pageCount - 1, p + 1)),
    [pageCount]
  );

  // Each slide takes up (100 / perPage)% of the visible container
  const slideWidth = 100 / perPage;
  const offset = safePage * perPage * slideWidth;

  return (
    <div className="mb-6">
      <div className="relative">
        <div className="overflow-hidden rounded-lg border border-zinc-800">
          <div
            className="flex transition-transform duration-300 ease-out"
            style={{
              transform: `translateX(-${offset}%)`,
            }}
          >
            {slides.map((slide, i) => (
              <div
                key={i}
                className="flex-shrink-0 px-1 box-border"
                style={{ width: `${slideWidth}%` }}
              >
                <Slide slide={slide} />
              </div>
            ))}
          </div>
        </div>
        {safePage > 0 && (
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
        {safePage < pageCount - 1 && (
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
      {/* Dot indicators — one per page */}
      <div className="flex justify-center gap-1.5 mt-3">
        {Array.from({ length: pageCount }).map((_, i) => (
          <button
            key={i}
            onClick={() => setPage(i)}
            className={`w-1.5 h-1.5 rounded-full transition-colors ${
              i === safePage ? "bg-zinc-300" : "bg-zinc-700"
            }`}
            aria-label={`Go to page ${i + 1}`}
          />
        ))}
      </div>
    </div>
  );
}
