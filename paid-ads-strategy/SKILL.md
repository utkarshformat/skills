---
name: paid-ads-strategy
description: Use when planning or diagnosing a paid advertising strategy — channel selection, audience targeting, campaign structure, budget allocation, retargeting design, or performance diagnosis — grounded in real customer language from Format. Trigger phrases include "paid ads strategy", "which channel should I run", "LinkedIn vs Google", "who should I target", "build a retargeting plan", "audit my ads", "our CPA is too high", "why aren't our ads converting", "paid media plan", "campaign structure", "ad budget allocation", or "set up paid ads". This skill uses the Format MCP to ground targeting, angles, and exclusions in real customer signals — so the plan is evidence-backed, not gut-felt. Runs end-to-end in one response. For writing the ad copy itself, use paid-ads-copy. Not for landing page design or tracking implementation — those are downstream.
---

# Paid Ads Strategy

## Execution principle

This skill runs silently and completes in a single response. When invoked, Claude's immediate next action is a tool call — not a chat message. No scoping questions, no opening statement, no progress narration, no "want me to continue?" prompts.

The skill pulls customer signal from Format, infers ICP / buying committee / channel fit / competitive pressure, and writes a paid ads strategy grounded in that signal. Done.

The document is the deliverable. Everything else is noise.

---

## What this skill produces

A single markdown file with seven sections:

1. **Strategy snapshot** — the one-page summary of what channel to run, who to target, what angle wins, and what success looks like
2. **Channel recommendation** — which channels fit this product and buyer, ranked, with evidence
3. **Targeting plan** — firmographics, job titles, intent signals, lookalike seed, exclusions
4. **Campaign structure** — account architecture, naming conventions, initial budget split
5. **Angle portfolio** — 3–5 distinct angles for the creative team to adapt, each tied to a customer quote
6. **Retargeting plan** — funnel stages, windows, frequency caps, exclusions
7. **Measurement plan** — primary metric, secondary metrics, attribution approach, week-by-week review cadence

One document. Section headers use human labels — never "Artifact 1, Artifact 2."

---

## Hard constraints

- **Total tool-call budget: 10.** Hard cap.
- **Runs in one turn.** If it feels like it needs to say "continue" — scope narrower instead.
- **Every strategic claim must trace to Format data.** If the data says "most best-fit buyers are VP Sales at 50–200 person SaaS," say that. If the data doesn't support a claim, don't make it.
- **No copy production.** This skill briefs the creative team — it doesn't write ads. If the user needs copy, point to `paid-ads-copy` at the end.
- **No landing page design, visuals, or tracking implementation.** Those are downstream skills.

---

## When to use

- Before launching a new paid channel
- Diagnosing why existing paid campaigns aren't working
- Entering a new vertical or persona and planning paid from scratch
- Reviewing a paid plan built without customer data
- Briefing an agency before they start

## When NOT to use

- Writing ad copy or headlines — use `paid-ads-copy`
- Designing landing pages — separate skill
- Setting up conversion tracking, pixels, UTMs — separate skill
- Creative briefs for visuals — separate skill
- Fewer than 30 relevant conversations in Format — not enough signal for a grounded plan

## Setup

If Format MCP isn't connected yet:
1. Settings → Connectors → Add custom connector
2. URL: `https://useformat.ai/api/mcp`
3. Authenticate with your Format account

---

## The run

### Step 0: Check for shared company context (silent, 0 calls)

Look for `company-context.md` in the working directory or `/mnt/user-data/uploads/`. If present, read it and use the ICP, personas, competitive landscape, and brand voice sections to frame the run — skip re-deriving those from Format. Still pull paid-specific signal live (pre-purchase language, retargeting triggers, pain points fresh enough for creative).

If the file exists, note it silently in the header block: `Company context loaded from company-context.md (last refreshed [date]).` Do not announce it mid-run.

If not present, proceed with the full topic queries below. No prompt, no offer to run the other skill — the user can run `customer-insights-company-context` separately if they want.

