<!--
Sources: https://docs.github.com/en/rest/search/search
         https://docs.github.com/en/graphql
         https://explore.hireez.com/blog/how-to-source-candidates-on-github/
         https://builtin.com/recruiting/github-advanced-search
         https://www.kula.ai/blog/github-beginners-guide-source-candidates
GitHub 2026: 180M+ active devs. REST + GraphQL search APIs. hireEZ aggregates 45+
platforms including GitHub. AmazingHiring + SeekOut overlay GitHub + Stack Overflow
+ Kaggle into single dev profile.
-->
# GitHub Talent Mining — Language + Stars + Commits — SKILL

Mine GitHub via REST (`/search/users`, `/search/repositories`, `/search/commits`) and GraphQL (`repository.collaborators` + `contributionsCollection`) to surface devs by language depth, repo signal, and recent commit activity. The 2026 pattern: top-starred repo in target language → contributor list → score each by commit recency + owned-repo language depth + follower count.

## When to use

- User wants to **find {language} developers** by repo activity, not LinkedIn title.
- User wants to **identify contributors to {repo / org / topic}** for outreach.
- Validation step after LinkedIn Boolean: "is this person actually shipping {language}?"
- User wants to **score candidates by commit recency** rather than self-reported skills.
- Trigger phrases: "GitHub sourcing", "find Rust devs", "who contributes to X repo", "active OSS devs in Berlin", "validate commit history".

Do not use for: Stack Overflow reputation (`stack-overflow-talent-reputation-tag`); AmazingHiring 50-platform overlay (`amazinghiring-findem-seekout-diversity`); Kaggle / HackerRank specifically.

## Setup

```bash
# Personal access token (classic) — public_repo + read:user scopes sufficient for search.
# https://github.com/settings/tokens
export GITHUB_TOKEN="ghp_xxx"

# Or via GitHub MCP server already registered in agent.yaml mcp_servers.
# MCP exposes: search_users, search_repositories, search_code, search_commits, get_user, get_repo, list_contributors.
```

Rate limits:
- Authenticated: 30 req/min for search endpoints; 5,000 req/hour for core REST.
- GraphQL: 5,000 points/hour (each query 1-200 points based on connection size).
- Unauthenticated: 10 req/min for search — useless for production sourcing.

## Common recipes

### Recipe 1: User search by location + language + signal

```bash
# Devs in Berlin writing Python with >50 followers (proxy for community signal)
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/users?q=language:python+location:berlin+followers:%3E50&sort=followers&per_page=100"

# Devs anywhere writing Rust with >10 public repos (proxy for shipping cadence)
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/users?q=language:rust+repos:%3E10&sort=followers&per_page=100"

# Specific company alumni (people who listed company in their profile)
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/users?q=stripe+in:bio+language:go&per_page=100"
```

