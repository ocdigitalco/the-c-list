import { db, rawQuery } from "@/lib/db";
import { sets } from "@/lib/schema";
import type { Metadata } from "next";
import { SetsCoverageClient } from "./SetsCoverageClient";

export const revalidate = 3600;

export const metadata: Metadata = {
  title: "Sets Coverage — Checklist2",
  description: "Coverage tracker for all trading card sets across Topps, Panini, and more.",
};

// ---------------------------------------------------------------------------
// Manufacturer detection
// ---------------------------------------------------------------------------

const TOPPS_PREFIXES = [
  "topps", "bowman", "finest", "chrome", "stadium club", "heritage",
  "dynasty", "tribute", "museum", "sterling", "inception", "luminaries",
  "definitive", "diamond icons", "gilded", "pristine", "tier one",
  "transcendent", "five star", "midnight", "cosmic chrome", "royalty",
  "knockout", "archives", "complete sets", "holiday", "brooklyn",
  "collector kit", "pro debut", "gold label", "graphite", "big league",
  "merlin", "gpk", "garbage pail", "wacky", "worst of", "marvel",
  "star wars", "disney", "spongebob", "pixar", "deadpool", "x-men",
  "veefriends", "stranger things", "dune", "bob ross",
];

const PANINI_PREFIXES = [
  "panini", "select", "prizm", "donruss", "contenders", "mosaic",
  "hoops", "national treasures", "immaculate", "flawless", "optic",
  "spectra", "revolution", "obsidian", "court kings", "noir",
  "chronicles", "absolute", "certified", "elite", "prestige",
  "score", "classics", "playoff", "crown royale",
];

function inferManufacturer(name: string): "Topps" | "Panini" | "Other" {
  const lower = name.toLowerCase();
  // Strip leading year/season prefix to get to the brand word
  const stripped = lower.replace(/^\d{4}[/-]?\d{0,2}\s+/, "");

  for (const prefix of PANINI_PREFIXES) {
    if (stripped.startsWith(prefix)) return "Panini";
    if (lower.includes(prefix)) return "Panini";
  }
  for (const prefix of TOPPS_PREFIXES) {
    if (stripped.startsWith(prefix)) return "Topps";
    if (lower.includes(prefix)) return "Topps";
  }
  return "Other";
}

