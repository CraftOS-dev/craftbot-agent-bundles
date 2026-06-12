<!--
Sources: https://www.talentprise.com/linkedin-boolean-search-guide/
         https://developer.linkedin.com/product-catalog/talent
         https://www.unipile.com/linkedin-recruiter-search-api-guide-for-developers-and-editors/
         https://explore.hireez.com/blog/how-to-source-candidates-on-github/
2026 SOTA: nested Boolean within ≤1,000 char keyword field; layer LinkedIn's 40+ filters;
AI Boolean Builder fallback via hireEZ/SeekOut Assist/Juicebox; LinkedIn Recruiter AI surfaces
+69% reply-rate lift since Apr 2026.
-->
# LinkedIn Recruiter — Boolean Search Strings — SKILL

Author 2026-SOTA LinkedIn Recruiter (and Sales Nav) Boolean keyword strings, layer the 40-filter cabinet on top, and fall back to AI Boolean Builders (hireEZ / SeekOut Assist / Juicebox) when complexity exceeds the recruiter's hand-author budget. Boolean beats LinkedIn search filters by 10×; the cabinet beats the keyword field for everything that isn't title/skill/exclusion.

## When to use

- User wants to **build a sourcing string for {role}** on LinkedIn Recruiter, Sales Navigator, or LinkedIn-classic.
- User pastes a JD and asks "give me a Boolean".
- User's current string returns 0 results, returns 50,000 results, or returns the wrong seniority band.
- Trigger phrases: "Boolean for X", "search string", "sourcing query", "LinkedIn search", "Recruiter query", "0 results", "too noisy", "too many".

Do not use for: composing the InMail (`cold-inmail-warm-intro`), pushing to ATS (`gem-hireez-beamery-talent-crm` push-to-ATS recipe), or building a target-company list (`target-company-mapping-crunchbase-linkedin`).

## Setup

```bash
# LinkedIn Recruiter — seat required; no public Boolean API.
# Two execution paths:
#   1) Hand-paste authored string into LinkedIn Recruiter UI keyword field.
#   2) playwright-mcp UI automation (non-Partner recipients).
#   3) Talent Solutions Recruiter Search API (Partner-approved only).

# Optional: Talent Solutions API via Unipile proxy (non-Partner workaround).
export UNIPILE_API_KEY="xxx"      # https://www.unipile.com/
export UNIPILE_ACCOUNT_ID="xxx"   # account that owns the Recruiter seat

# Optional: AI Boolean Builder seats.
export HIREEZ_API_KEY="xxx"       # AI Boolean Builder + 45+ source aggregation
export SEEKOUT_API_KEY="xxx"      # SeekOut Assist — paste JD → Boolean overlay
```

Hard limit: the keyword field is **≤1,000 characters**. Plan your AND/OR clusters before authoring.

## Common recipes

### Recipe 1: Boolean string grammar (the only syntax LinkedIn parses)

```
( "phrase one" OR "phrase two" )    # OR — at least one match
AND ( term1 OR term2 )              # AND — all clusters required
AND NOT ( exclude1 OR exclude2 )    # NOT — knock out noise
NOT recruiter                       # works without parens for a single term
"quoted phrase"                     # exact match; required for multi-word terms
```

Rules that bite people:
- Operators MUST be UPPERCASE (`AND` / `OR` / `NOT`) — lowercase is a literal keyword.
- Use parentheses around every OR cluster. LinkedIn parses left-to-right without them.
- LinkedIn's keyword field caps at ~1,000 chars; over-long strings silently truncate.
- Wildcards (`*`) work but are slow and produce drift; prefer enumerated OR.
- Diacritics: LinkedIn folds accents (`Jürgen` matches `Jurgen`).

### Recipe 2: Title cluster — the load-bearing AND

```
("staff" OR "principal" OR "senior staff" OR "senior" OR "lead")
AND ("software engineer" OR "backend engineer" OR "platform engineer")
```

Pattern: seniority OR cluster × role-noun OR cluster. Always quote multi-word titles.

### Recipe 3: Skill cluster — required tech / methods

```
AND (Python OR Golang OR Go OR Rust)
AND ("distributed systems" OR Kubernetes OR microservices OR "API design")
```

Pattern: language(s) OR stack × architecture/method OR cluster. Keep clusters short — every AND eliminates ~70% of the pool.

### Recipe 4: Exclusion cluster — the silent quality lever

```
AND NOT (recruiter OR consultant OR "hiring manager" OR student OR intern OR coach OR "career advisor")
```

Pattern: anti-roles + early-career + agency. Always exclude `recruiter` (your own world will pollute results).

### Recipe 5: Senior Backend Engineer (Python/Go) — startup ICP

```
(("staff" OR "principal" OR "senior" OR "lead") AND ("software engineer" OR "backend engineer" OR "platform engineer"))
AND (Python OR Golang OR Go OR Rust)
AND ("distributed systems" OR Kubernetes OR microservices OR "API design")
AND NOT (recruiter OR consultant OR "hiring manager" OR student OR intern)
```