Operators for `/search/users`:
- `location:"San Francisco"` / `location:Berlin OR location:Munich`
- `language:python` / `language:typescript` (matches users' primary language)
- `followers:>50` / `followers:10..500`
- `repos:>10` / `repos:5..50`
- `fullname:"Jane Doe"` / `in:email jane@`
- `sort=followers-desc` / `sort=joined-desc` / `sort=repositories-desc`

### Recipe 2: Repo search → contributor extraction (the highest-signal pattern)

```bash
# Step 1 — find top-starred repos in target language
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/repositories?q=language:typescript+stars:%3E500+pushed:%3E2026-04-01&sort=stars&per_page=50"

# Step 2 — per repo, pull contributors
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/repos/{owner}/{repo}/contributors?per_page=100"

# Step 3 — per contributor, pull their owned repos to validate language depth
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/users/{login}/repos?type=owner&sort=updated&per_page=100"
```

### Recipe 3: Topic search (machine-learning, web3, infrastructure)

```bash
# Active ML repos with stars 50-500 (avoiding mega-projects + dead-letter)
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/repositories?q=topic:machine-learning+language:python+stars:50..500+pushed:%3E2026-03-01&sort=updated&per_page=100"

# Org-scoped — pull all of openai's public Python repos
curl -H "Authorization: token $GITHUB_TOKEN" \
  "https://api.github.com/search/repositories?q=org:openai+language:python&per_page=100"
```

### Recipe 4: Commit search (recent activity + author intent)

```bash
# All recent commits in Rust by a specific author
curl -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.cloak-preview+json" \
  "https://api.github.com/search/commits?q=author:rust-lang+committer-date:%3E2026-01-01+language:rust&per_page=100"

# Commits touching kernel scheduler subsystem
curl -H "Authorization: token $GITHUB_TOKEN" \
  -H "Accept: application/vnd.github.cloak-preview+json" \
  "https://api.github.com/search/commits?q=author:torvalds+path:kernel/sched&per_page=100"
```

### Recipe 5: GraphQL — contributor scoring (preferred for batch)

```graphql
query ContributorScoring($owner: String!, $name: String!) {
  repository(owner: $owner, name: $name) {
    collaborators(first: 100, affiliation: ALL) {
      edges {
        node {
          login
          email
          location
          followers { totalCount }
          contributionsCollection(from: "2025-06-01T00:00:00Z") {
            totalCommitContributions
            totalRepositoryContributions
            totalPullRequestContributions
            commitContributionsByRepository(maxRepositories: 5) {
              repository { nameWithOwner stargazerCount primaryLanguage { name } }
              contributions { totalCount }
            }
          }
        }
      }
    }
  }
}
```

```bash
curl -H "Authorization: bearer $GITHUB_TOKEN" -X POST \
  -d '{"query":"<above>","variables":{"owner":"vercel","name":"next.js"}}' \
  https://api.github.com/graphql
```

### Recipe 6: User profile signal pull

```bash
# Per-candidate: profile + email + repos + last activity
USER="janedoe"
curl -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/users/$USER"
curl -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/users/$USER/repos?sort=pushed&per_page=20"
curl -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/users/$USER/events/public?per_page=30"
```

The `email` field on `/users/{login}` is the user's chosen public email; many devs leave it null. Falling back: scrape commit history → `git log --format='%ae'` on cloned repo → most-common email is the author's real email. Use only for ToS-aligned outreach (the email is public because the dev put it in commits).

### Recipe 7: Candidate scoring formula (the agent should run this for every candidate)

```python
import math
from datetime import datetime, timezone

def score_github_candidate(user, repos, target_language):
    """Returns 0-100 score for sourcing fit."""
    score = 0

    # Follower count — community signal
    score += min(20, math.log2(max(1, user["followers"])) * 4)

    # Owned-repo count — shipping cadence
    score += min(15, math.log2(max(1, user["public_repos"])) * 3)

    # Language depth — % of recent repos in target language
    recent = [r for r in repos if r["language"] == target_language]
    if repos:
        score += 25 * len(recent) / len(repos)

    # Recency — pushed within 90 days
    cutoff = datetime.now(timezone.utc).timestamp() - 90 * 86400
    fresh = [r for r in recent if datetime.fromisoformat(r["pushed_at"].rstrip("Z")).timestamp() > cutoff]
    score += 20 * (1 if fresh else 0)

    # Stars on owned repos — quality signal
    owned_stars = sum(r["stargazers_count"] for r in repos if not r["fork"])
    score += min(20, math.log2(max(1, owned_stars)) * 3)

    return round(score, 1)
```

Cutoffs: ≥60 = sourcing-worthy; ≥75 = high-priority outreach; <40 = skip.

### Recipe 8: Pagination + rate-limit handling

```bash
# Cursor-based pagination on search results (capped at 1,000 total per query)
PAGE=1
while [ $PAGE -le 10 ]; do
  curl -H "Authorization: token $GITHUB_TOKEN" \
    "https://api.github.com/search/users?q=language:go+location:berlin&per_page=100&page=$PAGE"
  # Sleep 2.5s between calls — stays under 30 req/min search limit
  sleep 2.5
  PAGE=$((PAGE+1))
done
```

GitHub caps search results at 1,000 per query. To go deeper, partition by `followers` range or `created` date range and re-query.

### Recipe 9: Cross-reference with LinkedIn (the matching join)

```python
# Pseudo — agent stitches GitHub → LinkedIn via name + location + email
github_user = {"name": "Jane Doe", "location": "Berlin", "company": "@vercel"}

# Author LinkedIn Boolean from GitHub signal
linkedin_boolean = f'fullname:"{github_user["name"]}" AND ({github_user["company"]} OR Vercel)'
# Then use linkedin-recruiter-boolean-search-strings skill
```

## Examples

### Example 1: Find 100 Rust devs in EU for a systems role
**Goal:** Senior Rust devs, EU-located, recent commit activity.
**Steps:**
1. `GET /search/users?q=language:rust+location:berlin+OR+location:london+OR+location:amsterdam+followers:>20&per_page=100` (Recipe 1).
2. For each user, pull their last 20 repos (Recipe 6).
3. Score per Recipe 7; threshold ≥60.
4. Pipe top 100 to `target-company-mapping-crunchbase-linkedin` for current-employer enrichment.

**Result:** 100 EU Rust devs with shipping cadence proof. Ready for outreach via `cold-inmail-warm-intro`.

### Example 2: Source the next ML hire from PyTorch contributors
**Goal:** Active PyTorch contributors who are not currently Meta employees.
**Steps:**
1. `GET /repos/pytorch/pytorch/contributors?per_page=100` (Recipe 2).
2. GraphQL query per contributor (Recipe 5) for `contributionsCollection.totalCommitContributions` in last 12 months.
3. Filter `contributor.company != "@meta"` (use `/users/{login}` company field).
4. Cross-reference LinkedIn via `linkedin-recruiter-boolean-search-strings` for current title verification.

**Result:** 30-50 high-signal PyTorch contributors outside Meta. Outreach via warm intro through mutual contributors.

### Example 3: Validate a sourced engineer's commit history
**Goal:** User says "I LinkedIn-sourced Jane Doe; is she really a Go dev?"
**Steps:**
1. `GET /users/janedoe` — note `public_repos`, `followers`, `created_at`.
2. `GET /users/janedoe/repos?sort=pushed&per_page=20` — check `language` distribution.
3. `GET /search/commits?q=author:janedoe+language:go+committer-date:>2026-01-01` — recent Go commits.
4. Score per Recipe 7.

**Result:** Confidence-rated yes/no on whether her LinkedIn-claimed skills match GitHub activity.

## Edge cases / gotchas

- **Search rate limit is 30 req/min, not 5,000/hour.** Search endpoints are quota-isolated; sleep 2s between search calls or use `X-RateLimit-Remaining` header to backoff.
- **Search results capped at 1,000 per query.** Even if 50,000 users match, you get the top 1,000 sorted. Partition by `created` date or `followers` range to drill further.
- **The `email` field is usually null.** GitHub hides email by default since 2017. Workaround: scrape commit history (`/repos/{r}/commits?author={login}`) → most-frequent author email is real.
- **Forks pollute scoring.** Always filter `fork:false` when scoring owned-repo count.
- **`language:` matches the user's primary repo language**, not their full polyglot fluency. A Python dev with 1 Rust repo still surfaces in `language:rust` search. Validate via Recipe 7 language-depth check.
- **`location:` is user-set text, not validated.** "Earth", "Remote", "🌍" are common. Use as a heuristic; cross-validate via LinkedIn / Apollo for ground truth.
- **GraphQL `collaborators(affiliation: ALL)` only includes collaborators the requesting user can see.** For private repos you don't own, returns empty. Public-repo contributor lists via REST `/contributors` always work.
- **Commit search requires preview header** (`Accept: application/vnd.github.cloak-preview+json`) — without it, 415 Unsupported Media Type.
- **`contributionsCollection.from` window is capped at 365 days.** Multi-year contribution analysis requires multiple queries stitched together.
- **GitHub Actions noise inflates `totalCommitContributions`.** Bot accounts and CI commits show in the contributor list. Filter `node.type != "Bot"` and exclude commits matching `actions[bot]@users.noreply.github.com`.
- **Profile bio "looking for work" / "open to opportunities"** — strong intent signal. Boolean: `q=language:python+%22open+to+work%22+in:bio`.
- **Org membership requires the user to have set it public.** `/users/{login}` `company` field is self-reported; 30-40% of devs leave blank.
- **For Kaggle / HackerRank / Bitbucket / DEV.to overlay**, defer to `amazinghiring-findem-seekout-diversity` (AmazingHiring aggregates 50+ networks).
- **Defer to `cold-inmail-warm-intro`** for actual outreach prose — this skill produces the candidate list, not the InMail.

## Sources

- GitHub Search REST API: https://docs.github.com/en/rest/search/search
- GitHub GraphQL API: https://docs.github.com/en/graphql
- GitHub Rate Limits: https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting
- hireEZ — Complete Guide to Source Candidates on GitHub (45+ platforms): https://explore.hireez.com/blog/how-to-source-candidates-on-github/
- Built In — How to Use GitHub Advanced Search for Recruiters: https://builtin.com/recruiting/github-advanced-search
- Kula — How to Recruit Top Developers on GitHub 2026: https://www.kula.ai/blog/github-beginners-guide-source-candidates
