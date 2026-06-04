---
name: aeo-seo-blog-post
description: "Write B2B SaaS blog posts that rank in traditional search AND get cited by AI answer engines (ChatGPT, Perplexity, Google AI Overviews, Claude). Use when the user wants to write a blog post, draft a blog article, create content for their blog, or mentions 'blog post,' 'blog article,' 'write a post about,' 'draft a blog,' 'content brief,' 'blog draft,' 'SEO blog post,' 'AEO blog post,' 'AI-optimized blog post,' or 'write about [topic].' This skill produces blog posts that are structured for both human readers and AI extraction — answer-first, extractable, opinionated, and backed by data. Works best with a customer intelligence platform like Format (MCP server) for sourcing original insights, but also works standalone."
---

# Blog Post Playbook

Every B2B SaaS company publishes blog posts. Almost none of them get cited by AI search engines. The posts that do get cited share three properties: they answer a specific question directly, they contain information AI can't fabricate on its own, and they're structured so an LLM can lift a clean passage without losing meaning.

This playbook builds blog posts that work for both audiences — human readers who skim, and AI systems that extract. One post, two lenses: search demand for humans, extractable answers for machines.

---

## Step 1: Pick the Right Post Type

Not all blog content is equally citable. Choose the format that matches the query intent.

| Format | Best for | AI citation strength |
|--------|----------|---------------------|
| **Comparison post** ("X vs Y") | Buyer evaluation queries | Very high — AI maps these to decision tasks |
| **How-to guide** | Implementation, setup, migration queries | High — step structure is easy to chunk and cite |
| **Definitive guide** | Category education, "what is X" queries | High — becomes the go-to explanation source |
| **Original research** | Authority building, recurring citations | Highest — contains data AI can't fabricate |
| **Listicle** ("Best X for Y") | Commercial shortlist queries | High — scannable, entity-rich |
| **Opinion / analysis** | Thought leadership | Low unless grounded in data and frameworks |

**What almost never gets cited:** brand-first promotional pages, generic top-of-funnel posts rehashing common advice, thin thought leadership with no data, content that sounds like marketing, and purely subjective opinion pieces.

**The test:** If an LLM already knows everything in your post from its training data, it has no reason to cite you. Your post needs to contain something it can't make up — proprietary data, real customer examples, a novel framework, or specific operational detail.

---

## Step 2: Build the Content Brief

Before writing, build a brief with two lenses: SEO demand and AI extractability.

### Keyword + prompt research

Start with the primary topic, then expand into the sub-questions an AI system would break it into. AI search does "query fan-out" — one prompt expands into multiple longer, more specific follow-up queries.

**Workflow:**
1. Pick the primary topic and its commercial intent.
2. Pull 5–15 related question variants from Google, "People Also Ask," customer calls, sales notes, and AI prompt testing (ask the question in ChatGPT/Perplexity and see what follow-ups they generate).
3. Group into sub-intents: define, compare, evaluate, implement, troubleshoot, prove.
4. Map one page as the canonical answer. Supporting questions become H2 sections, FAQ blocks, or separate cluster posts.

### With Format MCP (the fast path)

Format gives you something most blogs don't have: the actual language your customers use to describe their problems. This is gold for blog content because it's original, specific, and impossible for AI to fabricate.

```
1. Format MCP → search_insights
   Search for how customers talk about the topic:
   - Pain language: "struggling with," "we used to," "the problem is"
   - Solution language: "now we can," "what changed," "the difference"
   - Comparison language: "compared to," "switched from," "better than"

2. Format MCP → get_record
   Pull specific conversation snippets for:
   - Real quotes to use in the post
   - Specific details and numbers customers mentioned
   - The exact words they use (not your marketing language)

3. Format MCP → list_records
   Check which customers are talking about this topic most,
   and whether there's enough material for a mini case study
   or data point to embed in the post.
```

This takes about 15 minutes and gives you original customer evidence that no competitor can replicate. A blog post with three real customer quotes and a specific metric from your data is infinitely more citable than one with generic advice.

### Without Format (manual path)

Pull customer language from call recordings (Gong, Fireflies, Fathom), support tickets, sales notes, and Slack. Ask CS and Sales: "How do customers describe this problem in their own words?" and "Has anyone mentioned specific numbers or before/after comparisons?"

### Brief template

```
TOPIC: [Primary topic]
TARGET QUERY: [The question this post answers]
POST TYPE: [Comparison / How-to / Guide / Research / Listicle / Opinion]

PRIMARY ANSWER: [One sentence — what would you want an AI to quote?]

SUB-QUESTIONS (H2 candidates):
- [Question 1]
- [Question 2]
- [Question 3]
- [Question 4]

ORIGINAL EVIDENCE:
- [Customer quote or data point 1]
- [Customer quote or data point 2]
- [Proprietary framework or insight]
- [Specific metric or benchmark]

EXPERT ATTRIBUTION:
- [Who is the author? What makes them credible on this topic?]
- [Any external experts to quote?]

COMPETING CONTENT:
- [Top 3 posts currently ranking / getting cited for this query]
- [What do they cover that you must also cover?]
- [What are they missing that you can add?]
```

