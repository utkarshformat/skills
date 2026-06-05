---
name: closed-lost-winback
description: >-
  Turn a CRM export of closed-lost / lost opportunities into an evidence-backed
  win-back tracker, using customer conversation data from the Format MCP. Cross-
  references each lost deal's recorded calls against the rep's CRM note and flags
  where the conversation DISAGREES with what the rep logged — the part a sales
  leader can't get from their own notes. Produces a RAG-rated (🟢/🟡/🔴) per-account
  table with reasons, evidence, and a turn-around play, plus an optional Format
  Lens Brief (useformat.ai link). USE THIS whenever the user wants to analyze
  closed-lost or lost deals, understand "why did we lose", build a win-back or
  re-engagement list, reactivate dead deals, run a loss/post-mortem analysis, or
  work a list of lost opportunities from events/conferences — even if they don't
  name Format. Triggers: "closed lost", "why did we lose these", "win-back",
  "lost deals", "lost opps", "deals that didn't close", "re-engage lost accounts",
  "loss reasons", "post-mortem on lost deals".
---

# Closed-Lost Win-Back Analysis

## What this does and why it's shaped this way

A sales leader hands you a CRM export of deals they lost and asks "why?" and "which can I win back?". The trap is to hand their own notes back to them — they wrote those, it's zero value. **The only thing they can't get themselves is where the actual recorded conversation says something different than the rep logged.** That delta is the product. Everything below is built to surface it honestly.

This skill joins two sources:
- **The CRM export** = the source of truth for *which* deals are closed-lost, the dollar value, and the rep's "Next Step" note. Format has no deal-stage/CRM data, so this export is **required** — never try to infer "closed-lost" from Format alone.
- **The Format MCP** (customer conversation data: calls, emails, insights) = the source of truth for *what the customer actually said*.

## When to use

Any closed-lost / lost-deal / win-back / loss-post-mortem request where you have access to the customer's Format org. Two modes — pick by what the user has and asks for:

