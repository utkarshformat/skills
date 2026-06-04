---
name: customer-insights-company-context
description: Use when a team wants to generate a shared company context document — the foundational brief on their positioning, ICP, personas, voice, and proof points — grounded in real customer conversations from their Format workspace. Trigger phrases include "build our company context", "generate our shared context", "create a company brief", "what's our positioning", "who are we really selling to", "extract our brand voice", "what do customers say about us", "build shared context for our team", "one source of truth for marketing", "generate our product marketing context", or "refresh our positioning doc". Uses the Format MCP to produce a single markdown document covering product overview, ICP, personas, pain points, competitive landscape, brand voice, and proof points — all backed by verbatim customer quotes. Runs end-to-end in one response. Re-run quarterly to refresh as the customer base evolves. Not for writing blog posts, emails, ads, or case studies — those are downstream skills that read this context.
---

# Customer Insights Company Context

## What this skill is for

Most teams describe their company differently to Claude every time they open a new chat. Sales says one thing, marketing says another, the founder says a third. The result: outputs that don't match, messaging that drifts, and every teammate re-explaining the basics on every prompt.

This skill fixes that. One run → one comprehensive markdown file → every teammate working from the same foundation.

The document is not aspirational. It is not what the founder wishes the company sounded like. It is what the company actually is, extracted from what real customers say in calls, emails, and support channels via the Format MCP.

## Execution principle

This skill runs silently and completes in a single response. When invoked, Claude's immediate next action is a tool call — not a chat message. No opening statement, no progress narration, no interim findings, no mid-run bailouts, no "want me to continue?" prompts.

The user sees tool calls rendered by the UI. Claude's next chat output is the finished document, rendered inline in chat AND saved as a downloadable markdown file.

The document is the deliverable. Everything else is noise.

## What this skill produces

A single markdown file named `company-context.md`, delivered two ways:

1. **Inline in chat** so the user can read it immediately.
2. **As a downloadable markdown file** via the `present_files` tool, so the user can save it to Notion, Google Docs, a shared drive, the repo, or wherever their team works.

The document has fourteen sections:

1. **Product overview** — one-liner, what it does, category, business model
2. **Target audience & JTBD** — who it's for, jobs to be done, use cases by team
3. **ICP** — firmographic sweet spot, triggers, disqualifiers
4. **Personas** — 3–4 archetypes in a table: cares about / challenge / value we promise
5. **Problems & pain points** — core problem, why alternatives fall short, what it costs, emotional tension
6. **Competitive landscape** — high / medium / low risk competitors, category summary, positioning statement
7. **Differentiation** — key differentiators, how we do it, why it's better, why customers choose us
8. **Objections** — table of objection / response / customer proof
9. **Anti-persona & sales cycle pattern** — who it's not for, common buying path
10. **Switching dynamics (JTBD forces)** — Push / Pull / Habit / Anxiety, each with verbatim quotes
11. **Customer language** — how they describe the problem (thematic clusters), how they describe the product, words to use, words to avoid, glossary
12. **Brand voice** — tone, style, personality with evidence quotes
13. **Proof points** — testimonials, value themes, notable customers, buyer profile pattern, geography, stack
14. **Last refreshed** — date + what changed since last run

Section headers use human labels. The file is structured to be pasted into any doc tool without reformatting.

## When to use

- First time setting up a shared GTM foundation for a team
- Before launching a new marketing motion (content, outbound, ads, events)
- Quarterly refresh as the customer base evolves
- When onboarding new marketing, sales, or CS hires
- When positioning feels stale or outputs from different teammates are drifting apart
- Before a board deck, fundraise, or major messaging update

## When NOT to use

- Fewer than 50 customer conversations in Format — not enough signal for this depth
- Writing a single deliverable (blog post, email, ad, case study) — those are downstream skills
- Refreshing just one section (ICP only, voice only) — use a narrower skill for that

## Setup

If Format MCP isn't connected yet:
1. Settings → Connectors → Add custom connector
2. URL: `https://useformat.ai/api/mcp`
3. Authenticate with your Format account

No configuration needed beyond that. The skill queries whatever Format workspace the MCP is connected to.

---

## The run — how the skill executes

Tight sequence. Target: 12–16 tool calls total. Broad topic-first queries, parallelized where possible.

### Step 1: Orient (2 calls)

```
list_organizations()  → get orgId (use the first one returned)
list_topics(orgId)    → see what's actually in this workspace
```