**When reusing quotes from `company-context.md`:** keep attribution intact (speaker, company, source, date). Do not launder quotes as synthesized claims.

### Step 1: Orient (3 calls)

```
list_organizations()  → get orgId
list_topics(orgId)    → see what's actually in this workspace
count_insights(orgId) → total corpus size for the header
```

Topic names vary across Format orgs. Map available topics to the roles below and proceed. Do not surface this mapping to the user.

**Topic role mapping:**

| Analytical role | Candidate topic names (pick closest available) |
|---|---|
| Best cohort signal | Expansion and Contraction Signals (positive), Customer Love, Positive Feedback |
| Pain / problem signal | Negative Product Feedback, Churn Risk Signals, Buying Objections |
| Product gaps | Feature Requests, Feature Requests and Workarounds |
| Competitive / displacement | Competitive Intelligence, Competitors and Alternative Solutions |
| Pre-purchase / buying language | Go-to-market Signals, Buying Objections |

### Step 2: Build the Best cohort and firmographics (3 calls)

```
search_insights(orgId, topicName: [best cohort topic], select: "analysis", limit: 75)
count_insights(orgId, filters: { company: [Best cohort] }, groupBy: "company.industry")
count_insights(orgId, filters: { company: [Best cohort] }, groupBy: "person.role")
```

Extract unique company names from the best cohort. Get dominant industry and dominant buyer role. These feed Channel recommendation, Targeting plan, and Campaign structure.

### Step 3: Pull the language for angles and competitive pressure (3–4 calls, parallel)

```
search_insights(orgId, topicName: [pain topic],         company: [Best cohort], select: "analysis", limit: 40)
search_insights(orgId, topicName: [best cohort topic],  company: [Best cohort], select: "analysis", limit: 40)
search_insights(orgId, topicName: [competitive topic],                           select: "analysis", limit: 30)
search_insights(orgId, topicName: [pre-purchase topic],                          select: "analysis", limit: 30)
```

Skip any topic with fewer than 15 insights. Don't pad.

Combined with orientation: 8–10 total calls.

---

## How to turn Format data into strategy

### Channel recommendation

Infer from the best cohort firmographics and the pre-purchase language:

| Signal from Format | Primary channel lean |
|---|---|
| Buyers discovered via search ("Googled," "was looking for," "comparing X vs Y") | **Google Ads** — high intent, bottom-funnel first |
| Buyers discovered via LinkedIn ("saw a post," "connected with") or via peer referral in a specific vertical | **LinkedIn Ads** — narrow firmographic targeting |
| Buyers discovered via specific communities, podcasts, newsletters | **Sponsorships / programmatic** — paid social may underperform |
| Large deal sizes + long cycles + small TAM | **LinkedIn + targeted Google brand/category** — paid should assist, not lead |
| Small deal sizes + PLG motion + broad TAM | **Google Ads + Meta retargeting** — LinkedIn too expensive per click |
| Buyers are specific named titles | **LinkedIn wins** on targeting precision |
| Buyers are functional generalists without consistent titles | **Google / intent-based** — LinkedIn title targeting breaks |

Don't rank channels in the abstract. Rank them against this specific customer base, then say why.

### Targeting plan

From Format data, extract:

- **Primary firmographics** — industry, company size, region (from `company.industry` and named accounts in best cohort)
- **Primary titles** — exact LinkedIn-searchable titles (from `person.role` groupBy)
- **Adjacent titles** — near-misses worth testing
- **In-market signals** — phrases that indicate readiness, pulled from pre-purchase language
- **Lookalike seed** — 15–30 best-cohort company names, comma-separated, ready for Clay / Sales Nav / LinkedIn Ads matched audience upload
- **Exclusions** — disqualifier patterns from the worst cohort, plus existing customers, competitors, and low-fit verticals

### Campaign structure

Opinionated defaults based on the customer profile, not generic:

