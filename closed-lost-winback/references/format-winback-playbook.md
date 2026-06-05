# Format MCP Playbook — closed-lost win-back

Detailed tactics for the steps in SKILL.md. Format MCP server id starts `7bd33c8a`.

## Account matching (Step 2)

Export account names carry noise the Format company name won't have. Normalize then search.

**Normalize:** drop product/dept suffixes (`- Front Desk`, `- Deeds`, `- County Clerk`, `- Recorder of Deeds`, `- Appraisal District`, `- Assessor`, `- Tax Collector`, `- Auto Indexing`) and the trailing state code (`, AL`). Keep the core ("Baldwin County", "Cedarburg", "Collin County").

**Search ladder (stop at first solid hit):**
1. `list_companies` `nameSearch: "<core>"` — but beware false friends ("Collin" → "Lake County" via a person named Collins; "Jefferson" → "Jefferson City, MO"). Verify the state/domain matches.
2. `list_companies` `domainSearch` — guess the domain (`baldwincountyal.gov`, `cedarburg.wi.us`). County/city gov domains are inconsistent; this is a long shot.
3. `list_persons` `emailSearch: "<town token>"` (e.g. "two-rivers", "melrose") — catches conversations attributed to a person whose company was never resolved.
4. `list_persons` `nameSearch: "<contact named in the rep note>"` (e.g. "Fouts", "Devyn").

**Watch for wrong-office matches:** a county often has multiple offices. "Lamar County Clerk" (lost) ≠ "Lamar County Appraisal District" (a different opp that may exist in Format). Match the OPP, not just the county.

**Bucket honestly:** has-call / no-call / no-match. A no-match or no-call is a real finding ("this deal never produced a recorded conversation"), not a gap to paper over.

## Pulling records & insights (Step 3)

- `list_records` `dateRange` requires **full ISO 8601 datetimes** (`2026-01-01T00:00:00Z`), unlike `search_insights` which accepts bare dates. Window: from ~30 days before `created` to ~30 days after `close`.
- A record's `insightCount: 0` means it exists but was never processed for a topic — you can still `get_record` (`includeInsights: true`) and read the raw transcript.
- `search_insights` filters: `companyIds`, `topicNames` (e.g. `["Buying objections"]`), `dateRange`, `semanticQuery` (vector search), `keywordSearch`. Each insight carries a `shareUrl` (stable Format UI link) and the verbatim `quote`.
- Insights may live under topics other than the obvious one (a protest-season "on hold" quote landed under *Customer-Side Implementation Blockers*, not *Buying objections*). Don't over-filter by topic; a company-scoped search catches more.

## Why coverage is usually thin (and what actually fixes it)

The Format extraction model runs **per conversation** — it has no concept of lists, CRM records, deal outcomes, or other topics. It can only extract from calls that were **recorded and ingested**. The deals that die — no-shows, canceled demos, ghosts — are precisely the ones that never produced a recorded call. So:
- A wider processing window only helps accounts that *have* calls in that window.
- Reprocessing cannot surface a conversation that was never recorded.
- The real lever for fuller coverage next time is **recording hygiene** (Gong/Fathom capturing early-funnel disco calls), not topic config.

Say this plainly in the deliverable when coverage is low — it's the most actionable finding for the customer's RevOps.

## Win-back comparison (optional, Step 4)

To find "a deal that was saved despite the same objection": parse the export with `--all` to get open opps (Discovery → Proposal → Procurement = still advancing). The export gives you the *outcome* (still open) that Format lacks; Format gives you the *objection*. Cross-reference: an account in a later stage that raised the same objection is a turnaround candidate — read its transcript for the language that moved it.

## Lens Brief (optional Step 6 output)

`create_lens_brief` persists a typed block tree and returns a `shareUrl` (`useformat.ai/published/<orgId>/brief/<id>`). It does no AI work — you author every block. Validate first with `validateOnly: true`.

Block types: `callout` (variant: highlight/tldr/warning/info), `section` (heading + level 2/3 + child blocks; sections can't nest), `text` (GFM markdown; inline `{{insight:<id>}}` chips), `table` (headers + rows of cells; cells are markdown-able and accept `{{insight:<id>}}` chips), `insight` (full embedded insight by `insightId`), `chart`, `component`.

Recommended structure for this deliverable:
1. `callout` (highlight) — the thesis.
2. `section` "The picture" — `text` with the exec-summary bullets.
3. `section` "Where the calls disagree with the notes" — `insight` block(s) for proven accounts + `text` deltas.
4. `section` "Win-back tracker" — `text` legend + `table` (RAG | Account | $ | Reason & evidence | Turn-around play).
5. `section` "How this gets better" — coverage note.

A ready-to-edit payload is in `assets/lens-brief-payload.example.json`.

**Gotchas:**
- **Tier-gated:** `INSUFFICIENT_TIER: ... requires LensBrief access` means the org doesn't have the feature — a superadmin must enable it. Not a bug in your payload.
- **Cross-org chips:** an `{{insight:<id>}}` chip or `insight` block only resolves in the org that owns that insight. To preview a customer's brief in a different org you control, swap the chip for plain quoted text.
- Use a stable `idempotencyKey` to avoid duplicate briefs on re-runs.
