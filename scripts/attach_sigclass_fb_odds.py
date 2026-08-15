"""
Signature Class Football (set 850): create parallels (runs + exclusivity) and
attach pack_odds in ONE pass. Local SQLite only. Pre-commit gates; rollback on
any mismatch.

Mapping ruling (Tyler-confirmed) for the 26 non-chrome autograph rows:
  "Veteran Class Autograph *" -> subset "Veteran Class Autograph Variation"
  "Rookie Class Autograph *"  -> BOTH "Rookie Class Autograph Variation I" and
                                 "Rookie Class Autograph Variation II" (the
                                 official sheet publishes one combined line;
                                 printed values attached to each verbatim).
All other rows map by tolerant longest token-prefix.

Odds outer keys aligned to set 850 box_config (hobby, hobby_jumbo, value, mega):
  Hobby->hobby  Jumbo->hobby_jumbo  Value->value  Mega->mega  Target Mega->target_mega
"""
import json, os, re, sqlite3

DB = os.path.join(os.path.dirname(__file__), "..", "the-c-list.db")
SRC = "/private/tmp/claude-501/-Users-tyler-Documents-Development-the-c-list/1d898db3-312e-40c2-b51f-b061eade264d/scratchpad/sigclass_fb_odds.jsonl"
SET_ID = 850

FMT = {"Hobby": "hobby", "Jumbo": "hobby_jumbo", "Value": "value", "Mega": "mega", "Target Mega": "target_mega"}
FMT_ORDER = ["hobby", "hobby_jumbo", "value", "mega", "target_mega"]

# Extra base-version serials (Tyler's {subset} Base convention) for the two multi-sig subsets
EXTRA_BASE = [
    ("Signature Class Dual Signatures", "Base", 25),
    ("Signature Class Triple Signatures", "Base", 25),
]


def toks(s):
    return re.sub(r"\s+", " ", s.strip().lower()).split(" ")


def teq(a, b):
    return a == b or a.rstrip("s") == b.rstrip("s")


def is_prefix(sub_t, row_t):
    return len(sub_t) <= len(row_t) and all(teq(sub_t[i], row_t[i]) for i in range(len(sub_t)))