- If B2B / high ACV / LinkedIn-led: 1 brand campaign (Google) + 2 LinkedIn campaigns (cold + retargeting) + 1 Google non-brand intent campaign. Budget skew 20/50/20/10.
- If PLG / low ACV / broad TAM: Google non-brand leads, Meta retargeting assists, LinkedIn only if ICP is narrow enough. Budget skew 60/30/10.
- If brand-new to paid: start with search brand + retargeting only, prove conversion, then expand. Don't run cold social from day one.

Include naming convention block:

```
[Platform]_[Funnel stage]_[Audience]_[Offer]_[Launch date]
```

### Angle portfolio

3–5 angles, each grounded in a Format quote. This briefs the creative team — it does not produce copy.

| # | Angle statement | Category | Anchor quote | Source |
|---|---|---|---|---|
| 1 | [One-line angle] | [Pain / Outcome / Competitive / Identity / Curiosity] | "[Verbatim, trimmed]" | [Speaker, Title @ Company — source, date] |

The creative team (or `paid-ads-copy` skill) takes this list and produces headlines, descriptions, and intro text per channel.

### Retargeting plan

Funnel stages matched to what's observable in the customer journey:

| Stage | Audience definition | Primary message | Window | Frequency cap |
|---|---|---|---|---|
| Hot | [Trial signups, demo no-shows, pricing page visitors — match to actual conversion events the company has] | [Objection handling, urgency, proof] | 1–7 days | Higher OK |
| Warm | [Key feature page visitors, blog readers on commercial-intent topics] | [Case studies, customer logos, outcome angles] | 7–30 days | 3–5x / week |
| Cold | [Broad site visitors, video viewers, social engagers] | [Education, brand, top-angle story] | 30–90 days | 1–2x / week |

Exclusions: existing customers (unless upsell), recent converters (7–14 days), bounces under 10 sec, careers / support page visitors.

### Measurement plan

Based on the dominant conversion event in the customer data:

| Layer | Metric | Why |
|---|---|---|
| Primary | [CPA on demo / trial / signup — whichever is the first committed action] | Tied to revenue, not vanity |
| Secondary | [CTR, landing page conversion rate, frequency, assisted conversions] | Diagnostic — why is CPA moving |
| Leading | [MQL → SQL rate for this cohort] | Catches quality problems before they hit CPA |

Review cadence:

- **Daily (first 2 weeks):** spend pacing, major breaks, policy rejections
- **Weekly:** CPA vs target, top / bottom ads, frequency check, audience breakdown
- **Monthly:** channel mix, angle rotation, budget reallocation between winners

Attribution note — one line on why platform-reported CPA will look better than blended CAC, and what to trust.

---

## Output structure

### Strategy snapshot (front of document)

One-page summary readable in 30 seconds:

```
## Strategy snapshot — [Company] paid ads

**Who to target:** [Primary persona + firmographics in one sentence]
**Primary channel:** [Channel] — [one-line why]
**Secondary channel:** [Channel] — [one-line why]
**Core angle:** [Angle #1 from portfolio — the strongest one]
**Primary KPI:** [Metric + target if inferable, otherwise "tied to [conversion event]"]
**Exclude:** [Key disqualifiers in one line]
**Budget lean:** [One-line budget split across channels]
```

Everything else in the document justifies or expands this block.

### Channel recommendation section

Table — channels ranked 1 → N with evidence:

| Rank | Channel | Why it fits this buyer | Why NOT (honest risk) | Phase to start |
|---|---|---|---|---|
| 1 | [Channel] | [Grounded in firmographics + pre-purchase language] | [Real risk — cost, targeting limits, intent mismatch] | [Now / Phase 2 / Only after X] |

Include at least one "Don't run this" row if a channel would be a mistake. Opinionated > exhaustive.

### Targeting plan section

**Firmographics table:**

| Dimension | Primary | Adjacent (test) | Exclude |
|---|---|---|---|
| Industry | [From data] | [Near-miss industries] | [Low-fit or competitor-heavy] |
| Company size | [Specific band] | [Adjacent band] | [Too small / too large] |
| Region | [Primary geos] | [Adjacent geos] | [Out of scope] |

