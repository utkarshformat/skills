---
name: paid-ads-copy
description: Use when drafting, iterating, or refreshing paid ad copy for LinkedIn Ads, Google Ads, or LinkedIn Lead Gen Forms — grounded in real customer language from Format. Trigger phrases include "write LinkedIn ads", "Google ad copy", "RSA headlines", "Lead Gen Form copy", "paid ad variations", "refresh our LinkedIn ads", "new ad angles", "ad creative from customer quotes", "ads that sound like our customers", "iterate on these ads", or "performance is dropping, give me new ads". This skill uses the Format MCP to source in-market language, pain points, and outcome language directly from customer conversations — then produces spec-compliant ad copy for LinkedIn Single Image Ads, Google RSAs, and LinkedIn Lead Gen Forms. Runs end-to-end in one response. For channel selection, targeting, campaign structure, or retargeting design, use paid-ads-strategy instead. Not for landing page CRO or ad visuals — those are downstream.
---

# Paid Ads Copy

## Execution principle

This skill runs silently and completes in a single response. When invoked, Claude's immediate next action is a tool call — not a chat message. No scoping questions, no opening statement, no progress narration, no "want me to continue?" prompts.

The skill pulls customer language from Format, clusters it into 3–5 ad angles, generates spec-compliant creative for every requested channel, and presents the file. Done.

The document is the deliverable. Everything else is noise.

---

## What this skill produces

A single markdown file with, for each requested channel:

- **3–5 angles** — each grounded in a verbatim customer quote (with speaker, company, source, date) so the user can defend the angle in a brief
- **Spec-compliant ad copy** for every variant — character counts shown next to every field, anything over limit gets auto-trimmed
- **A CSV block** per channel for direct upload or paste into the ad platform
- **An iteration log** if performance data was provided

Default scope: all three channels (LinkedIn Single Image, Google RSA, LinkedIn Lead Gen Form). If the user asks for only one, generate only that one.

---

## Hard constraints

- **Total tool-call budget: 8.** Hard cap.
- **Runs in one turn.** If it feels like it needs to say "continue" — scope narrower instead.
- **Every angle must be traceable to at least one verbatim quote from Format.** No invented pain points. No generic "save time, save money" angles.
- **Every piece of copy must be validated against platform character limits before shipping.** Anything over gets trimmed in the same response.
- **No ad visuals.** This skill is copy-only. Visuals are a downstream skill.

---

## When to use

- Launching a new paid campaign and starting from scratch
- Refreshing fatigued creative (CTR dropping, frequency climbing)
- Testing new angles on existing campaigns
- Building ads for a new persona, vertical, or use case
- Briefing an agency with grounded starting creative

## When NOT to use

- Campaign strategy, targeting, budgets, bidding — those are separate
- Landing page copy or CRO — separate skill
- Ad visuals (images, video, carousels) — separate skill
- Organic LinkedIn posts — separate skill
- Fewer than 30 relevant conversations in Format — not enough language signal

## Setup

If Format MCP isn't connected yet:
1. Settings → Connectors → Add custom connector
2. URL: `https://useformat.ai/api/mcp`
3. Authenticate with your Format account

---

## The run

### Step 0: Check for shared company context (silent, 0 calls)

Look for `company-context.md` in the working directory or `/mnt/user-data/uploads/`. If present, read it and use the personas, pain points, brand voice, and "words to use / avoid" sections to shape the angles and copy tone. Still pull fresh customer language from Format for the verbatim anchor quotes — the company doc frames, Format grounds.

If the file exists, note it silently in the header block: `Company context loaded from company-context.md (last refreshed [date]).` Do not announce it mid-run.

If not present, proceed with the full topic queries below. No prompt, no offer to run the other skill.

**When reusing quotes from `company-context.md`:** keep attribution intact (speaker, company, source, date). Do not launder quotes as synthesized claims. If a quote from `company-context.md` is the strongest anchor for an angle, reuse it verbatim — don't re-query Format for a weaker alternative just to avoid overlap.

### Step 1: Orient (2 calls)

```
list_organizations()  → get orgId
list_topics(orgId)    → see what's actually in this workspace
```

