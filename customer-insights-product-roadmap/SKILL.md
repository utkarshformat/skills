---
name: customer-insights-product-roadmap
description: Use when a product manager wants to generate a product roadmap from customer conversation data. Triggers include "build me a roadmap", "what should we build next", "turn our customer feedback into a roadmap", "prioritize features from customer calls", "what do customers actually want", "roadmap from customer insights", "quarterly roadmap from feedback", or "help me decide what to ship next". This skill uses the Format MCP to produce an opinionated, evidence-backed Now / Next / Later roadmap with a "considered and rejected" section and signal-vs-noise notes. Runs end-to-end in one response. Not for roadmaps with no customer data, writing PRDs, or drafting release notes.
---

# Customer Insights Product Roadmap

## Execution principle

This skill runs silently and completes in a single response. When invoked, Claude's immediate next action is a tool call — not a chat message. No scoping questions. No opening statement. No progress narration. No "want me to continue?" prompts.

The skill infers everything it needs from Format MCP data, clusters a sample of quotes into themes semantically, writes the roadmap, saves the file. Done.

The document is the deliverable. Everything else is noise.

---

## Hard constraints

- **Total tool-call budget: 10.** Hard cap.
- **Runs in one turn.** If the skill ever feels like it needs to say "continue" — it's wrong. Scope narrower instead.
- **Never claim determinism the skill can't deliver.** The sample is not the full corpus. The top themes are stable across reruns because dominant signal in a large corpus recurs constantly — but don't pretend the numbers are precise.

---

## What Claude infers (instead of asking)

| What | How |
|---|---|
| Product principles | Extracted from positive-feedback themes — what the product is already winning on. Surface with verbatim quote per principle. |
| Motion (PLG / Enterprise / Dual) | Inferred from deal-size mentions and account tier language. ≥70% one direction = call it. Otherwise "Dual." |
| Current OKR anchor | Inferred from signal density — churn-heavy = Retention. Activation-heavy = Activation. Expansion-heavy = NRR. New-logo-heavy = Growth. |
| Competitor set | From Competitors topic in Format if it exists (≥10 insights). Otherwise skip the competitor-chasing check — do not burn web searches. |
| Company slug | Lowercase, hyphenated. "Granola" → `granola`. |

Surface all four inferences at the top of the roadmap with one-line provenance. PM reads, spots anything wrong, replies in one line, skill reruns. No upfront friction.

---

## The run

### Step 1: Orient (3 calls)

```
list_organizations()                    → get orgId
list_topics(orgId)                      → see what exists
count_insights(orgId)                   → total corpus size for the header
```

### Step 2: Pull the sample (5 calls, parallel)

60 insights per topic across the 5 ranking topics. No pagination. No offset. No "let me get more."

```
search_insights(orgId, topicName: "Feature Requests",                 select: "analysis", limit: 60)
search_insights(orgId, topicName: "Feature Requests and Workarounds", select: "analysis", limit: 60)
search_insights(orgId, topicName: "Negative Product Feedback",        select: "analysis", limit: 60)
search_insights(orgId, topicName: "Expansion and Contraction Signals", select: "analysis", limit: 60)
search_insights(orgId, topicName: "Positive Feedback",                select: "analysis", limit: 60)
```

Skip any topic that doesn't exist or has fewer than 20 insights. Don't substitute other topics.

### Step 3: One skew check (1 call)

```
count_insights(orgId, filters: { topicName: "Feature Requests" }, groupBy: "company")
```

Used to detect account dominance for the signal-vs-noise section. One call is enough — dominance patterns across topics correlate heavily.

### Step 4: Optional competitor context (0–1 calls)

If the Format workspace has a `Competitors and Alternative Solutions` topic with ≥10 insights, pull 30 insights from it:

```
search_insights(orgId, topicName: "Competitors and Alternative Solutions", select: "analysis", limit: 30)
```

