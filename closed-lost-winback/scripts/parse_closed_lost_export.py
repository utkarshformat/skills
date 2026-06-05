#!/usr/bin/env python3
"""
Parse a CRM closed-lost opportunities export (CSV or XLSX) into clean JSON.

Why this exists: Salesforce "opportunity" reports are exported as a GROUPED
report. The first opportunity under each grouping (e.g. a campaign/conference)
sits on the same row as the group label, so its data columns are shifted right
by however many group columns precede it; subsequent rows in that group are not
shifted. Absolute column indexing therefore breaks.

The robust trick: don't index by absolute column. Anchor on the Stage cell.
Stage values follow a recognizable pattern ("9.0 - Qualified Out (Closed Lost)",
"1.0 - Discovery", etc.). Once we find the Stage cell in a row, every other
field sits at a FIXED OFFSET from it (the canonical Salesforce opp-report column
order), regardless of how far the row was shifted by grouping.

Usage:
    python parse_closed_lost_export.py <file.csv|file.xlsx> [--all] [--out path.json]

    --all   keep every stage, not just Closed Lost (useful for the win-back
            comparison set: open opps that raised the same objection).
    --out   write JSON to a file instead of stdout.

Output: JSON list of opp dicts:
    {account, opportunity, stage, owner, amount, created, close, next_step, conference}
"""
import sys, csv, json, re, argparse, datetime

# Canonical Salesforce opp-report column order, expressed as OFFSETS from the
# Stage column. Derived from the header row at runtime when possible; these are
# the fallback defaults matching the standard layout.
DEFAULT_OFFSETS = {
    "owner": 2,          # "Opportunity Owner"
    "account": 3,        # "Account Name"
    "opportunity": 4,    # "Opportunity Name"
    "amount": 6,         # "Amount"
    "close": 9,          # "Close Date"
    "created": 10,       # "Created Date"
    "next_step": 11,     # "Next Step"
}

# Header labels we try to locate (lowercased substring match) to derive offsets.
HEADER_LABELS = {
    "owner": "opportunity owner",
    "account": "account name",
    "opportunity": "opportunity name",
    "amount": "amount",
    "close": "close date",
    "created": "created date",
    "next_step": "next step",
}

STAGE_RE = re.compile(r"^\s*\d+(\.\d+)?\s*-\s*\S")  # "9.0 - Qualified Out ..."
STAGE_WORDS = ("closed lost", "qualified out", "discovery", "demo",
               "proposal", "procurement", "closed won", "negotiation")
LOST_MARKERS = ("closed lost", "qualified out")


def load_rows(path):
    if path.lower().endswith((".xlsx", ".xlsm")):
        import warnings
        warnings.filterwarnings("ignore")
        import openpyxl
        wb = openpyxl.load_workbook(path, data_only=True)
        ws = wb.worksheets[0]
        return [[c for c in row] for row in ws.iter_rows(values_only=True)]
    else:
        with open(path, newline="", encoding="utf-8-sig") as f:
            return [row for row in csv.reader(f)]


def cell(v):
    if v is None:
        return ""
    if isinstance(v, (datetime.datetime, datetime.date)):
        d = v.date() if isinstance(v, datetime.datetime) else v
        return d.isoformat()
    return str(v).strip()


def parse_date(s):
    s = cell(s)
    if not s:
        return ""
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y"):
        try:
            return datetime.datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            pass
    return s


def find_stage_index(row):
    """Return the column index of the Stage cell, or None."""
    for i, v in enumerate(row):
        t = cell(v).lower()
        if not t:
            continue
        if STAGE_RE.match(cell(v)) or any(w in t for w in STAGE_WORDS):
            return i
    return None


def derive_offsets(rows):
    """Find the header row and derive field offsets relative to 'Stage'."""
    for row in rows:
        cells = [cell(v).lower() for v in row]
        if "stage" in cells:
            s = cells.index("stage")
            offsets = {}
            for key, label in HEADER_LABELS.items():
                idx = next((i for i, c in enumerate(cells) if label in c), None)
                if idx is not None:
                    offsets[key] = idx - s
            # fall back to defaults for anything not found in the header
            return {**DEFAULT_OFFSETS, **offsets}
    return dict(DEFAULT_OFFSETS)


def parse(path, keep_all=False):
    rows = load_rows(path)
    offsets = derive_offsets(rows)
    # Track the current grouping label (often a campaign/conference) so we can
    # attribute it when present. The group label tends to sit to the LEFT of the
    # Stage cell on group-header rows.
    out = []
    current_group = ""
    for row in rows:
        s = find_stage_index(row)
        if s is None:
            continue
        stage = cell(row[s])
        # Skip subtotal/count artifact rows.
        if stage.lower() in ("count", "subtotal", "grand total"):
            continue

        def get(key):
            i = s + offsets.get(key, DEFAULT_OFFSETS.get(key, 0))
            return cell(row[i]) if 0 <= i < len(row) else ""

        # Capture a group label if anything meaningful sits left of Stage.
        left = [cell(v) for v in row[:s] if cell(v) and cell(v) not in ("2026", "Conference")]
        if left:
            current_group = left[-1]

        stage_l = stage.lower()
        if not keep_all and not any(m in stage_l for m in LOST_MARKERS):
            continue
        amount = get("amount").replace("$", "").replace(",", "")
        out.append({
            "account": get("account"),
            "opportunity": get("opportunity"),
            "stage": stage,
            "owner": get("owner"),
            "amount": amount,
            "created": parse_date(get("created")),
            "close": parse_date(get("close")),
            "next_step": get("next_step"),
            "conference": current_group,
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--all", action="store_true", help="keep all stages, not just closed-lost")
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    opps = parse(args.file, keep_all=args.all)
    payload = {"count": len(opps), "opportunities": opps}
    text = json.dumps(payload, indent=2)
    if args.out:
        with open(args.out, "w") as f:
            f.write(text)
        print(f"Wrote {len(opps)} opps -> {args.out}")
    else:
        print(text)


if __name__ == "__main__":
    main()