**Titles table:**

| Priority | Exact titles (LinkedIn-searchable) | Adjacent titles | Not the buyer |
|---|---|---|---|
| P0 | [From person.role data] | [Near-misses] | [Frequently mistaken titles to exclude] |

**In-market phrases** (for Google keywords and LinkedIn interest targeting):

- "[Pre-purchase phrase from data]"
- "[Comparison phrase]"
- "[Problem-aware phrase]"

**Lookalike seed (LinkedIn Matched Audience / Google Customer Match upload):**

```
[Company 1], [Company 2], [Company 3], [Company 4], [Company 5], ...
```

15–30 companies, comma-separated, one block. Pastes directly into Clay / Sales Nav / ad platform uploads.

**Exclusions:**

- Existing customers (CRM sync)
- Closed-lost in last 90 days
- [Competitor domains if relevant for LinkedIn exclude-companies]
- [Disqualifier patterns — named examples from worst cohort]

### Campaign structure section

Tree view of recommended account architecture, sized to the customer's scale (don't over-engineer for a small budget):

```
Account
├── [Platform 1]
│   ├── [Campaign 1 — objective + audience]
│   │   ├── Ad set: [targeting]
│   │   └── Ad set: [targeting]
│   └── [Campaign 2]
└── [Platform 2]
    └── [Campaign]
```

Plus:

- Naming convention block
- Initial budget allocation as a percentage split with justification
- Bid strategy progression: start with X, switch to Y after N conversions

### Angle portfolio section

Table of 3–5 angles as described above. One sentence of orientation before the table:

> "These angles are the input to creative production. The `paid-ads-copy` skill turns this list into headlines, descriptions, and intro text per channel."

### Retargeting plan section

The three-tier table described above. Plus a short paragraph on sequencing — do you retarget before or alongside cold, what's the order of operations.

### Measurement plan section

The metric tiers table. Plus:

- Primary conversion event definition (match to what the customer actually tracks — from the data if possible, otherwise labelled as an assumption)
- Attribution approach (platform vs GA4 vs blended CAC)
- Review cadence
- Kill criteria — when to pause a campaign, not just optimise

---

## Close with next-steps offer

After the full document is displayed inline, add a single sentence picking 3 from this menu:

1. Produce the ad copy for these angles — LinkedIn, Google, Lead Gen Forms
2. Draft landing page copy that matches the angle
3. Build the conversion tracking / UTM plan
4. Build the Lead Gen Form email nurture sequence
5. Generate ad visual briefs from the angle portfolio
6. Set up a monthly paid ads review cadence with dashboard template

One sentence. No methodology note afterwards.

---

## File output

Save the deliverable to `/mnt/user-data/outputs/[company-slug]-paid-ads-strategy.md` and present via `present_files`.

```
present_files(filepaths=["/mnt/user-data/outputs/[company-slug]-paid-ads-strategy.md"])
```

No commentary around the file presentation. The download link appears, user saves it, run is complete.

---

## Scope boundaries

- Runs silently, completes in one response
- Strategy only — no ad copy, no visuals, no tracking implementation
- Every strategic claim traceable to Format data
- Opinionated over exhaustive — ranks channels, picks winners, flags things not to do
- Channel-agnostic examples (this skill ships to every Format customer)
- No framework names (AIDA, PAS, See/Think/Do) as section headers

## Quality bar before shipping

- Zero chat output between the user's request and the Strategy snapshot
- All seven sections present (or scope narrowed with a one-line note, not a "continue?" bail-out)
- Strategy snapshot stands alone — readable in 30 seconds
- Targeting plan has a pasteable lookalike seed list
- Angle portfolio has 3–5 angles with verbatim Format quotes
- Retargeting plan is sized to the customer's real funnel, not a generic template
- Closing line offers next steps from the standard menu, with `paid-ads-copy` as option 1
- Markdown file saved to `/mnt/user-data/outputs/[company-slug]-paid-ads-strategy.md` and presented via `present_files` as the final action
