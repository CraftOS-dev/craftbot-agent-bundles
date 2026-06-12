<!--
Sources: https://amazinghiring.com
         https://www.selectsoftwarereviews.com/buyer-guide/best-candidate-sourcing-tools
         https://skima.ai/blog/product-deep-dives/seekout-review
         https://docs.github.com/en/rest/search/search
AmazingHiring 50+ dev networks. SeekOut full-graph + technical-skill + GitHub
activity scoring. 800M+ profile DBs at SeekOut and Loxo complement LinkedIn for
technical roles. GitHub commit history validates LinkedIn-claimed skills.
-->
# Technical Sourcing — Developer-Focused — SKILL

Source developers via the multi-platform overlay (AmazingHiring 50+ dev networks + SeekOut full-graph + GitHub commit history + Stack Overflow tag depth). Pattern: AI Boolean Builder paste JD → review → execute → cross-validate via GitHub + Stack Overflow → score → outreach. This is the wider net than LinkedIn-Boolean-only.

## When to use

- User wants to **source devs across multiple networks at once** (not LinkedIn only).
- User wants to **validate LinkedIn-claimed skills** against actual code activity.
- User wants to **find niche-tech devs** (CUDA, Triton, Rust, Erlang, Postgres internals) where LinkedIn is too broad.
- User asks "expand my dev sourcing beyond LinkedIn" or "validate this candidate's actual coding".
- Trigger phrases: "developer sourcing", "technical sourcing", "AmazingHiring search", "validate commit history", "multi-platform dev", "niche-tech sourcing".

Do not use for: design-specific sourcing (`product-designer-sourcing-dribbble-behance`); diversity-only sourcing (`amazinghiring-findem-seekout-diversity` for diversity focus); exec sourcing (`cto-vp-eng-exec-sourcing`); LinkedIn-only Boolean (`linkedin-recruiter-boolean-search-strings`).

## Setup

```bash
# AmazingHiring — paid seat $300-700/mo. 50+ networks aggregator.
export AMAZINGHIRING_API_KEY="xxx"

# SeekOut — paid enterprise seat $500-1,200/user/mo. SeekOut Assist + GitHub activity scoring.
export SEEKOUT_API_KEY="xxx"

# GitHub MCP for commit-history validation.
export GITHUB_TOKEN="ghp_xxx"

# Stack Exchange API for tag-depth validation.
export STACKEX_KEY="xxx"

# Optional: hireEZ for AI Boolean Builder.
export HIREEZ_API_KEY="xxx"
```

## Common recipes

### Recipe 1: AmazingHiring multi-network search

```bash
curl -X POST "https://api.amazinghiring.com/v1/candidates/search" \
  -H "Authorization: Bearer $AMAZINGHIRING_API_KEY" \
  -d '{
    "skills": ["Python", "PyTorch", "CUDA"],
    "location": "Berlin OR Munich OR Hamburg",
    "min_score": 70,
    "networks": [
      "github",
      "stackoverflow",
      "kaggle",
      "huggingface",
      "leetcode",
      "papers_with_code",
      "devpost",
      "bitbucket",
      "dev_to",
      "hackerrank"
    ],
    "limit": 100
  }'
```

AmazingHiring's 50+ network aggregation surfaces devs LinkedIn misses (researcher track via papers_with_code, comp-track via leetcode, kaggle track via competitions).

### Recipe 2: SeekOut Assist — JD-to-Boolean for dev roles

```bash
curl -X POST "https://api.seekout.com/v1/assist/generate" \
  -H "Authorization: Bearer $SEEKOUT_API_KEY" \
  -d '{
    "job_description": "<full JD>",
    "include_github_filters": true,
    "include_stackoverflow_filters": true
  }'

# Response includes:
# - Boolean for LinkedIn/Recruiter
# - GitHub filters: languages, min_stars, active_in_last_n_days
# - Stack Overflow filters: tags, min_reputation
# - Estimated pool size + diversity overlay (if enabled)
```

### Recipe 3: SeekOut technical-skill + GitHub activity overlay

```bash
curl -X POST "https://api.seekout.com/v1/search/people" \
  -H "Authorization: Bearer $SEEKOUT_API_KEY" \
  -d '{
    "boolean": "(senior OR staff) AND (machine learning OR ML engineer)",
    "technical_skills": ["Python", "PyTorch", "CUDA"],
    "github_activity": {
      "languages": ["python", "cuda", "rust"],
      "min_stars_on_owned_repos": 50,
      "active_last_180_days": true,
      "min_followers": 20
    },
    "location": ["United States", "Germany"],
    "limit": 100
  }'
```

