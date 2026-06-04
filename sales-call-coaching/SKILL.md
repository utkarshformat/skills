---
name: sales-call-coaching
description: "Use when assessing the selling competency of a sales rep from their real call recordings in Format. Triggers include: 'coach [rep]', 'score [rep]'s calls', 'how is [rep] selling', 'competency assessment for our AEs', 'sales coaching', 'review call quality', 'where is [rep] losing deals', or 'rep scorecard'. The skill requires a single named rep and a time window, pulls full call transcripts from the Format workspace via the Format MCP, classifies and scores EVERY real conversation in the window (no sampling, no cap) against a rubric calibrated for short outbound prospecting calls, and produces a competency assessment with verbatim evidence and one prioritised coaching focus. Assessment only — it surfaces evidence and a single coaching priority; it does not write call scripts or run the coaching session itself."
---

# Sales Call Coaching Skill

## What this skill does

Given **one named rep** and a time window, this skill reads **every** real call transcript that rep had in the window from your Format workspace, scores **all** of the genuine prospecting conversations (no sampling) against a behavioural rubric calibrated for **short outbound prospecting calls**, and produces a competency assessment.

It is an **assessment tool, not a coaching session and not a script writer.** It surfaces scored evidence and names the single highest-leverage thing the rep should fix next. The human runs the actual coaching conversation.

## Why this rubric is calibrated for short outbound calls

Standard SaaS-discovery rubrics (15–20 discovery questions, 35–40% talk ratio, MEDDIC multi-threading, economic-buyer mapping) assume long video calls with a buying committee in the room. They unfairly fail reps who run **short outbound phone calls** — where the rep is often fighting through a switchboard to reach one contact, and the "deal" may be a long procurement or budget cycle that won't open for months or years.

So this rubric keeps the **behaviours that matter on a short outbound call** and drops the volume metrics that don't. The goal of such a call is almost never "close" — it is **earn the next step** (a booked meeting or a concrete, dated follow-up).

> If your team runs long discovery/demo calls instead, treat this rubric as a starting point and adjust the dimension weights before relying on the scores.

## Required inputs

1. **One specific rep name — REQUIRED.** This skill assesses **exactly one named rep per run**. **Never default, never guess, never assess "the team."** If the user does not name a specific rep (e.g. "how are the reps doing?", "score the outbound team"), **stop and ask which single rep to assess** before doing anything else.

   ⚠️ **Role caveat:** a team often runs *different motions* — some reps prospect, others manage late-stage deals, run implementation, or do support. This skill scores **prospecting** behaviour. Never assume a named person is a prospector; let the call classification (Step 4) decide, and if the named rep ran no prospecting calls, say so. Confirm who is actually meant to be selling before treating an assessment as final.
2. **Time window** — date range to pull calls from (e.g. "last 14 days", "since May 1"). **Never default this. Always ask if missing.**

## Standing configuration

- **Workspace / org:** confirm which Format org to query if there's any ambiguity (use `list_organizations`). Never assess against the wrong workspace.
- **Output language:** score in the **language the calls are in**; **explain findings to the user in the user's language.** Evidence quotes stay **verbatim in the original language** of the call (never paraphrase or translate inside the quote marks).
- **Coverage — read EVERY conversation. No cap, no sampling.** Read every real conversation the rep had in the window. Do not stop at 10, do not "sample the richest calls" — that biases the result toward the rep's best work. Use insight count only to *order* the reads (Step 4), not to limit them.
- **Minimum sample:** if fewer than **8** real conversations exist in the window, still score them all but label the assessment "⚠️ low-confidence — small sample" and present it as provisional.

### Presentation & formatting standards (apply to every output)
- **Never write walls of text.** Break everything up. Lead with tables; use bullet points, short paragraphs, indented sub-points, and clear section headers.
- **Use emojis as light visual signposting** in headers and callouts (e.g. 📊 summary, 🟢 strength, 🔴 weakness, 🎯 priority, ✅ correct disqualification, ⚠️ caveat). Keep it tasteful — signposting, not decoration.
- **Score format is always "out of total."** Every dimension score is shown as `0/2`, `1/2`, or `2/2` — never a bare `1`. Every per-call weighted total and every rep average is shown as `X.X/2.0` (e.g. `1.45/2.0`, `1.13/2.0`).
- **Call duration is always `M:SS`.** The `context` field gives seconds (e.g. `589s`); convert and display as `9:49`. Never show bare seconds in the output.

