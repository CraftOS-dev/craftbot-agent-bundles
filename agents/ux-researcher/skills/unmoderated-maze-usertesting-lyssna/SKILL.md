<!--
Sources:
Maze API — https://help.maze.co/hc/en-us/articles/maze-api
UserTesting API — https://www.usertesting.com/api
Lyssna API — https://help.lyssna.com/api
NN/g — Unmoderated vs Moderated — https://www.nngroup.com/articles/moderated-vs-unmoderated-usability-studies/
-->
# Unmoderated Usability: Maze + UserTesting + Lyssna — SKILL

Three-platform routing for unmoderated usability. Maze (Figma-native, fastest, AI-prototype-ready). UserTesting (enterprise, largest panel, native video review). Lyssna (formerly UsabilityHub — design-first: 5-second, first-click, preference, copy tests). Pick by use case + budget.

## When to use

- Testing a Figma prototype or live URL with 15-30 users for task success + SUS.
- Validating design choices at scale (preference test, 5-second test).
- Comparing two designs head-to-head.
- Speed beats moderation (no observer needs, no live debrief).
- AI prototype validation (Claude artifacts / v0 / lovable / bolt) — see `ai-prototype-testing-claude-chatgpt`.

Trigger phrases: "unmoderated test on Figma", "set up Maze test", "preference test A vs B", "5-second test", "SUS at scale", "test prototype with 30 users".

## Setup

```bash
# Maze
curl -fsSL "https://api.maze.co/v1/teams/me" \
  -H "Authorization: Bearer $MAZE_API_KEY"

# UserTesting
curl -fsSL "https://api.usertesting.com/v1/me" \
  -H "Authorization: Bearer $USERTESTING_API_KEY"

# Lyssna
curl -fsSL "https://api.lyssna.com/v1/me" \
  -H "Authorization: Bearer $LYSSNA_API_KEY"
```

Auth + cost:
- `MAZE_API_KEY` — $99-249/mo Starter/Team; from Settings → Integrations.
- `USERTESTING_API_KEY` — enterprise contract; per-session billing.
- `LYSSNA_API_KEY` — $75-175/mo; cheapest of the three.

## Platform routing

| Use case | First choice | Why | Cost note |
|---|---|---|---|
| Figma prototype, solo founder, fastest setup | **Maze** | Native Figma integration + click maps + heatmaps | Starter $99/mo |
| Enterprise scale, video annotation | **UserTesting** | Largest panel + native video review | Enterprise contract |
| 5-second / preference / design-first | **Lyssna** | Cheapest + design-focused | $75-175/mo |
| AI-prototype testing | **Maze** | URL-based; works with v0/lovable/Claude artifacts | + trust gates |
| Multi-step prototype with branching | **Maze** | Branching + custom paths | + heatmap |
| Side-by-side preference | **Lyssna** | Preference test as first-class block | Cheap |
| Long-form survey wrapped in test | **UserTesting** | Best survey-+-test combo | Enterprise |
| Tree test / card sort | use **Optimal Workshop** (see IA skill) | Specialized | — |

## Common recipes

### Recipe 1: Maze unmoderated test on Figma prototype

```bash
curl -X POST "https://api.maze.co/v1/campaigns" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
  -d '{
    "name": "Onboarding redesign test — Q3",
    "type": "prototype_test",
    "blocks": [
      {
        "type": "figma_prototype",
        "figmaUrl": "https://www.figma.com/proto/abc123/Onboarding?node-id=42-100",
        "task": "You are a new user. Set up your first project.",
        "successPath": ["42:100", "42:200", "42:300", "42:400"],
        "timeLimitSeconds": 300
      },
      {
        "type": "likert",
        "question": "How easy was that task?",
        "scale": 7
      },
      {
        "type": "open_text",
        "question": "What confused you, if anything?"
      },
      {
        "type": "sus_survey"
      }
    ],
    "sampleTarget": 30,
    "recruitment": {"source": "custom_panel", "panel_id": "<panel-id>"}
  }'
```

### Recipe 2: UserTesting test create

