---
name: kb-taxonomy-design-categories-tags-hierarchy
description: KB taxonomy design — 5-tier IA (domain → category → subcategory → article → tag overlay), Diataxis overlay for customer KBs, card-sort + first-click validation via OptimalSort TreeJack, sidebar mapping. Use when designing or restructuring an information architecture.
---

# KB taxonomy design — categories, tags, hierarchy

## When to use

User asks "design our KB", "restructure information architecture", "fix our nav", "build sitemap", "card sort the docs", or "we have too many orphan articles". Reach here BEFORE writing search/synonyms work (taxonomy is half of the search experience) and BEFORE any migration (the redirect map depends on the new IA).

Defer to `seo-specialist` for public KB topical-clustering for SERP, and to `customer-support-agent` if the goal is ticket-flow routing rather than article browsing.

## Setup

```bash
# Optimal Workshop CLI (paid) for first-click testing
# Free baseline: pen + sticky notes; record results in Notion DB

# Diataxis self-check helper (markdown lint via Vale custom style)
brew install vale
mkdir -p .vale/styles/Diataxis

# OptimalSort / TreeJack — no CLI, work via REST
export OPTIMAL_API_KEY=...  # https://app.optimalworkshop.com/account/api
```

Auth / API key requirements:
- `OPTIMAL_API_KEY` — OptimalSort API (paid; ~$166/mo as of 2026)
- For free first-click testing: Maze (free up to 3 testers) or Useberry trial
- For card-sort data: Google Forms export or Notion database (no key needed)

## Common recipes

### Recipe 1: Pull signal data (tickets, no-result, rage-clicks)

```bash
# Last 90d support ticket categories
curl -s "https://YOUR.zendesk.com/api/v2/incremental/tickets.json?start_time=$(date -d '90 days ago' +%s)" \
  -u "$ZENDESK_USER:$ZENDESK_API_TOKEN" \
  | jq -r '.tickets[] | "\(.priority)\t\(.tags | join(","))\t\(.subject)"' > tickets-90d.tsv

# Algolia no-result searches
curl -s "https://analytics.algolia.com/2/searches/noResults" \
  -H "X-Algolia-Application-Id: $ALGOLIA_APP_ID" \
  -H "X-Algolia-API-Key: $ALGOLIA_ANALYTICS_KEY" \
  -G --data-urlencode 'index=docs' \
  --data-urlencode "startDate=$(date -d '30 days ago' +%F)" \
  > no-result.json
```

### Recipe 2: Run card-sort with 5-10 users (OptimalSort)

```bash
# Create card-sort study via OptimalSort API
curl -X POST 'https://app.optimalworkshop.com/api/v2/studies' \
  -H "Authorization: Bearer $OPTIMAL_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "type": "OnlineCardSort",
    "name": "KB taxonomy 2026-Q2",
    "cards": ["Quickstart","SSO Okta","Webhooks retry","Billing plans","Rate limits","API keys","Error codes"]
  }'
```

After sort: download "Standardization Grid" (≥0.6 agreement = strong grouping; <0.4 = split or rename).

### Recipe 3: Apply Diataxis overlay (customer-facing KBs)

Top-level slices for customer KB:

```
docs/
  get-started/      # Tutorial — learning-oriented
  how-to/           # How-to — task-oriented
  concept/          # Explanation — understanding-oriented
  reference/        # Reference — information-oriented
  troubleshooting/  # Common pain
```

Never mix tiers in one article. A "Get started with SSO" article that includes the full event-type reference table breaks Diataxis.

### Recipe 4: Build 5-tier IA scaffold

```bash
# Generate scaffold from a YAML taxonomy declaration
cat > taxonomy.yml << 'EOF'
domains:
  - slug: get-started
    categories: [quickstart, first-integration, account-setup]
  - slug: how-to
    categories:
      - slug: authentication
        subcategories: [sso-okta, sso-auth0, api-keys]
      - slug: webhooks
        subcategories: [configure, verify-signatures, retry-strategy]
EOF

# Generate folders
python -c "
import yaml, pathlib
t = yaml.safe_load(open('taxonomy.yml'))
for d in t['domains']:
    for c in d['categories']:
        if isinstance(c, dict):
            for s in c.get('subcategories', []):
                pathlib.Path(f\"docs/{d['slug']}/{c['slug']}/{s}.md\").parent.mkdir(parents=True, exist_ok=True)
                pathlib.Path(f\"docs/{d['slug']}/{c['slug']}/{s}.md\").touch()
        else:
            pathlib.Path(f\"docs/{d['slug']}/{c}.md\").parent.mkdir(parents=True, exist_ok=True)
"
```

### Recipe 5: First-click test (TreeJack)

