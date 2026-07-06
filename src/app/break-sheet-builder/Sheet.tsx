"use client";

/**
 * Break Sheet Builder — spreadsheet grid.
 * Google-Sheets-style: click to select, type / Enter / double-click to edit,
 * Tab / Enter / arrow navigation, drag the fill handle to copy down, and
 * per-row selection. Ported to TSX from the imported design's grid.
 */

import {
  memo,
  useCallback,
  useRef,
  useState,
  type KeyboardEvent as ReactKeyboardEvent,
  type MouseEvent as ReactMouseEvent,
} from "react";

export type ColumnType = "const" | "mono" | "text" | "num" | "type";

export interface GridColumn {
  key: string;
  label: string;
  type: ColumnType;
  readOnly?: boolean;
  money?: boolean;
  width: number;
  sortable?: boolean;
  placeholder?: string;
}

export interface GridRow {
  id: string;
  kind: "entity" | "give";
  meta: { name: string; team?: string; isRC?: boolean; initials?: string };
  cells: Record<string, string>;
}

export type SortDir = "asc" | "desc";

interface SheetProps {
  rows: GridRow[];
  columns: GridColumn[];
  onEdit: (id: string, key: string, val: string) => void;
  onFill: (key: string, ids: string[], val: string) => void;
  selected: Set<string>;
  toggleSel: (id: string) => void;
  selectAll: () => void;
  allSelected: boolean;
  sortKey: string;
  sortDir: SortDir;
  onSort: (key: string) => void;
  mode: "athletes" | "teams";
}

interface FillState {
  c: number;
  min: number;
  max: number;
  start: number;
}

// ─── Title highlighting: wrap "(TAG)" groups in an accent span ──────────────────
function titleParts(str: string) {
  const segs = String(str)
    .split(/(\([^)]*\))/g)
    .filter((s) => s !== "");
  return segs.map((s, i) =>
    s.startsWith("(") ? (
      <span key={i} className="tok-paren">
        {s}
      </span>
    ) : (
      <span key={i}>{s}</span>
    )
  );
}

function DisplayCell({ col, value }: { col: GridColumn; value: string }) {
  if (col.type === "type") {
    const v = value === "Auction" ? "auc" : value === "Giveaway" ? "give" : "bin";
    const label =
      value === "Auction" ? "AUCTION" : value === "Giveaway" ? "GIVEAWAY" : "BUY IT NOW";
    return (
      <div className="cell">
        <span className={"typetag " + v}>{label}</span>
      </div>
    );
  }
  const has = value !== "" && value != null;
  if (col.type === "const") {
    return <div className={"cell const" + (has ? "" : " muted")}>{has ? value : "—"}</div>;
  }
  if (col.type === "num") {
    const money = col.money && has;
    return (
      <div className={"cell num" + (has ? "" : " muted")}>
        {money ? <span className="price-pre">$</span> : null}
        {has ? value : col.placeholder ?? "—"}
      </div>
    );
  }
  if (col.type === "mono") {
    return <div className="cell mono">{titleParts(value)}</div>;
  }
  return <div className={"cell" + (has ? "" : " muted")}>{has ? value : col.placeholder ?? "—"}</div>;
}

interface RowProps {
  row: GridRow;
  columns: GridColumn[];
  vIndex: number;
  isSel: boolean;
  isActiveRow: boolean;
  activeC: number;
  editing: boolean;
  draft: string;
  onCellMouseDown: (e: ReactMouseEvent, r: number, c: number) => void;
  onCellDblClick: (r: number, c: number) => void;
  onStartFill: (e: ReactMouseEvent, c: number, startR: number) => void;
  onDraft: (v: string) => void;
  commitDraft: (dir?: string) => void;
  cancelDraft: () => void;
  fill: FillState | null;
  toggleSel: (id: string) => void;
}

