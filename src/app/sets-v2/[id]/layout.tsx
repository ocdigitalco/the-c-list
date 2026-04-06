import { V2ThemeWrapper } from "@/components/sets-v2/ThemeToggle";

export const dynamic = "force-dynamic";

export default function V2Layout({
  children,
}: {
  children: React.ReactNode;
}) {
  return <V2ThemeWrapper>{children}</V2ThemeWrapper>;
}