def main():
    rows = [json.loads(l) for l in open(SRC, encoding="utf-8") if l.strip()]
    if len(rows) != 261:
        print(f"STOP: {len(rows)} rows, exp 261"); raise SystemExit(1)

    db = sqlite3.connect(os.path.abspath(DB))
    po_now = db.execute("SELECT pack_odds FROM sets WHERE id=?", (SET_ID,)).fetchone()[0]
    if po_now:
        print("STOP: pack_odds already populated."); raise SystemExit(1)

    subs = [(iid, name) for iid, name in db.execute("SELECT id,name FROM insert_sets WHERE set_id=? ORDER BY id", (SET_ID,))]
    sub_tok = [(iid, name, toks(name)) for iid, name in subs]
    name_to_id = {name: iid for iid, name in subs}

    def resolve(row_name):
        """Return list of (subset_name, remainder_verbatim). Raise on unmapped/ambiguous."""
        rt = toks(row_name)
        cands = [(iid, name, st) for iid, name, st in sub_tok if is_prefix(st, rt)]
        if cands:
            maxlen = max(len(st) for _, _, st in cands)
            top = [c for c in cands if len(c[2]) == maxlen]
            if len({c[1] for c in top}) > 1:
                raise ValueError(f"AMBIGUOUS: {row_name} -> {[c[1] for c in top]}")
            name = top[0][1]
            rem = " ".join(row_name.split()[maxlen:])
            return [(name, rem)]
        # alias ruling for the two non-chrome autograph ladders
        if rt[:3] == ["veteran", "class", "autograph"]:
            return [("Veteran Class Autograph Variation", " ".join(row_name.split()[3:]))]
        if rt[:3] == ["rookie", "class", "autograph"]:
            rem = " ".join(row_name.split()[3:])
            return [("Rookie Class Autograph Variation I", rem), ("Rookie Class Autograph Variation II", rem)]
        raise ValueError(f"UNMAPPED: {row_name}")

    # ---- build parallels + pack_odds ----
    pack = {f: {} for f in FMT_ORDER}
    # parallel spec: (subset_id, parallel_name) -> (print_run, exclusivity)
    par_spec = {}
    mapping_report = []  # (row, subset, key_suffix, is_base_tier)
    base_key_count = 0

    for r in rows:
        targets = resolve(r["row"])
        for subset_name, rem in targets:
            sid = name_to_id[subset_name]
            if r["is_base_tier"]:
                if rem.strip():
                    raise ValueError(f"base_tier row has remainder: {r['row']} -> {subset_name} rem='{rem}'")
                suffix = "Base"
                base_key_count += 1
                # base-tier: NO parallel row created here
            else:
                suffix = rem
                key = (sid, rem)
                if key in par_spec:
                    prev = par_spec[key]
                    if prev != (r.get("print_run"), r.get("exclusivity")):
                        raise ValueError(f"parallel conflict {subset_name}/{rem}: {prev} vs {(r.get('print_run'), r.get('exclusivity'))}")
                else:
                    par_spec[key] = (r.get("print_run"), r.get("exclusivity"))
            okey = f"{subset_name} {suffix}"
            for fmt_name, val in r["odds"].items():
                if fmt_name not in FMT:
                    raise ValueError(f"unknown format {fmt_name} in {r['row']}")
                if "," in str(val):
                    raise ValueError(f"comma in odds value {val} ({r['row']})")
                pack[FMT[fmt_name]][okey] = val
            mapping_report.append((r["row"], subset_name, okey, r["is_base_tier"]))

    # extra Base /25 rows for the two multi-sig subsets
    for subset_name, pname, pr in EXTRA_BASE:
        sid = name_to_id[subset_name]
        key = (sid, pname)
        if key in par_spec:
            raise ValueError(f"extra Base collides: {subset_name}/{pname}")
        par_spec[key] = (pr, None)

    # ---- write parallels ----
    for (sid, pname), (pr, ex) in par_spec.items():
        db.execute("INSERT INTO parallels (insert_set_id, name, print_run, exclusivity) VALUES (?,?,?,?)",
                   (sid, pname, pr, ex))

    # ---- write pack_odds (drop empty formats, keep order) ----
    pack_final = {f: pack[f] for f in FMT_ORDER if pack[f]}
    db.execute("UPDATE sets SET pack_odds=? WHERE id=?", (json.dumps(pack_final), SET_ID))

    # ---- gates ----
    fail = []
    all_keys = set()
    for f in pack_final.values():
        all_keys |= set(f.keys())
    if len(all_keys) != 274:
        fail.append(f"pack_odds distinct inner keys={len(all_keys)} exp 274")
    nbase = sum(1 for k in all_keys if k.endswith(" Base"))
    if nbase != 36:
        fail.append(f"base-tier keys={nbase} exp 36")

    npar = db.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=?", (SET_ID,)).fetchone()[0]
    if npar != 240:
        fail.append(f"parallel rows={npar} exp 240")
    npr = db.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=? AND p.print_run IS NOT NULL", (SET_ID,)).fetchone()[0]
    if npr != 208:
        fail.append(f"print_run non-null={npr} exp 208")
    nex = db.execute("SELECT COUNT(*) FROM parallels p JOIN insert_sets i ON i.id=p.insert_set_id WHERE i.set_id=? AND p.exclusivity IS NOT NULL", (SET_ID,)).fetchone()[0]
    if nex != 16:
        fail.append(f"exclusivity set={nex} exp 16")

    # format keys subset check
    for f in pack_final:
        if f not in FMT_ORDER:
            fail.append(f"unexpected format outer key {f}")

    print(f"pack_odds formats: {list(pack_final.keys())}")
    print(f"distinct inner keys={len(all_keys)}  base-tier keys={nbase}")
    print(f"parallels: total={npar} print_run_nonnull={npr} exclusivity={nex}")

    if fail:
        db.rollback()
        print("\nINTEGRITY GATE MISMATCHES (rolled back):")
        for m in fail:
            print("  ", m)
        raise SystemExit(1)

    db.commit()
    print("\nINTEGRITY GATES: all pass. Committed.")

    # mapping report for the two alias families
    print("\n=== created parallels grouped by subset ===")
    for iid, name in subs:
        prs = db.execute("SELECT name, print_run, exclusivity FROM parallels WHERE insert_set_id=? ORDER BY id", (iid,)).fetchall()
        if prs:
            print(f"\n{name} ({len(prs)}):")
            for pn, pr, ex in prs:
                print(f"   {pn:<28} run={pr if pr is not None else '-':<6} excl={ex or '-'}")
    db.close()


if __name__ == "__main__":
    main()
