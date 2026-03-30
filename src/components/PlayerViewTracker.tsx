"use client";

import { useEffect } from "react";

export function PlayerViewTracker({ playerId }: { playerId: number }) {
  useEffect(() => {
    fetch("/api/events", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ playerId, eventType: "view" }),
    }).catch(() => {});
  }, [playerId]);

  return null;
}
