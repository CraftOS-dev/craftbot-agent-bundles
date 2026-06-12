<!--
Sources: https://api.stackexchange.com/docs
         https://totalent.eu/stack-overflow-exits-the-talent-acquisition-sphere-announces-plans-to-discontinue-jobs/
         https://www.herohunt.ai/blog/how-to-source-tech-talent-on-stack-overflow/
Stack Overflow Jobs was discontinued March 2022. Stack Exchange API (/users,
/users/{id}/top-tags, /users/{id}/answers) still exposes reputation + tags + answers.
2026 pattern: filter by reputation tier + top-tag depth + recent activity.
-->
# Stack Overflow — Reputation + Top-Tag Sourcing — SKILL

Surface developers via the Stack Exchange API by reputation, top-tag depth, and answer quality. Stack Overflow Jobs shut down March 2022; reputation-based sourcing is the surviving SO channel. Best for niche-tech sourcing where GitHub depth alone is ambiguous (e.g., DB internals, kernel, compiler, GPU, embedded).

## When to use

- User wants devs with **deep niche-tech expertise** signaled by high-reputation answers in {tag}.
- Cross-validation step after GitHub mining — "is this person actually a recognized SME?"
- User wants to source **teaching-quality engineers** (top answers signal communication skill).
- Trigger phrases: "Stack Overflow sourcing", "find {tag} experts", "high-rep devs in X", "teaching-quality engineers", "SME validation".

Do not use for: posting jobs (SO Jobs discontinued 2022); LinkedIn sourcing (`linkedin-recruiter-boolean-search-strings`); broader 50-platform dev overlay (`amazinghiring-findem-seekout-diversity`).

## Setup

```bash
# Stack Exchange API — no auth required for public endpoints (rate-limited to 10k req/day per IP).
# Optional: register an app for higher quota.
# https://stackapps.com/apps/oauth/register
export STACKEX_KEY="xxx"        # 10k/day → 100k/day with key
export STACKEX_SITE="stackoverflow"   # also: serverfault, superuser, math, etc.
```

Rate limits:
- Unauthenticated: 10,000 req/day per IP.
- With app key: 100,000 req/day per IP+key combo.
- Per request: ~30 req/sec sustained acceptable; spikes >40 trigger 429.
- Backoff header: `backoff: <seconds>` — respect it.

## Common recipes

### Recipe 1: Top-reputation users by tag

```bash
# Top 100 Python users by reputation
curl "https://api.stackexchange.com/2.3/users?order=desc&sort=reputation&site=$STACKEX_SITE&tagged=python&pagesize=100&key=$STACKEX_KEY"

# Top users tagged kubernetes
curl "https://api.stackexchange.com/2.3/users?order=desc&sort=reputation&site=stackoverflow&tagged=kubernetes&pagesize=100&key=$STACKEX_KEY"

# Top users tagged rust+wasm intersection (multi-tag)
curl "https://api.stackexchange.com/2.3/users?order=desc&sort=reputation&site=stackoverflow&tagged=rust;wasm&pagesize=100&key=$STACKEX_KEY"
```

The `tagged=` parameter is a semicolon-separated AND. `tagged=rust;wasm` means "users with reputation in BOTH tags".

### Recipe 2: User top-tags (validate domain depth)

```bash
# For a given user_id, what tags do they answer in?
USER_ID=12345
curl "https://api.stackexchange.com/2.3/users/$USER_ID/top-tags?site=$STACKEX_SITE&pagesize=20&key=$STACKEX_KEY"

# Response shape:
# {
#   "items": [
#     {"answer_score": 4500, "answer_count": 280, "question_score": 200, "question_count": 12, "tag_name": "python"},
#     {"answer_score": 1200, "answer_count": 95, ..., "tag_name": "asyncio"},
#   ]
# }
```

Filter: `answer_score / answer_count > 5` indicates quality (not just volume) per tag.

### Recipe 3: User top answers (teaching signal)

```bash
# Top-voted answers by user — strong signal of teaching ability
curl "https://api.stackexchange.com/2.3/users/$USER_ID/answers?order=desc&sort=votes&site=$STACKEX_SITE&pagesize=20&key=$STACKEX_KEY"

# Include the question text for context
curl "https://api.stackexchange.com/2.3/users/$USER_ID/answers?order=desc&sort=votes&site=$STACKEX_SITE&pagesize=20&filter=withbody&key=$STACKEX_KEY"
```

### Recipe 4: User profile + activity recency

```bash
# Full profile — display name, location, website, age of account, reputation history
curl "https://api.stackexchange.com/2.3/users/$USER_ID?site=$STACKEX_SITE&filter=!Lpb_Y_2u4WqfV.GqQ.zJ.kHsz&key=$STACKEX_KEY"

# Recent activity — was their last answer within 30 days?
curl "https://api.stackexchange.com/2.3/users/$USER_ID/timeline?site=$STACKEX_SITE&pagesize=10&key=$STACKEX_KEY"
```

