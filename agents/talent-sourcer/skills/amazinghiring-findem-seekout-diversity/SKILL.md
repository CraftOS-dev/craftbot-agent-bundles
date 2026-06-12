<!--
Sources: https://juicebox.ai/blog/seekout-reviews
         https://skima.ai/blog/product-deep-dives/seekout-review
         https://mindhuntai.com/blog/diversity-sourcing-strategies
         https://www.findem.ai/
         https://amazinghiring.com
SeekOut 800M+ profiles, 330M URM profiles, Bias Reducer mode, SeekOut Assist (Apr 2026).
Findem people-as-data graph, attribute-based filters.
AmazingHiring 50+ dev networks (GitHub + SO + Kaggle + Bitbucket + DEV.to + HackerRank + LeetCode + conference speakers).
-->
# AmazingHiring / Findem / SeekOut — Diversity + Aggregator Sourcing — SKILL

Surface candidates from the three SOTA aggregator platforms that overlay LinkedIn with diversity filters and 50+ dev-network signals. SeekOut for diversity scale + Bias Reducer mode. Findem for attribute-based filters (surfaces candidates title-search misses). AmazingHiring for 50-platform dev-specific overlay. Diversity sourcing is intentional — these tools surface the pool that LinkedIn alone misses.

## When to use

- User wants **diversity-filtered sourcing** (women, Black, Latine, LGBTQ+, veteran, AAPI) for a req.
- User asks "expand my source mix beyond LinkedIn for this technical role".
- User wants candidates **surfaced by attributes**, not titles (e.g., "ex-FAANG", "open-source contributor", "former founder").
- Cross-validation of GitHub / Stack Overflow signal in a unified profile.
- Trigger phrases: "diversity sourcing", "URM candidates", "SeekOut search", "Findem attribute filter", "AmazingHiring dev profile", "Bias Reducer", "expand source mix".

Do not use for: LinkedIn-only Boolean (`linkedin-recruiter-boolean-search-strings`); project-community channels (`diversity-channel-sourcing-dev-color-code2040`); naive name-based diversity inference (Antipattern 3 in role.md).

## Setup

```bash
# SeekOut — paid enterprise seat $500-1,200/user/mo typical.
# https://app.seekout.com/api-settings
export SEEKOUT_API_KEY="xxx"

# Findem — paid seat; pricing custom.
# https://app.findem.ai/settings/api
export FINDEM_API_KEY="xxx"

# AmazingHiring — paid seat $300-700/mo per recruiter.
# https://app.amazinghiring.com/settings/integrations
export AMAZINGHIRING_API_KEY="xxx"
```

Most recipients have ONE of these three (rarely all). Skill auto-detects which key is set; falls back to free path (GitHub + Stack Overflow + LinkedIn Boolean + project-channel warm intros).

## Common recipes

### Recipe 1: SeekOut — diversity-filtered search

```bash
curl -X POST "https://api.seekout.com/v1/search/people" \
  -H "Authorization: Bearer $SEEKOUT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "boolean": "(staff OR principal) AND (software engineer) AND (python OR golang)",
    "location": ["United States"],
    "diversity": {
      "gender": ["female"],
      "ethnicity": ["Black", "Hispanic", "AAPI"],
      "veteran": false
    },
    "limit": 100
  }'
```

Diversity filters use probabilistic signals (name + photo + school + community membership). Treat as confidence-banded, NOT ground truth (see Antipattern 3 in role.md). The actual confidence band is in the response per-candidate.

### Recipe 2: SeekOut Bias Reducer mode

```bash
# Bias Reducer: returns candidates without name + photo + school in initial response
# Reviewer screens on skills + experience only; identity revealed on shortlist
curl -X POST "https://api.seekout.com/v1/search/people" \
  -H "Authorization: Bearer $SEEKOUT_API_KEY" \
  -d '{
    "boolean": "(staff OR principal) AND (data engineer)",
    "bias_reducer": true,
    "limit": 100
  }'
```

Bias Reducer addresses screening bias, not sourcing bias. Pair with diversity filter from Recipe 1 for full-funnel intervention.

### Recipe 3: SeekOut Assist — paste JD → Boolean + filter overlay

```bash
# SeekOut Assist auto-generates Boolean from JD; adds diversity filter overlay automatically
curl -X POST "https://api.seekout.com/v1/assist/generate" \
  -H "Authorization: Bearer $SEEKOUT_API_KEY" \
  -d '{
    "job_description": "<full JD text>",
    "diversity_overlay": true
  }'

# Response:
# {
#   "boolean": "(senior OR staff) AND (machine learning engineer) AND (pytorch OR tensorflow)",
#   "filters": {"location": "US", "diversity": {"gender": "female", "ethnicity": ["Black", "Hispanic"]}},
#   "estimated_pool_size": 12500
# }
```

### Recipe 4: SeekOut — technical-skill + GitHub activity scoring

