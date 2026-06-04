# Worked Scoring Example (gold standard)

This is the reference for **what a fully-substantiated scored call looks like.** Every run must match this standard: a per-dimension table, a source link in the card header, and evidence cells written so the reader grasps the score without decoding French. The example below is a **real scored call** (Simon Tanguy, 29 May 2026) with genuine quotes and Format/Aircall source links.

## Evidence-cell formula (read this — it is the point of the example)

Each evidence cell must be legible at a glance. Don't lean on the French quote to carry the meaning. Build every cell in this order:

1. **Plain-English point first** — the opening words say what the rep did. The quote is *proof*, not the explanation.
2. **Tag the speaker** — `Simon:` or `Prospect:` before every quote. Never leave it ambiguous who spoke.
3. **Short verbatim French quote** — add a 3–6 word English gloss in brackets only when the French isn't self-evident.
4. **`Missing: [≤5 words]`** at the end of any cell scored below `2/2` — the single thing that would have raised it. Omit on a clean `2/2`.

Cell shape: *Plain-English point. Speaker: "short FR quote" (gloss if needed). Missing: [≤5 words].*

Keep cells short. One quote per speaker per cell is usually enough; the `Missing:` note is the coaching takeaway, written for the reader.

## How to cite evidence

Every record from `get_record` carries source links:

- **Call source** — the `sourceUrl` field. Aircall: `https://workspace.aircall.io/inbox/conversations/{id}`. Video calls carry a Fathom share link instead.
- **Insight source** — each insight in the `insights` array has a `shareUrl` (`https://useformat.ai/share/insight/{id}`). Prefer this when the evidence is a Format-extracted insight; it deep-links to the exact moment and topic.

Put the **call source link in the card header** (one per call), and drop an insight `shareUrl` inline only on the specific cell it substantiates. Quote **verbatim French**, never paraphrased, never translated inside the quote marks. The English reading goes outside the quotes.

---

## Worked example — Simon Tanguy / CC Vallees de l'Orne et de Ledon (Mme Guillot)
**Date:** 29 May 2026 - **Duration:** 9:49 - **Direction:** outbound
**Call source:** https://workspace.aircall.io/inbox/conversations/3815851703
**Call type:** Prospecting (re-engagement of a lead first contacted earlier in the year) - **Reachability:** Conversation (got through the switchboard to the named contact)

### Per-dimension scoring

| Dimension | Wt | Score | Evidence |
|---|---|---|---|
| Opening & permission | 10% | `2/2` | Cleared the switchboard by name and reason, then re-anchored the prior contact. Simon: *"Vous pouvez me passer madame Guillot, s'il vous plait... On avait deja pu echanger en ce debut d'annee."* |
| Reason-for-call clarity | 10% | `2/2` | Said why he was calling in the first turn. Simon: *"je vous rappelle... pour voir si l'IA s'avait reussi a diminuer le taux d'erreur de tri."* |
| Discovery / pain | 20% | `2/2` | Probed with a number and surfaced the decision driver. Simon: *"en termes d'erreurs de tri, vous savez a combien? Parce que vous etiez a 23 pour 100."* Prospect: *"un objectif... d'etre en dessous des 20 pour 100... d'ici 2030"* (a mandate priority). -> https://useformat.ai/share/insight/znhacuirrmv3yh2qnvwdff9h |
| Value framing | 15% | `2/2` | Tied the product to her exact setup (chipped bins) with cross-territory proof. Simon: *"vu que vous avez le bac, c'est la camera... avec le bac puce, ca fait vraiment un tres bon effet."* |
| Objection handling | 20% | `1/2` | Took two brush-offs at face value. Prospect: *"on l'envisage peut-etre pour le futur marche... pas avant 2030"* -> Simon: *"Ok, je comprends, pas de souci"* (pivoted without testing the date). -> https://useformat.ai/share/insight/ydanjbig99uyid3f3nn7bklq Missing: a "what would change that?" probe. |
| Next step secured | 20% | `1/2` | Pitched a 30-min meeting well but let it close undated. Prospect: *"vous pouvez m'envoyer un support... j'ai deja des documents"* -> Simon accepted. Missing: a dated commitment. |
| Call control & register | 5% | `2/2` | Steered start to finish, warm register, never pushy. |

**Weighted score: (0.10×2 + 0.10×2 + 0.20×2 + 0.15×2 + 0.20×1 + 0.20×1 + 0.05×2) = `1.60/2.0`**

### Reading
Strong discovery, value framing, and control - a genuinely good prospecting call. The ceiling is the same one that defines Simon across the sample: when a real objection lands (outsourcing, 2030 timing), he acknowledges and pivots instead of probing what would actually change the picture, and lets the next step close undated. Note the buying signal he *did* surface but didn't convert: she named a concrete future trigger (2027 ADEME market renewal with performance contracts -> https://useformat.ai/share/insight/g6jflzijkec6770ydahfapxn). A score-2 version of this call books a dated call for Q4 2027 on the spot, or at minimum agrees a specific date to send tailored territory benchmarks and review them.

**Coaching priority:** objection handling -> next-step conversion. One behaviour, two dimensions: turn "je comprends, pas de souci" into "what would need to be true for this to move?" and convert the answer into a dated commitment.

---

## Source-link rules for the skill
- Put the **call `sourceUrl`** in the card header for every scored call so the user can open the recording.
- When a specific cell rests on a Format insight, drop its **`shareUrl`** inline on that cell — it deep-links to the moment and shows the topic tag.
- Every evidence cell follows the formula: plain-English point first, speaker tag on every quote, short verbatim French quote (+ gloss if needed), and `Missing: [≤5 words]` on anything below `2/2`.
- Never fabricate a link. If a record has no `sourceUrl`, write "(no source link on this record)".
- A routine `2/2` (clean opening, good register) can stand on the plain-English point alone; any `0/2` or `1/2` MUST carry a specific verbatim quote showing why, plus its `Missing:` note.