Custom filter (`filter=!...`) — generated at https://api.stackexchange.com/docs/users — selects which fields to return. Default filter strips most useful fields.

### Recipe 5: Reputation tier formula

The agent should apply these cutoffs:

| Tier | Reputation floor | Outreach priority |
|------|------------------|-------------------|
| Hobbyist | < 1,000 | Skip — too early-career |
| Active intermediate | 1,000 - 5,000 | Skip unless tag-perfect |
| Senior | 5,000 - 20,000 | Source for IC roles |
| Staff+ | 20,000 - 100,000 | High-priority outreach |
| Distinguished | > 100,000 | Direct exec / staff outreach |

### Recipe 6: Composite candidate score

```python
import math
from datetime import datetime, timezone

def score_so_candidate(user, top_tags, target_tag, days_since_last_activity):
    """Returns 0-100 score for sourcing fit."""
    score = 0

    # Reputation — log scale
    rep = user.get("reputation", 0)
    score += min(35, math.log10(max(1, rep)) * 7)

    # Target-tag depth — % of total answer_score from target tag
    if top_tags:
        total_answer_score = sum(t["answer_score"] for t in top_tags)
        target_answer_score = sum(t["answer_score"] for t in top_tags if t["tag_name"] == target_tag)
        score += 25 * (target_answer_score / max(1, total_answer_score))

    # Tag rank — is target_tag #1, #2, or #3 in their top tags?
    if top_tags:
        for i, t in enumerate(top_tags[:3]):
            if t["tag_name"] == target_tag:
                score += [20, 12, 6][i]
                break

    # Recency — last activity within 30/90 days
    if days_since_last_activity <= 30:
        score += 20
    elif days_since_last_activity <= 90:
        score += 10

    return round(score, 1)
```

Cutoffs: ≥60 = source-worthy; ≥75 = high-priority; <40 = skip.

### Recipe 7: Geographic filter via location field

```bash
# SO doesn't expose location search natively — must pull users + filter client-side
curl "https://api.stackexchange.com/2.3/users?order=desc&sort=reputation&site=stackoverflow&tagged=python&pagesize=100&filter=!9_bDDxJY5&key=$STACKEX_KEY" \
  | jq '.items[] | select(.location | test("Berlin|Munich|Hamburg"; "i")) | {user_id, display_name, reputation, location, website_url}'
```

`filter=!9_bDDxJY5` — generated custom filter that includes `location` + `website_url`. Without it, location not in response.

### Recipe 8: Tag combination (multi-skill match)

```bash
# Users answering in distributed-systems AND rust — the precise senior systems eng filter
curl "https://api.stackexchange.com/2.3/users?order=desc&sort=reputation&site=stackoverflow&tagged=rust;distributed-systems&pagesize=100&key=$STACKEX_KEY"

# Users tagged in postgresql AND performance — DB tuning experts
curl "https://api.stackexchange.com/2.3/users?order=desc&sort=reputation&site=stackoverflow&tagged=postgresql;performance&pagesize=100&key=$STACKEX_KEY"
```

`;` between tags = AND. Maximum 5 tags per query.

### Recipe 9: Cross-reference with GitHub by website_url

Many high-rep SO users link their GitHub profile in `website_url`:

```bash
# Extract GitHub username from SO website_url field
curl "https://api.stackexchange.com/2.3/users/$USER_ID?site=stackoverflow&filter=!9_bDDxJY5&key=$STACKEX_KEY" \
  | jq -r '.items[0].website_url' \
  | grep -oP 'github\.com/\K[^/]+'

# Then pipe to github-talent-mining-language-stars-commits skill for commit validation
```

### Recipe 10: Engagement signal — recent question askers (intent signal)

```bash
# Users asking questions in target tag in last 30 days — "still learning" but engaged
curl "https://api.stackexchange.com/2.3/questions?order=desc&sort=creation&tagged=rust&fromdate=$(date -d '30 days ago' +%s)&site=stackoverflow&pagesize=100&key=$STACKEX_KEY" \
  | jq '.items[].owner.user_id'
```

Different signal than top-rep: these are devs *actively learning* the target stack. Good for early-career sourcing where commitment to the stack is the signal, not depth.

## Examples

### Example 1: Find 50 Postgres internals SMEs
**Goal:** Senior DB engineers with deep Postgres + performance + indexing.
**Steps:**
1. Top users by reputation tagged `postgresql;performance` (Recipe 8).
2. For each, pull top-tags (Recipe 2) — keep only those where `postgresql` is rank #1 or #2.
3. Filter `reputation > 10,000` (Recipe 5 — senior tier).
4. Score per Recipe 6; threshold ≥70.
5. Cross-reference GitHub via `website_url` (Recipe 9) for commit history.
6. Pipe to `cold-inmail-warm-intro` for outreach.