Topic structures vary across Format orgs. Map available topics to the analytical roles below and proceed silently.

**Topic role mapping:**

| Analytical role | Candidate topic names |
|---|---|
| Positive signal / praise | Positive Feedback, Customer Love, Expansion and Contraction Signals (positive) |
| Pain / gaps | Negative Product Feedback, Feature Requests, Feature Requests and Workarounds, Buying Objections |
| Competitive mentions | Go-to-market Signals, Competitive Intelligence, Competitive Mentions |
| Use cases / onboarding | Customer Onboarding, Implementation Feedback, Use Cases |
| Objections / concerns | Buying Objections, Security & Compliance Concerns, Pricing Concerns |
| Switching signals | Churn Risk Signals, Expansion and Contraction Signals (negative), Workflow Friction |

If a topic exists, use it. If not, fall back to semantic queries against all topics.

### Step 2: Firmographics (2 calls)

```
count_insights(orgId, groupBy: "company.industry")
count_insights(orgId, groupBy: "person.role")
```

Shows dominant industry and buyer role patterns. Feeds ICP, Personas, buyer profile in Proof Points.

### Step 3: Core content pass (4 calls, parallel)

**Positive signals** — feeds Voice, Proof points, Differentiation, Customer Language (praise):
```
search_insights(orgId, topic: [positive topic], select: "analysis", limit: 75)
```

**Pain & gaps** — feeds Problems, Personas, Switching Dynamics (Push), Customer Language (problem):
```
search_insights(orgId, topic: [pain topic], select: "analysis", limit: 75)
```

**Competitive mentions** — feeds Competitive landscape, Differentiation, Objections:
```
search_insights(orgId, topic: [competitive topic], select: "analysis", limit: 50)
```

**Use cases / onboarding** — feeds Personas, Target Audience, Product Overview:
```
search_insights(orgId, topic: [use cases topic, if available], select: "analysis", limit: 40)
```

### Step 4: JTBD forces pass (3–4 calls, parallel)

These queries specifically feed the Switching Dynamics section — one of the most valuable sections for marketing/sales.

**Push (dissatisfaction with current state):**
```
search_insights(orgId, query: "frustrated OR broken OR can't keep up OR too manual OR losing OR disconnected", limit: 30)
```

**Pull (attraction to new solution):**
```
search_insights(orgId, query: "love OR finally OR exactly what OR we needed OR game changer", limit: 30)
```

**Anxiety (concerns about switching):**
```
search_insights(orgId, topic: [objections topic], query: "worried OR concern OR not sure OR data OR security OR reliable", limit: 30)
```

**Habit (inertia / why existing workflow feels fine):**
```
search_insights(orgId, query: "already using OR works fine OR good enough OR don't need another", limit: 20)
```

### Step 5: Objections pass (1 call)

```
search_insights(orgId, topic: [objections topic], select: "analysis", limit: 40)
```

Feeds the Objections table. Cross-reference with positive signals from Step 3 to find customer-proof rebuttals for each objection.

### Step 6: Check for existing context (1 call, optional)

If `company-context.md` already exists in the working directory, read it to identify what's changed since the last refresh. The "What changed since last refresh" section goes near the top of the file.

### Step 7: Synthesize

All fourteen sections built from the extracted insight pool. No additional tool calls needed.

**Thematic clustering is critical.** In the Customer Language section, do NOT dump random quotes. Cluster quotes into 3–5 themes per subsection, with a bolded theme label above each cluster. Example:

> **"We're data rich and insight poor"**
> - "[Quote 1]" — [Name], [Company]
> - "[Quote 2]" — [Name], [Company]
> - "[Quote 3]" — [Name], [Company]
>
> **"Insights get filtered and distorted"**
> - "[Quote 1]" — [Name], [Company]

This is the product-marketer move — it turns raw quotes into reusable messaging pillars.

**Flag gaps honestly.** Some sections can only be partially filled from customer conversations. Mark them clearly rather than fabricating:

