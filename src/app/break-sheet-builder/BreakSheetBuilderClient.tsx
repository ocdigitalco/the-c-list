"use client";

import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useRouter } from "next/navigation";
import "./breaksheet.css";
import { Sheet, type GridColumn, type GridRow, type SortDir } from "./Sheet";
import { Button } from "@/components/Button";
import { trackEvent } from "@/lib/analytics";
import {
  breakInfo as computeBreakInfo,
  buildCsv,
  buildSharePath,
  buildTitle,
  CATEGORY,
  subCategoryFor,
  configToParams,
  type BreakConfig,
  type BreakSheetData,
  type BreakSheetPlayerRow,
  type CatFilter,
} from "@/lib/breakSheet";

export interface SetOption {
  slug: string;
  name: string;
  sport: string;
}

interface Props {
  setOptions: SetOption[];
  data: BreakSheetData | null;
  initialConfig: BreakConfig;
}

// ─── Grid column definitions (Whatnot order) ────────────────────────────────────
const COLUMNS: GridColumn[] = [
  { key: "Category", label: "Category", type: "const", readOnly: true, width: 110 },
  { key: "Sub Category", label: "Sub Category", type: "const", readOnly: true, width: 132 },
  { key: "Title", label: "Title", type: "mono", width: 300, sortable: true, placeholder: "—" },
  { key: "Description", label: "Description", type: "text", width: 250, placeholder: "—" },
  { key: "Quantity", label: "Qty", type: "const", readOnly: true, width: 52 },
  { key: "Type", label: "Type", type: "type", width: 140 },
  { key: "Price", label: "Price", type: "num", money: true, width: 92, sortable: true, placeholder: "$" },
  { key: "Shipping Profile", label: "Shipping", type: "text", width: 104, placeholder: "—" },
  { key: "Offerable", label: "Offerable", type: "const", readOnly: true, width: 94 },
  { key: "Hazmat", label: "Hazmat", type: "const", readOnly: true, width: 104 },
  { key: "Condition", label: "Condition", type: "const", readOnly: true, width: 84 },
  { key: "Cost Per Item", label: "Cost / Item", type: "num", money: true, width: 100, placeholder: "$" },
  { key: "SKU", label: "SKU", type: "text", width: 82, placeholder: "—" },
  ...Array.from({ length: 8 }, (_, i) => ({
    key: `Image URL ${i + 1}`,
    label: `Image ${i + 1}`,
    type: "text" as const,
    width: 88,
    placeholder: "—",
  })),
];

const CAT_FILTERS: CatFilter[] = ["Total Cards", "Autographs", "Inserts", "Numbered"];
const SHIPPING_PROFILES = ["0-1 oz", "1-3 oz", "4-7 oz", "8-11 oz", "12-15 oz"];
const TAG_FIELDS: [string, keyof BreakConfig["tagLabels"]][] = [
  ["Autograph", "AUTO"],
  ["Mem Auto", "MEM AUTO"],
  ["Relic", "RELIC"],
  ["Rookie", "RC"],
];

// ─── Entity model ───────────────────────────────────────────────────────────────
interface Entity {
  id: string;
  kind: "ath" | "team";
  name: string;
  team: string;
  isRC: boolean;
  player?: BreakSheetPlayerRow;
}