const Row = memo(
  function Row(props: RowProps) {
    const {
      row,
      columns,
      vIndex,
      isSel,
      isActiveRow,
      activeC,
      editing,
      draft,
      onCellMouseDown,
      onCellDblClick,
      onStartFill,
      onDraft,
      commitDraft,
      cancelDraft,
      fill,
      toggleSel,
    } = props;
    const give = row.kind === "give";
    return (
      <tr className={(isSel ? "row-sel " : "") + (give ? "row-give" : "")} data-r={vIndex}>
        <td className="col-num">
          <div className="rownum">
            <span className="num">{vIndex + 1}</span>
            <span className="chk">
              <div
                className="minibox"
                onClick={(e) => {
                  e.stopPropagation();
                  toggleSel(row.id);
                }}
              >
                {isSel ? <Check /> : null}
              </div>
            </span>
          </div>
        </td>
        <td className="col-player">
          {give ? (
            <div className="player">
              <div className="give-ic">
                <Gift />
              </div>
              <div>
                <div className="pn">{row.meta.name}</div>
              </div>
            </div>
          ) : (
            <div className="player">
              <div className="avatar">{row.meta.initials}</div>
              <div style={{ minWidth: 0 }}>
                <div className="pn">
                  {row.meta.name}
                  {row.meta.isRC ? <span className="rc">RC</span> : null}
                </div>
                {row.meta.team ? <div className="pt">{row.meta.team}</div> : null}
              </div>
            </div>
          )}
        </td>
        {columns.map((col, c) => {
          const val = row.cells[col.key] ?? "";
          const isActive = isActiveRow && activeC === c;
          const isEditing = isActive && editing;
          const inFill =
            fill && fill.c === c && vIndex >= fill.min && vIndex <= fill.max && fill.start !== vIndex;
          const classes = [
            "col-" + col.key.replace(/[^a-z]/gi, "").toLowerCase(),
            col.type === "const" ? "td-const" : "",
            isEditing ? "td-edit" : isActive ? "td-active" : "",
            inFill ? "td-infill" : "",
          ]
            .filter(Boolean)
            .join(" ");

          let inner: React.ReactNode;
          if (isEditing) {
            if (col.type === "type") {
              inner = (
                <select
                  className="cell-select"
                  autoFocus
                  value={draft}
                  onChange={(e) => onDraft(e.target.value)}
                  onBlur={() => commitDraft()}
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === "Tab") {
                      e.preventDefault();
                      commitDraft(e.key === "Tab" ? "right" : "down");
                    }
                    if (e.key === "Escape") cancelDraft();
                  }}
                >
                  <option value="Buy it Now">Buy it Now</option>
                  <option value="Auction">Auction</option>
                  <option value="Giveaway">Giveaway</option>
                </select>
              );
            } else {
              inner = (
                <input
                  className={
                    "cell-input" +
                    (col.type === "num" ? " num" : "") +
                    (col.type === "mono" ? " mono" : "")
                  }
                  autoFocus
                  value={draft}
                  inputMode={col.type === "num" ? "decimal" : undefined}
                  onChange={(e) => onDraft(e.target.value)}
                  onBlur={() => commitDraft()}
                  onKeyDown={(e) => {
                    if (e.key === "Enter") {
                      e.preventDefault();
                      commitDraft("down");
                    } else if (e.key === "Tab") {
                      e.preventDefault();
                      commitDraft(e.shiftKey ? "left" : "right");
                    } else if (e.key === "Escape") {
                      cancelDraft();
                    }
                  }}
                />
              );
            }
          } else {
            inner = <DisplayCell col={col} value={val} />;
          }
          return (
            <td
              key={col.key}
              className={classes}
              data-r={vIndex}
              data-c={c}
              onMouseDown={(e) => onCellMouseDown(e, vIndex, c)}
              onDoubleClick={() => onCellDblClick(vIndex, c)}
            >
              {inner}
              {isActive && !editing && !col.readOnly ? (
                <div className="fillh" onMouseDown={(e) => onStartFill(e, c, vIndex)} />
              ) : null}
            </td>
          );
        })}
      </tr>
    );
  },
  (a, b) =>
    a.row === b.row &&
    a.isSel === b.isSel &&
    a.columns === b.columns &&
    a.isActiveRow === b.isActiveRow &&
    a.activeC === b.activeC &&
    a.editing === b.editing &&
    a.draft === b.draft &&
    a.fill === b.fill &&
    a.vIndex === b.vIndex
);