| Section | Usually well-covered by Format | Usually needs founder input |
|---|---|---|
| Product overview | What it does, category | One-liner, business model, pricing |
| Target audience & JTBD | Jobs, use cases | Stage cutoffs, ICP boundaries |
| ICP | Triggers, roles, industries | Firmographic ranges, funding stage |
| Personas | Pains, language, roles | Decision authority, budget authority |
| Problems & pain points | All of it | — |
| Competitive landscape | Who's mentioned, how framed | Strategic categorization |
| Differentiation | What customers say is different | Founder's intended positioning |
| Objections | Actual objections raised | Rebuttals for unhandled objections |
| Anti-persona | Stalled deals, bad fits | Explicit exclusion rules |
| Switching dynamics | All four forces | — |
| Customer language | All of it | — |
| Brand voice | All of it | — |
| Proof points | Testimonials, themes | Hard metrics (revenue, hours saved) |
| Last refreshed | Date, what changed | — |

Where a subsection has no data support, write:

> *Gap — founder input needed. Format data doesn't cover this. Paste your [homepage / pricing page / one-liner / founder description] and Claude can enrich this section.*

Do not guess. Do not fill with generic B2B copy. An honest gap is better than a made-up answer.

### Step 8: Offer enrichment (after delivering the doc)

At the very end of the response — after `present_files` — append a single short prompt:

> *Want to fill the gaps? Paste any of these and I'll enrich the relevant sections: your homepage URL, pricing page, one-liner, or founder's description of the business.*

Keep it to one line. Don't elaborate. The user either responds with URLs/text (and Claude enriches) or they don't (and the doc stands as-is).

---

## Adaptation rules

**Small conversation pool (<150 insights).** Deliver what's supportable. Switching Dynamics may be thin — that's fine, flag it. Do not fabricate personas or forces that aren't in the data.

**Different topic names.** Map silently via the topic role table. Don't surface the mapping to the user.

**Heavy prospect skew.** If most conversations are pre-sales discovery, treat "high-intent prospects who chose us" as the primary cohort. Switching Dynamics still applies — these prospects are switching from something (even if that something is "nothing" / manual).

**Single-vertical customer base.** Write ICP and personas for the vertical that's actually winning. Don't hedge with "B2B companies broadly."

**Sparse competitive mentions.** If fewer than 5 competitors appear in conversations, present a simple list rather than the high/medium/low risk structure. Flag the rest as a gap.

---

## Deliverable format

See `references/document-template.md` for the exact structure, section headers, and formatting rules.

**Every claim in the document must be evidence-backed or flagged as a gap.** Every persona pain point has a verbatim customer quote. Every value theme has a quote. Every voice characteristic has a quote. Every JTBD force has 2–3 quotes. If there's no quote to support a claim, either mark it as a gap or omit it. Never fabricate.

**Voice rules:**
- Direct, specific, no hedging
- No generic B2B phrases ("industry-leading", "best-in-class", "enterprise-grade")
- Use customer language, not marketing language
- Quotes stay verbatim — don't polish them
- Thematic clusters in Customer Language, not quote dumps

**File output:**
- Save as `company-context.md` in the working directory
- Present with `present_files` tool at the end of the response
- Inline the same content in chat so the user sees it immediately
- Add the single-line enrichment prompt (Step 8) after `present_files`

---

## Enrichment mode

If the user responds to the enrichment prompt by pasting a URL, pricing info, or a founder-written description:

1. If it's a URL, use `web_fetch` to pull the page content
2. Re-read the existing `company-context.md`
3. Fill in the gap-flagged sections using the pasted / fetched content
4. Preserve all Format-grounded sections verbatim — do not rewrite them
5. Mark enriched sections with a small note: *Enriched from [homepage / founder input / pricing page] on [date].*
6. Save the updated file and present it again

Enrichment content is secondary to customer data. Where they conflict, customer data wins — because the whole point is to ground context in what customers actually say, not what the website claims.

---

## Anti-patterns

**Don't** open with "I'll now analyze your Format workspace..." → start with the tool call.
**Don't** narrate each step → the UI shows the tool calls.
**Don't** dump partial findings and ask to continue → scope narrower and finish in one response.
**Don't** invent generic personas not grounded in the data.
**Don't** write aspirational brand voice — extract what's actually there.
**Don't** fill data-thin sections with generic B2B copy — flag them as gaps instead.
**Don't** dump random quotes in the Customer Language section — cluster them into themes with bolded theme labels.
**Don't** auto-fetch the website on the first run — only fetch in enrichment mode when the user explicitly shares a URL.
**Don't** re-ask for the org ID or any config — Format MCP is already scoped to the customer's workspace.
**Don't** let website copy override customer quotes during enrichment — customer data always wins.
**Don't** skip the Switching Dynamics section — it's one of the most valuable and Format data almost always supports it.