```bash
curl -X POST "https://api.usertesting.com/v1/tests" \
  -H "Authorization: Bearer $USERTESTING_API_KEY" \
  -d '{
    "title": "Checkout flow — moderated remote",
    "device_type": ["desktop"],
    "target_user_count": 20,
    "tasks": [
      {
        "type": "think_aloud",
        "instruction": "Find a product, add it to cart, and complete checkout.",
        "success_criteria": "Reach order confirmation"
      },
      {
        "type": "scenario",
        "instruction": "Imagine the product is out of stock. What would you do next?"
      }
    ],
    "audience_filters": {
      "country": ["US"],
      "age_range": [25, 55],
      "online_purchase_frequency": "weekly_or_more"
    },
    "post_test_questions": [
      {"type": "likert", "text": "Overall ease (1-7)?", "scale": 7},
      {"type": "open_text", "text": "What would you change?"}
    ]
  }'
```

### Recipe 3: Lyssna preference test (A vs B)

```bash
curl -X POST "https://api.lyssna.com/v1/studies" \
  -H "Authorization: Bearer $LYSSNA_API_KEY" \
  -d '{
    "name": "Hero headline A vs B",
    "type": "preference_test",
    "blocks": [
      {
        "type": "preference",
        "options": [
          {"label": "A", "image_url": "https://cdn.yourco.com/hero-a.png"},
          {"label": "B", "image_url": "https://cdn.yourco.com/hero-b.png"}
        ],
        "question": "Which version makes you most likely to sign up?"
      },
      {
        "type": "open_text",
        "question": "Why did you choose that one?"
      }
    ],
    "sample_target": 50
  }'
```

### Recipe 4: Lyssna 5-second test

```bash
curl -X POST "https://api.lyssna.com/v1/studies" \
  -H "Authorization: Bearer $LYSSNA_API_KEY" \
  -d '{
    "name": "Landing page 5-second test — Q3",
    "type": "five_second_test",
    "blocks": [
      {"type": "image", "src": "https://cdn.yourco.com/landing-v2.png", "duration_seconds": 5},
      {"type": "open_text", "question": "What do you remember?"},
      {"type": "open_text", "question": "What is this page for?"},
      {"type": "open_text", "question": "Who is it for?"}
    ],
    "sample_target": 30
  }'
```

### Recipe 5: Standard task structure (paste into any platform)

```markdown
# Unmoderated test brief — paste structure

## Pre-test screener (3-5 Qs)
- Behavior question (e.g., "How often do you do X?")
- Segment question
- Anti-screen (professional respondent guard)

## Welcome (1 paragraph)
- What we're testing
- Estimated time
- Incentive

## Task block (3-5 tasks)
- **Task:** outcome-framed, real-world scenario
- **Success criteria:** what reaching success looks like
- **Time limit:** 3-5 min per task

## Post-task questions (per task)
- SEQ (Single Ease Question): "How easy was that? (1-7)"
- Open text: "What was confusing, if anything?"

## Post-test survey
- SUS (10 items) OR UMUX-Lite (4 items)
- NPS (optional)
- "Anything we should know that we didn't ask?"
```

### Recipe 6: Pull aggregated Maze results

```bash
curl -fsSL "https://api.maze.co/v1/campaigns/$CAMPAIGN_ID/results" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
| jq '{
    respondents: .total_responses,
    completion_rate: .completion_rate,
    sus_score: .sus.score,
    by_task: [.blocks[] | select(.type=="figma_prototype") | {
      task: .task,
      success_rate: .success_rate,
      median_time: .median_time_seconds,
      misclick_rate: .misclick_rate
    }]
  }'
```

### Recipe 7: Compute SUS score from raw responses

```python
# SUS items: odd are positive, even are negative. Convert all to 0-4 then × 2.5.
SUS_POS = [1, 3, 5, 7, 9]
SUS_NEG = [2, 4, 6, 8, 10]

def sus_score(response):
    """response: dict {item_1: 1-5, item_2: 1-5, ...}"""
    total = 0
    for i in SUS_POS:
        total += (response[f"item_{i}"] - 1)
    for i in SUS_NEG:
        total += (5 - response[f"item_{i}"])
    return total * 2.5  # 0-100

# Benchmark: >68 = above average; >80 = excellent
def sus_benchmark(score):
    if score >= 80: return "A — excellent"
    if score >= 68: return "B — above average"
    if score >= 51: return "C — below average"
    return "F — failing"
```

### Recipe 8: UMUX-Lite (4-item alternative)