Topic names vary across Format orgs. Map the available topics to the roles below and proceed. Do not surface this mapping to the user.

**Topic role mapping:**

| Analytical role | Candidate topic names (pick closest available) |
|---|---|
| Pain points | Negative Product Feedback, Churn Risk Signals, Buying Objections, Feature Requests and Workarounds |
| Outcomes / value | Positive Feedback, Customer Love, Expansion and Contraction Signals (positive) |
| Competitive / displacement | Competitive Intelligence, Competitors and Alternative Solutions, Go-to-market Signals |
| Pre-purchase language | Go-to-market Signals, Buying Objections |

### Step 2: Pull the language (4–5 calls, parallel)

Pull raw customer language for each ad angle category. `select: "analysis"` keeps the verbatim quote and metadata.

```
search_insights(orgId, topicName: [pain topic],         select: "analysis", limit: 40)
search_insights(orgId, topicName: [outcome topic],      select: "analysis", limit: 40)
search_insights(orgId, topicName: [competitive topic],  select: "analysis", limit: 30)
search_insights(orgId, topicName: [pre-purchase topic], select: "analysis", limit: 30)
```

Skip any topic that doesn't exist or has fewer than 15 insights. Don't substitute — better to run with 3 strong categories than pad with weak ones.

### Step 3: Optional persona or product filter (0–1 calls)

If the user named a specific persona, vertical, or product line in the request, add one filtered search:

```
search_insights(orgId, topicName: [primary topic], filters: {...}, limit: 30)
```

Otherwise skip.

---

## How to turn Format data into ad angles

For each angle, you need **one verbatim quote** from Format as the anchor. The angle line itself should be the pain/outcome compressed into a headline-grade statement — not the quote itself. Quotes stay as proof; copy stays as copy.

**Target: 3–5 angles total across all channels.** Do not generate channel-specific angles — the same angle gets adapted to each channel's specs.

### Angle selection heuristics

- **Cluster quotes by theme.** Five different quotes saying the same thing = one strong angle, not five weak ones.
- **Prefer quotes with specificity** — numbers, tool names, time spans, role-specific workflows.
- **Reject generic quotes.** "It's great, saves us time" is noise. "We used to pull reports every Monday morning for 3 hours" is signal.
- **Cover distinct motivations.** Don't ship 5 pain-point angles. Mix pain, outcome, competitive displacement, identity, and curiosity.

### Standard angle categories (pick 3–5)

| Category | When it works | Source topic |
|---|---|---|
| Pain point | Target is problem-aware and frustrated | Pain topic |
| Outcome / transformation | Target knows solutions exist, wants proof | Outcome topic |
| Competitive displacement | Target currently uses a named competitor | Competitive topic |
| Status quo callout | Target is DIYing or using spreadsheets | Pain or pre-purchase |
| Identity / role | Target self-identifies with a specific job pattern | Any |
| Social proof / volume | You have customer density worth citing | Outcome topic |

---

## Platform specs (validate every piece of copy against these)

### LinkedIn Single Image Ad

| Field | Recommended | Hard max |
|---|---|---|
| Introductory text | 150 chars | 600 chars |
| Headline | 70 chars | 200 chars |
| Description | 100 chars | 300 chars |

Rules:
- Front-load the hook in the first 150 chars of intro — anything after gets a "…see more" cutoff on feed
- Headline appears below the image; description only shows on some placements, treat it as optional reinforcement
- Do not rely on emojis to carry meaning — they render inconsistently

### Google Ads — Responsive Search Ad (RSA)

| Field | Limit | Quantity |
|---|---|---|
| Headline | 30 chars | Up to 15 (min 3) |
| Description | 90 chars | Up to 4 (min 2) |

Rules:
- Every headline must stand alone AND combine sensibly with any other headline
- Include at least one keyword-focused headline, one benefit headline, one CTA headline
- Don't pin headlines unless you have a specific reason — pinning reduces Google's optimisation
- Avoid all-caps, excessive punctuation, or repeated exclamation marks (policy risk)

### LinkedIn Lead Gen Form

Two layers to write: the **ad that drives to the form** (same specs as Single Image Ad above) and the **form itself**.