**Result:** 30-50 high-rep Postgres SMEs ready for senior IC outreach with comp-tier appropriate framing.

### Example 2: Validate a sourced ML eng's actual Python depth
**Goal:** Confirm LinkedIn-claimed Python expertise via SO answer history.
**Steps:**
1. Look up user via `display_name` or `website_url` match (often: `/users?inname={name}`).
2. Pull top-tags (Recipe 2). Is `python` rank #1?
3. Pull top answers (Recipe 3). Read top 3 — are they teaching-quality?
4. Check timeline (Recipe 4) — last activity within 90 days?

**Result:** Confidence-rated yes/no on SO depth. Pair with GitHub validation for full picture.

### Example 3: Source 100 Kubernetes SMEs for a Series B infra team
**Goal:** Devs with deep K8s + cloud-native expertise, ideally with location signal.
**Steps:**
1. Top users tagged `kubernetes` (Recipe 1) with reputation > 5,000.
2. Pull location via Recipe 7; filter to target metros (Berlin, SF, NYC, London).
3. Score per Recipe 6 (target_tag=`kubernetes`); threshold ≥65.
4. Cross-reference LinkedIn via display_name + location to verify current role.
5. Run through `target-company-mapping-crunchbase-linkedin` for current-employer enrichment.

**Result:** 100 K8s SMEs with location + employer + reputation evidence. Outreach via `passive-candidate-outreach-campaigns`.

## Edge cases / gotchas

- **Default API filter strips fields aggressively.** `location`, `website_url`, `about_me` are NOT in the default response. Generate a custom filter at https://api.stackexchange.com/docs/users → include the fields you need → pass `filter=!...` in the URL.
- **`backoff: N` response header MUST be respected.** SO API will hard-block your IP if you ignore. Sleep at least the indicated seconds before next call.
- **Rate limit 10k/day is per IP without a key.** Register an app + pass `key=` for 100k/day. Most production sourcing needs the key.
- **Reputation does not equal seniority.** A 30k-rep user could be a hobbyist who answered thousands of Python basics. Always validate with Recipe 2 top-tags ordering + Recipe 3 answer quality.
- **`tagged=` is case-sensitive lowercase**. `tagged=Python` returns 0 items. Always lowercase.
- **Max 5 tags per query.** `tagged=a;b;c;d;e;f` returns 400 Bad Request.
- **`pagesize` max is 100.** Pagination via `page=`; cap at `page=25` for a given search (search API caps total results).
- **Stack Overflow includes Stack Exchange network sites.** Use `site=stackoverflow` to scope to programming Q&A. `site=serverfault` for sysadmins; `site=superuser` for power-users; `site=math` for math research.
- **The `user_type` field can be `"unregistered"`** for old anonymous answers. Skip these.
- **Display name is not unique.** Three people named "John Smith" exist. Match by `account_id` (cross-network unique) or `user_id` (per-site unique).
- **Location is free text.** "Earth", "Internet", "Remote" common. Use as heuristic, validate via LinkedIn.
- **Privacy: emails are NEVER exposed via API.** Outreach requires LinkedIn or website_url → company → enrichment via Apollo / Hunter / Findymail. Never assume an SO ID can be DM'd.
- **Stack Overflow Jobs is gone (March 2022).** Don't try to post; refer to `hired-wellfound-built-in-otta-niche-boards` for posting channels.
- **Top-rep users get heavy outreach.** They mute / disable contact forms. Lead with a specific answer or question you found valuable — generic "I saw your profile" gets ignored.
- **Activity drift since 2022.** SO traffic + answer volume both dropped ~40% post-ChatGPT (mid-2023). New high-rep users are increasingly rare; the pool of established 20k+-rep users is the source surface.
- **Hand off outreach to `cold-inmail-warm-intro`** — this skill produces candidate evidence, not InMail prose.

## Sources

- Stack Exchange API docs: https://api.stackexchange.com/docs
- Stack Exchange `/users` endpoint: https://api.stackexchange.com/docs/users
- Stack Exchange `/users/{ids}/top-tags`: https://api.stackexchange.com/docs/top-user-tags
- Stack Exchange `/users/{ids}/answers`: https://api.stackexchange.com/docs/answers-on-users
- Totalent — Stack Overflow Exits Talent Acquisition (March 2022): https://totalent.eu/stack-overflow-exits-the-talent-acquisition-sphere-announces-plans-to-discontinue-jobs/
- HeroHunt — How to Source Tech Talent on Stack Overflow: https://www.herohunt.ai/blog/how-to-source-tech-talent-on-stack-overflow/
- Stack Apps app registration: https://stackapps.com/apps/oauth/register