Char count: 287. Filter layer: geography (target metros), current company headcount 50-1000, seniority Senior IC / Manager+, years 5+.

### Recipe 6: Staff Frontend Engineer (React/TS) — growth-stage

```
(("staff" OR "principal" OR "senior staff") AND ("frontend engineer" OR "web engineer" OR "UI engineer"))
AND (React AND (TypeScript OR Typescript))
AND ("design system" OR Storybook OR accessibility OR "web performance")
AND NOT (recruiter OR consultant OR student OR intern)
```

Char count: 270. Filter: seniority Senior IC, years 7+, company stage Series A-D.

### Recipe 7: Engineering Manager (50-150 person team)

```
(("engineering manager" OR "director of engineering" OR "VP engineering") AND NOT (CTO OR "CTO/VP"))
AND ("team of" OR "leading" OR "managing")
AND ("hired" OR "scaled" OR "grew the team")
AND NOT (recruiter OR consultant)
```

Char count: 235. Filter: function Engineering, seniority Director/VP, company headcount 100-500.

### Recipe 8: Product Designer (B2B SaaS)

```
(("senior product designer" OR "staff product designer" OR "lead designer" OR "principal designer") AND ("B2B" OR "SaaS" OR "enterprise"))
AND (Figma AND ("design system" OR "design ops"))
AND (research OR "user research" OR "user testing")
AND NOT (graphic OR brand OR illustration OR motion OR student)
```

Char count: 313. Filter: function Design, industry SaaS/B2B, geography target metros.

### Recipe 9: Account Executive (SaaS $50-150K ACV)

```
(("account executive" OR "senior AE" OR "enterprise AE") AND ("SaaS" OR "B2B"))
AND ("quota" OR "ARR" OR "ACV" OR "closed won")
AND ("100%" OR "110%" OR "120%" OR "President's Club" OR "President Club")
AND NOT (BDR OR SDR OR "sales development" OR student)
```

Char count: 271. Filter: function Sales, seniority Senior IC, years 3-7, current company SaaS.

### Recipe 10: CTO / VP Engineering (Series B-D)

```
((CTO OR "chief technology officer" OR "VP of engineering" OR "head of engineering") AND ("series B" OR "series C" OR "series D" OR "growth stage"))
AND ("scaled" OR "hired" OR "built the team" OR "founding")
AND NOT (recruiter OR consultant OR student OR "in transition")
```

Char count: 274. Filter: function Engineering, seniority CXO/VP, current/past company Series B-D, tenure 3-5y.

### Recipe 11: Layer the 40-filter cabinet (do NOT cram into Boolean)

LinkedIn Recruiter / Sales Nav filters that beat keyword-field equivalents:

geography · current company · past company · current title · past title · school · years of experience · years at current company · function · industry · seniority · profile language · group membership · skills · certifications · languages · willing to relocate · recent activity · employer signals (layoffs / funding) · TeamLink (mutual connections) · Open Candidates flag · Project / Folder · Saved Search membership · InMail status (opened / not contacted / replied) · interest signals (Open to Work) · Spotlights (Liking job posts, Following company) · profile completeness · photo presence · recent job change · company size · company growth rate · HQ geography · Premium subscriber · profile views last 90d · school graduation year · military experience.

Use Boolean for title + skill + exclusion only. Everything else goes in filter dropdowns.

### Recipe 12: AI Boolean Builder fallback (paste JD → Boolean)

```bash
# hireEZ (preferred — 45+ source aggregation overlay)
curl -X POST "https://api.hireez.com/v1/boolean/generate" \
  -H "Authorization: Bearer $HIREEZ_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"job_description":"<full JD text>","platform":"linkedin"}'

# SeekOut Assist — UI-only (paste JD → review Boolean + diversity filter overlay)
# Open SeekOut → Assist → paste JD → run → copy Boolean for LinkedIn paste

# Juicebox — natural-language search pioneer (good for niche queries)
# Open Juicebox → paste JD → review candidate list → export Boolean

# LinkedIn Recruiter native AI (since April 2026; 69% reply-rate lift on assisted outreach)
# Recruiter UI → "Generate search" → paste JD → review + edit
```

### Recipe 13: Talent Solutions API call (Partner-approved only)

```bash
# Direct Recruiter Search API (Partner-tier LinkedIn Talent Solutions)
curl -H "Authorization: Bearer $LINKEDIN_TOKEN" \
  -H "X-Restli-Protocol-Version: 2.0.0" \
  "https://api.linkedin.com/v2/recruiterSearch?q=fullText&keywords=<URL-encoded-boolean>&start=0&count=25"

# Non-Partner workaround via Unipile proxy
curl -H "X-API-KEY: $UNIPILE_API_KEY" \
  "https://api.unipile.com/api/v1/linkedin/search?account_id=$UNIPILE_ACCOUNT_ID&keywords=<encoded>&type=people"
```

### Recipe 14: playwright-mcp non-API path