SeekOut's GitHub activity overlay is the differentiator vs LinkedIn-only. Validates commit recency + language depth in-platform.

### Recipe 4: GitHub commit-history validation (post-sourcing)

```bash
# For each LinkedIn-sourced candidate, validate via GitHub
USER="janedoe"

# Owned repos in target language
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/users/$USER/repos?type=owner&sort=updated&per_page=100" \
  | jq '[.[] | select(.language == "Python")] | length'

# Recent commits (last 180 days)
curl -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.cloak-preview+json" \
  "https://api.github.com/search/commits?q=author:$USER+committer-date:>$(date -d '180 days ago' +%Y-%m-%d)+language:python&per_page=100"

# Contributor stats on big public repos
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/pytorch/pytorch/contributors?per_page=100" \
  | jq '.[] | select(.login == "'$USER'")'
```

See `github-talent-mining-language-stars-commits` for full GitHub recipe set.

### Recipe 5: Stack Overflow tag-depth validation

```bash
# Validate dev's actual SO tag depth
USER_ID=12345
curl "https://api.stackexchange.com/2.3/users/$USER_ID/top-tags?site=stackoverflow&pagesize=20&key=$STACKEX_KEY" \
  | jq '.items[] | {tag_name, answer_score, answer_count}'

# Filter: is target tag (e.g., "kubernetes") rank #1, #2, or #3 in their top tags?
# Cross-reference vs LinkedIn-claimed primary skill
```

See `stack-overflow-talent-reputation-tag` for full SO recipe set.

### Recipe 6: Composite dev candidate score (cross-platform)

```python
def score_dev_candidate(c):
    """0-100 score from cross-platform signals."""
    score = 0

    # LinkedIn — base signal (seniority + tenure)
    if c.get("linkedin", {}).get("seniority") in ["staff", "principal", "senior"]:
        score += 15

    # GitHub — language depth + recency + community signal
    gh = c.get("github", {})
    if gh:
        # Language depth (% of recent repos in target language)
        depth = gh.get("target_language_pct", 0)
        score += depth * 0.25

        # Recency
        if gh.get("active_last_90d"):
            score += 15
        elif gh.get("active_last_180d"):
            score += 8

        # Community
        followers = gh.get("followers", 0)
        score += min(15, math.log2(max(1, followers)) * 3)

    # Stack Overflow — niche depth signal
    so = c.get("stackoverflow", {})
    if so:
        # Reputation tier
        rep = so.get("reputation", 0)
        score += min(15, math.log10(max(1, rep)) * 3)

        # Target tag rank (#1 = best, #5 = ok, none = penalty)
        target_tag = c.get("target_skill")
        for i, tag in enumerate(so.get("top_tags", [])[:5]):
            if tag["tag_name"] == target_tag:
                score += [12, 8, 5, 3, 1][i]
                break

    # Conference speaker / paper signal — high-signal but rare
    if c.get("conference_speakers"):
        score += 10
    if c.get("papers_published"):
        score += 8

    return min(100, score)
```

Cutoffs: ≥75 = high-priority; 60-74 = source; <60 = skip.

### Recipe 7: Niche-tech-specific sourcing matrix

| Niche tech | Primary source | Cross-validate | Signal |
|------------|----------------|----------------|--------|
| Rust systems | GitHub (rust-lang org contributors) | LinkedIn ("Rust" in title) | Crates.io publish + GitHub commits |
| CUDA / GPU | GitHub (PyTorch/Triton/cuDNN contributors) + papers_with_code | LinkedIn (NVIDIA / AMD alumni) | Recent commits to GPU repos + arXiv |
| Postgres internals | Stack Overflow (`postgresql;performance`) | GitHub (postgres + pgvector contributors) | High-rep SO + commits |
| Compiler | GitHub (LLVM / Rust / V8 contributors) | Conference speakers (CppCon, LLVM Dev Mtg) | Talks + commits |
| Distributed systems | GitHub (etcd / Kafka / Cassandra contributors) | Stack Overflow (`distributed-systems`) | Commits + answers |
| ML research | papers_with_code + arXiv author search | GitHub (model release repos) | Papers + reproducible code |
| Embedded / firmware | GitHub (embedded OSes + RTOS) + Hackaday | LinkedIn (semiconductor alumni) | Project repos + hardware bios |
| Kernel | LKML mailing list + GitHub (Linux mirror) | Conference speakers (LPC, KernelCon) | Patches + LKML traffic |
| Cryptography / security | DEF CON / Black Hat speakers + GitHub | Stack Overflow (`cryptography;security`) | Disclosures + commits + talks |