If no competitor topic exists, skip. Don't run web searches — the budget doesn't allow it.

**Total tool calls: 9–10. Done.**

### Step 5: Synthesize

All clustering, theme extraction, principle inference, moat testing, failure-mode checks, 70/20/10 allocation, and document writing happens internally. No more tool calls.

---

## Processing rules

### Semantic clustering — no fixed taxonomy

Cluster the ~300 sampled quotes into 8–15 themes. A theme is a Job-to-be-Done, not a feature request. If customers ask for CSV export + API + Zapier, the theme is "share platform data with external tools."

**Look for these patterns because they show up in every B2B SaaS dataset** — if the underlying quotes exist, they should be themes:

- "Different readers need different cuts" (per-role, per-team, per-module reports)
- "Who said this / which account / when" (attribution, rep names)
- "Is this real or one loud customer" (frequency, counts, quantification)
- "Meet me where I work" (Slack, email, CRM delivery)
- "Let me self-serve" (ad-hoc queries, MCP, custom configs)
- "Ingest my other channels" (Intercom, Zendesk, Slack channels as data sources)
- "Turn insight into action" (Jira/GitHub tickets, alerts)
- "Is this accurate / can I trust it" (hallucinations, confidence, source linking)

These aren't fixed buckets. They're reminders of patterns that easily get under-clustered. If the quotes don't support one, skip it.

### Evidence tiering

- **T2:** 6+ accounts across 2+ source types (sales, support, CS, product). Strong echo.
- **T3:** 2–5 accounts, or 6+ accounts from a single source type. Directional.
- **T4:** 1 account, or no customer quotes (strategic bets).

Now items must be T2. Next can be T3. Later can be T4.

### Segment-weighted volume (qualitative)

Weight quotes by the account behind them:
- Enterprise (named, high ACV in data): high weight
- Active trial / high-intent prospect: high weight
- Churn-risk or contraction-signal account: high weight (retention gold)
- Mid-market PLG customer: medium weight
- Free tier / individual user: low weight

Use **qualitative tags** ("high / medium / low WACV weight") — not numeric scores. The sample doesn't support precise numbers and fake precision erodes trust.

### Principle filter

For each theme, check against the inferred principles. Themes that violate a principle go to "Considered and rejected" with explicit rationale. Never silently drop.

### Failure-mode checks

For each Now candidate, stamp with flags if any apply:

- **Wrapper trap** — could a generic ChatGPT/Claude prompt do this? If yes, flag.
- **Vocal minority** — are >60% of quotes from 1–2 accounts? If yes, flag and deprioritize.
- **Competitor-chasing** — triggered primarily by "competitor X has Y"? Reframe as anxiety about the underlying problem.
- **PLG pollution** — enterprise ask that corrupts self-serve simplicity? If motion is PLG or Dual, flag for isolated enterprise track.
- **Feature factory** — no clear outcome metric attachable? Reject.

2+ flags on a single theme = don't place in Now.

### Moat test (strict)

For each theme, ask: does shipping this create accruing benefit or mounting loss for the user? A moat tag requires explicitly naming what accrues or what's lost on switching.

- Moat: "Each added role cut locks in another user per account. Switching means reconfiguring every role."
- Not a moat: Slack delivery (table-stakes integration). Rep attribution (basic data hygiene). Translation (market expansion, not defensibility).

If 6+ items across all horizons end up with a moat tag, re-check — under-tag is safer than over-tag.

### 70 / 20 / 10 allocation

- **Now (70%):** 4–6 items, T2, clean failure-flag check
- **Next (20%):** 3–4 items, either architectural dependencies of Now or T3 buckets below the Now cut
- **Later (10%):** 2–3 T4 strategic bets. Protected slot — defend against "move this to Now" asks.

### Overlap check

Before finalizing Now items, ensure no two items cite the same quote from the same speaker. If they do, the clustering needs a re-pass — either merge the items or re-split the quotes.