```python
def umux_lite_score(q1, q2):
    """q1: capabilities meet requirements (1-7), q2: easy to use (1-7)"""
    # Convert to SUS equivalent
    return ((q1 - 1) + (q2 - 1)) * 8.33 + 22.9
```

### Recipe 9: Heatmap + first-click analysis

```bash
curl -fsSL "https://api.maze.co/v1/campaigns/$CAMPAIGN_ID/blocks/$BLOCK_ID/heatmap" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
| jq '{
    first_click_correct_rate: .first_click.correct_rate,
    misclick_zones: .first_click.misclick_clusters,
    heatmap_url: .heatmap_image_url
  }'
```

### Recipe 10: Synthesize verbatims via Dovetail

```bash
# Pull open-text responses → upload to Dovetail for theme tagging
curl -fsSL "https://api.maze.co/v1/campaigns/$CAMPAIGN_ID/responses" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
| jq -r '.responses[] | select(.block_type=="open_text") | "\(.respondent_id)\t\(.answer)"' \
> verbatims.tsv

# Upload to Dovetail as notes
while IFS=$'\t' read -r RID ANSWER; do
  curl -X POST "https://dovetail.com/api/v1/projects/$DOVETAIL_PROJECT/notes" \
    -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
    -d "{\"title\":\"$RID Maze open-text\",\"body\":\"$ANSWER\"}"
done < verbatims.tsv
```

## Examples

### Example 1: Maze test on a Figma onboarding redesign
**Goal:** Validate the new onboarding flow with 30 users + SUS.

**Steps:**
1. Build campaign (Recipe 1) with Figma URL + success path + UMUX-Lite.
2. Use custom panel (your user list) OR Maze panel.
3. Launch; wait 3-5 days to N=30.
4. Pull results (Recipe 6) — success rate, time, SUS.
5. Heatmap + misclick analysis (Recipe 9).
6. Verbatims to Dovetail (Recipe 10) for theme synthesis.

**Result:** Success rate + SUS + heatmap + theme list, ready for design iteration.

### Example 2: Lyssna preference test for hero copy
**Goal:** Pick the hero headline.

**Steps:**
1. Run preference test (Recipe 3) with 50 trial-segment users.
2. Compare select rates.
3. Read open-text rationale for why.
4. Decision: pick winner if ≥60% prefer + rationale aligns.

**Result:** Defensible copy choice with quant + qual evidence.

## Edge cases / gotchas

- **Figma prototype must be public.** Private file = test fails silently. Set to "Anyone with the link" before pushing to Maze.
- **Success path mismatch.** If the success node IDs don't match the Figma frames, completion always reads 0%.
- **Panel pollution.** Maze/UserTesting panels contain pros — anti-screen in pre-test screener.
- **SUS conflation.** Don't combine moderated SUS + unmoderated SUS; report separately.
- **5-second test on dense screens.** Below threshold for stable recall; reserve for hero / above-the-fold.
- **Preference test as proxy for behavior.** Stated preference ≠ behavior. Pair with behavioral data.
- **Open-text fatigue.** Pure open-text after each task = response quality drops. Limit to 1-2.
- **Sample target reached but quality varies.** Filter responses for completion + attention checks before SUS calc.
- **Rate limits.** Maze 100 req/min; pagination needed for large pulls.
- **NPS in unmoderated.** Low context → meaningless score. Don't ask NPS unless they've actually used product.
- **AI prototype URLs.** Maze accepts URL — use v0.dev deploy / lovable deploy / Claude artifact URL (see `ai-prototype-testing-claude-chatgpt`).
- **Attention check item.** Add "Please select 'Strongly Agree' for this question" to filter clickfarmers.

## Sources

- [Maze API docs](https://help.maze.co/hc/en-us/articles/maze-api)
- [UserTesting API](https://www.usertesting.com/api)
- [Lyssna API](https://help.lyssna.com/api)
- [NN/g — Moderated vs Unmoderated Usability Studies](https://www.nngroup.com/articles/moderated-vs-unmoderated-usability-studies/)
- [System Usability Scale (SUS)](https://measuringu.com/sus/)
- [UMUX-Lite (Lewis et al.)](https://uxpajournal.org/wp-content/uploads/sites/8/pdf/JUS_Lewis_May2013.pdf)
- [Single Ease Question (SEQ)](https://measuringu.com/seq10/)
- [NN/g — 5-Second Tests](https://www.nngroup.com/articles/five-second-tests/)