### Recipe 8: Conference speaker mining (rarely automated)

```python
# Pseudo — most conferences publish speaker lists as PDF / HTML; use firecrawl-mcp
conferences_2026 = {
    "PyCon US 2026": "https://us.pycon.org/2026/speakers/",
    "KubeCon NA 2026": "https://events.linuxfoundation.org/kubecon-cloudnativecon-north-america/speakers/",
    "ICML 2026": "https://icml.cc/Conferences/2026/Schedule",
    "Strange Loop 2026": "https://www.thestrangeloop.com/2026/sessions.html",
    "CppCon 2026": "https://cppcon.org/speakers2026/",
    "AI Engineer Summit 2026": "https://www.ai.engineer/summit/2026/schedule"
}

for conf, url in conferences_2026.items():
    speakers = firecrawl.scrape(url, {"extract": {"schema": {"name": "string", "company": "string", "talk_title": "string"}}})
    # Cross-reference each speaker via LinkedIn + GitHub
    for s in speakers:
        candidate = {
            "name": s["name"],
            "current_company": s["company"],
            "conference_signal": f"{conf}: {s['talk_title']}",
            "tags": [f"conference-{conf.lower().replace(' ', '-')}"]
        }
        notion.add(candidate)
```

Conference speaker mining is high-effort + high-signal. Schedule quarterly review of major conferences in target tech.

### Recipe 9: Kaggle Grandmaster / HackerRank Star sourcing

```bash
# Kaggle (no public REST API; scrape leaderboard via firecrawl)
firecrawl.scrape("https://www.kaggle.com/rankings/competitions-grandmasters", {
  "extract": {"schema": {"rank": "number", "name": "string", "country": "string", "linkedin_url": "string"}}
})

# HackerRank (no public sourcing API; firecrawl problem-solver leaderboard)
firecrawl.scrape("https://www.hackerrank.com/leaderboard?domain=algorithms", {...})

# AmazingHiring overlays both natively (Recipe 1) — easier path if seat available
```

### Recipe 10: Validate cross-platform identity match

```python
def cross_validate_identity(linkedin_user, github_user, so_user):
    """Confidence that LinkedIn user X == GitHub user Y == SO user Z."""
    confidence = 0
    signals = []

    # Display name match
    if linkedin_user["name"].lower() == github_user.get("name", "").lower():
        confidence += 30; signals.append("name_match")

    # Email match (if both expose)
    if linkedin_user.get("email") and linkedin_user["email"] == github_user.get("email"):
        confidence += 40; signals.append("email_match")

    # Location match
    if linkedin_user["location"] == github_user.get("location"):
        confidence += 15; signals.append("location_match")

    # Company match
    if any(c.lower() in github_user.get("company", "").lower() for c in [linkedin_user["current_company"]]):
        confidence += 20; signals.append("company_match")

    # Website / LinkedIn URL on SO profile
    if so_user.get("website_url") and linkedin_user["url"] in so_user["website_url"]:
        confidence += 25; signals.append("so_links_linkedin")

    return {"confidence": min(100, confidence), "signals": signals}
```

Confidence ≥70 = treat as same person; 40-69 = ask for explicit confirmation; <40 = treat separately.

## Examples

### Example 1: Source 50 staff ML engineers via multi-platform overlay
**Goal:** Senior ML engineers with PyTorch + CUDA depth.
**Steps:**
1. SeekOut Assist (Recipe 2): paste JD → Boolean + GitHub filter overlay.
2. AmazingHiring search (Recipe 1): `skills=[PyTorch, CUDA]`, networks include `papers_with_code` + `kaggle`.
3. SeekOut full search (Recipe 3) with GitHub activity overlay.
4. Dedupe across 3 sources (linkedin_url || email_hash || github_handle).
5. Score per Recipe 6.
6. Validate cross-platform identity (Recipe 10) for top 50.
7. Pipe to `passive-candidate-outreach-campaigns` for sequence design.

**Result:** 50 staff ML engineers with cross-platform validation; richer signal than LinkedIn-only.