## Process

### Step 1: Confirm inputs
Two inputs are mandatory and **neither is ever defaulted**:
- **One named rep.** If the user did not name a specific single rep, stop and ask which one. Do not assess more than one rep in a run, and never silently assess "the team."
- **A time window.** If missing, ask for it (e.g. "last 14 days", "since May 1").

Do not pull any records until both are confirmed.

### Step 2: Resolve rep names to person IDs
Call `list_records` and read the `persons` array on returned records to find the rep's `person.id` (internal participants usually share the company email domain). Match the requested rep name to that person record. If a name doesn't match anyone, flag it and ask.

### Step 3: Pull the rep's full call list in the window
Call `list_records` with `personIds: [repId]` and the `dateRange`. **`dateRange.from` and `dateRange.to` must be full ISO datetimes** (e.g. `2026-05-22T00:00:00Z`, not `2026-05-22`) — plain dates throw a validation error. This returns call metadata (timestamp, data source, participants, **insight count**) but **not** transcripts.

**Paginate until you have the complete list.** `list_records` caps at 100 results per page and returns a `totalCount`. If `totalCount` exceeds what you've fetched, page through with `offset` until every record is collected. Missing the last page = missing conversations, which this skill must never do. Collect every record ID and note each one's `insightCount`.

### Step 4: Read transcripts and classify each call

**Order the reads by insight count, but read them ALL.** `insightCount > 0` is a reliable signal that the call was a real conversation (Format only extracts insights from genuine exchanges); `insightCount === 0` is very often a voicemail, switchboard-only, or no-answer. Order the reads by insight count descending so the richest calls come first, but **read every insight-bearing record — there is no cap.** Zero-insight records are non-conversations: count them for the activity table, but you don't need to transcribe each one (spot-check any borderline short ones if in doubt).

For each record, call `get_record` with `includeInsights: true`. The `content` field is the full transcript; the `context` field carries direction + duration in seconds (e.g. `outbound — 589s`) — **convert duration to `M:SS` for display** (589s → `9:49`); `insights` carries Format's topic-tagged signals.

**Classify before scoring — on TWO axes.** A call only gets scored if it passes *both*.

**Axis 1 — reachability:**
- **Conversation** — the rep reached and spoke with a real person. Eligible.
- **Non-conversation** — voicemail, switchboard/gatekeeper only, no-answer, wrong number, sub-~60s with no real exchange. **Not scored.** Count and report separately (a high non-conversation rate is itself a finding — list quality or call timing, not rep skill).

**Axis 2 — motion type** (critical — a team often runs different jobs and only one is prospecting):
- **Prospecting** — rep is opening or advancing a *new* opportunity: introducing the company, qualifying, discovering pain, re-engaging a dormant lead, pushing for a first meeting. **Score these against the rubric.**
- **Deal management** — late-stage work on an *already-won or near-won* deal: pricing/quote negotiation, competitor comparison, procurement logistics, contract steps. **Not scored** (different motion). Flag as "deal-management call — not scored."
- **Implementation / post-sale** — scheduling installs, technician handoffs, onboarding on a live deployment. **Not scored.** Flag.
- **Support** — product issues, bug reports, complaints on a live deployment. **Not scored.** Flag.

For each non-prospecting call, name the motion in the output and set it aside. **Never score a deal-management, implementation, or support call against the prospecting rubric** — doing so produces unfair, meaningless numbers. If a rep has *zero* prospecting calls in the window, say so plainly: "[Rep] ran no prospecting calls this window (N deal-management / M support) — nothing to score against this rubric."

