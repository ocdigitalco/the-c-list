"use client";

interface Props {
  setName: string;
  onMenuClick: () => void;
}

export function V2MobileBar({ setName, onMenuClick }: Props) {
  return (
    <div className="md:hidden sticky top-0 z-20 flex items-center gap-3 px-4 py-2.5 border-b border-zinc-800 bg-zinc-900">
      <button
        onClick={onMenuClick}
        className="shrink-0 p-1.5 rounded-lg hover:bg-zinc-800 transition-colors"
        aria-label="Open sidebar"
      >
        <svg className="w-5 h-5 text-zinc-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
          <path strokeLinecap="round" strokeLinejoin="round" d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5" />
        </svg>
      </button>
      <p className="text-sm font-semibold text-white truncate">{setName}</p>
    </div>
  );
}
