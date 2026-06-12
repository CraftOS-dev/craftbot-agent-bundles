<!--
Sources:
Optimal Workshop API — https://help.optimalworkshop.com/en/articles/2079834-treejack-api
Optimal Workshop OptimalSort API — https://help.optimalworkshop.com/en/articles/2079831-optimalsort-api
NN/g — Tree Testing — https://www.nngroup.com/articles/tree-testing/
NN/g — Card Sorting — https://www.nngroup.com/articles/card-sorting-definition/
UXtweak (alt) — https://www.uxtweak.com/docs/api
-->
# Tree Testing + Card Sorting — Optimal Workshop — SKILL

Information architecture validation: Treejack for tree testing (does the proposed IA support task completion?), OptimalSort for card sorting (what categories make sense to users?). Output: success rate per task + directness % + similarity matrix + dendrogram. UXtweak is the cheaper alt.

## When to use

- Validating a proposed navigation hierarchy before front-end build.
- Discovering natural categories users group concepts into (open card sort).
- Validating proposed categories (closed card sort).
- Hybrid: testing categories + letting users add new ones.
- Comparing tree A vs tree B for redesign decision.

Trigger phrases: "tree test", "card sort", "test the IA", "validate the nav", "Treejack", "OptimalSort", "where would users find X", "what categories make sense".

## Setup

```bash
# Optimal Workshop API
curl -fsSL "https://api.optimalworkshop.com/v1/me" \
  -H "Authorization: Bearer $OPTIMAL_WORKSHOP_API_KEY"

# UXtweak alt
curl -fsSL "https://api.uxtweak.com/v1/me" \
  -H "Authorization: Bearer $UXTWEAK_API_KEY"
```

Auth + cost:
- `OPTIMAL_WORKSHOP_API_KEY` — Account → Integrations → API. Paid (~$166/mo Pro).
- `UXTWEAK_API_KEY` — cheaper alt; ~$80/mo.

API surface:
- Treejack: `POST /treejack/studies`, `GET /treejack/studies/{id}/results`
- OptimalSort: `POST /optimalsort/studies`, `GET /optimalsort/studies/{id}/results`
- Chalkmark: `POST /chalkmark/studies` (see `first-click-5-second-tests` skill)

## Common recipes

### Recipe 1: Treejack — create a tree test

```bash
curl -X POST "https://api.optimalworkshop.com/v1/treejack/studies" \
  -H "Authorization: Bearer $OPTIMAL_WORKSHOP_API_KEY" \
  -d '{
    "name": "Settings IA tree test — Q3 redesign",
    "tree": [
      {"label": "Account", "children": [
        {"label": "Profile"},
        {"label": "Billing", "children": [
          {"label": "Payment method"},
          {"label": "Invoices"},
          {"label": "Plan & usage"}
        ]},
        {"label": "Security"}
      ]},
      {"label": "Workspace", "children": [
        {"label": "Team members"},
        {"label": "Roles & permissions"},
        {"label": "Integrations"}
      ]},
      {"label": "Notifications"},
      {"label": "Help & support"}
    ],
    "tasks": [
      {
        "id": "t1",
        "prompt": "Where would you go to change your credit card?",
        "correct_paths": [["Account", "Billing", "Payment method"]]
      },
      {
        "id": "t2",
        "prompt": "Where would you go to invite a teammate?",
        "correct_paths": [["Workspace", "Team members"]]
      },
      {
        "id": "t3",
        "prompt": "Where would you go to turn off email notifications?",
        "correct_paths": [["Notifications"]]
      }
    ],
    "sample_target": 50
  }'
```

### Recipe 2: Pull Treejack results

```bash
curl -fsSL "https://api.optimalworkshop.com/v1/treejack/studies/$STUDY_ID/results" \
  -H "Authorization: Bearer $OPTIMAL_WORKSHOP_API_KEY" \
| jq '{
    respondents: .total_respondents,
    by_task: [.tasks[] | {
      prompt,
      success_rate: .success_rate,
      directness: .directness,
      median_time_seconds: .median_time,
      common_wrong_paths: .top_wrong_paths
    }]
  }'
```

### Recipe 3: Tree test design rules

