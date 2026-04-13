"use client";

import { useState, useCallback } from "react";
import { V2ThemeProvider } from "./V2ThemeProvider";
import { V2Sidebar } from "./V2Sidebar";
import { V2SidebarDrawer } from "./V2SidebarDrawer";
import { V2MobileBar } from "./V2MobileBar";
import type { SidebarPlayer, BoxFormatSummary } from "./types";

interface Props {
  setId: number;
  setSlug?: string | null;
  setName: string;
  sport: string;
  league: string | null;
  season: string;
  tier: string;
  releaseDate: string | null;
  sampleImageUrl: string | null;
  boxFormats: BoxFormatSummary[];
  players: SidebarPlayer[];
  children: React.ReactNode;
}

export function V2Shell({
  setId,
  setSlug,
  setName,
  sport,
  league,
  season,
  tier,
  releaseDate,
  sampleImageUrl,
  boxFormats,
  players,
  children,
}: Props) {
  const [drawerOpen, setDrawerOpen] = useState(false);
  const closeDrawer = useCallback(() => setDrawerOpen(false), []);

  return (
    <V2ThemeProvider>
      <div className="h-full flex flex-col overflow-hidden">
        {/* Mobile sub-header */}
        <V2MobileBar setName={setName} onMenuClick={() => setDrawerOpen(true)} />

        <div className="flex-1 flex overflow-hidden">
          {/* Desktop sidebar */}
          <aside className="hidden md:flex md:w-60 lg:w-72 shrink-0 border-r border-zinc-800 overflow-y-auto bg-zinc-900">
            <V2Sidebar
              setId={setId}
              setSlug={setSlug}
              setName={setName}
              sport={sport}
              league={league}
              season={season}
              tier={tier}
              releaseDate={releaseDate}
              sampleImageUrl={sampleImageUrl}
              boxFormats={boxFormats}
              players={players}
            />
          </aside>

          {/* Mobile drawer */}
          {drawerOpen && (
            <V2SidebarDrawer onClose={closeDrawer}>
              <V2Sidebar
                setId={setId}
                setSlug={setSlug}
                setName={setName}
                sport={sport}
                league={league}
                season={season}
                tier={tier}
                releaseDate={releaseDate}
                sampleImageUrl={sampleImageUrl}
                boxFormats={boxFormats}
                players={players}
                onNavigate={closeDrawer}
              />
            </V2SidebarDrawer>
          )}

          {/* Main content */}
          <main className="flex-1 overflow-y-auto">{children}</main>
        </div>
      </div>
    </V2ThemeProvider>
  );
}
