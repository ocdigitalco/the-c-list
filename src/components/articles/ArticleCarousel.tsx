"use client";

import { useState } from "react";

export function ArticleCarousel({
  slides,
}: {
  slides: Array<{
    src: string;
    caption: string;
    subcaption?: string;
  }>;
}) {
  const [index, setIndex] = useState(0);

  // On desktop show 2 at a time, mobile 1
  const perPage = typeof window !== "undefined" && window.innerWidth >= 640 ? 2 : 1;
  const maxIndex = Math.max(0, slides.length - perPage);
  const safeIndex = Math.min(index, maxIndex);

  const prev = () => setIndex(Math.max(0, safeIndex - 1));
  const next = () => setIndex(Math.min(maxIndex, safeIndex + 1));

  return (
    <div className="mb-6">
      <div className="relative">
        <div className="overflow-hidden rounded-lg border border-zinc-800">
          <div
            className="flex transition-transform duration-300 ease-out"
            style={{
              transform: `translateX(-${safeIndex * (100 / perPage)}%)`,
              width: `${(slides.length / perPage) * 100}%`,
            }}
          >
            {slides.map((slide, i) => (
              <div
                key={i}
                className="flex-shrink-0 px-1"
                style={{ width: `${100 / slides.length}%` }}
              >
                <div className="aspect-[3/4] bg-zinc-900 rounded-lg overflow-hidden">
                  <img
                    src={slide.src}
                    alt={slide.caption}
                    className="w-full h-full object-cover"
                  />
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
        {/* Arrow buttons */}
        {safeIndex > 0 && (
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
        {safeIndex < maxIndex && (
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
      {/* Dot indicators */}
      <div className="flex justify-center gap-1.5 mt-3">
        {Array.from({ length: maxIndex + 1 }).map((_, i) => (
          <button
            key={i}
            onClick={() => setIndex(i)}
            className={`w-1.5 h-1.5 rounded-full transition-colors ${
              i === safeIndex ? "bg-zinc-300" : "bg-zinc-700"
            }`}
            aria-label={`Go to slide ${i + 1}`}
          />
        ))}
      </div>
    </div>
  );
}
