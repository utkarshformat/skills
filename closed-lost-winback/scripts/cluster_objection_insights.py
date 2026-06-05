#!/usr/bin/env python3
"""
Theme-cluster Format "Buying objections" (or similar) insights into loss drivers.

Why this exists: search_insights returns hundreds of verbatim quotes with no
theme tags (the topic is per-conversation; aggregation happens downstream — see
references/format-winback-playbook.md). Large pulls overflow the tool result and
get saved to files. This script reads one or more of those saved JSON files (or a
raw JSON list), filters by date, classifies each quote into a loss-driver theme,
and prints ranked counts + representative quotes with share links — the input to
the "all-accounts" objection analysis and its lens-brief chart.

Usage:
    python cluster_objection_insights.py <file1.json> [file2.json ...] [--since YYYY-MM-DD]

Each input file is the saved output of a search_insights call: either
{"insights": [...]} or a bare list. Insights need: timestamp, quote, context,
company{name}, person{name}, shareUrl.
"""
import sys, json, argparse
from collections import defaultdict, Counter

# Loss-driver taxonomy. Order matters only for display; classification is by
# keyword-hit count (highest wins), so keep keywords specific to each driver.
THEMES = [
    ("Budget & fiscal timing", ["budget", "fiscal", "fund", "funding", "afford", "deficit",
        "next year", "fy2", "fy '2", "dollars", "money", "cut our budget", "cost", "expensive",
        "price", "can't pay", "can't spend"]),
    ("Authority / approval gate", ["board", "commission", "council", "committee", "approv",
        "procurement", "purchasing", "director", "sign off", "sign-off", "rfp", "it department",
        "auditor", "vote", "authority", "legal", "put out a bid"]),
    ("Competitor / incumbent / status-quo", ["already have", "already in place", "we use",
        "existing system", "in place", "another vendor", "other vendors", "competitor",
        "quote in hand", "not interested in something new", "satisfied", "service request platform"]),
    ("Product / integration fit", ["integrat", "cama", "infocon", "legacy", "cisco",
        "phone system", "metes and bounds", "doesn't handle", "technical", "voip", "api", "sync"]),
    ("Size / volume fit", ["too small", "small city", "small department", "small county",
        "don't have the volume", "not enough", "low volume", "call volume", "not that burdensome",
        "don't have a need", "very many calls"]),
    ("AI trust / constituent readiness", ["ai bot", "chatbot", "automated", "actual human",
        "talk to a person", "real person", "suspicious of ai", "aging population", "want a human"]),
    ("Champion / staffing / capacity", ["retire", "retirement", "drop", "new pio", "new director",
        "bandwidth", "fatigue", "capacity", "staff time", "no support", "short-staffed", "busy",
        "vacation", "too quick", "new here", "just switched", "covered up"]),
]


def load(files):
    out = []
    for fn in files:
        d = json.load(open(fn))
        out += d.get("insights", d if isinstance(d, list) else [])
    return out


def company(i):
    c = i.get("company") or {}
    return c.get("name") or (i.get("person") or {}).get("name") or "?"


def classify(i):
    t = ((i.get("context") or "") + " " + (i.get("quote") or "")).lower()
    best, best_n = None, 0
    for name, kws in THEMES:
        n = sum(1 for k in kws if k in t)
        if n > best_n:
            best, best_n = name, n
    return best or "Other / general hesitation"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="+")
    ap.add_argument("--since", default=None, help="ISO date; keep insights with timestamp >= this")
    args = ap.parse_args()

    ins = load(args.files)
    if args.since:
        ins = [i for i in ins if (i.get("timestamp") or "")[:10] >= args.since]

    buckets = defaultdict(list)
    for i in ins:
        buckets[classify(i)].append(i)

    total_accounts = len(set(company(i) for i in ins))
    print(f"{len(ins)} insights | {total_accounts} distinct accounts"
          + (f" | since {args.since}" if args.since else ""))
    print()
    for name in sorted(buckets, key=lambda k: -len(buckets[k])):
        items = buckets[name]
        n_acct = len(set(company(i) for i in items))
        print(f"### {name} — {len(items)} moments, {n_acct} accounts")
        for i in sorted(items, key=lambda x: len(x.get("quote") or ""))[:3]:
            q = (i.get("quote") or "").replace("\n", " ")
            q = q[:140] + ("…" if len(q) > 140 else "")
            sid = (i.get("shareUrl") or "").rstrip("/").split("/")[-1]
            print(f'   - [{company(i)}] "{q}"  ({sid})')
        print()


if __name__ == "__main__":
    main()