**Flag disqualifications — and separate them from caves.** When a prospecting call ends quickly with no further probing, decide *why* before scoring it:
- ✅ **Correct disqualification** — the prospect said something that makes them a genuine, structural non-fit, and the rep recognised it and ended efficiently. This is **good judgement, not a failure.** Genuine disqualifiers are *fit-based*, e.g.:
  - a setup the product physically can't serve,
  - an equivalent owned/contracted solution they're committed to and can't leave,
  - a hard structural/ICP miss with no realistic re-entry.
  - **How to handle:** label the call `✅ Disqualification (correct)`, mark **Objection handling** and **Next step** as **N/A** (exclude from the average — do not score a 0), and **do not** use the call in the coaching priority, the SBI, or any "where they're losing deals" guidance. A swift, clean exit from a non-fit is the *right* call; never coach against it.
- 🔴 **Cave** — the rep abandoned a *viable* opportunity without exploring it. **Timing / political / budget stalls are NOT disqualifiers** — "new leadership settling in", "budget frozen", "not this fiscal year", "we're mid-contract", "call me next quarter" are the dominant *stall* family, and a viable opportunity should be probed and a low-commitment next step attempted. Caving on a stall **is** an objection-handling / next-step failure and scores accordingly.

When in doubt between disqualification and cave, ask whether a competent rep could realistically have advanced it: if yes, it's a cave; if no, it's a disqualification.

### Step 5: Score each prospecting conversation against the rubric
Score every **prospecting conversation** (passed both axes, and not a correct disqualification) on each of the seven dimensions, using the anchors in `references/rubric.md`. **Read `references/scoring-example.md` first — it is the gold standard for evidenced scoring.** Every scored call must produce: a dimension-by-dimension table and the call's `sourceUrl` (or an insight `shareUrl`) in the card header.

**Evidence cells must be legible at a glance.** Each cell: lead with the plain-language point, tag the speaker (`Rep:` / `Prospect:`) on every verbatim quote, add a short gloss only if the quote isn't self-evident (e.g. when the call is in another language), and for any score below `2/2` end with `Missing: [≤5 words]`. Shape: *Plain point. Speaker: "short quote" (gloss). Missing: [≤5 words].*

- **Show every dimension score as `X/2`** (`0/2`, `1/2`, `2/2`) — never a bare number.
- **Show the per-call weighted total as `X.X/2.0`** (e.g. `1.45/2.0`).
- Where a dimension had genuinely no opportunity (e.g. a pure scheduling/holding call, or a correct disqualification), mark it **N/A** and exclude it from that call's weighted total rather than scoring 0.

### Step 6: Roll up and render — summary FIRST
Aggregate across the rep's **scored prospecting conversations** (correct disqualifications and holding-call N/A dimensions excluded from the averages). Compute per-dimension averages and the headline weighted average (`X.X/2.0`). Identify the consistently weakest dimension — that is the rep's one coaching priority (pick the earliest weak rung on the ladder; see Coaching delivery).

Render in the order in the Output structure below: **the activity table and headline summary come first**, then the per-call deep dive, then a condensed table covering every remaining conversation so none is skipped.

## The rubric (calibrated for short outbound calls)

Seven dimensions, scored 0/1/2, weighted. Full behavioural anchors are in `references/rubric.md` — read that file before scoring.

| Dimension | Weight | What it scores |
|---|---|---|
| Opening & permission | 10% | Names self/company, earns the right to keep talking, survives the gatekeeper |
| Reason-for-call clarity | 10% | States plainly and early why they're calling |
| Discovery / pain | 20% | Asks about current process, quantifies the problem, uncovers who decides; uncovers real pain vs. talking at them |
| Value framing | 15% | Ties the offering to *their* stated situation, not a canned pitch |
| Objection handling | 20% | Acknowledges the brush-off, explores it, reframes — vs. caving or steamrolling |
| Next step secured | 20% | Lands a dated meeting or a concrete agreed follow-up — not "I'll send some documents" |
| Call control & register | 5% | Guides the call, handles the gatekeeper, professional register |

**Weighting rationale:** discovery, objection handling, and next-step land most of the weight because on a prospecting call those three are what move a deal forward. Opening and register matter but are foundational hygiene, not the differentiator.