```python
# Pseudo — talent-sourcer wires this via playwright-mcp
await playwright.goto("https://recruiter.linkedin.com/")
await playwright.fill("[data-test-keyword-input]", BOOLEAN_STRING)
await playwright.click("[data-test-search-button]")
for profile in await playwright.query_all(".profile-row"):
    yield extract(profile)
```

## Examples

### Example 1: 0-result Boolean rescue
**Goal:** User's string returns 0; identify the over-constraining cluster.
**Steps:**
1. Count AND clauses. >4 AND clauses is the usual cause (Antipattern 1 in role.md).
2. Drop the most-specific AND (usually the architecture / tool cluster); re-run.
3. If still 0, drop the seniority cluster; re-run; widen seniority on the filter cabinet.
4. Target: 80-200 results (the sweet spot for a single sourcing pass).

**Result:** Each AND drop typically multiplies result set 3-10×. Stop at 80-200.

### Example 2: 50,000-result Boolean tighten
**Goal:** User's string returns >10k; needs precision.
**Steps:**
1. Add an exclusion cluster: `AND NOT (recruiter OR student OR consultant OR intern OR coach)`.
2. Quote partial-match terms: `senior engineer` → `"senior engineer"` (drops ~40%).
3. Move 2-3 nice-to-haves from `OR` to `AND` (forces presence).
4. Filter cabinet: tighten geography, current company headcount, years experience.

**Result:** 50k → 200-500. Then layer Spotlights (Open to Work) for further qualification.

### Example 3: JD → Boolean via SeekOut Assist
**Goal:** Author Boolean for a niche role (e.g., "GPU kernel engineer with CUDA + Triton").
**Steps:**
1. Paste full JD into SeekOut Assist (UI).
2. Review auto-generated Boolean + diversity filter overlay.
3. Copy Boolean → paste into LinkedIn Recruiter keyword field.
4. Cross-validate by running same string in hireEZ AI Boolean Builder; pick the tighter cluster set.

**Result:** Niche Boolean authored in <5 min; hand-author would take 20-30 min and miss synonyms.

## Edge cases / gotchas

- **The ≤1,000 char limit silently truncates.** Author in a text editor; check char count before pasting.
- **`OR` without parens is the #1 bug.** `A OR B AND C` parses as `A OR (B AND C)`, not `(A OR B) AND C`.
- **LinkedIn parses `AND NOT` as `NOT` if you forget the AND.** Always write `AND NOT (...)`.
- **Boolean does NOT search profile education / experience fields.** Use the filter cabinet for school, current company, past company, years experience. Boolean only hits the keyword index (current title + about + experience descriptions).
- **Wildcards `*`** match suffix only (`engineer*` matches `engineering` but not `re-engineering`). Avoid; prefer enumerated OR.
- **Recruiter Lite ≠ Recruiter ≠ Recruiter Corporate.** Lite caps at 30 InMails/mo, no AI Boolean assist, no Recruiter API. Corporate tier needed for high-volume + API surfaces.
- **Talent Solutions Recruiter Search API is partner-gated.** Non-Partner recipients use `playwright-mcp` UI automation or Unipile proxy. Either path violates LinkedIn ToS at high volumes — rate-limit aggressively (≤30 searches/hour) to avoid account flags.
- **LinkedIn's "AI Assist" since April 2026** drives a 69% reply-rate lift on assisted outreach — enable in Recruiter settings; it costs no extra seat fee on Corporate tier.
- **Recruiter Search results vary by region.** US-only Recruiter Corporate seats see a different result distribution than EMEA/APAC. Test in target geo before locking the string.
- **0 / 1 / 2 result outputs usually mean the Boolean intersected an empty cell, not "no candidates exist".** Drop the most-specific clause first.
- **Saved Searches lose Boolean when reopened on mobile.** Always edit on desktop.
- **`"phrase"` ≠ `phrase`**. `"product designer"` is exact; `product designer` returns anyone with both words anywhere in the indexed text.
- **Defer compensation philosophy + offer structure to `ceo-agent` / `operations-agent`.** This skill authors strings only.

## Sources

- Talentprise — LinkedIn Boolean Search Complete 2026 Guide: https://www.talentprise.com/linkedin-boolean-search-guide/
- LinkedIn Developer — Talent Solutions Product Catalog: https://developer.linkedin.com/product-catalog/talent
- Unipile — LinkedIn Recruiter Search API Guide: https://www.unipile.com/linkedin-recruiter-search-api-guide-for-developers-and-editors/
- hireEZ — Complete Guide to Source Candidates on GitHub (covers AI Boolean Builder): https://explore.hireez.com/blog/how-to-source-candidates-on-github/
- Juicebox — SeekOut Reviews 2026 (SeekOut Assist): https://juicebox.ai/blog/seekout-reviews
- ConnectSafely — LinkedIn InMail Templates Response Rates 2026 (AI Assist 69% lift): https://connectsafely.ai/articles/linkedin-inmail-templates-response-rates-2026
- Salesflow — LinkedIn InMail Best Practices 2026: https://salesflow.io/blog/linkedin-inmail-best-practices-improve-response-rates