### Example 2: Validate "PyTorch expert" claim on LinkedIn
**Goal:** Candidate's LinkedIn says "PyTorch internals" — validate.
**Steps:**
1. GitHub username lookup (often in LinkedIn profile or via name + location match).
2. `GET /repos/pytorch/pytorch/contributors` → does candidate appear?
3. If yes: check rank + commit count.
4. If no: search recent PyTorch-related commits by author (Recipe 4).
5. Stack Overflow: tagged `pytorch`, reputation tier (Recipe 5).
6. Composite score (Recipe 6): if >70, claim validated.

**Result:** Confidence-rated yes/no on LinkedIn claim; reduces false-positive on outreach to non-actual PyTorch experts.

### Example 3: Niche-tech sourcing — Triton kernel developers
**Goal:** Source 20 Triton (OpenAI Triton, not Apache) developers for ML infra role.
**Steps:**
1. AmazingHiring (Recipe 1): `skills=[Triton, CUDA]`, networks=[github, stackoverflow, papers_with_code].
2. GitHub direct: `GET /repos/openai/triton/contributors` → ~50 contributors.
3. Per contributor: pull owned repos (Recipe 4) for Triton + CUDA + Python language depth.
4. Stack Overflow `triton-language` tag if exists (rare; very niche).
5. Cross-reference LinkedIn for current employer + role.
6. Composite score (Recipe 6) → top 20.
7. Outreach via `cold-inmail-warm-intro` referencing specific Triton PR / commit.

**Result:** 20 Triton developers identified; this niche is nearly invisible to LinkedIn-only Boolean.

## Edge cases / gotchas

- **AmazingHiring's `min_score` is internal.** Calibrate against your team's actual hire bar — 70 may be light or heavy depending on role.
- **SeekOut's GitHub activity scoring caches up to 30 days behind real GitHub.** Recent-commits filter may miss devs who pushed today.
- **Cross-platform identity match has 10-20% false-positive rate** for common names. Always validate via 2+ signals (Recipe 10).
- **GitHub `email` field is null for most users.** Outreach via GitHub-detected email requires extracting from commit history (`git log --format='%ae'` after clone) — only when ToS-aligned.
- **Stack Overflow tag-depth validation hits its limit at niche tech.** If target tag has <500 lifetime answers, even high-rep candidates won't have meaningful tag activity.
- **Conference speaker lists from past 2 years are golden.** Older than 2y signals fade — speaker may have moved 2+ times since.
- **Kaggle Grandmasters are extremely competitive.** Only 200-300 worldwide. Outreach must reference specific competition placement; generic "Kaggle Grandmaster" claim invites skepticism.
- **HackerRank star rank is much less predictive of staff-IC seniority** than GitHub commit history. HackerRank measures puzzle skill; not the same as production engineering.
- **Open source contributions are NOT a proxy for "good engineer".** Many great engineers contribute privately (employer-owned). Don't penalize absent OSS unless OSS is core to the role.
- **AmazingHiring's `diversity_filter` is opt-in per account.** Talk to CS to enable.
- **SeekOut + AmazingHiring sometimes return the same candidate at different scores.** Trust the platform with deeper validation (GitHub commits > LinkedIn title).
- **For pure ML researcher track, prioritize papers_with_code + arXiv** over LinkedIn + GitHub. Researcher career rewards papers, not commits.
- **For sales-facing engineering (Forward Deployed, Sales Eng), GitHub + SO depth is LESS predictive than LinkedIn + customer-case-study volume.** Different ICP.
- **Hand off to `cold-inmail-warm-intro`** for outreach prose — this skill produces candidate evidence.
- **Hand off to `gem-hireez-beamery-talent-crm`** for sequence enrollment + ATS push.
- **Defer to `amazinghiring-findem-seekout-diversity`** when diversity is the primary lens (this skill is tech-depth lens).

## Sources

- AmazingHiring — 50+ developer networks: https://amazinghiring.com
- SelectSoftware Reviews — Best Talent Sourcing Tools 2026: https://www.selectsoftwarereviews.com/buyer-guide/best-candidate-sourcing-tools
- Skima — SeekOut Review 2026: https://skima.ai/blog/product-deep-dives/seekout-review
- GitHub Search API: https://docs.github.com/en/rest/search/search
- Stack Exchange API: https://api.stackexchange.com/docs
- papers_with_code: https://paperswithcode.com/
- Kaggle: https://www.kaggle.com/
- hireEZ — AI Boolean Builder: https://explore.hireez.com/