## Coaching delivery (how to frame the output)

When you present a rep's weakest dimension, frame it with **SBI** (Situation–Behaviour–Impact), not judgement:
- *Situation:* name the specific call and moment.
- *Behaviour:* describe what the rep did, observably, no adjective.
- *Impact:* state the consequence.

Sequence coaching foundationally: fix openings → discovery → value → objections → next step, in that order. Don't coach advanced objection reframing on a rep who isn't yet getting past the gatekeeper. See `references/coaching-frames.md`.

**Never coach a correct disqualification.** If a call was flagged `✅ Disqualification (correct)`, it is off-limits for the coaching priority, the SBI example, and any "losing deals" framing. Ending a non-fit call quickly is good selling. Coaching only ever targets **caves** (viable opportunities the rep dropped), not smart exits.

**Rep-level vs pattern-level.** If the *same* weakness shows up across reps (e.g. everyone caves on the same budget-timing brush-off), that's a **team enablement gap** — surface it as a pattern and suggest one shared session (e.g. build a single rebuttal to drill), not the same coaching item repeated per rep.

## Output structure

Render in **this order**. Lead with the summary. Use tables, bullets, emoji signposting, and short paragraphs throughout — never a wall of text.

```
# 🎯 Sales Call Coaching Assessment — [Rep name]
**Window:** [range]

## 📊 1. Activity & headline   ← ALWAYS FIRST

| Metric | Count |
|---|---|
| Total logged call records | [N] |
| Connected to nobody (voicemail / switchboard / no-answer) | [N] |
| Real conversations (insight-bearing) | [N] |
| Conversations scored | [N] ([P] substantive · [H] holding/logistics) |
| ✅ Correct disqualifications (excluded from coaching) | [N] |
| Dial-to-conversation rate | [%] |

**Overall weighted score: `X.X/2.0`** across [N] scored prospecting calls[ · ⚠️ low-confidence if <8].

**🟢 Strengths / 🔴 Weaknesses** (dimension averages):

| Dimension | Avg | Read |
|---|---|---|
| Opening & permission | `X.X/2.0` | [one line] |
| Reason-for-call | `X.X/2.0` | [one line] |
| Discovery / pain | `X.X/2.0` | [one line] |
| Value framing | `X.X/2.0` | [one line] |
| Objection handling | `X.X/2.0` | [one line] |
| Next step secured | `X.X/2.0` | [one line] |
| Call control & register | `X.X/2.0` | [one line] |

**🎯 Coaching priority (one thing):** [the earliest weak rung, framed as what to work on next — one short paragraph].

## 🔍 2. Deep dive (full scoring sheets)
[Full per-call sheet for the most instructive calls — strongest, weakest, and the clearest pattern examples. One table per call.]

### [Call label] — [Company / contact] ([date], [M:SS]) — `X.X/2.0`
→ [sourceUrl]

| Dim | Wt | Score | Evidence |
|---|---|---|---|
| Opening | 10% | `2/2` | [Plain point.] Rep: "[short quote]" |
| Reason | 10% | `2/2` | [Plain point.] Rep: "[short quote]" |
| Discovery | 20% | `2/2` | [Plain point.] Rep: "[short quote]" |
| Value | 15% | `1/2` | [Plain point.] Rep: "[short quote]". Missing: [≤5 words] |
| Objection | 20% | `1/2` | [Plain point.] Prospect: "[quote]" → Rep: "[quote]". Missing: [≤5 words] |
| Next step | 20% | `1/2` | [Plain point.] Rep: "[short quote]". Missing: [≤5 words] |
| Control | 5% | `2/2` | [Plain point.] |

[Repeat per deep-dive call.]

## 🗂️ 3. Every other conversation (condensed — nothing skipped)
| Call (date) | Duration | Type | Score | One-line | Source |
|---|---|---|---|---|---|
| [contact] ([date]) | [M:SS] | Prospecting / Holding / ✅ Disqual | `X.X/2.0` or N/A | [one line] | [link] |
[...one row for every remaining conversation, so the deep-dive set + this table = every scored conversation.]

## ✅ 4. Disqualifications (for the record, not coached)
[Bullet list of any correct disqualifications: contact, the verbatim line that disqualified them, why it's a genuine non-fit. Note these are NOT held against the rep.]

## 🎯 5. Coaching priority, framed SBI
- **Situation:** [call, date, M:SS, moment] → [sourceUrl]
- **Behaviour:** "[verbatim quote]" (observable, no adjective)
- **Impact:** [consequence]
[Never built on a disqualification.]

## ⚠️ What this misses
[Standard caveat — see hard rules.]

[If the named rep ran NO prospecting calls:]
**No prospecting calls this window** — [N] calls were [motion breakdown]. Nothing to score against the prospecting rubric. (This rep may not be running an outbound motion — confirm their role.)
```

