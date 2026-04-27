/**
 * Fire a player event to /api/events.
 * Used for tracking searches and views across leaderboard components.
 * Fails silently — tracking should never break the UI.
 */
export function trackEvent(
  playerId: number,
  eventType: "search" | "view",
): void {
  fetch("/api/events", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ playerId, eventType }),
  }).catch(() => {});
}