// ---------------------------------------------------------------------------
// Static catalog — { name, year, sport }
// These are known sets from manufacturer product lists, whether or not they
// are in the database yet.
// ---------------------------------------------------------------------------
const CATALOG: Array<{ name: string; year: number; sport: string }> = [
  // ── 2026 ──────────────────────────────────────────────────────────────────
  { name: "2025-26 Bowman Basketball",                                     year: 2026, sport: "Basketball" },
  { name: "2025-26 Topps Cosmic Chrome Basketball",                        year: 2026, sport: "Basketball" },
  { name: "2025 Bowman's Best Baseball",                                   year: 2026, sport: "Baseball" },
  { name: "2025 Bowman Draft Baseball Sapphire Edition",                   year: 2026, sport: "Baseball" },
  { name: "2026 Topps Brooklyn Collection",                                year: 2026, sport: "Baseball" },
  { name: "2025-26 Topps Chrome Sapphire Basketball",                      year: 2026, sport: "Basketball" },
  { name: "2025-26 Topps Chrome Cactus Jack Basketball",                   year: 2026, sport: "Basketball" },
  { name: "2025 Topps Chrome Deadpool",                                    year: 2026, sport: "Entertainment" },
  { name: "2025 Topps Chrome Formula 1 Sapphire Edition",                  year: 2026, sport: "Racing" },
  { name: "2025 Topps Chrome McDonald's All-American Basketball",          year: 2026, sport: "Basketball" },
  { name: "2026 Topps Chrome U.S. Winter Olympics & Paralympic Team Hopefuls", year: 2026, sport: "Other" },
  { name: "2026 Topps Collector Kit",                                      year: 2026, sport: "Baseball" },
  { name: "2026 Topps Disney Neon",                                        year: 2026, sport: "Entertainment" },
  { name: "2025 Topps Disneyland 70th Anniversary",                        year: 2026, sport: "Entertainment" },
  { name: "2025-26 Topps Finest Basketball",                               year: 2026, sport: "Basketball" },
  { name: "2026 Topps Finest Fantastic Four",                              year: 2026, sport: "Entertainment" },
  { name: "2026 Topps Finest Premier League",                              year: 2026, sport: "Soccer" },
  { name: "2026 Topps Heritage Baseball",                                  year: 2026, sport: "Baseball" },
  { name: "2025 Topps Marvel Studios Chrome Sapphire",                     year: 2026, sport: "Entertainment" },
  { name: "2025 Topps Marvel The Collector",                               year: 2026, sport: "Entertainment" },
  { name: "2025 Topps Museum Collection Baseball",                         year: 2026, sport: "Baseball" },
  { name: "2025 Topps Royalty UFC",                                        year: 2026, sport: "MMA" },
  { name: "2026 Topps Series 1 Baseball",                                  year: 2026, sport: "Baseball" },
  { name: "2025 Topps Stadium Club Baseball",                              year: 2026, sport: "Baseball" },
  { name: "2025 Topps Star Wars Smugglers Outpost",                        year: 2026, sport: "Entertainment" },
  { name: "2025-26 Topps Three Basketball",                                year: 2026, sport: "Basketball" },
  { name: "2025 Topps Universe WWE",                                       year: 2026, sport: "Wrestling" },

  // ── 2025 ──────────────────────────────────────────────────────────────────
  { name: "2025 Bowman Baseball",                                          year: 2025, sport: "Baseball" },
  { name: "2025 Bowman Baseball Sapphire",                                 year: 2025, sport: "Baseball" },
  { name: "2025 Bowman Mega Box Baseball",                                 year: 2025, sport: "Baseball" },
  { name: "2025 Bowman Chrome Baseball",                                   year: 2025, sport: "Baseball" },
  { name: "2025 Bowman Chrome Baseball Mega Box",                          year: 2025, sport: "Baseball" },
  { name: "2025 Bowman Chrome Baseball Sapphire Edition",                  year: 2025, sport: "Baseball" },
  { name: "2025 Bowman Draft Baseball",                                    year: 2025, sport: "Baseball" },
  { name: "2025 Bowman Draft Baseball Mega Box",                           year: 2025, sport: "Baseball" },
  { name: "2024/25 Bowman University Best Basketball",                     year: 2025, sport: "Basketball" },
  { name: "2024 Bowman University Best Football",                          year: 2025, sport: "Football" },
  { name: "2024/25 Bowman University Chrome Basketball",                   year: 2025, sport: "Basketball" },
  { name: "2024-25 Bowman University Chrome Basketball Sapphire",          year: 2025, sport: "Basketball" },
  { name: "2025 Bowman University Chrome Football",                        year: 2025, sport: "Football" },
  { name: "2025 Pixar Gold",                                               year: 2025, sport: "Entertainment" },
  { name: "2024 Topps Archives Baseball",                                  year: 2025, sport: "Baseball" },
  { name: "2025 Topps Archives Signature Series Active Player Edition",    year: 2025, sport: "Baseball" },
  { name: "2025-26 Topps Basketball",                                      year: 2025, sport: "Basketball" },
  { name: "2025 Topps Chrome Baseball",                                    year: 2025, sport: "Baseball" },
  { name: "2025 Topps Chrome Baseball Logofractor Edition",                year: 2025, sport: "Baseball" },
  { name: "2025 Topps Chrome Baseball Sapphire Edition",                   year: 2025, sport: "Baseball" },
  { name: "2025 Topps Chrome Baseball Update Series",                      year: 2025, sport: "Baseball" },
  { name: "2025-26 Topps Chrome Basketball",                               year: 2025, sport: "Basketball" },
  { name: "2024/25 Topps Chrome Basketball",                               year: 2025, sport: "Basketball" },
  { name: "2025 Topps Chrome Basketball Sapphire",                         year: 2025, sport: "Basketball" },
  { name: "2025 Topps Chrome Black Baseball",                              year: 2025, sport: "Baseball" },
  { name: "2024 Topps Chrome Black Star Wars",                             year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Chrome Bundesliga",                                  year: 2025, sport: "Soccer" },
  { name: "2025 Topps x Bob Ross The Joy of Baseball",                     year: 2025, sport: "Baseball" },
  { name: "2025 Topps Chrome Sapphire Bundesliga",                         year: 2025, sport: "Soccer" },
  { name: "2025 Topps Chrome Disney",                                      year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Chrome Disney Sapphire",                             year: 2025, sport: "Entertainment" },
  { name: "2024 Topps Chrome Football",                                    year: 2025, sport: "Football" },
  { name: "2024 Topps Chrome Football Sapphire Edition",                   year: 2025, sport: "Football" },
  { name: "2025 Topps Chrome Formula 1",                                   year: 2025, sport: "Racing" },
  { name: "2024 Topps Chrome Sapphire Formula 1",                          year: 2025, sport: "Racing" },
  { name: "2024 Topps Chrome Sapphire Garbage Pail Kids",                  year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Chrome Spongebob 25th Anniversary",                  year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Chrome Spongebob 25th Anniversary Sapphire",         year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Chrome Star Wars",                                   year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Chrome Star Wars Costco",                            year: 2025, sport: "Entertainment" },
  { name: "2025 Chrome Star Wars Galaxy",                                  year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Chrome Star Wars The National",                      year: 2025, sport: "Entertainment" },
  { name: "2024 Topps Chrome Boxing",                                      year: 2025, sport: "Boxing" },
  { name: "2024/25 Topps Chrome UEFA Club Competitions",                   year: 2025, sport: "Soccer" },
  { name: "2024/25 Topps Chrome UEFA Club Competitions Sapphire Edition",  year: 2025, sport: "Soccer" },
  { name: "2025 Topps Chrome UFC",                                         year: 2025, sport: "MMA" },
  { name: "2025 Topps Chrome UFC Sapphire Edition",                        year: 2025, sport: "MMA" },
  { name: "2025 Topps Chrome VeeFriends",                                  year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Chrome WWE x Cactus Jack",                           year: 2025, sport: "Wrestling" },
  { name: "2025 Topps Complete Sets Baseball",                             year: 2025, sport: "Baseball" },
  { name: "2024 Topps Cosmic Chrome Football",                             year: 2025, sport: "Football" },
  { name: "2024 Topps Definitive Baseball",                                year: 2025, sport: "Baseball" },
  { name: "2025 Topps Diamond Icons Baseball",                             year: 2025, sport: "Baseball" },
  { name: "2024 Topps Diamond Icons Baseball",                             year: 2025, sport: "Baseball" },
  { name: "2025 Topps Disney Wonder",                                      year: 2025, sport: "Entertainment" },
  { name: "2024 Topps Dune Chrome",                                        year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Dynamic Duals Baseball",                             year: 2025, sport: "Baseball" },
  { name: "2024 Topps Dynasty Baseball",                                   year: 2025, sport: "Baseball" },
  { name: "2025 Topps Dynasty Formula 1",                                  year: 2025, sport: "Racing" },
  { name: "2024 Topps Dynasty Formula 1",                                  year: 2025, sport: "Racing" },
  { name: "2025 Topps Finest Baseball",                                    year: 2025, sport: "Baseball" },
  { name: "2024/25 Topps Finest Basketball",                               year: 2025, sport: "Basketball" },
  { name: "2024 Topps Finest Football",                                    year: 2025, sport: "Football" },
  { name: "2024 Topps Finest Formula 1",                                   year: 2025, sport: "Racing" },
  { name: "2025 Topps Formula 1 Fanatics Fest Exclusive",                  year: 2025, sport: "Racing" },
  { name: "2024 Topps Finest MLS",                                         year: 2025, sport: "Soccer" },
  { name: "2024-2025 Topps Finest UCC",                                    year: 2025, sport: "Soccer" },
  { name: "2024 Topps Finest UFC",                                         year: 2025, sport: "MMA" },
  { name: "2025 Topps Finest X-Men 97",                                    year: 2025, sport: "Entertainment" },
  { name: "2024 Topps Garbage Pail Kids Chrome 7 Hobby",                   year: 2025, sport: "Entertainment" },
  { name: "2024 Topps Garbage Pail Kids Chrome 7 Retail",                  year: 2025, sport: "Entertainment" },
  { name: "2024 GPK Battle of the Bands Green Day",                        year: 2025, sport: "Entertainment" },
  { name: "2024/25 Topps G-League Basketball",                             year: 2025, sport: "Basketball" },
  { name: "2025 Topps Heritage Baseball",                                  year: 2025, sport: "Baseball" },
  { name: "2024 Topps Heritage High Number",                               year: 2025, sport: "Baseball" },
  { name: "2024 Topps High-Tek Stranger Things",                           year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Holiday Baseball",                                   year: 2025, sport: "Baseball" },
  { name: "2025-26 Topps Holiday Basketball",                              year: 2025, sport: "Basketball" },
  { name: "2024 Topps Inception Baseball",                                 year: 2025, sport: "Baseball" },
  { name: "2024/25 Topps Inception Basketball",                            year: 2025, sport: "Basketball" },
  { name: "2024 Topps Inception Football",                                 year: 2025, sport: "Football" },
  { name: "2025 Topps Knockout UFC",                                       year: 2025, sport: "MMA" },
  { name: "2024 Topps Luminaries Baseball",                                year: 2025, sport: "Baseball" },
  { name: "2025 Marvel Comic Book Heroes 1975 Anniversary",                year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Marvel Comics Chrome",                               year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Marvel Comics Chrome Sapphire",                      year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Marvel Studios Chrome",                              year: 2025, sport: "Entertainment" },
  { name: "2024 Topps Masterwork Star Wars",                               year: 2025, sport: "Entertainment" },
  { name: "2024 Topps McDonald's All American Chrome",                     year: 2025, sport: "Basketball" },
  { name: "2025-26 Topps Midnight Basketball",                             year: 2025, sport: "Basketball" },
  { name: "2024-25 Topps Midnight Bundesliga",                             year: 2025, sport: "Soccer" },
  { name: "2024 Topps Midnight Football",                                  year: 2025, sport: "Football" },
  { name: "2025 Topps Midnight UFC",                                       year: 2025, sport: "MMA" },
  { name: "2025 Topps Mint Disney",                                        year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Mint Marvel",                                        year: 2025, sport: "Entertainment" },
  { name: "2025 Topps MLB Dynamic Duals",                                  year: 2025, sport: "Baseball" },
  { name: "2024 Topps MLS Chrome Sapphire Edition",                        year: 2025, sport: "Soccer" },
  { name: "2023-24 Topps Motif Basketball",                                year: 2025, sport: "Basketball" },
  { name: "2024/25 Topps NBL Chrome Basketball",                           year: 2025, sport: "Basketball" },
  { name: "2024-25 Topps NHL Sticker Collection",                          year: 2025, sport: "Other" },
  { name: "2024 Topps NOW Football Rookie Campaign",                       year: 2025, sport: "Football" },
  { name: "2025/26 Topps Premier League",                                  year: 2025, sport: "Soccer" },
  { name: "2025 Topps Pro Debut Baseball",                                 year: 2025, sport: "Baseball" },
  { name: "2024 Topps Resurgence Football",                                year: 2025, sport: "Football" },
  { name: "2024-25 Topps Reverence UCC",                                   year: 2025, sport: "Soccer" },
  { name: "2023/24 Topps Royalty Basketball",                              year: 2025, sport: "Basketball" },
  { name: "2024 Topps Royalty Tennis",                                     year: 2025, sport: "Other" },
  { name: "2024 Topps Royalty UFC",                                        year: 2025, sport: "MMA" },
  { name: "2025 Topps Series 1 Baseball",                                  year: 2025, sport: "Baseball" },
  { name: "2025 Topps Series 1 Mega Celebration",                         year: 2025, sport: "Baseball" },
  { name: "2025 Topps Series 2 Baseball",                                  year: 2025, sport: "Baseball" },
  { name: "2025 Topps Welcome to the Club",                                year: 2025, sport: "Baseball" },
  { name: "2024 Topps Signature Class Football",                           year: 2025, sport: "Football" },
  { name: "2025 Topps Stadium Club UFC",                                   year: 2025, sport: "MMA" },
  { name: "2024 Topps Star Wars Galactic Antiquities",                     year: 2025, sport: "Entertainment" },
  { name: "2024 Topps Star Wars High-Tek",                                 year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Star Wars Hyperspace",                               year: 2025, sport: "Entertainment" },
  { name: "2024 Topps Star Wars Hyperspace",                               year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Star Wars Meiyo",                                    year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Sterling Baseball",                                  year: 2025, sport: "Baseball" },
  { name: "2023-24 Topps Three Basketball",                                year: 2025, sport: "Basketball" },
  { name: "2025 Topps Tier One Baseball",                                  year: 2025, sport: "Baseball" },
  { name: "2025 Topps Tribute Baseball",                                   year: 2025, sport: "Baseball" },
  { name: "2025 Topps Baseball Update Series",                             year: 2025, sport: "Baseball" },
  { name: "2025 Topps Wacky Packages All New Series",                      year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Wacky Packages All New Series Halloween Edition",    year: 2025, sport: "Entertainment" },
  { name: "2025 Topps WWE Chrome",                                         year: 2025, sport: "Wrestling" },
  { name: "2025 Topps Chrome Sapphire WWE",                                year: 2025, sport: "Wrestling" },
  { name: "2025 Worst of Garbage Pail Kids 40th Anniversary",              year: 2025, sport: "Entertainment" },
  { name: "2025 Topps Finest WWE",                                         year: 2025, sport: "Wrestling" },

  // ── 2024 ──────────────────────────────────────────────────────────────────
  { name: "2024 Topps Baseball Series 1",                                  year: 2024, sport: "Baseball" },
  { name: "2024 Topps Baseball Series 2",                                  year: 2024, sport: "Baseball" },
  { name: "2024 Topps Allen & Ginter Baseball",                            year: 2024, sport: "Baseball" },
  { name: "2024 Topps Allen & Ginter X",                                   year: 2024, sport: "Baseball" },
  { name: "2024 Topps Baseball Holiday Mega Box",                          year: 2024, sport: "Baseball" },
  { name: "2024 Topps Baseball Holiday Advent Calendar",                   year: 2024, sport: "Baseball" },
  { name: "2024 Bowman Baseball",                                          year: 2024, sport: "Baseball" },
  { name: "2024 Bowman Baseball Sapphire Edition",                         year: 2024, sport: "Baseball" },
  { name: "2024 Bowman's Best Baseball",                                   year: 2024, sport: "Baseball" },
  { name: "2024 Bowman Chrome Baseball",                                   year: 2024, sport: "Baseball" },
  { name: "2024 Bowman Chrome Baseball Mega Box",                          year: 2024, sport: "Baseball" },
  { name: "2023 Bowman Draft Baseball Sapphire Edition",                   year: 2024, sport: "Baseball" },
  { name: "2024 Bowman Draft Baseball",                                    year: 2024, sport: "Baseball" },
  { name: "2024 Bowman Draft Baseball Sapphire Edition",                   year: 2024, sport: "Baseball" },
  { name: "2023 Bowman Inception Baseball",                                year: 2024, sport: "Baseball" },
  { name: "2024 Bowman Mega Box Baseball",                                 year: 2024, sport: "Baseball" },
  { name: "2024 Bowman Sterling Baseball",                                 year: 2024, sport: "Baseball" },
  { name: "2023 Bowman University Best Football",                          year: 2024, sport: "Football" },
  { name: "2023-24 Bowman University Chrome Basketball",                   year: 2024, sport: "Basketball" },
  { name: "2024 Bowman University Chrome Football",                        year: 2024, sport: "Football" },
  { name: "2024 Bowman University Chrome Football Sapphire Edition",       year: 2024, sport: "Football" },
  { name: "2024 Bowman U Best Basketball",                                 year: 2024, sport: "Basketball" },
  { name: "2024 Complete Sets Baseball",                                   year: 2024, sport: "Baseball" },
  { name: "2024 Topps Cosmic Chrome Baseball",                             year: 2024, sport: "Baseball" },
  { name: "2023-24 Topps Cosmic Chrome Basketball",                        year: 2024, sport: "Basketball" },
  { name: "2024 Cosmic Chrome X Cactus Jack",                              year: 2024, sport: "Basketball" },
  { name: "2024 National Silver Pack Checklist",                           year: 2024, sport: "Other" },
  { name: "2024 Topps Brooklyn Collection Baseball",                       year: 2024, sport: "Baseball" },
  { name: "2023/24 Topps Chrome NBL",                                      year: 2024, sport: "Basketball" },
  { name: "2024 Topps Chrome Baseball",                                    year: 2024, sport: "Baseball" },
  { name: "2024 Topps Chrome Baseball FFNYC",                              year: 2024, sport: "Baseball" },
  { name: "2024 Topps Chrome Baseball Sapphire Edition",                   year: 2024, sport: "Baseball" },
  { name: "2023-24 Topps Chrome Basketball Hobby",                         year: 2024, sport: "Basketball" },
  { name: "2023-24 Topps Chrome Basketball Retail",                        year: 2024, sport: "Basketball" },
  { name: "2023-24 Topps Chrome Basketball Sapphire Edition",              year: 2024, sport: "Basketball" },
  { name: "2023-24 Topps Chrome Bundesliga",                               year: 2024, sport: "Soccer" },
  { name: "2024 Topps Chrome Baseball Logofractor Edition",                year: 2024, sport: "Baseball" },
  { name: "2024 Topps Chrome Formula 1",                                   year: 2024, sport: "Racing" },
  { name: "2024 Topps Chrome Tennis",                                      year: 2024, sport: "Other" },
  { name: "2024 Topps Chrome Tennis Sapphire Edition",                     year: 2024, sport: "Other" },
  { name: "2024 Topps Chrome UFC",                                         year: 2024, sport: "MMA" },
  { name: "2023-24 Topps Chrome UEFA Club Competitions",                   year: 2024, sport: "Soccer" },
  { name: "2023-24 Topps Chrome UEFA Club Competitions Sapphire Edition",  year: 2024, sport: "Soccer" },
  { name: "2024 Topps Chrome UEFA EURO",                                   year: 2024, sport: "Soccer" },
  { name: "2024 Topps Chrome UEFA EURO Sapphire Edition",                  year: 2024, sport: "Soccer" },
  { name: "2024 Topps Chrome UEFA Women's Champions League Sapphire Edition", year: 2024, sport: "Soccer" },
  { name: "2024 Topps Chrome Update Series Baseball",                      year: 2024, sport: "Baseball" },
  { name: "2024 Topps Chrome Updates Baseball Sapphire Edition",           year: 2024, sport: "Baseball" },
  { name: "2024 Topps Chrome U.S. Olympic & Paralympic Team Hopefuls",     year: 2024, sport: "Other" },
  { name: "2023-24 Topps Chrome UWCL",                                     year: 2024, sport: "Soccer" },
  { name: "2023-24 Topps Finest Basketball",                               year: 2024, sport: "Basketball" },
  { name: "2024 GPK Series 1",                                             year: 2024, sport: "Entertainment" },
  { name: "2023/24 Topps G League Basketball",                             year: 2024, sport: "Basketball" },
  { name: "2024 Topps Gilded Collection Baseball",                         year: 2024, sport: "Baseball" },
  { name: "2024 Topps Gold Label UFC",                                     year: 2024, sport: "MMA" },
  { name: "2024 Topps Graphite Tennis",                                    year: 2024, sport: "Other" },
  { name: "2024 Topps Heritage Baseball",                                  year: 2024, sport: "Baseball" },
  { name: "2024 Topps Heritage Mini Edition",                              year: 2024, sport: "Baseball" },
  { name: "2024 Topps Knockout UFC",                                       year: 2024, sport: "MMA" },
  { name: "2023 Topps Luminaries Baseball",                                year: 2024, sport: "Baseball" },
  { name: "2023-24 Topps Midnight Basketball",                             year: 2024, sport: "Basketball" },
  { name: "2023-24 Topps Mercury Victor Wembanyama",                       year: 2024, sport: "Basketball" },
  { name: "2024 MLB Topps NOW",                                            year: 2024, sport: "Baseball" },
  { name: "2024 Topps MLS Chrome Hobby",                                   year: 2024, sport: "Soccer" },
  { name: "2024 Topps MLS Chrome Mania",                                   year: 2024, sport: "Soccer" },
  { name: "2024 Topps MLS Superstars",                                     year: 2024, sport: "Soccer" },
  { name: "2024 Topps Midnight UFC",                                       year: 2024, sport: "MMA" },
  { name: "2023 Topps Motif Football",                                     year: 2024, sport: "Football" },
  { name: "2024 Topps Museum Collection Baseball",                         year: 2024, sport: "Baseball" },
  { name: "2023-24 Topps Museum Collection UEFA Champions League",         year: 2024, sport: "Soccer" },
  { name: "2024 Topps UFC NYC",                                            year: 2024, sport: "MMA" },
  { name: "2023-24 Topps NBL",                                             year: 2024, sport: "Basketball" },
  { name: "2024 Olympics Games Topps NOW",                                 year: 2024, sport: "Other" },
  { name: "2023/24 Topps Overtime Elite Chrome",                           year: 2024, sport: "Basketball" },
  { name: "2024 Topps Paddock Pass Formula 1",                             year: 2024, sport: "Racing" },
  { name: "2024 Topps Pristine Baseball",                                  year: 2024, sport: "Baseball" },
  { name: "Topps Pristine Road to UEFA EURO 2024",                         year: 2024, sport: "Soccer" },
  { name: "2024 Topps Pro Debut Baseball",                                 year: 2024, sport: "Baseball" },
  { name: "2024 Topps 50/50 Shohei Ohtani",                               year: 2024, sport: "Baseball" },
  { name: "2023 Topps Stadium Club Baseball",                              year: 2024, sport: "Baseball" },
  { name: "2024 Topps Stadium Club Baseball",                              year: 2024, sport: "Baseball" },
  { name: "2024 Topps Stadium Club Chrome UEFA Champions League",          year: 2024, sport: "Soccer" },
  { name: "2024 Topps Star Wars Chrome",                                   year: 2024, sport: "Entertainment" },
  { name: "2024 Topps Star Wars Chrome Galaxy",                            year: 2024, sport: "Entertainment" },
  { name: "2024 Topps Star Wars Chrome Sapphire",                          year: 2024, sport: "Entertainment" },
  { name: "2024 Topps Sterling Baseball",                                  year: 2024, sport: "Baseball" },
  { name: "2024 Topps Tier One Baseball",                                  year: 2024, sport: "Baseball" },
  { name: "2024 Topps Tribute Baseball",                                   year: 2024, sport: "Baseball" },
  { name: "2024 Topps Triple Threads Baseball",                            year: 2024, sport: "Baseball" },
  { name: "2023 Topps Transcendent Collection Baseball",                   year: 2024, sport: "Baseball" },
  { name: "2024 Topps Transcendent Baseball",                              year: 2024, sport: "Baseball" },
  { name: "2024 Topps Transcendent VIP Baseball",                          year: 2024, sport: "Baseball" },
  { name: "2023-24 Topps UCC Merlin",                                      year: 2024, sport: "Soccer" },
  { name: "2022-23 Topps UCL Dynasty",                                     year: 2024, sport: "Soccer" },
  { name: "2023/24 Topps UEFA Club Competitions",                          year: 2024, sport: "Soccer" },
  { name: "2024-25 Topps UEFA Club Competitions",                          year: 2024, sport: "Soccer" },
  { name: "2024 Topps Baseball Update Series",                             year: 2024, sport: "Baseball" },
  { name: "2024 Topps Archives Signature Series Active Player Edition",    year: 2024, sport: "Baseball" },
  { name: "2024 Topps Archives Signature Series Retired Player Edition",   year: 2024, sport: "Baseball" },
  { name: "2024 Topps Big League Baseball",                                year: 2024, sport: "Baseball" },
  { name: "2024 Topps Chrome Black Baseball",                              year: 2024, sport: "Baseball" },
  { name: "2023 Topps Chrome Platinum '54 Baseball",                       year: 2024, sport: "Baseball" },
  { name: "2023 Topps Composite Football",                                 year: 2024, sport: "Football" },
  { name: "2023 Topps Diamond Icons Baseball",                             year: 2024, sport: "Baseball" },
  { name: "2023 Topps Dynasty Baseball",                                   year: 2024, sport: "Baseball" },
  { name: "2024 Topps Five Star Baseball",                                 year: 2024, sport: "Baseball" },
  { name: "2024 Topps Finest Baseball",                                    year: 2024, sport: "Baseball" },
  { name: "2023 Topps Finest MLS",                                         year: 2024, sport: "Soccer" },
  { name: "Topps Finest Road to EURO 2024",                                year: 2024, sport: "Soccer" },
  { name: "2023/24 Topps Finest UEFA Club Competitions",                   year: 2024, sport: "Soccer" },
  { name: "2023 Topps Five Star Baseball",                                 year: 2024, sport: "Baseball" },
  { name: "2023 Topps Formula 1 Chrome",                                   year: 2024, sport: "Racing" },
  { name: "2023 Topps Formula 1 Chrome Sapphire Edition",                  year: 2024, sport: "Racing" },
  { name: "2023 Topps Formula 1 Dynasty",                                  year: 2024, sport: "Racing" },
  { name: "2024 Topps NOW Football",                                       year: 2024, sport: "Football" },
  { name: "2024 Topps 206 Baseball",                                       year: 2024, sport: "Baseball" },
  { name: "2024 Topps x Lids",                                             year: 2024, sport: "Baseball" },
];

// ---------------------------------------------------------------------------
// Name normalization for fuzzy matching
// ---------------------------------------------------------------------------

function normalize(s: string): string {
  return s
    .toLowerCase()
    .replace(/[®™©'''\u2018\u2019]/g, "")
    .replace(/\bformula\s+one\b/g, "f1")
    .replace(/\bformula\s+1\b/g, "f1")
    .replace(/\s*&\s*/g, " and ")
    .replace(/\bedition\b/g, "")
    .replace(/\s+/g, " ")
    .trim();
}

function sortedTokens(norm: string): string {
  return norm.split(" ").filter(Boolean).sort().join(" ");
}

// ---------------------------------------------------------------------------
// Shared row type passed to the client component
// ---------------------------------------------------------------------------

export interface CoverageRow {
  name: string;
  year: number;
  sport: string;
  manufacturer: "Topps" | "Panini" | "Other";
  matchedSetId: number | null;
  matchedSetSlug: string | null;
  hasChecklist: boolean;
  hasBoxConfig: boolean;
  hasPackOdds: boolean;
  hasParallels: boolean;
  releaseDate: string | null;
}

// ---------------------------------------------------------------------------
// Page (server component)
// ---------------------------------------------------------------------------

export default async function SetsCoveragePage() {
  // Fetch hidden set IDs (is_visible column may not exist on Turso yet)
  let hiddenSetIds = new Set<number>();
  try {
    const hidden = await rawQuery.all<{ id: number }>("SELECT id FROM sets WHERE is_visible = 0");
    hiddenSetIds = new Set(hidden.map((r) => r.id));
  } catch { /* is_visible column may not exist yet */ }

  const allSets = (await db.select().from(sets)).filter((s) => !hiddenSetIds.has(s.id));

  // Query which sets have at least one parallel
  const setsWithParallelsRows = await rawQuery.all<{ id: number }>(
    `SELECT DISTINCT s.id FROM sets s
     JOIN insert_sets i ON i.set_id = s.id
     JOIN parallels p ON p.insert_set_id = i.id`
  );
  const setsWithParallels = new Set(setsWithParallelsRows.map((r) => r.id));

  // Query which sets have at least one player appearance (checklist)
  const setsWithChecklistRows = await rawQuery.all<{ id: number }>(
    `SELECT DISTINCT s.id FROM sets s
     JOIN insert_sets i ON i.set_id = s.id
     JOIN player_appearances pa ON pa.insert_set_id = i.id`
  );
  const setsWithChecklist = new Set(setsWithChecklistRows.map((r) => r.id));

  // Query slugs for all sets (slug not in Drizzle schema)
  const setSlugMap = new Map<number, string>();
  try {
    const slugRows = await rawQuery.all<{ id: number; slug: string | null }>(
      "SELECT id, slug FROM sets"
    );
    for (const row of slugRows) {
      if (row.slug) setSlugMap.set(row.id, row.slug);
    }
  } catch { /* slug column may not exist yet */ }

  // Build normalized name → set row map
  const setsNormMap = new Map<string, typeof allSets[0]>();
  const setsSortedMap = new Map<string, typeof allSets[0]>();
  for (const s of allSets) {
    const norm = normalize(s.name);
    setsNormMap.set(norm, s);
    setsSortedMap.set(sortedTokens(norm), s);
  }

  function findMatch(catalogName: string): typeof allSets[0] | null {
    const normName = normalize(catalogName);
    // 1. Exact normalized match
    if (setsNormMap.has(normName)) return setsNormMap.get(normName)!;
    // 2. Substring containment — only if lengths are within 20% of each other
    //    to prevent e.g. "Chrome UFC" matching "Chrome UFC Sapphire"
    for (const [normSetName, setRow] of setsNormMap) {
      if (normName.includes(normSetName) || normSetName.includes(normName)) {
        const longer = Math.max(normName.length, normSetName.length);
        const shorter = Math.min(normName.length, normSetName.length);
        if (shorter / longer >= 0.8) return setRow;
      }
    }
    // 3. Order-insensitive token match
    const sorted = sortedTokens(normName);
    if (setsSortedMap.has(sorted)) return setsSortedMap.get(sorted)!;
    return null;
  }

  function getSetStatus(s: typeof allSets[0]) {
    let hasBoxConfig = false;
    let hasPackOdds = false;
    if (s.boxConfig) {
      try {
        const bc = JSON.parse(s.boxConfig);
        const cfg = bc.hobby ?? bc;
        hasBoxConfig = cfg.packs_per_box != null;
      } catch {}
    }
    if (s.packOdds) {
      try {
        hasPackOdds = Object.keys(JSON.parse(s.packOdds)).length > 0;
      } catch {}
    }
    const hasParallels = setsWithParallels.has(s.id);
    const hasChecklist = setsWithChecklist.has(s.id);
    return { hasBoxConfig, hasPackOdds, hasParallels, hasChecklist };
  }

  // Track which DB sets are matched by catalog entries
  const matchedDbIds = new Set<number>();

  // Build rows from catalog
  const rows: CoverageRow[] = CATALOG.map((entry) => {
    const matchedSet = findMatch(entry.name);
    if (matchedSet) matchedDbIds.add(matchedSet.id);
    const status = matchedSet ? getSetStatus(matchedSet) : { hasBoxConfig: false, hasPackOdds: false, hasParallels: false, hasChecklist: false };
    return {
      ...entry,
      manufacturer: inferManufacturer(entry.name),
      matchedSetId: matchedSet?.id ?? null,
      matchedSetSlug: matchedSet ? (setSlugMap.get(matchedSet.id) ?? null) : null,
      hasChecklist: status.hasChecklist,
      hasBoxConfig: status.hasBoxConfig,
      hasPackOdds: status.hasPackOdds,
      hasParallels: status.hasParallels,
      releaseDate: matchedSet?.releaseDate ?? null,
    };
  });

  // Auto-sync: add DB sets that aren't in the catalog
  for (const s of allSets) {
    if (matchedDbIds.has(s.id)) continue;
    const status = getSetStatus(s);
    // Infer year from season field or set name
    let year = 2024;
    const seasonMatch = s.season?.match(/(\d{4})/);
    if (seasonMatch) {
      const seasonYear = parseInt(seasonMatch[1], 10);
      // Map season to release era: 2025-26 → 2026, 2024-25 → 2025, etc.
      year = s.season && s.season.includes("-") ? seasonYear + 1 : seasonYear;
    } else {
      const nameMatch = s.name.match(/(\d{4})/);
      if (nameMatch) year = parseInt(nameMatch[1], 10);
    }
    rows.push({
      name: s.name,
      year,
      sport: s.sport,
      manufacturer: inferManufacturer(s.name),
      matchedSetId: s.id,
      matchedSetSlug: setSlugMap.get(s.id) ?? null,
      hasChecklist: status.hasChecklist,
      hasBoxConfig: status.hasBoxConfig,
      hasPackOdds: status.hasPackOdds,
      hasParallels: status.hasParallels,
      releaseDate: s.releaseDate ?? null,
    });
  }

  return <SetsCoverageClient rows={rows} />;
}