```markdown
# Treejack rules

## Tree
- Strip all visuals — text-only labels
- Strip nav bars / breadcrumbs — testing labels not chrome
- Keep depth realistic (≤4 levels for most apps)
- Use the actual proposed labels — not abbreviations

## Tasks
- 5-10 tasks (not 30 — fatigue)
- Outcome-framed in user language: "Where would you go to [achieve outcome]?"
- NOT: "Find the Payment Method page" (gives the answer)
- Cover the breadth of the tree (not just one branch)

## Sample
- ≥50 participants per tree for stable directness
- 100+ for confident comparison between two trees
```

### Recipe 4: OptimalSort — open card sort

```bash
curl -X POST "https://api.optimalworkshop.com/v1/optimalsort/studies" \
  -H "Authorization: Bearer $OPTIMAL_WORKSHOP_API_KEY" \
  -d '{
    "name": "Settings card sort — open mode",
    "mode": "open",
    "cards": [
      {"id": "c1", "label": "Change my password"},
      {"id": "c2", "label": "Update credit card"},
      {"id": "c3", "label": "Invite a teammate"},
      {"id": "c4", "label": "Connect Slack"},
      {"id": "c5", "label": "Email digest settings"},
      {"id": "c6", "label": "Download my data"},
      {"id": "c7", "label": "Two-factor authentication"},
      {"id": "c8", "label": "API keys"},
      {"id": "c9", "label": "Theme: dark / light"},
      {"id": "c10", "label": "Workspace name"}
    ],
    "sample_target": 30
  }'
```

### Recipe 5: OptimalSort — closed card sort

```bash
curl -X POST "https://api.optimalworkshop.com/v1/optimalsort/studies" \
  -H "Authorization: Bearer $OPTIMAL_WORKSHOP_API_KEY" \
  -d '{
    "name": "Settings card sort — closed validation",
    "mode": "closed",
    "categories": [
      {"id": "cat1", "label": "Account"},
      {"id": "cat2", "label": "Workspace"},
      {"id": "cat3", "label": "Notifications"},
      {"id": "cat4", "label": "Integrations"},
      {"id": "cat5", "label": "Privacy & security"}
    ],
    "cards": [
      {"id": "c1", "label": "Change my password"},
      {"id": "c2", "label": "Update credit card"},
      {"id": "c3", "label": "Invite a teammate"}
    ],
    "sample_target": 30
  }'
```

### Recipe 6: Hybrid card sort

```bash
curl -X POST "https://api.optimalworkshop.com/v1/optimalsort/studies" \
  -H "Authorization: Bearer $OPTIMAL_WORKSHOP_API_KEY" \
  -d '{
    "name": "Settings card sort — hybrid",
    "mode": "hybrid",
    "categories": [
      {"id": "cat1", "label": "Account"},
      {"id": "cat2", "label": "Workspace"},
      {"id": "cat3", "label": "Notifications"}
    ],
    "allow_new_categories": true,
    "cards": [...],
    "sample_target": 30
  }'
```

### Recipe 7: Pull card sort results (similarity matrix + dendrogram)

```bash
curl -fsSL "https://api.optimalworkshop.com/v1/optimalsort/studies/$STUDY_ID/results" \
  -H "Authorization: Bearer $OPTIMAL_WORKSHOP_API_KEY" \
| jq '{
    respondents: .total_respondents,
    similarity_matrix: .similarity_matrix,
    dendrogram_url: .dendrogram_image_url,
    standardization_grid: .standardization_grid,
    most_agreed_categories: .top_agreement,
    least_agreed_cards: .high_disagreement_cards
  }'
```

### Recipe 8: When to use which mode

| Mode | Use when | Sample |
|---|---|---|
| **Open** | Discovering natural categories (greenfield IA) | ≥30 |
| **Closed** | Validating proposed categories (refining IA) | ≥30 |
| **Hybrid** | Validating + discovering gaps | ≥30 |

### Recipe 9: Interpret directness vs success

```python
# Treejack metrics
def interpret_task(task_result):
    success = task_result["success_rate"]
    directness = task_result["directness"]

    if success >= 0.80 and directness >= 0.70:
        return "Strong — IA supports this task"
    if success >= 0.60 and directness < 0.50:
        return "Indirect — users find it but wander; check label clarity"
    if success < 0.50:
        return "Weak — IA fails this task; redesign branch"
    if directness < 0.30:
        return "Lost — users explore many wrong paths; labels confusing"
    return "Marginal — investigate further"
```