---

## Step 3: Structure the Post

The fundamental unit of an AI-optimized blog post is the **self-contained semantic chunk** — a passage that makes complete sense when lifted out of the page. Every major section should work as a standalone answer.

### The template

```
H1: Topic + year if freshness matters
    [2–3 sentence intro with the direct answer first]

H2: What is [topic]?
    [Definition in first sentence → why it matters → concrete example]

H2: Why does [topic] matter for [audience]?
    [Hook → explanation → evidence → takeaway]

H2: How to [do the thing] (or: How it works)
    [Steps, each as H3 or numbered list]

H2: [Comparison / Common mistakes / What most people get wrong]
    [Table or structured contrast]

H2: [Real example / Case study / What we learned]
    [Specific, named, detailed]

H2: FAQ
    [3–7 real questions, answered in under 60 words each]
```

This gives AI systems multiple clean entry points for retrieval while reading naturally for humans.

### Structural rules

**Headings as retrieval anchors:**
- One H1 that clearly names the topic.
- H2s phrased as questions that match how people actually search ("How do B2B SaaS companies reduce churn?" not "Churn Reduction Strategies").
- H3s for definitions, examples, steps, and caveats.
- Consistent patterns — if one section is "How to…" don't label the next one "Tips."

**Paragraphs as extractable units:**
- 2–5 sentences per paragraph, one idea each.
- 40–60 words is the sweet spot for snippet extraction.
- Each paragraph should make sense if copied out of context — no orphan pronouns ("this," "that," "they") pointing to earlier paragraphs.
- Lead every section with the direct answer, then expand.

**Answer blocks throughout:**
- Short definition paragraphs ("In one sentence, X is…").
- Step lists for processes.
- Tables for comparisons, metrics, frameworks.
- FAQ sections with question-based headings.
- Blockquote-formatted expert quotes with name and title.

> For the full section-by-section writing guide, voice rules, and the H.E.A.R.T. framework for each section, read `references/writing-guide.md`

---

## Step 4: Write for Both Audiences

The biggest trap in "AI-optimized" content is stripping away all voice and personality until it reads like a textbook. You need structure *plus* soul.

### What makes a post human

- **Specific situations, not abstractions.** Instead of "Benefits of call summaries," use "How a CS leader actually uses call summaries in QBRs."
- **At least one story or mini-case per post.** Two or three paragraphs about a real customer, experiment, or failure instantly separates you from generic AI copy.
- **Opinionated edges.** If everything sounds like a consensus committee, both readers and AI ranking models treat it as commodity content.
- **Natural rhythm.** Short sentences for punch, longer ones for nuance. Don't start five sentences the same way.
- **First-person and "we."** Human content uses personal references and lived-experience anecdotes. LLM-generated content is relentlessly third-person and formal.

### What makes a post citable

- **Statistics with sources.** "72% of AI-generated responses referenced content with schema markup" beats "schema can help your AI visibility."
- **Explicit relationships.** Don't just list concepts — connect them: "Topical authority helps AI systems trust your coverage, while structured data clarifies relationships between pages."
- **Named experts and roles.** "According to Jane Doe, VP of RevOps at Z…" gives both humans and AI entities to anchor on.
- **Original data.** Your own product analytics, customer benchmarks, survey results, or anonymized case data. This is the single strongest citation signal — it's information AI can't fabricate.
- **Definitive phrasing.** AI systems prioritize confident, factual statements over hedged, speculative language. "Enterprise CRM implementations experience a 63% failure rate" gets cited; "Many companies struggle with CRM implementations" does not.

### The 3-part pattern for balancing synthesis and originality

For any section, use:

1. **Baseline** — Briefly recap the accepted view (often with an external source).
2. **Tension** — What's missing, broken, or oversimplified in that view.
3. **Take** — Your framework, heuristic, or evidence that resolves the tension.

This naturally produces content that AI needs to cite (because the "Take" is original) while including enough canonical context for the model to understand what the page is about.

> For detailed voice rules, the editing checklist, and examples, read `references/writing-guide.md`

---

## Step 5: On-Page SEO + AEO Elements

Before publishing, add the technical layer that helps both traditional search and AI systems.

### Title tag
Primary keyword + clear outcome, early in the string. Avoid cleverness that hides the topic. AI embedding models need to classify the page from the title alone.

### Meta description
Concise, plain-language summary of the post's main answer. Still mostly a CTR play, but AI systems parse it during initial relevance scoring.

### Schema markup
Use schema as **entity clarification**, not magic ranking juice. Deploy as JSON-LD:

| Schema type | When to use |
|------------|-------------|
| `Article` / `BlogPosting` | Every blog post — headline, author, datePublished, dateModified |
| `FAQPage` | When you have an FAQ section — 3–7 questions, answers under 60 words |
| `Organization` | Site-wide — name, url, logo, sameAs links |
| `Person` | Author schema — name, credentials, sameAs links to LinkedIn etc. |

FAQ schema is the highest-leverage extraction trigger. When FAQ sections have real user queries answered in under 60 words starting with a direct factual statement, they get pulled into AI Overviews routinely.

### Internal linking
- Link from high-authority existing pages to the new post immediately.
- Link out to related cluster pages with descriptive anchor text.
- Build bidirectional links so the topical graph is obvious to crawlers.
- Use natural language anchors, not exact-match commercial keywords.

### Author bio
Not an afterthought. Include relevant experience, niche specialization, notable companies, and a line that ties directly to the topic. Add photo and links to LinkedIn, conference talks, or bylined work. AI systems cross-reference the author's name across the web to build a credibility profile.

### Freshness signals
- Show "Last updated: [date]" visibly on the page.
- Use `dateModified` in schema (ISO 8601 format).
- AI-cited content is notably fresher than traditional organic results.

> For the full pre-publish and post-publish checklist, read `references/seo-aeo-checklist.md`

---

## Step 6: Publish and Distribute

Publication is the starting line, not the finish. AI citation visibility compounds when the post is distributed, linked, and referenced across multiple credible surfaces.

### Launch sequence

1. **Publish** with strong title, intro, headings, and schema.
2. **Internal link** from 3–5 relevant high-authority pages on your site immediately.
3. **Share on LinkedIn** — not a link drop, but a native post that extracts the core insight and links to the full post.
4. **Repurpose** the core insight into a YouTube video (transcript = searchable text layer), a Quora answer, and a relevant subreddit discussion.
5. **Earn external links** — partner blogs, roundups, analyst mentions, or guest posts that reference the post's data or framework.
6. **Refresh within 30–60 days** — add new data, examples, or a stronger answer. Update `dateModified` schema.

### Timeline to citation

- **Hours to days:** Crawl and indexing for a well-connected page.
- **1–4 weeks:** Earliest AI citations if topic is timely, structure is clean, and distribution is strong.
- **30–60 days:** Realistic window for noticeable citation gains after updates and external mentions accumulate.
- **Ongoing:** Citation visibility compounds with refreshes and repeated references.

### Platform priority for AI visibility

| Platform | Why it helps | Best use |
|----------|-------------|----------|
| **Reddit** | Heavily cited in AI answers for experience-based queries | Participate authentically in relevant subreddits |
| **YouTube** | Transcripts are rich in entities and step-by-step explanations | Walkthroughs, comparisons, demos with transcripts |
| **LinkedIn** | Primary extraction source for B2B queries | Syndicate core insights as native thought-leadership posts |
| **G2 / review sites** | AI relies on these for product evaluation queries | Build genuine reviews mentioning specific features and use cases |
| **Quora** | Surfaces in "how to" and "what is" AI answers | Answer detailed buyer questions with practical specifics |

### What matters most

Prioritize **credible third-party mentions, strong internal linking, and freshness** over raw social volume. For B2B SaaS, the combination that works best is: one authoritative blog post, one or two supporting refreshes, a few good contextual backlinks, a syndication or guest post version, and visible presence on at least one third-party discussion or review platform.

---

## Why This Works

Most B2B blog posts fail at AI citation because they contain nothing an LLM doesn't already know. They rehash common advice in generic language with no data, no customer evidence, and no structural hooks for extraction.

This playbook fixes that by combining three things:

1. **Structure that AI can extract** — answer-first sections, question-based headings, self-contained paragraphs, tables, and FAQ blocks.
2. **Content that AI needs to cite** — original data, real customer quotes, proprietary frameworks, and specific operational detail that can't be fabricated.
3. **Distribution that AI trusts** — the same claims validated across your blog, LinkedIn, Reddit, review sites, and partner mentions.

With Format, the original evidence sourcing takes about 15 minutes. Without it, you can do the same thing by mining call recordings and support tickets manually — it just takes longer.

Either way: structure for extraction, write for both audiences, and give AI a reason to cite you.

---

## Reference Files

- **`references/writing-guide.md`** — Section-by-section writing template, voice rules, the H.E.A.R.T. framework, editing checklist, and before/after examples.

- **`references/seo-aeo-checklist.md`** — Pre-publish and post-publish checklist for SEO and AEO elements. Schema templates, internal linking rules, and distribution steps.

- **`references/content-patterns.md`** — Templates for the five blog post types that get cited most: comparison, how-to, definitive guide, original research, and listicle. Structural patterns and examples for each.