```bash
curl -X POST "https://api.seekout.com/v1/search/people" \
  -H "Authorization: Bearer $SEEKOUT_API_KEY" \
  -d '{
    "boolean": "(senior OR staff) AND (machine learning OR ML engineer)",
    "github_activity": {
      "languages": ["python", "rust"],
      "min_stars_on_repos": 50,
      "active_last_180_days": true
    },
    "limit": 100
  }'
```

GitHub activity scoring is the SeekOut differentiator vs Findem. Use when GitHub signal is the validation gate.

### Recipe 5: Findem — attribute-based search (the title-blind surface)

```bash
# Findem surfaces candidates by attributes, not titles
curl -X POST "https://api.findem.ai/v1/search" \
  -H "Authorization: Bearer $FINDEM_API_KEY" \
  -d '{
    "attributes": {
      "has_worked_at": ["Stripe", "Plaid", "Square"],
      "open_source_contributor": true,
      "conference_speaker": ["KubeCon", "PyCon"],
      "patents_filed": ">0",
      "current_seniority": ["Staff", "Principal"],
      "former_founder": true
    },
    "location": ["San Francisco", "New York"],
    "limit": 100
  }'
```

Attribute filters surface candidates whose titles don't match your Boolean but whose actual experience does. Common surprise: founders who joined as IC at a competitor (Findem catches; LinkedIn title-search misses).

### Recipe 6: Findem — diversity-attribute search

```bash
curl -X POST "https://api.findem.ai/v1/search" \
  -H "Authorization: Bearer $FINDEM_API_KEY" \
  -d '{
    "attributes": {
      "current_seniority": ["Senior", "Staff"],
      "education_diversity": {"hbcu": true},
      "community_affiliation": ["devcolor", "code2040", "lesbians-who-tech"]
    },
    "limit": 100
  }'
```

`community_affiliation` flags self-disclosed membership in diversity communities — surfaces warm-intro paths via the project-channel skill.

### Recipe 7: AmazingHiring — 50-network dev overlay

```bash
curl -X POST "https://api.amazinghiring.com/v1/candidates/search" \
  -H "Authorization: Bearer $AMAZINGHIRING_API_KEY" \
  -d '{
    "skills": ["Python", "PyTorch", "CUDA"],
    "location": "Berlin",
    "min_score": 70,
    "networks": ["github", "stackoverflow", "kaggle", "huggingface", "leetcode", "papers_with_code"],
    "diversity_filter": true,
    "limit": 100
  }'
```

AmazingHiring aggregates 50+ networks into a single dev profile with a 0-100 score. The `diversity_filter: true` is opt-in (talk to AmazingHiring CS to enable).

### Recipe 8: AmazingHiring — single-candidate profile pull

```bash
# Get full multi-network profile for a sourced candidate
curl "https://api.amazinghiring.com/v1/candidates/{candidate_id}/profile" \
  -H "Authorization: Bearer $AMAZINGHIRING_API_KEY"

# Returns:
# - GitHub: commits, stars, languages, last_active
# - Stack Overflow: reputation, top tags
# - Kaggle: competitions, rank
# - HackerRank / LeetCode: problems solved
# - Conference speakers: talks, dates
# - DEV.to / Medium: blog posts
# - All linked via name + location + email match
```

### Recipe 9: Cross-aggregator deduplication

When sourcing across SeekOut + Findem + AmazingHiring, dedupe by:

```python
def dedupe_aggregator_candidates(candidates):
    """Dedupe by (linkedin_url || email_hash || github_handle)."""
    seen = set()
    deduped = []
    for c in candidates:
        keys = {
            c.get("linkedin_url"),
            hashlib.sha256(c.get("email", "").lower().encode()).hexdigest() if c.get("email") else None,
            c.get("github_handle"),
        }
        keys = {k for k in keys if k}
        if any(k in seen for k in keys):
            continue
        seen.update(keys)
        deduped.append(c)
    return deduped
```

### Recipe 10: Bias-reducer review workflow

For senior hires where bias risk is highest:

1. SeekOut Bias Reducer search (Recipe 2) → shortlist 50.
2. Engineer / hiring manager rates skills + experience on anonymized profiles (1-5 scale).
3. Reveal identities after rating; verify rating doesn't shift.
4. Calibrate weekly — if reveal causes consistent rating shift in any direction, retrain the reviewer panel.

Bias reducer is a process, not a checkbox.

## Examples

### Example 1: Diversity-overlay search for staff ML eng
**Goal:** 100 staff ML engineers in US with SeekOut diversity + GitHub activity overlay.
**Steps:**
1. SeekOut Assist (Recipe 3) — paste JD, get Boolean + diversity overlay.
2. Refine GitHub activity filter (Recipe 4) — `languages=[python], stars>50, active_180d`.
3. Bias Reducer (Recipe 2) → 100 anonymized shortlist.
4. Hiring manager skill-rates anonymized.
5. Reveal + outreach via `cold-inmail-warm-intro`.