| Form field | Limit | Notes |
|---|---|---|
| Form name (internal) | 256 chars | Admin-only, not shown to user |
| Offer headline | 60 chars | Shown at top of form |
| Offer detail | 160 chars | 1–2 sentences describing what they get |
| Privacy policy URL | — | Required |
| Custom privacy text | 2,000 chars | Optional |
| CTA button label | Pick from LinkedIn preset list | e.g. Download, Get quote, Register, Subscribe |
| Confirmation headline | 60 chars | Post-submit |
| Confirmation message | 300 chars | Post-submit thank-you |
| Confirmation CTA | Pick from preset list | e.g. View now, Visit website |

Rules:
- Offer must be tangible (guide, template, demo, audit, report) — not a vague "learn more"
- Offer headline and ad headline can differ — often the ad uses the hook, the form uses the specific deliverable name
- Keep custom questions to 3 max — every extra field drops completion rate

---

## Output structure

### Header block

```
# Paid Ad Creative — [Company name from orgId]
Generated from [N] customer conversations across [topics pulled].
Channels: LinkedIn Single Image | Google RSA | LinkedIn Lead Gen Form
```

### The angles (appears once, before the channel sections)

Table of 3–5 angles with anchor quotes:

| # | Angle | Category | Anchor quote | Source |
|---|---|---|---|---|
| 1 | [One-line angle statement] | [Pain / Outcome / Competitive / etc.] | "[Verbatim quote, trimmed to the punch]" | [Speaker, Title @ Company — source channel, date] |

Each anchor quote is proof the angle exists in the real world. The user can defend the angle in a brief by pointing to the source.

### Per-channel sections

For each channel (LinkedIn Single Image, Google RSA, LinkedIn Lead Gen Form), generate a section with copy for all 3–5 angles.

#### LinkedIn Single Image Ad section

For each angle:

```
### Angle [#]: [Angle name]

**Introductory text** (150 char target)
[Copy] (N chars)

**Headline** (70 char target)
[Copy] (N chars)

**Description** (100 char target, optional)
[Copy] (N chars)
```

Follow with a CSV block for bulk upload:

```csv
angle,intro_text,headline,description
1,"[intro]","[headline]","[description]"
2,"[intro]","[headline]","[description]"
```

#### Google RSA section