---

## The deliverable

### Document structure

```
# [Company] Product Roadmap

*Generated from a sample of ~300 insights across your [TOTAL]-insight Format workspace. The top themes below are stable across reruns — dominant signal in a corpus this size surfaces in any reasonable sample. The long tail (Next items, some rejections) is directional.*

*Horizon: Now (90d) / Next (90–180d) / Later (exploratory).*

**Inferences** — correct any of these in one line and I'll rerun:

- **Motion:** [PLG / Enterprise / Dual] *(inferred from [one-line signal])*
- **Current OKR anchor:** [Retention / Activation / Expansion / Growth] *(inferred from [one-line signal])*
- **Principles (inferred from positive-feedback patterns):**
  1. **[Principle]** — "[Verbatim quote]" — [Speaker], [Company]
  2. **[Principle]** — "[Verbatim quote]" — [Speaker], [Company]
  3. **[Principle]** — "[Verbatim quote]" — [Speaker], [Company]
  4. **[Principle if found]** — "[Verbatim quote]" — [Speaker], [Company]
- **Competitors watched:** [C1, C2, C3, C4]

---

## At a glance

| Horizon | # | Theme | Evidence | WACV weight | Moat |
|---|---|---|---|---|---|
| Now | 1 | [Theme] | T2 · [N] accts | high / med / low | 🛡️ or — |
| Now | 2 | [Theme] | T2 · [N] accts | ... | ... |
| Now | 3 | [Theme] | T2 · [N] accts | ... | ... |
| Now | 4 | [Theme] | T2 · [N] accts | ... | ... |
| Now | 5 | [Theme if 5th] | T2 · [N] accts | ... | ... |
| Next | 1 | [Theme] | T3 | ... | ... |
| Next | 2 | [Theme] | T3 | ... | ... |
| Next | 3 | [Theme] | T3 | ... | ... |
| Later | 1 | [Bet] | T4 | — | ... |
| Later | 2 | [Bet] | T4 | — | ... |

**The shape of this quarter:**

- **The bet:** [One line on what the Now-set is collectively pointing at.]
- **Biggest moat-deepeners:** [2–3 items with accruing-benefit dynamics.]
- **Biggest silent-churn risks:** [2–3 named accounts with one-line tell.]
- **One deferred decision:** [Surfaced in Later — a doubled-down vs defocus choice if one exists.]
- **Protected bets:** [The 10% the skill is asking you to defend.]

---

## Roadmap summary

[2–3 sentences: what the data is saying, the 1–2 biggest themes, the most surprising finding.]

---

## Now — next 90 days (70% capacity)

### 1. [Theme name — phrased as JTBD, not feature]

**Evidence:** T2 · [N] accts · WACV weight [high/med/low] · Sources: [sales, support, CS]
**Segment driver:** [Enterprise / PLG / Dual]
**Outcome metric:** [What this moves — tie to the inferred OKR]
**Flags:** [flags or ✅ clean]
**Moat:** [🛡️ with explicit reason, or —]

**What customers are saying:**

> "[Verbatim quote]" — [Speaker], [Company], [Source], [Date]

> "[Verbatim quote]" — [Speaker], [Company], [Source], [Date]

**Why this is Now:** [1–2 sentences — what the evidence says + why it passes the principle filter + why it moves the OKR]

**What to announce when shipped:** [One-sentence customer-facing announcement draft]

---

### 2. [Next theme — same structure]

[4–6 items total in Now]

---

## Next — 90–180 days (20% capacity)

### 1. [Theme]

**Evidence:** T3
**Why it's here:** [Usually adjacent platform/debt — supports Now. Explain the connection.]
**What to watch for:** [What would promote this to Now?]

[3–4 items in Next]

---

## Later / Strategic bets — protected 10%

### 1. [Bet]

**Why this earns space:** [Strategic logic — model layer, moat, market timing. May have no customer quote; that's the point.]
**What we're protecting:** [What would get cut if this lost its slot]

[2–3 items in Later]

---

## Considered and rejected

| Theme | Volume | Why rejected |
|---|---|---|
| [Theme] | [N accts] | [Which principle it violated or which flag killed it] |
| [Theme] | [N accts] | [Rationale] |
| [Theme] | [N accts] | [Rationale] |

---

## Signal-vs-noise notes

**Accounts dominating the feedback stream:**

For each account contributing >10% of the Feature Requests volume, split their asks:

- **[Account]:** [N quotes].
  - **Echoed by others:** [their asks that also appear in ≥2 other accounts — high-signal]
  - **Unique to this account:** [asks that ONLY this account made — skew risk]
  - **Skew verdict:** [distorting or not, with why]

**Silent-churn flags worth investigating:**

- [Account or theme]: [what's quietly going wrong — contraction language, engagement decline, increasingly formal CS replies]

**Competitor-anxiety themes (reframed):**

- Customers mention [competitor] in context of [X]. The root anxiety is [underlying JTBD], not the feature itself. Don't ship the feature — solve the anxiety.

---

## Audience re-reads

Same roadmap, different framings. Hard limit: 1–2 sentences each.

**Board / Exec:** [Business-outcome framing. NRR, moat, ACV, strategic bets. Name the 1 initiative that matters most for the thesis.]

**Engineering:** [Architectural dependencies, the Next-column debt that unblocks Now, where AI-layer shifts could reshape the plan.]

**Sales & CS:** [Which Now items unlock which deals. Directional timing, no hard dates.]

**Public / Customers:** [Themes not features. No dates. Acknowledge the feedback that shaped it.]
```

