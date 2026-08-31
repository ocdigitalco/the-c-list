import React from "react";
import Link from "next/link";

/**
 * Shared button from the Checklist² Site Theme (.btn):
 *   variants — pri (Card Red primary), sec (ink), gho (ghost outline)
 *   sizes    — md (generic .btn: 13.5px / 10×16 / r8), sm (detail .aside .btn: 13px / 9×14 / r7)
 * Renders a <Link> when `href` is given, otherwise a <button>.
 */
type Variant = "pri" | "sec" | "gho";
type Size = "sm" | "md";

function cls(variant: Variant, size: Size, extra?: string): string {
  return `ui-btn ui-btn-${size} ui-btn-${variant}${extra ? " " + extra : ""}`;
}

type CommonProps = { variant?: Variant; size?: Size; className?: string; children: React.ReactNode };

type LinkProps = CommonProps & { href: string } & Omit<React.ComponentProps<typeof Link>, "href" | "className" | "children">;
type NativeProps = CommonProps & { href?: undefined } & Omit<React.ButtonHTMLAttributes<HTMLButtonElement>, "className" | "children">;

export function Button(props: LinkProps | NativeProps) {
  const { variant = "pri", size = "md", className, children } = props;
  const c = cls(variant, size, className);
  if (props.href !== undefined) {
    const { variant: _v, size: _s, className: _c, children: _ch, ...rest } = props as LinkProps;
    return <Link className={c} {...rest}>{children}</Link>;
  }
  const { variant: _v, size: _s, className: _c, children: _ch, ...rest } = props as NativeProps;
  return <button className={c} {...rest}>{children}</button>;
}
