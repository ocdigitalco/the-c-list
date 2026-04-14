"use client";

import { useState } from "react";
import { getNBAHeadshotUrl } from "@/lib/nba-headshot";
import { getUFCHeadshotUrl } from "@/lib/ufc-headshot";
import { getMLBHeadshotUrl } from "@/lib/mlb-headshot";

interface Props {
  name: string;
  nbaPlayerId: number | null | undefined;
  ufcImageUrl?: string | null;
  mlbPlayerId?: number | null;
  imageUrl?: string | null;
  size?: "sm" | "lg";
}

function InitialsAvatar({ name, size }: { name: string; size: "sm" | "lg" }) {
  const initials = name
    .split(" ")
    .map((n) => n[0])
    .slice(0, 2)
    .join("")
    .toUpperCase();

  const sizeClass = size === "lg" ? "w-[120px] h-[120px] text-2xl" : "w-10 h-10 text-sm";

  return (
    <div
      className={`${sizeClass} rounded-full flex items-center justify-center font-semibold flex-shrink-0`}
      style={{ background: "var(--v2-badge-bg)", color: "var(--v2-text-secondary)" }}
    >
      {initials}
    </div>
  );
}

export function AthleteHeadshot({ name, nbaPlayerId, ufcImageUrl, mlbPlayerId, imageUrl, size = "sm" }: Props) {
  const [imgError, setImgError] = useState(false);
  const url = getNBAHeadshotUrl(nbaPlayerId) ?? getUFCHeadshotUrl(ufcImageUrl) ?? getMLBHeadshotUrl(mlbPlayerId) ?? (imageUrl || null);

  if (!url || imgError) {
    return <InitialsAvatar name={name} size={size} />;
  }

  const sizeClass = size === "lg" ? "w-[120px] h-[120px]" : "w-10 h-10";
  const borderWidth = size === "lg" ? "3px" : "2px";

  return (
    <img
      src={url}
      alt={name}
      loading="lazy"
      onError={() => setImgError(true)}
      className={`${sizeClass} rounded-full object-cover object-top flex-shrink-0`}
      style={{ border: `${borderWidth} solid var(--v2-border)` }}
    />
  );
}