**Result:** Skill-rated shortlist before identity disclosed; reduces bias at top of funnel + screening.

### Example 2: Title-blind sourcing via Findem attributes
**Goal:** Find ex-Stripe engineers who are now solo founders (high signal for staff IC roles).
**Steps:**
1. Findem attribute search (Recipe 5): `has_worked_at=[Stripe], former_founder=true, current_seniority=[Senior, Staff]`.
2. Filter for those who LEFT a founder role recently (open-to-employment signal).
3. Cross-validate via LinkedIn for current employer + tenure.
4. Outreach via warm intro path (often via mutual ex-Stripe network).

**Result:** 30-50 "stealth-mode founders open to staff IC" — candidates LinkedIn Boolean misses.

### Example 3: AmazingHiring 50-network ML researcher mining
**Goal:** Find PyTorch contributors + Kaggle Grandmasters + ICML reviewers (research-track ML).
**Steps:**
1. AmazingHiring search (Recipe 7): `skills=[PyTorch, ICML]`, networks include `kaggle` + `papers_with_code` + `huggingface`.
2. Per candidate, pull full profile (Recipe 8) — Kaggle rank, paper count, GitHub stars.
3. Score: composite of Kaggle medal count + first-author paper count + GitHub stars.
4. Top 50 → high-priority outreach for research-track ML eng.

**Result:** Research-validated ML engineers identified across 6 networks in one search; impossible via LinkedIn alone.

## Edge cases / gotchas

- **SeekOut diversity filters are probabilistic.** Name + photo + school heuristics. Confidence band is per-candidate; never report aggregate diversity from these signals as ground truth (Antipattern 3 in role.md).
- **SeekOut Assist auto-generated Boolean defaults to LinkedIn syntax.** Validate before pasting elsewhere.
- **SeekOut requires explicit `diversity_overlay: true` in Bias Reducer mode** — they're separate flags; Bias Reducer alone hides identity but doesn't filter pool.
- **Findem attribute filters depend on data quality of the source profile.** "Open source contributor" requires GitHub linkage in their graph; without it, candidate is missed.
- **Findem doesn't expose raw Boolean.** Attribute combinator only. Pair with LinkedIn Boolean for breadth + Findem attributes for precision.
- **AmazingHiring's diversity filter is opt-in per account.** Email AmazingHiring CS to enable. Default account doesn't include it.
- **AmazingHiring's score is aggregator-internal.** A 90/100 in AmazingHiring may not align with your team's seniority bar. Calibrate against 5-10 known hires first.
- **All three aggregators have ToS limits on bulk export.** SeekOut + Findem cap profile views per user-day. AmazingHiring caps profile-pulls per month. Plan against tier.
- **Cross-aggregator dedupe is non-trivial.** Same person may have different LinkedIn / email / GitHub keys across platforms. Dedupe by (linkedin_url || email_hash || github_handle) — Recipe 9.
- **Bias Reducer is not a substitute for diversity sourcing.** It mitigates screening bias, not pipeline composition. Pair with project-community channels (`diversity-channel-sourcing-dev-color-code2040`).
- **Treat self-disclosed community_affiliation (Findem) as warm-intro signal**, not a hire decision input. Some candidates self-disclose; many don't. Absence is not evidence of non-affiliation.
- **Free fallback when no paid seat:** Github + Stack Overflow + LinkedIn Boolean + project-channel warm intros (`diversity-channel-sourcing-dev-color-code2040`). Lose 50% of pool but full executable.
- **Diversity reporting:** never claim attribution from probabilistic signals. Only attribute when candidate self-IDs in screener OR sourced via channel (e.g., Code2040 partner intro).
- **Defer to `cold-inmail-warm-intro`** for outreach prose — this skill produces candidate evidence.
- **Defer to `operations-agent`** for legal compliance review on diversity reporting (EEO-1 reporting, state-level requirements).

## Sources

- Juicebox — SeekOut Reviews 2026: https://juicebox.ai/blog/seekout-reviews
- Skima — SeekOut Review 2026: https://skima.ai/blog/product-deep-dives/seekout-review
- MindHunt AI — Diversity Sourcing Strategies 2026: https://mindhuntai.com/blog/diversity-sourcing-strategies
- Findem — platform: https://www.findem.ai/
- AmazingHiring — 50+ developer networks: https://amazinghiring.com
- AmazingHiring — Search for Designers on Dribbble + Behance: https://amazinghiring.com/blog/searching-for-designers-on-dribbble-and-behance
- Project Include — Diversity-of-Thought Best Practices: https://projectinclude.org
- SelectSoftware Reviews — Best Talent Sourcing Tools 2026: https://www.selectsoftwarereviews.com/buyer-guide/best-candidate-sourcing-tools