- **Mode A — per-account win-back** (the default). The user hands you a CRM export of *specific* lost deals and wants to know why each closed and which to win back. Requires the export (it's the source of truth for "lost"). → Steps 1–6 below.
- **Mode B — all-accounts objection analysis.** No export, broader ask: "what's killing deals lately," a loss/objection theme report across *everyone* in a time window. Reads the objection topic straight from Format and themes it. → See "Mode B" near the end.

If the user wants per-account "why did THESE close" and has no export, ask for it — Mode A can't run without it.

## Required inputs

1. **A CRM export** (CSV or XLSX) of the lost opportunities. Often a grouped Salesforce report.
2. **Format org access** via the Format MCP. Confirm the org with `list_organizations`; the user will tell you which customer.

If either is missing, say so and stop — don't fabricate.

## Workflow

### Step 1 — Parse the export
Run the bundled parser; it handles the fiddly grouped-report column-shift so you don't reinvent it each time:
```
python scripts/parse_closed_lost_export.py <export.csv|xlsx> --out /tmp/lost.json
```
It anchors on the Stage cell and emits closed-lost opps with `account, opportunity, stage, owner, amount, created, close, next_step, conference`. (Add `--all` to also pull open opps — useful as the win-back comparison set in Step 4.) If the parse looks wrong (0 rows, garbled fields), open the file, find the header row and the Stage column, and adjust — every CRM export is a little different.

### Step 2 — Resolve each account to Format (fuzzy, expect partial coverage)
Account names in the export ("Baldwin County, AL - Front Desk") rarely match Format company names exactly. For each account:
- Strip dept/product suffixes and state codes ("- County Clerk", "- Front Desk", ", AL") down to the core name.
- Try `list_companies` `nameSearch` (core name) and `domainSearch` (guess the .gov/.us domain).
- If no company, try `list_persons` `emailSearch` (town token, e.g. "cedarburg") and `nameSearch` (a contact named in the note).
- Bucket each account: **has-call / no-call / no-match**.

Read `references/format-winback-playbook.md` for the exact matching tactics and tool params.

### Step 3 — Pull conversations for matched accounts
For accounts that resolved, `list_records` (by `companyIds` + a `dateRange` from a bit before `created` to a bit after `close`; **dateRange needs full ISO datetimes**). For records, prefer existing insights via `search_insights` (by `companyIds` / `topicNames`); when insights are thin, `get_record` with `includeInsights: true` to read the transcript directly.

### Step 4 — Build the per-account reason, and flag note-vs-call deltas
This is the core. For each account:
- If **no call**: the reason is the rep's CRM note, labeled honestly as `(rep note — no recorded call)`. Do not dress it up as proof.
- If **a call exists**: compare what the customer actually said to the rep's note. **Lead with the delta** where they disagree (e.g. "marked Closed Lost, but the call shows a timing hold until July, not a loss"). Quote the customer verbatim and link the record/insight.

### Step 4b — Win-back: the objection is the way-pointer
To find *how to beat* a given objection, don't hunt for a "turnaround" insight or topic — there isn't one, and you don't need it. Use the objection itself as a pointer to where someone already beat it:

1. Take the lost account's objection insight and call `search_insights` with **`similarToInsightId`** (falls back to semantic) — or `semanticQuery` — to surface the *same objection* across other deals.
2. Among those, find the ones that **advanced** — the insight's `followUp` shows a next step booked, or the account sits in a later pipeline stage. Those are your pointers.
3. **`get_record` that conversation and read the source** — how did the rep actually counter it? Lift that language as the play for the lost account.

This works because a well-handled objection lives in the *source transcript* of a deal that kept moving, not in a separate signal. Example: Omro's "a new system may already cover this" → matched Riverside County's "we already have Fresh Service + IVR," which advanced → the source call shows the rep reframing the product as a *layer that unifies* existing systems, a maintenance-trap rebuttal, and a low-commitment after-hours rollout. That becomes Omro's win-back move.

### Step 5 — RAG + turn-around play
Rate each account by winnability and write one concrete next move:
- 🟢 **act now** — a real re-engagement trigger or active warming (budget cycle date, champion change, "circle back in X", call already resuming).
- 🟡 **revivable** — had genuine engagement but stalled with no clear trigger; needs re-qualification.
- 🔴 **low odds** — never engaged (no-show/ghost) or structurally disqualified (too small, lost on price, integration impossible). Still give one re-attempt-then-stop move.

### Step 6 — Output
Produce the tracker (see "Output format"). Offer the optional Lens Brief.

## Output format — default is a markdown report (inline + a `.md` file)

The default deliverable is **markdown**: render it inline in chat and also save a `.md`. That's what to produce unless the user explicitly asks for a spreadsheet, a PDF, or a Format Lens Brief (all optional — see below). Keep it self-contained and shareable; no walls of text. Use this structure (it mirrors what a sales leader actually wants):

1. **Exec summary** — a one-line headline thesis + 3–5 bullets: the dominant loss pattern, the biggest $ at risk, the "not now" deferrals worth re-approaching, and a one-line honest caveat on coverage.

2. **Scope & coverage** *(required — this is what stops the reader being confused)* — be explicit and upfront: how many opportunities were reviewed, how many had a recorded conversation, how many of those gave a *usable customer reason*, and the date range the conversations span. State plainly that the remaining accounts had no recorded conversation, so their reason comes from the rep's CRM note. If you also ran a broader objection pull, cite the count ("N insights across M accounts over <period>") so the reader sees the engine works at scale and the gap is specific to these deals.

3. **Account-by-account table** — one row per account, with columns the reader can act on:

   `Event attended | Account | $ | Closed-lost reason | Indicative quote | Source`

   - **Event** comes from the export's campaign/grouping (the parser captures it).
   - **Indicative quote** = the customer's verbatim words + a link where a call exists; otherwise the rep's CRM note — and the **Source** column says which (`customer call` vs `rep CRM note`). Never present a rep note as a customer quote.
   - Optional extra columns to go deeper: `Win-back (RAG 🟢/🟡/🔴)` and `Suggested next move`.
   - Where a recorded call *contradicts* the rep note, call it out — that delta is the highest-value finding.

4. **Short closing summary** — the single takeaway + where to start.

See `assets/example-winback-tracker.md` for a worked example.

## Optional outputs (only when the user asks)

The markdown report above is the default and is itself shareable. Produce these **only on explicit request**:

- **Spreadsheet (.xlsx / .csv):** the same account-by-account columns — good when the user wants to filter/sort or get their own sheet handed back enriched. Build with openpyxl; color the RAG column.
- **Format Lens Brief (useformat.ai link):** a live Format artifact with clickable insight chips + an optional bar chart (`create_lens_brief`, `validateOnly: true` first; add a chart via `insert_block`, `chartType: "bar"`). Tier-gated per org (INSUFFICIENT_TIER = a superadmin toggle, not your error); `{{insight:<id>}}` chips only render in the org that **owns** the insight. See `references/format-winback-playbook.md`.
- **Branded PDF:** via the format-branding skill's `scripts/format_pdf.py` (markdown → branded PDF, cover + customer logo). Caveat: its styles map bold but not italic — keep `*italic*` out of the source markdown or it errors.

## Mode B — all-accounts objection analysis

When there's no export and the ask is broad ("why are we losing deals lately", a loss/objection report across everyone):

1. `search_insights` the objection topic (e.g. `topicNames: ["Buying objections"]`) at `level: 0` over the window. Large pulls overflow the tool result and auto-save to a file — page through (`offset` 0, 200, 400…) and let them land as files.
2. Run `python scripts/cluster_objection_insights.py <saved-file(s)> --since <YYYY-MM-DD>` to filter by date, theme-cluster, and print ranked drivers + representative quotes with share-link IDs. (Don't hand-cluster hundreds of quotes in context — the script does it deterministically and is reusable.)
3. Publish a Lens Brief: a `callout` thesis, a "picture" `text` with inline `{{insight:<id>}}` chips, a **bar `chart`** of moments-by-driver, a theme `table`, and a few `insight` blocks for color. Lead with the through-line (for gov/SMB it's almost always *money + permission > product*).

Note: this reads *objections raised in conversations*, not CRM-confirmed closed-lost (Format has no deal stage) — frame it as "loss/objection signals across active deals," and say so in the brief.

## The honesty rules (do not break these — they're the whole credibility of the deliverable)

1. **Never hand back the rep's note as if it were proof.** Label every row `customer-proven` (a real quote + link exists) vs `rep note only`. The delta in coverage is itself a finding.
2. **Expect partial coverage and say so.** Most lost deals — especially no-shows/ghosts — have NO recorded call in Format, because the deal died before anyone got on a call. Report how many of N are customer-verifiable up front.
3. **Processing/reprocessing a topic can't conjure missing conversations.** It only extracts from calls that were recorded. If coverage is thin, the fix is recording hygiene (Gong/Fathom), not a wider processing window. (See `references/format-winback-playbook.md`.)
4. **The export is the source of truth for "lost," not Format.** Always require it.

## Customer context (swap per engagement)
Defaults are tuned for **JustAppraised** (`org_qubeqqxpzb63zzjuwfp4w3el`, gov-sector buyers, existing topic "Buying objections"). For a different Format customer, swap the org ID, the export schema if it differs, and the relevant topic names — the workflow is identical. Gov/SMB sales motions tend to lose on *timing, budget, and approval gates* far more than on product; weight your reasons accordingly but let the data lead.