### Recipe 10: Report template (tree test or card sort)

```markdown
# Tree Test Readout: [Study Name]

**Date:** [YYYY-MM-DD] · **Researcher:** [Name] · **N=[X]**

## TL;DR
- [1-2 sentences on overall IA verdict]
- [Top 2-3 problem tasks]

## Tasks + metrics

| Task | Prompt | Success | Directness | Verdict |
|---|---|---|---|---|
| t1 | Where to change credit card | 78% | 62% | Strong |
| t2 | Where to invite teammate | 52% | 28% | Weak — investigate |
| t3 | Where to turn off email | 91% | 88% | Strong |

## Common wrong paths (per failing task)
### t2: "Invite teammate"
- 31% went Account → ... → couldn't find. Expected /team in top nav.
- 14% looked under "Notifications" — possibly confusing label.

## Recommendations
1. [Task → branch redesign → expected impact]
2. ...

## Appendix
- Study: [Optimal Workshop link]
- Tree spec: [Notion link]
- Raw results: [CSV export]
```

## Examples

### Example 1: Validate settings IA redesign
**Goal:** Decide whether new IA ships.

**Steps:**
1. Build tree JSON (Recipe 1) from proposed nav.
2. Write 8 tasks covering breadth.
3. Push to Treejack, recruit N=50 via in-product intercept or panel.
4. Pull results (Recipe 2).
5. Interpret per task (Recipe 9).
6. Decision: ≥75% success + ≥60% directness on ≥6 of 8 tasks → ship.

**Result:** Quant verdict + branch-level redesign recommendations.

### Example 2: Discover natural settings categories
**Goal:** Before redesigning, see how users actually group settings concepts.

**Steps:**
1. Open card sort (Recipe 4) with 30 settings items.
2. Recruit N=30.
3. Pull similarity matrix + dendrogram (Recipe 7).
4. Build IA from clusters; validate with closed sort (Recipe 5).

**Result:** User-derived categories ground the redesign.

## Edge cases / gotchas

- **Leading task prompts.** "Find the Billing page" tells the user. Use outcome framing.
- **Sample below 50 for tree test.** Directness unstable; recruit more.
- **Tree with hidden chrome.** Treejack auto-strips, but include only labels — not "Click Settings → Account → ...".
- **Card sort fatigue.** >40 cards = drop-off. Cap at 25-35.
- **Closed sort with unfair categories.** Including "Other" as a dump bucket = signals categories are wrong.
- **Open card sort with vague items.** "Stuff" / "Things" labels = noise. Standardize labels post-hoc via similarity matrix.
- **Hybrid mode misuse.** If users mostly create new categories → proposed categories failing → switch to open.
- **One-shot test.** Tree test is one-and-done in users' heads. Different users → different tasks if you want to triangulate.
- **Comparing trees with different sample.** Always recruit same panel + balance.
- **No qualitative follow-up.** Tree test tells *what*, not *why*. Pair with 5 moderated sessions.
- **Re-using same users for A and B.** Order effects bias the second tree. Use separate samples or counterbalance.
- **UXtweak fallback.** When OW budget unavailable, UXtweak handles the same flows at ~50% cost.

## Sources

- [Optimal Workshop Treejack API](https://help.optimalworkshop.com/en/articles/2079834-treejack-api)
- [Optimal Workshop OptimalSort API](https://help.optimalworkshop.com/en/articles/2079831-optimalsort-api)
- [NN/g — Tree Testing](https://www.nngroup.com/articles/tree-testing/)
- [NN/g — Card Sorting: Designing Usable Categories](https://www.nngroup.com/articles/card-sorting-definition/)
- [NN/g — Tree Testing for Information Architecture](https://www.nngroup.com/articles/tree-test-information-architecture/)
- [UXtweak API](https://www.uxtweak.com/docs/api)
- [Donna Spencer — Card Sorting: Designing Usable Categories](https://rosenfeldmedia.com/books/card-sorting/)
