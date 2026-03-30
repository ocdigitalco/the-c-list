"use server";

import { db } from "@/lib/db";
import { players } from "@/lib/schema";
import { like } from "drizzle-orm";

export async function searchPlayers(query: string) {
  if (!query.trim()) {
    return db.query.players.findMany({
      orderBy: (p, { asc }) => [asc(p.name)],
    });
  }
  return db
    .select()
    .from(players)
    .where(like(players.name, `%${query}%`))
    .orderBy(players.name);
}
