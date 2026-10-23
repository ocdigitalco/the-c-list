import { V2ThemeWrapper } from "@/components/sets/ThemeToggle";

// On-demand ISR for the whole /sets/[id] subtree: no time-based floor. Next uses
// the MINIMUM revalidate across layout+page, so this must be false — otherwise it
// would cap the set/athlete/team pages below their own (longer) windows.
export const revalidate = false;

export default function V2Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <V2ThemeWrapper>{children}</V2ThemeWrapper>;
}
