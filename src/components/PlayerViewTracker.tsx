"use client";

import { useEffect, useRef } from "react";

export function PlayerViewTracker({ playerId }: { playerId: number }) {
  const hasFired = useRef(false);

  useEffect(() => {
    if (hasFired.current) return;
    hasFired.current = true;
    fetch("/api/events", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ playerId, eventType: "view" }),
    }).catch(() => {});
  }, [playerId]);

  return null;
}