export function Sheet(props: SheetProps) {
  const { rows, columns, onEdit, onFill, selected, toggleSel, selectAll, allSelected, sortKey, sortDir, onSort, mode } =
    props;
  const [active, setActive] = useState<{ r: number; c: number } | null>(null);
  const [editing, setEditing] = useState(false);
  const [draft, setDraft] = useState("");
  const [fill, setFill] = useState<FillState | null>(null);
  const wrapRef = useRef<HTMLDivElement>(null);
  const fillRef = useRef<(FillState & { startVal: string }) | null>(null);

  const nRows = rows.length;
  const nCols = columns.length;

  const focusWrap = () => {
    if (wrapRef.current) wrapRef.current.focus();
  };

  const beginEdit = useCallback(
    (r: number, c: number, initial?: string) => {
      const col = columns[c];
      if (col.readOnly) return;
      const cur = rows[r].cells[col.key];
      setActive({ r, c });
      setEditing(true);
      setDraft(initial != null ? initial : cur == null ? "" : String(cur));
    },
    [rows, columns]
  );

  const move = useCallback(
    (r: number, c: number, dir: string) => {
      let nr = r;
      let nc = c;
      if (dir === "down") nr = Math.min(nRows - 1, r + 1);
      else if (dir === "up") nr = Math.max(0, r - 1);
      else if (dir === "right") {
        nc = c + 1;
        if (nc >= nCols) {
          nc = 0;
          nr = Math.min(nRows - 1, r + 1);
        }
      } else if (dir === "left") {
        nc = c - 1;
        if (nc < 0) {
          nc = nCols - 1;
          nr = Math.max(0, r - 1);
        }
      }
      setActive({ r: nr, c: nc });
    },
    [nRows, nCols]
  );

  const commitDraft = useCallback(
    (dir?: string) => {
      if (!active || !rows[active.r]) return;
      const col = columns[active.c];
      onEdit(rows[active.r].id, col.key, draft);
      setEditing(false);
      if (typeof dir === "string") move(active.r, active.c, dir);
      requestAnimationFrame(focusWrap);
    },
    [active, columns, rows, draft, onEdit, move]
  );

  const cancelDraft = useCallback(() => {
    setEditing(false);
    requestAnimationFrame(focusWrap);
  }, []);

  const onCellMouseDown = useCallback(
    (_e: ReactMouseEvent, r: number, c: number) => {
      if (editing && active && (active.r !== r || active.c !== c)) commitDraft();
      setActive({ r, c });
      setEditing(false);
      focusWrap();
    },
    [editing, active, commitDraft]
  );

  const onCellDblClick = useCallback((r: number, c: number) => beginEdit(r, c), [beginEdit]);

  const onStartFill = useCallback(
    (e: ReactMouseEvent, c: number, startR: number) => {
      e.preventDefault();
      e.stopPropagation();
      const startVal = rows[startR].cells[columns[c].key] ?? "";
      fillRef.current = { c, start: startR, min: startR, max: startR, startVal };
      setFill({ c, min: startR, max: startR, start: startR });
      const onMove = (ev: globalThis.MouseEvent) => {
        const el = document.elementFromPoint(ev.clientX, ev.clientY);
        const td = el && el.closest ? el.closest("td[data-r]") : null;
        if (td) {
          const rr = parseInt(td.getAttribute("data-r") || "", 10);
          if (!Number.isNaN(rr) && fillRef.current) {
            const f = fillRef.current;
            f.min = Math.min(f.start, rr);
            f.max = Math.max(f.start, rr);
            setFill({ c: f.c, min: f.min, max: f.max, start: f.start });
          }
        }
      };
      const onUp = () => {
        window.removeEventListener("mousemove", onMove);
        window.removeEventListener("mouseup", onUp);
        const f = fillRef.current;
        if (f) {
          const ids: string[] = [];
          for (let r = f.min; r <= f.max; r++) {
            if (r !== f.start && rows[r]) ids.push(rows[r].id);
          }
          if (ids.length) onFill(columns[f.c].key, ids, f.startVal);
        }
        fillRef.current = null;
        setFill(null);
      };
      window.addEventListener("mousemove", onMove);
      window.addEventListener("mouseup", onUp);
    },
    [rows, columns, onFill]
  );

  const onKeyDown = useCallback(
    (e: ReactKeyboardEvent) => {
      if (!active || editing || active.r >= nRows) return;
      const { r, c } = active;
      if (e.key === "ArrowDown") {
        e.preventDefault();
        move(r, c, "down");
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        move(r, c, "up");
      } else if (e.key === "ArrowRight") {
        e.preventDefault();
        move(r, c, "right");
      } else if (e.key === "ArrowLeft") {
        e.preventDefault();
        move(r, c, "left");
      } else if (e.key === "Tab") {
        e.preventDefault();
        move(r, c, e.shiftKey ? "left" : "right");
      } else if (e.key === "Enter" || e.key === "F2") {
        e.preventDefault();
        beginEdit(r, c);
      } else if (e.key === "Backspace" || e.key === "Delete") {
        e.preventDefault();
        if (!columns[c].readOnly) onEdit(rows[r].id, columns[c].key, "");
      } else if (e.key.length === 1 && !e.metaKey && !e.ctrlKey) {
        beginEdit(r, c, e.key);
      }
    },
    [active, editing, nRows, move, beginEdit, onEdit, rows, columns]
  );

  // Ignore a stale active cell that fell out of range when the row set shrank.
  const activeInRange = active && active.r < nRows ? active : null;

  return (
    <div className="scroller" ref={wrapRef} tabIndex={0} onKeyDown={onKeyDown}>
      <table className="sheet">
        <thead>
          <tr>
            <th className="col-num">
              <div className="minibox" style={{ margin: "0 auto" }} onClick={selectAll}>
                {allSelected ? <Check /> : null}
              </div>
            </th>
            <th className="col-player">
              <span className="sortable" onClick={() => onSort("name")}>
                {mode === "teams" ? "Team" : "Player"}
                {sortKey === "name" ? <Caret dir={sortDir} /> : null}
              </span>
            </th>
            {columns.map((col) => (
              <th key={col.key} style={{ minWidth: col.width, width: col.width }}>
                {col.sortable ? (
                  <span className="sortable" onClick={() => onSort(col.key)}>
                    {col.label}
                    {sortKey === col.key ? <Caret dir={sortDir} /> : null}
                  </span>
                ) : (
                  col.label
                )}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, r) => (
            <Row
              key={row.id}
              row={row}
              columns={columns}
              vIndex={r}
              isSel={selected.has(row.id)}
              isActiveRow={!!activeInRange && activeInRange.r === r}
              activeC={activeInRange && activeInRange.r === r ? activeInRange.c : -1}
              editing={editing}
              draft={draft}
              onCellMouseDown={onCellMouseDown}
              onCellDblClick={onCellDblClick}
              onStartFill={onStartFill}
              onDraft={setDraft}
              commitDraft={commitDraft}
              cancelDraft={cancelDraft}
              fill={fill}
              toggleSel={toggleSel}
            />
          ))}
        </tbody>
      </table>
    </div>
  );
}

// ─── Inline icons ───────────────────────────────────────────────────────────────
function Check() {
  return (
    <svg width={11} height={11} viewBox="0 0 12 12" fill="none">
      <path
        d="M2.5 6.2l2.2 2.3 4.8-5"
        stroke="currentColor"
        strokeWidth={2}
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
function Gift() {
  return (
    <svg width={15} height={15} viewBox="0 0 24 24" fill="none">
      <path
        d="M20 12v8H4v-8M2 7h20v5H2zM12 22V7M12 7s-1.5-4-4-4a2 2 0 100 4h4zM12 7s1.5-4 4-4a2 2 0 110 4h-4z"
        stroke="currentColor"
        strokeWidth={1.7}
        strokeLinejoin="round"
      />
    </svg>
  );
}
function Caret({ dir }: { dir: SortDir }) {
  return (
    <svg
      width={9}
      height={9}
      viewBox="0 0 10 10"
      fill="none"
      style={{ transform: dir === "desc" ? "rotate(180deg)" : "none" }}
    >
      <path d="M5 2l3 4H2z" fill="currentColor" />
    </svg>
  );
}