```bash
curl -X POST 'https://app.optimalworkshop.com/api/v2/studies' \
  -H "Authorization: Bearer $OPTIMAL_API_KEY" \
  -H 'Content-Type: application/json' \
  -d @- <<'JSON'
{
  "type": "TreeTest",
  "name": "KB nav 2026-Q2",
  "tree": [
    {"label": "Get started", "children": [{"label":"Quickstart"}]},
    {"label": "How-to", "children": [
      {"label":"Authentication", "children":[{"label":"SSO Okta"},{"label":"API keys"}]}
    ]}
  ],
  "tasks": [
    {"question":"Where do you go to set up SSO with Okta?", "correctNodes":["SSO Okta"]},
    {"question":"Where do you create an API key?", "correctNodes":["API keys"]}
  ]
}
JSON
```

Target: ≥80% directness + ≥80% success on top 20 use cases.

### Recipe 6: Generate sidebar mapping per platform

```javascript
// Docusaurus sidebars.js
module.exports = {
  docs: [
    'intro',
    {type: 'category', label: 'Get started', items: ['get-started/quickstart']},
    {type: 'category', label: 'How-to', items: [
      {type: 'category', label: 'Authentication', items: ['how-to/authentication/sso-okta']}
    ]},
  ],
};
```

```yaml
# MkDocs nav
nav:
  - Get started:
    - Quickstart: get-started/quickstart.md
  - How-to:
    - Authentication:
      - SSO Okta: how-to/authentication/sso-okta.md
```

### Recipe 7: Build tag glossary

```yaml
# docs/_taxonomy.md frontmatter
tags:
  v2: "Articles relevant only to product v2 and later"
  enterprise: "Enterprise-tier features"
  mobile: "Mobile-app specific"
  legacy: "Deprecated but kept for in-flight customers"
```

Only 4-8 tags total. More = noise.

### Recipe 8: Write redirect map for renames

```json
{
  "redirects": [
    {"from":"/docs/sso","to":"/docs/how-to/authentication/sso-okta","code":301},
    {"from":"/docs/single-sign-on","to":"/docs/how-to/authentication/sso-okta","code":301}
  ]
}
```

## Examples

### Example 1: Restructure customer KB (B2B SaaS)

**Goal:** Cut nav from 7 levels to 3; raise first-click success from 54% → 85%.

**Steps:**
1. Pull 90d ticket categories + Algolia no-result + Clarity rage-clicks (Recipe 1).
2. Strip down to 30-50 representative articles for card-sort.
3. Run OptimalSort with 8 users; output Standardization Grid (Recipe 2).
4. Apply Diataxis overlay (Recipe 3); restructure into 5 top-level slices.
5. Build scaffold (Recipe 4); commit to feature branch.
6. TreeJack first-click test (Recipe 5).
7. Iterate weak nodes (<60% directness); re-test.
8. Generate sidebar + redirect map (Recipes 6, 8).
9. Land PR; ship.

**Result:** First-click success ≥80%, time-to-find ≤15s for top tasks.

### Example 2: Add Diataxis to existing flat KB

**Goal:** 120 articles in one folder; split into Tutorial / How-to / Concept / Reference.

**Steps:**
1. Tag each article with intended tier via frontmatter `diataxis: how-to`.
2. Run `vale --output=JSON docs/ | jq '.[] | select(.Rule == "Diataxis.MixedTier")'` to flag mixed-tier articles.
3. Move files: `git mv docs/sso.md docs/how-to/authentication/sso.md`.
4. Build redirect map for every moved file.
5. First-click test.

**Result:** Articles fit cleanly in one tier; tutorial readers don't drown in reference detail.

## Edge cases / gotchas

- **OptimalSort is paid** — ~$166/mo. For free: Maze (3 testers) or pen-and-paper.
- **Card-sort needs 30-50 cards max** — beyond that, fatigue corrupts signal.
- **5 users catches 80% of nav issues** — Nielsen Norman finding. Don't wait for n=50.
- **Tag explosion** — 4-8 tags total. Auto-add to vocabulary file; PR-gate new tags.
- **Diataxis mixing is the #1 author mistake** — instrument Vale to flag "this article has tutorial verbs and reference tables together."
- **Renames need redirects** — every moved URL needs a 301. Skip at your peril; SEO + inbound links die.
- **Don't restructure in place** — branch + feature-flag preview; A/B old vs new for 2 weeks.
- **Per-article ACLs in IA** — antipattern. Use SSO groups at the section level.
- **Card-sort with proxy data only** — if no users available, use ticket categories + no-result queries as proxy; document the limitation.

## Sources

- Diataxis framework: https://diataxis.fr/
- Nielsen Norman card-sorting: https://www.nngroup.com/articles/card-sorting-definitive-guide/
- OptimalSort TreeJack: https://www.optimalworkshop.com/treejack
- Maze (free first-click test): https://maze.co/
- Docusaurus sidebar: https://docusaurus.io/docs/sidebar
- MkDocs nav: https://www.mkdocs.org/user-guide/configuration/#nav
- Mintlify navigation: https://mintlify.com/docs/navigation
