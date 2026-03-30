import { createClient, type InValue } from "@libsql/client";
import { drizzle } from "drizzle-orm/libsql";
import * as schema from "./schema";

// Use Turso in production, local file in development
const client = createClient(
  process.env.TURSO_DATABASE_URL
    ? {
        url: process.env.TURSO_DATABASE_URL,
        authToken: process.env.TURSO_AUTH_TOKEN,
      }
    : {
        url: "file:the-c-list.db",
      }
);

export const db = drizzle(client, { schema });
export type DB = typeof db;

// Unified async interface for raw SQL queries
export const rawQuery = {
  get: async <T = Record<string, unknown>>(sql: string, ...args: (string | number | null)[]) => {
    const result = await client.execute({ sql, args: args as InValue[] });
    return result.rows[0] as T | undefined;
  },
  all: async <T = Record<string, unknown>>(sql: string, ...args: (string | number | null)[]) => {
    const result = await client.execute({ sql, args: args as InValue[] });
    return result.rows as T[];
  },
};