## Hard rules

- **One named rep, always.** Never assess more than one rep per run and never default. If no specific rep is named, ask before doing anything.
- **Read every conversation. No cap, no sampling.** Page through `list_records` to the full `totalCount`, then read every insight-bearing record. Never limit to the "best" or "richest" calls.
- **Summary first.** Always open with the 📊 activity table + headline score + strengths/weaknesses table + the one coaching priority, before any per-call detail.
- **Score format is always out of total.** Dimension scores as `X/2`; per-call totals and rep averages as `X.X/2.0`. Never a bare number.
- **Duration is always `M:SS`.** Convert the `context` seconds before display.
- **Never wall-of-text.** Tables, bullets, indents, short paragraphs, tasteful emoji signposting. Every output should be skimmable.
- **Flag disqualifications and never coach them.** A correct, fit-based disqualification (swift clean exit from a genuine non-fit) is good judgement: label it ✅, N/A its Objection and Next-step dimensions, and keep it out of the coaching priority and SBI. Timing/budget/political stalls are NOT disqualifiers — caving on those is still scored.
- **Assess, don't script.** Surface scored evidence and name the priority. Do not write the rep's next call script or role-play dialogue unless asked separately.
- **Classify on both axes before scoring.** Never score a voicemail/gatekeeper call (reachability), and never score a deal-management, implementation, or support call against the prospecting rubric (motion).
- **Every score is substantiated, and evidence must be legible at a glance.** Per-dimension table with a source link in the card header (`sourceUrl`, or insight `shareUrl`). A score with no evidence and no link is not allowed. Never fabricate a link.
- **Verbatim quotes only.** Never paraphrase or translate inside the quote marks. The plain-language explanation goes outside the quote; add a short gloss in brackets if the call is in another language.
- **Respect the minimum sample.** Under 8 real conversations, mark the assessment ⚠️ low-confidence and provisional.
- **Never default the time window.** Always ask if missing.
- **One coaching priority.** Name the single weakest (earliest-rung) dimension. Overwhelm kills coaching.
- **Frame with SBI, never judgement.** No "the rep is weak at X." Always Situation → Behaviour → Impact.
- **Always append the coverage caveat:**
  > ⚠️ **What this misses:** This is a read of recorded calls only. It can't see emails, in-person meetings, or deals that progressed off-call. Recording and transcription quality vary — treat a low score on a single call as a prompt to listen to the recording, not a final verdict. Scores reflect *call behaviour*, not pipeline outcomes.

## How to prompt this skill

```
Using the Format MCP and the sales-call-coaching skill, assess [one rep name] over [time window].
```

### Example 1 — single rep (the normal case)
> Using the sales-call-coaching skill, assess [Rep] over the last 14 days.

→ Resolves the rep's person ID, pages through their full call list, reads **every** real conversation, classifies (incl. disqualification vs cave), scores them all, and renders the assessment summary-first with one SBI coaching priority.

### Example 2 — no rep named
> How are our reps doing on calls?

→ "Which single rep should I assess, and over what window?" **Asks for both — never defaults, never assesses the team at once.**

### Example 3 — "the whole team"
> Score the outbound team since May 1.

→ "This skill assesses one rep at a time. Which would you like to start with?" Waits for a name, then runs the single-rep flow. (Run it again per rep if they want several.)
```
