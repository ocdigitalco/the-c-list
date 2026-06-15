type EventParams = Record<string, string | number | boolean>;

declare global {
  interface Window {
    gtag?: (command: string, eventName: string, params?: EventParams) => void;
  }
}

export function trackEvent(name: string, params: EventParams = {}): void {
  if (typeof window === "undefined") return;
  if (typeof window.gtag !== "function") return;
  try {
    window.gtag("event", name, params);
  } catch {
    // analytics must never break UX — swallow silently
  }
}