One RSA per angle cluster, OR one consolidated RSA with 10–15 headlines and 3–4 descriptions spanning all angles (user's choice — default to consolidated because RSAs perform better with more variants).

```
### RSA — [Campaign theme]

**Headlines** (30 char max each, aim for 10–15)
1. [Headline] (N)
2. [Headline] (N)
3. [Headline] (N)
...

**Descriptions** (90 char max each, aim for 3–4)
1. [Description] (N)
2. [Description] (N)
...
```

Tag each headline with its intent for the user's reference (not uploaded):

| Type | Example tag |
|---|---|
| Keyword | `[KW]` |
| Benefit | `[BEN]` |
| CTA | `[CTA]` |
| Proof / number | `[PROOF]` |

Follow with a CSV:

```csv
type,copy,char_count
headline,"[copy]",N
headline,"[copy]",N
description,"[copy]",N
```

#### LinkedIn Lead Gen Form section

Two parts.

**Part A — the ads driving to the form** (same structure as LinkedIn Single Image above, but CTA should match the offer: Download / Register / Get quote, not Learn more).

**Part B — the form itself**, for each angle:

```
### Form [#]: [Offer name]

- Offer headline (60): [Copy] (N)
- Offer detail (160): [Copy] (N)
- CTA button: [Preset label]
- Confirmation headline (60): [Copy] (N)
- Confirmation message (300): [Copy] (N)
- Confirmation CTA: [Preset label]
```

### Validation block at the end

Show a single line per channel confirming every piece of copy fits:

```
✓ LinkedIn: 15 fields, all within limits
✓ Google RSA: 12 headlines + 4 descriptions, all within limits
✓ Lead Gen Form: 5 forms, all within limits
```

If anything was trimmed, flag it here.

---

## Iteration mode

If the user provides performance data (CSV, pasted table, or just listing "headline X got 2.3% CTR, headline Y got 0.8%"), add an **Iteration log** section at the top of the deliverable, before the angles:

```
## Iteration log — Round [N]

**Top performers:**
- "[copy]" — [metric]: [value]
- "[copy]" — [metric]: [value]

**Bottom performers:**
- "[copy]" — [metric]: [value]

**Winning patterns:**
- [Specific pattern — e.g. "Numbers in first 5 words", "Question format", "Named competitor"]

**Losing patterns:**
- [Specific pattern]

**This round:**
- Doubling down on: [winning theme]
- Extending: [winning angle] into [N] new variants
- Retiring: [losing angle]
- New angle test: [angle + why it might work]
```

Then generate fresh copy that reflects those decisions — do not regenerate identical copy.

---

## Writing quality standards

Pulled from the original ad-creative skill, but tightened for customer-language grounding.

### Headlines that click

- **Specific over vague.** "Cut reporting time 75%" beats "Save time."
- **Customer language over marketing language.** If five customer quotes say "pulling reports every Monday for 3 hours," the headline is closer to "Stop pulling Monday reports" than "Streamline your reporting workflow."
- **Active voice.** "Ship reports in 5 min" beats "Reports can be shipped in 5 min."
- **Numbers when real.** Don't invent numbers. If Format has a verbatim "we saved 10 hours a week," you can say "save 10 hours a week." If not, don't.

### Avoid

- Jargon the customer data doesn't actually use
- Adjective stacks ("best-in-class leading enterprise-grade platform")
- Unsupported superlatives ("#1," "most powerful," "leading")
- All-caps for emphasis (platform policy risk)
- Clickbait the landing page can't deliver on
- Emojis carrying meaning — fine as accent, not as punctuation

### Descriptions

Descriptions should complement headlines, not repeat them. Use them for:
- Proof points (real numbers, named customer patterns, integrations)
- Objection handling ("No credit card required," "SOC 2 compliant")
- Reinforced CTAs ("Start your free trial today")
- Specificity the headline couldn't fit

---

## Quote handling — verbatim rules

- Every quote pulled from Format must appear verbatim. Do not paraphrase and present as a quote.
- Attribution format: `— First name, Title @ Company (source channel, date)`. If the Format record doesn't have one of these fields, use what exists and omit the rest.
- If a quote is too long to be punchy, trim with an ellipsis — but don't substitute words.
- The quote anchors the angle for defensibility. The ad copy is inspired by the quote's pattern, not a direct lift (direct lifts often don't meet character limits or platform policy).

---

## File output

Save the deliverable to `/mnt/user-data/outputs/[company-slug]-paid-ads-copy.md` and present via `present_files`.

```
present_files(filepaths=["/mnt/user-data/outputs/[company-slug]-paid-ads-copy.md"])
```

No commentary around the file presentation. The download link appears, user saves it, run is complete.

---

## Close with next-steps offer

After the document is displayed inline, add a single sentence offering 2–3 from this standard menu:

1. Adapt these ads for [additional channel not covered — Meta, TikTok, YouTube]
2. Draft landing page copy that matches the angle
3. Set up the tracking / UTM plan for these ads
4. Generate ad visual briefs from the winning angles
5. Write the Lead Gen Form email nurture sequence
6. Build a 4-week iteration plan with test structure

One sentence. No methodology note afterwards.

---

## Scope boundaries

- Runs silently, completes in one response
- Copy only — no visuals, no targeting, no budgets
- Every angle anchored to a verbatim quote from Format
- Every field validated against platform spec before shipping
- No framework names (PAS, AIDA, etc.) in the output
- No invented pain points or generic "save time, save money" angles
- Channel-agnostic examples (this skill ships to every Format customer)

## Quality bar before shipping

- Zero chat output between the user's request and the header block
- 3–5 angles, each with a verbatim Format quote
- Copy for every requested channel — LinkedIn Single Image, Google RSA, LinkedIn Lead Gen Form by default
- Character counts next to every field, all within limits
- CSV block per channel for direct upload
- Iteration log present if performance data was provided
- Markdown file saved to `/mnt/user-data/outputs/[company-slug]-paid-ads-copy.md` and presented via `present_files` as the final action