### Paste compatibility

The output must paste cleanly into Notion, Linear docs, Confluence, Google Docs, and Slack canvases:

- `---` horizontal rules only (not `***` or `___`)
- Lists stay one level deep (no indented sub-bullets)
- Tables stay ≤6 columns
- Each blockquote on its own line with blank line before and after
- Use `·` (middle dot) or ` — ` (em dash) as inline separators — not `|`
- No emoji in headings (🛡️ ⚠️ in body text is fine)
- No trailing spaces or hard line breaks

### File-saving

After rendering inline:

1. Write to `/mnt/user-data/outputs/[company-slug]-roadmap.md`
2. Call `present_files` with the path

Company slug: lowercase, hyphenated.

---

## Scope boundaries

- Opinionated Now/Next/Later structure — no RICE/Kano/WSJF alternatives
- No PRDs, Jira epics, or release notes — out of scope
- No Gantt charts, hard dates, calendar commitments
- No framework name-drops in the output (Fygurs tier, Hierarchy of Engagement, 70:20:10 are internal to the skill, not the deliverable)
- No methodology footer — document stands alone

## Quality bar before shipping

- **Zero chat output** between the user's request and the finished roadmap — first action is a tool call
- **10 tool calls max.** Exceeds budget → scope narrower, don't run extra calls
- **Completes in one turn.** No "continue" prompts
- Header shows true corpus size from `count_insights(orgId)`, not a guess
- Inferences block at the top with provenance on each
- Principles cite verbatim quotes with speaker + company
- At-a-glance scan table + 5-line narrative immediately after the inferences
- 4–6 Now items, 3–4 Next, 2–3 Later
- No two Now items share the same supporting quote
- Moat tags strict — explicit "what accrues / what's lost on switching"
- Now items are ~150–200 words each
- 3+ items in Considered-and-rejected with clear rationale
- Signal-vs-noise uses unique-vs-echoed split for dominant accounts
- Audience re-reads hit 1–2 sentence cap
- Paste-compatibility rules followed
- Markdown file saved to `/mnt/user-data/outputs/[company-slug]-roadmap.md` and presented via `present_files` as final action
