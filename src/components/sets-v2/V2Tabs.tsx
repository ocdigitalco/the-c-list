"use client";

import { useState } from "react";

interface Tab {
  key: string;
  label: string;
  content: React.ReactNode;
}

interface Props {
  tabs: Tab[];
  defaultTab?: string;
}

export function V2Tabs({ tabs, defaultTab }: Props) {
  const [active, setActive] = useState(defaultTab ?? tabs[0]?.key ?? "");

  return (
    <div>
      {/* Tab bar */}
      <div className="flex gap-1 border-b border-zinc-800 overflow-x-auto">
        {tabs.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActive(tab.key)}
            className={`px-4 py-2.5 text-sm font-medium whitespace-nowrap transition-colors border-b-2 -mb-px ${
              active === tab.key
                ? "border-indigo-500 text-indigo-400"
                : "border-transparent text-zinc-500 hover:text-zinc-300"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Tab content */}
      <div className="pt-6">
        {tabs.find((t) => t.key === active)?.content}
      </div>
    </div>
  );
}