function initials(name: string): string {
  const p = name
    .replace(/[^A-Za-z .'-]/g, "")
    .split(/\s+/)
    .filter(Boolean);
  return ((p[0]?.[0] || "") + (p[1]?.[0] || p[0]?.[1] || "")).toUpperCase();
}
function teamInit(name: string): string {
  return name
    .split(/\s+/)
    .map((w) => w[0])
    .join("")
    .slice(0, 3)
    .toUpperCase();
}
function fmtUSD(n: number): string {
  return "$" + (n || 0).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export function BreakSheetBuilderClient({ setOptions, data, initialConfig }: Props) {
  const router = useRouter();

  const [config, setConfig] = useState<BreakConfig>(initialConfig);
  const patch = useCallback(
    (p: Partial<BreakConfig>) => setConfig((c) => ({ ...c, ...p })),
    []
  );
  const setTagLabel = useCallback(
    (key: keyof BreakConfig["tagLabels"], val: string) =>
      setConfig((c) => ({ ...c, tagLabels: { ...c.tagLabels, [key]: val } })),
    []
  );

  const [search, setSearch] = useState("");
  const [edits, setEdits] = useState<Record<string, string>>({});
  const [excluded, setExcluded] = useState<Set<string>>(() => new Set());
  const [selected, setSelected] = useState<Set<string>>(() => new Set());
  const [sortKey, setSortKey] = useState("name");
  const [sortDir, setSortDir] = useState<SortDir>("asc");
  const [bulkVal, setBulkVal] = useState("");
  const [allPriceVal, setAllPriceVal] = useState("");
  const [cost, setCost] = useState(""); // what the breaker paid (ephemeral; not in URL)
  const [copied, setCopied] = useState(false);

  const sport = data?.sport ?? "";
  const league = data?.league ?? null;
  const category = CATEGORY; // always "Sports Cards"
  const subCategory = subCategoryFor(sport); // "{Sport} Breaks" (MMA → "UFC Breaks")

  // ── page-level open event (once) ──────────────────────────────────────────────
  const openedRef = useRef(false);
  useEffect(() => {
    if (openedRef.current) return;
    openedRef.current = true;
    trackEvent("break_sheet_open", { set_slug: data?.slug ?? "" });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // ── config → URL + debounced config event ─────────────────────────────────────
  const firstSync = useRef(true);
  useEffect(() => {
    if (firstSync.current) {
      firstSync.current = false;
      return;
    }
    if (!data) return;
    const t = setTimeout(() => {
      // Cost is intentionally NOT written to the shareable URL.
      const params = new URLSearchParams({ set: data.slug, ...configToParams(config) });
      window.history.replaceState(null, "", `?${params.toString()}`);
      trackEvent("break_sheet_config", {
        set_slug: data.slug,
        box_type: config.breakUnit,
        quantity: config.breakQty,
        cost: parseFloat(cost) || 0,
      });
    }, 400);
    return () => clearTimeout(t);
  }, [config, cost, data]);

  // ── entities (filtered) ───────────────────────────────────────────────────────
  const entities = useMemo<Entity[]>(() => {
    if (!data) return [];
    const q = search.trim().toLowerCase();
    if (config.mode === "teams") {
      let list: Entity[] = data.teams.map((t) => ({
        id: "team::" + t,
        kind: "team",
        name: t,
        team: "",
        isRC: false,
      }));
      if (q) list = list.filter((t) => t.name.toLowerCase().includes(q));
      return list;
    }
    let list: Entity[] = data.players.map((p) => ({
      id: "ath::" + p.id,
      kind: "ath",
      name: p.name,
      team: p.team,
      isRC: p.isRookie,
      player: p,
    }));
    if (q) list = list.filter((a) => a.name.toLowerCase().includes(q) || a.team.toLowerCase().includes(q));
    if (config.rookiesOnly) list = list.filter((a) => a.isRC);
    if (config.catFilter === "Autographs") list = list.filter((a) => (a.player?.autoCount ?? 0) > 0);
    else if (config.catFilter === "Inserts") list = list.filter((a) => a.player?.hasInsert);
    else if (config.catFilter === "Numbered") list = list.filter((a) => a.player?.hasNumbered);
    return list;
  }, [data, search, config.mode, config.rookiesOnly, config.catFilter]);

  // ── build a title for an entity ───────────────────────────────────────────────
  const titleFor = useCallback(
    (e: Entity): string => {
      if (e.kind === "team" || !e.player) return e.name;
      return buildTitle(e.player, config.tagLabels, config.labelFormat);
    },
    [config.tagLabels, config.labelFormat]
  );

  // ── build a cell map for an entity / giveaway ─────────────────────────────────
  const entityCells = useCallback(
    (e: Entity): Record<string, string> => {
      const get = (k: string, def: string) => edits[e.id + "::" + k] ?? def;
      const cells: Record<string, string> = {
        Category: category,
        "Sub Category": subCategory,
        Title: get("Title", titleFor(e)),
        Description: get("Description", config.description),
        Quantity: "1",
        Type: get("Type", config.listingType),
        Price: get("Price", ""),
        "Shipping Profile": get("Shipping Profile", config.shippingProfile),
        Offerable: config.offerable ? "TRUE" : "",
        Hazmat: "Not Hazmat",
        Condition: "New",
        "Cost Per Item": get("Cost Per Item", ""),
        SKU: get("SKU", ""),
      };
      for (let i = 1; i <= 8; i++) cells[`Image URL ${i}`] = get(`Image URL ${i}`, "");
      return cells;
    },
    [edits, category, subCategory, titleFor, config.description, config.listingType, config.shippingProfile, config.offerable]
  );

  const giveCells = useCallback(
    (id: string, name: string): Record<string, string> => {
      const get = (k: string, def: string) => edits[id + "::" + k] ?? def;
      const cells: Record<string, string> = {
        Category: category,
        "Sub Category": subCategory,
        Title: get("Title", name),
        Description: get("Description", config.description),
        Quantity: "1",
        Type: "Giveaway",
        Price: get("Price", ""),
        "Shipping Profile": get("Shipping Profile", config.shippingProfile),
        Offerable: config.offerable ? "TRUE" : "",
        Hazmat: "Not Hazmat",
        Condition: "New",
        "Cost Per Item": get("Cost Per Item", ""),
        SKU: get("SKU", ""),
      };
      for (let i = 1; i <= 8; i++) cells[`Image URL ${i}`] = get(`Image URL ${i}`, "");
      return cells;
    },
    [edits, category, subCategory, config.description, config.shippingProfile, config.offerable]
  );

  // ── rows (giveaways + buyers first, then sorted entities) ─────────────────────
  const rows = useMemo<GridRow[]>(() => {
    const out: GridRow[] = [];
    for (let i = 0; i < config.giveaways; i++) {
      const id = "give::" + i;
      if (excluded.has(id)) continue;
      const name = "Giveaway #" + (i + 1);
      out.push({ id, kind: "give", meta: { name: edits[id + "::Title"] ?? name }, cells: giveCells(id, name) });
    }
    if (config.buyersGiveaway && !excluded.has("give::buyers")) {
      const id = "give::buyers";
      out.push({
        id,
        kind: "give",
        meta: { name: edits[id + "::Title"] ?? "Buyers Giveaway" },
        cells: giveCells(id, "Buyers Giveaway"),
      });
    }

    const ents = entities.filter((e) => !excluded.has(e.id));
    const dir = sortDir === "asc" ? 1 : -1;
    const sorted = ents.slice().sort((a, b) => {
      if (sortKey === "Price") {
        const av = parseFloat(edits[a.id + "::Price"] || "0") || 0;
        const bv = parseFloat(edits[b.id + "::Price"] || "0") || 0;
        return (av - bv) * dir;
      }
      const av = sortKey === "Title" ? titleFor(a) : a.name;
      const bv = sortKey === "Title" ? titleFor(b) : b.name;
      return String(av).localeCompare(String(bv)) * dir;
    });

    for (const e of sorted) {
      out.push({
        id: e.id,
        kind: "entity",
        meta: {
          name: e.name,
          team: e.team,
          isRC: e.isRC,
          initials: e.kind === "team" ? teamInit(e.name) : initials(e.name),
        },
        cells: entityCells(e),
      });
    }
    return out;
  }, [entities, config.giveaways, config.buyersGiveaway, excluded, edits, sortKey, sortDir, titleFor, entityCells, giveCells]);

  // ── derived counts ────────────────────────────────────────────────────────────
  const rowCount = rows.length;
  const spotCount = useMemo(() => rows.filter((r) => r.kind === "entity").length, [rows]);
  const autoCount = useMemo(() => entities.filter((e) => (e.player?.autoCount ?? 0) > 0).length, [entities]);
  const insertCount = useMemo(() => entities.filter((e) => e.player?.hasInsert).length, [entities]);
  const numberedCount = useMemo(() => entities.filter((e) => e.player?.hasNumbered).length, [entities]);
  const pricedCount = useMemo(() => rows.filter((r) => r.cells.Price !== "" && r.cells.Price != null).length, [rows]);
  const priceTotal = useMemo(
    () => rows.reduce((sum, r) => sum + (parseFloat(r.cells.Price) || 0), 0),
    [rows]
  );
  const pricedPct = rowCount ? Math.round((pricedCount / rowCount) * 100) : 0;

  // Cost / Total / Profit. costNum is null when the field is blank; profit is
  // null (shown as "—") until a cost is entered.
  const costNum = cost.trim() === "" ? null : parseFloat(cost);
  const costValid = costNum != null && Number.isFinite(costNum);
  const profit = costValid ? priceTotal - (costNum as number) : null;

  const bi = useMemo(
    () => computeBreakInfo(config.breakUnit, config.breakQty, data?.boxesPerCase ?? null, data?.autosPerBox ?? null),
    [config.breakUnit, config.breakQty, data?.boxesPerCase, data?.autosPerBox]
  );

  // ── editing handlers ──────────────────────────────────────────────────────────
  const onEdit = useCallback((id: string, key: string, val: string) => {
    setEdits((p) => ({ ...p, [id + "::" + key]: val }));
  }, []);
  const onFill = useCallback((key: string, ids: string[], val: string) => {
    setEdits((p) => {
      const n = { ...p };
      ids.forEach((id) => (n[id + "::" + key] = val));
      return n;
    });
  }, []);
  const toggleSel = useCallback(
    (id: string) =>
      setSelected((p) => {
        const n = new Set(p);
        if (n.has(id)) n.delete(id);
        else n.add(id);
        return n;
      }),
    []
  );
  // Single source of truth for "every spot" — both the header select-all and the
  // "apply price to all" control derive from this, so they can't drift.
  const allRowIds = useMemo(() => rows.map((r) => r.id), [rows]);
  const allSelected = allRowIds.length > 0 && allRowIds.every((id) => selected.has(id));
  const selectAll = useCallback(() => {
    // header checkbox: toggle
    setSelected(allSelected ? new Set<string>() : new Set(allRowIds));
  }, [allRowIds, allSelected]);
  const selectAllRows = useCallback(() => setSelected(new Set(allRowIds)), [allRowIds]);
  const onSort = useCallback((key: string) => {
    setSortKey((k) => {
      if (k === key) {
        setSortDir((d) => (d === "asc" ? "desc" : "asc"));
        return k;
      }
      setSortDir("asc");
      return key;
    });
  }, []);
  const deleteSelected = () => {
    setExcluded((p) => {
      const n = new Set(p);
      selected.forEach((id) => n.add(id));
      return n;
    });
    setSelected(new Set());
  };
  // Shared price-apply path used by both the bulk bar and "apply to all".
  const applyPriceToIds = useCallback((ids: Iterable<string>, price: string) => {
    if (!price) return;
    setEdits((p) => {
      const n = { ...p };
      for (const id of ids) n[id + "::Price"] = price;
      return n;
    });
  }, []);
  const applyBulk = () => applyPriceToIds(selected, bulkVal);
  const applyPriceToAll = () => {
    if (!allPriceVal) return;
    selectAllRows(); // force select-all (same id source as the header select-all)
    applyPriceToIds(allRowIds, allPriceVal);
  };

  // Compose a break description from the current config.
  const autoGenerateDescription = () => {
    if (!data) return;
    const unitWord =
      config.breakUnit === "Cases"
        ? config.breakQty === 1
          ? "Case"
          : "Cases"
        : config.breakQty === 1
        ? "Box"
        : "Boxes";
    const spots = config.mode === "teams" ? "team spots" : "spots";
    const desc = `${config.breakQty} ${unitWord}! ${data.setName} — ${spotCount.toLocaleString()} ${spots} · ${config.listingType}`;
    patch({ description: desc });
  };
  const reset = () => {
    setEdits({});
    setExcluded(new Set());
    setSelected(new Set());
  };

  // ── export / share ────────────────────────────────────────────────────────────
  // Fire-and-forget save of the sheet + per-spot prices. Must never block or
  // fail the export — errors are logged and swallowed.
  const saveSheet = () => {
    if (!data) return;
    const subjectType = config.mode === "teams" ? "team" : "athlete";
    const prices = rows
      .filter((r) => r.kind === "entity")
      .map((r) => ({ subjectName: r.meta.name, subjectType, price: parseFloat(r.cells.Price) }))
      .filter((p) => Number.isFinite(p.price));
    const payload = {
      setSlug: data.slug,
      sport: data.sport,
      breakUnit: config.breakUnit.toLowerCase(), // "cases" | "boxes"
      quantity: config.breakQty,
      cost: costValid ? costNum : null,
      total: priceTotal,
      profit,
      config: JSON.stringify({ ...config, mode: config.mode, listingType: config.listingType }),
      prices,
    };
    // keepalive lets the request survive the navigation the download may trigger.
    fetch("/api/sheets", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
      keepalive: true,
    }).catch((err) => console.error("break sheet save failed (non-blocking):", err));
  };

  const download = () => {
    if (!data) return;
    const csv = buildCsv(rows.map((r) => r.cells));
    const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `${data.setName} - Break Sheet.csv`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    trackEvent("break_sheet_export", {
      action: "csv",
      set_slug: data.slug,
      box_type: config.breakUnit,
      quantity: rowCount,
    });
    saveSheet(); // fire-and-forget; download already happened above
  };
  const copyShareLink = async () => {
    if (!data) return;
    const url = window.location.origin + buildSharePath(data.slug, config);
    try {
      await navigator.clipboard.writeText(url);
      setCopied(true);
      setTimeout(() => setCopied(false), 1800);
    } catch {
      /* clipboard blocked — ignore */
    }
    trackEvent("break_sheet_export", {
      action: "share",
      set_slug: data.slug,
      box_type: config.breakUnit,
      quantity: rowCount,
    });
  };

  // ── switching sets navigates (server refetch), preserving config ──────────────
  const changeSet = (slug: string) => {
    if (!slug) return;
    router.push(buildSharePath(slug, config));
  };

  // ─── render ────────────────────────────────────────────────────────────────────
  const setSelect = (
    <select
      className="inp inp-sm"
      style={{ minWidth: 230 }}
      value={data?.slug ?? ""}
      onChange={(e) => changeSet(e.target.value)}
    >
      {!data && <option value="">Select a set…</option>}
      {setOptions.map((o) => (
        <option key={o.slug} value={o.slug}>
          {o.name}
        </option>
      ))}
    </select>
  );

  return (
    <div className="bsb">
      {/* Toolbar */}
      <div className="toolbar">
        <div className="tb-set">
          {data?.sampleImageUrl ? (
            // eslint-disable-next-line @next/next/no-img-element
            <img className="tb-cardimg" src={data.sampleImageUrl} alt="" />
          ) : (
            <div className="tb-cardimg">
              <span>CARD ART</span>
            </div>
          )}
          <div className="tb-meta">
            <div className="tb-crumb">
              {data ? `${data.sport}${league ? " · " + league : ""} · Break Sheet` : "Break Sheet Builder"}
            </div>
            <div className="tb-name">{data?.setName ?? "Select a set to begin"}</div>
          </div>
        </div>
        <div className="tb-spacer" />
        {data && (
          <>
            <div className="tb-stat">
              <div className="n">{rowCount.toLocaleString()}</div>
              <div className="l">Rows</div>
            </div>
            <div className="tb-stat">
              <div className="n">{(config.mode === "teams" ? data.teamCount : data.athleteCount).toLocaleString()}</div>
              <div className="l">{config.mode === "teams" ? "Teams" : "Athletes"}</div>
            </div>
            <Button variant="sec" onClick={copyShareLink}>
              <Share /> {copied ? "Copied!" : "Share"}
            </Button>
            <Button variant="gho" onClick={reset}>
              Reset
            </Button>
            <Button variant="pri" onClick={download}>
              <Dl /> Download CSV
            </Button>
          </>
        )}
      </div>

      {/* Ribbon (only when a set is loaded) */}
      {data && (
        <div className="ribbon-wrap">
          {/* Row 1 — what & how much */}
          <div className="ribbon">
            <Field label="Search" className="fill">
              <div className="search sm">
                <span className="ic">
                  <SearchIco />
                </span>
                <input
                  className="inp inp-sm"
                  placeholder={config.mode === "teams" ? "Search teams…" : "Search athletes…"}
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
              </div>
            </Field>

            <Field label="Roster">
              <Seg
                value={config.mode === "teams" ? "Teams" : "Athletes"}
                options={["Athletes", "Teams"]}
                onChange={(v) => patch({ mode: v === "Teams" ? "teams" : "athletes" })}
              />
            </Field>

            <Field label="Break">
              <div className="rb-row">
                <Seg
                  value={config.breakUnit}
                  options={["Cases", "Boxes"]}
                  onChange={(v) => patch({ breakUnit: v as BreakConfig["breakUnit"] })}
                />
                <Stepper
                  value={config.breakQty}
                  min={1}
                  onChange={(v) => patch({ breakQty: v })}
                />
              </div>
            </Field>
            <div className="rb-readout">
              <div className="ro">
                <span className="ro-n">{bi.boxes}</span>
                <span className="ro-l">{bi.boxes === 1 ? "box" : "boxes"}</span>
              </div>
              {bi.autos != null && (
                <>
                  <div className="ro-x">·</div>
                  <div className="ro">
                    <span className="ro-n">{bi.autos}</span>
                    <span className="ro-l">autos</span>
                  </div>
                </>
              )}
            </div>

            <Field label="Cost">
              <input
                className="inp inp-sm"
                style={{ width: 96 }}
                inputMode="decimal"
                placeholder="$ paid"
                value={cost}
                onChange={(e) => setCost(e.target.value)}
              />
            </Field>

            <Field label="Break Description" className="fill">
              <div className="rb-row" style={{ flexWrap: "nowrap" }}>
                <input
                  className="inp inp-sm"
                  style={{ flex: 1, minWidth: 0 }}
                  placeholder={`e.g. "${config.breakQty} ${config.breakUnit}! ${data.setName}"`}
                  value={config.description}
                  onChange={(e) => patch({ description: e.target.value })}
                />
                <button
                  className="rb-more"
                  style={{ flex: "0 0 auto" }}
                  onClick={autoGenerateDescription}
                  title="Auto-generate a description from your current config"
                >
                  <AutoIcon /> Auto
                </button>
              </div>
            </Field>

            <Field label="Listing">
              <Seg
                value={config.listingType}
                options={["Buy it Now", "Auction"]}
                onChange={(v) => patch({ listingType: v as BreakConfig["listingType"] })}
              />
            </Field>

            {/* Apply one price to every spot: force select-all, then price them all */}
            <Field label="Apply price to all">
              <div className="rb-row" style={{ flexWrap: "nowrap" }}>
                <input
                  className="inp inp-sm"
                  style={{ width: 88 }}
                  inputMode="decimal"
                  placeholder="$ price"
                  value={allPriceVal}
                  onChange={(e) => setAllPriceVal(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") applyPriceToAll();
                  }}
                />
                <button
                  className="btn btn-ghost"
                  style={{ height: 38, flex: "0 0 auto" }}
                  onClick={applyPriceToAll}
                  disabled={!allPriceVal}
                >
                  Apply to all
                </button>
              </div>
            </Field>
          </div>

          {/* Row 2 — details */}
          <div className="ribbon row2">
            {config.mode === "athletes" && (
              <Field label="Filter">
                <div className="rb-row">
                  <div className="pills">
                    {CAT_FILTERS.map((c) => (
                      <button
                        key={c}
                        className={"pill " + (config.catFilter === c ? "on" : "")}
                        onClick={() => patch({ catFilter: c })}
                      >
                        {c}
                      </button>
                    ))}
                  </div>
                  <label
                    className={"check " + (config.rookiesOnly ? "on" : "")}
                    onClick={() => patch({ rookiesOnly: !config.rookiesOnly })}
                    style={{ marginLeft: 4 }}
                  >
                    <span className="box">{config.rookiesOnly ? <Tick /> : null}</span>
                    Rookies
                  </label>
                </div>
              </Field>
            )}
            <Field label="Shipping">
              <select
                className="inp inp-sm"
                style={{ minWidth: 104 }}
                value={config.shippingProfile}
                onChange={(e) => patch({ shippingProfile: e.target.value })}
              >
                {SHIPPING_PROFILES.map((o) => (
                  <option key={o} value={o}>
                    {o}
                  </option>
                ))}
              </select>
            </Field>
            <Field label="Offers">
              <label
                className={"check " + (config.offerable ? "on" : "")}
                onClick={() => patch({ offerable: !config.offerable })}
                style={{ height: 38, alignItems: "center" }}
              >
                <span className="box">{config.offerable ? <Tick /> : null}</span>
                Offerable
              </label>
            </Field>
            <Field label="Giveaways">
              <Stepper value={config.giveaways} min={0} onChange={(v) => patch({ giveaways: v })} />
            </Field>
            <Field label="Buyers GA">
              <div
                className={"tgl " + (config.buyersGiveaway ? "on" : "")}
                onClick={() => patch({ buyersGiveaway: !config.buyersGiveaway })}
              >
                <div className="tgl-sw" />
              </div>
            </Field>
            <Field label="Labels">
              <Seg
                value={config.labelFormat}
                options={["Short", "Long"]}
                onChange={(v) => patch({ labelFormat: v as BreakConfig["labelFormat"] })}
              />
            </Field>
            <Field label="Tag Labels" style={{ flex: "0 1 auto", minWidth: 0 }}>
              <div className="taglab">
                {TAG_FIELDS.map(([cap, key]) => (
                  <div key={key} className="cell-tag">
                    <div className="cap">{cap}</div>
                    <input value={config.tagLabels[key]} onChange={(e) => setTagLabel(key, e.target.value)} />
                  </div>
                ))}
              </div>
            </Field>
          </div>
        </div>
      )}

      {/* Summary strip */}
      {data && (
        <div className="summary-strip">
          <SumChip n={rowCount} l="Total rows" accent />
          <SumChip n={autoCount} l="Autographs" />
          <SumChip n={insertCount} l="Inserts" />
          <SumChip n={numberedCount} l="Numbered" />
          <SumChip n={`${pricedCount} / ${rowCount}`} l="Priced" />
          <div style={{ flex: 1 }} />
          <div className="strip-progress">
            <div className="pb">
              <div className="pf" style={{ width: pricedPct + "%" }} />
            </div>
            <span>{pricedPct}% priced</span>
          </div>
          <div className="strip-money">
            <div className="sm-item">
              <span className="lab">Cost</span>
              <span className="amt neutral">{costValid ? fmtUSD(costNum as number) : "—"}</span>
            </div>
            <div className="sm-item">
              <span className="lab">Total</span>
              <span className="amt pos">{fmtUSD(priceTotal)}</span>
            </div>
            <div className="sm-item">
              <span className="lab">Profit</span>
              <span className={"amt " + (profit == null ? "neutral" : profit >= 0 ? "pos" : "neg")}>
                {profit == null ? "—" : fmtUSD(profit)}
              </span>
            </div>
          </div>
        </div>
      )}

      {/* Grid + bulk bar, or empty state */}
      {data ? (
        <div className="gridwrap">
          {selected.size > 0 && (
            <div className="bulkbar">
              <span>
                <b style={{ color: "#fff" }}>{selected.size}</b> selected
              </span>
              <input
                placeholder="Set price…"
                value={bulkVal}
                inputMode="decimal"
                onChange={(e) => setBulkVal(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === "Enter") applyBulk();
                }}
              />
              <button onClick={applyBulk}>Apply price</button>
              <div className="x">
                <button onClick={deleteSelected}>Remove from sheet</button>
                <button onClick={() => setSelected(new Set())}>Clear</button>
              </div>
            </div>
          )}
          <Sheet
            rows={rows}
            columns={COLUMNS}
            onEdit={onEdit}
            onFill={onFill}
            selected={selected}
            toggleSel={toggleSel}
            selectAll={selectAll}
            allSelected={allSelected}
            sortKey={sortKey}
            sortDir={sortDir}
            onSort={onSort}
          />
        </div>
      ) : (
        <div className="empty">
          <h2>Break Sheet Builder</h2>
          <p>
            Pick a set to auto-load its athlete checklist into a Whatnot-ready break sheet. Configure
            titles, giveaways and pricing, then download the CSV or share your setup as a link.
          </p>
          {setSelect}
        </div>
      )}

      {/* Status bar */}
      {data && (
        <div className="statusbar">
          <span className="dot" />
          <span>
            Auto-loaded from <b>{config.mode === "teams" ? "Team" : "Athlete"} Checklist</b>
          </span>
          <span style={{ color: "var(--faint)" }}>·</span>
          <span>
            <b>{rowCount.toLocaleString()}</b> rows ready
          </span>
          <span className="sp" />
          <span>
            Click a cell to edit · <span className="kbd">Tab</span> / <span className="kbd">Enter</span> to move ·
            drag the corner to fill down
          </span>
          <span style={{ color: "var(--faint)" }}>·</span>
          <span className="wn">
            Built for <span className="mk">W</span>whatnot
          </span>
        </div>
      )}
    </div>
  );
}

// ─── Small presentational helpers ───────────────────────────────────────────────
function Field({
  label,
  children,
  grow,
  style,
  className,
}: {
  label: string;
  children: React.ReactNode;
  grow?: boolean;
  style?: React.CSSProperties;
  className?: string;
}) {
  return (
    <div className={"rb-field" + (grow ? " grow" : "") + (className ? " " + className : "")} style={style}>
      <span className="rb-lab">{label}</span>
      {children}
    </div>
  );
}
function Seg({ value, options, onChange }: { value: string; options: string[]; onChange: (v: string) => void }) {
  return (
    <div className="seg">
      {options.map((o) => (
        <button key={o} className={value === o ? "on" : ""} onClick={() => onChange(o)}>
          {o}
        </button>
      ))}
    </div>
  );
}
function Stepper({ value, min, onChange }: { value: number; min: number; onChange: (v: number) => void }) {
  return (
    <div className="stepper">
      <button onClick={() => onChange(Math.max(min, value - 1))} disabled={value <= min}>
        –
      </button>
      <span className="val">{value}</span>
      <button onClick={() => onChange(value + 1)}>+</button>
    </div>
  );
}
function SumChip({ n, l, accent }: { n: number | string; l: string; accent?: boolean }) {
  return (
    <div className={"sumchip" + (accent ? " accent" : "")}>
      <div className="n">{typeof n === "number" ? n.toLocaleString() : n}</div>
      <div className="l">{l}</div>
    </div>
  );
}

// ─── Icons ──────────────────────────────────────────────────────────────────────
function Dl() {
  return (
    <svg width={16} height={16} viewBox="0 0 20 20" fill="none">
      <path
        d="M10 3v9m0 0l-3.2-3.2M10 12l3.2-3.2M4 15.5h12"
        stroke="currentColor"
        strokeWidth={1.9}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
function Share() {
  return (
    <svg width={15} height={15} viewBox="0 0 20 20" fill="none">
      <path
        d="M7 11l6-3.5M7 9l6 3.5M15 6.5a2 2 0 100-4 2 2 0 000 4zM5 12a2 2 0 100-4 2 2 0 000 4zM15 17.5a2 2 0 100-4 2 2 0 000 4z"
        stroke="currentColor"
        strokeWidth={1.6}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
function SearchIco() {
  return (
    <svg width={15} height={15} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth={1.7} strokeLinecap="round" strokeLinejoin="round">
      <path d="M11 11l3 3M7.5 12a4.5 4.5 0 100-9 4.5 4.5 0 000 9z" />
    </svg>
  );
}
function AutoIcon() {
  return (
    <svg width={14} height={14} viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth={1.5} strokeLinecap="round" strokeLinejoin="round">
      <path d="M9 2l1 2.5L12.5 5.5 10 6.5 9 9 8 6.5 5.5 5.5 8 4.5 9 2zM3.5 9l.6 1.4L5.5 11l-1.4.6L3.5 13l-.6-1.4L1.5 11l1.4-.6L3.5 9z" />
    </svg>
  );
}
function Tick() {
  return (
    <svg width={10} height={10} viewBox="0 0 12 12" fill="none">
      <path d="M2.5 6.2l2.2 2.3 4.8-5" stroke="currentColor" strokeWidth={2} strokeLinecap="round" strokeLinejoin="round" />
    </svg>
  );
}
