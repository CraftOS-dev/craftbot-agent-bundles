<!--
Source: https://help.maze.co/hc/en-us/articles/maze-api
Maze API, GA 2025-2026
-->
# Maze User Testing + User Research — SKILL

Maze is the SOTA platform for unmoderated user research, Kano surveys, SUS / NPS / CSAT, and Van Westendorp Price Sensitivity Meter. This pack covers campaign creation, response retrieval, and survey templates the PM agent reaches for most.

## When to use

- Running an unmoderated usability test on a Figma prototype.
- Launching a Kano survey to classify features (basic / performance / excitement).
- Running a Van Westendorp PSM for pricing experiments.
- Collecting NPS / CSAT / SUS scores in-app.
- Running a 5-second test, first-click test, or tree test.
- Recruiting from Maze's panel OR using a custom panel (your user list).

Trigger phrases: "run a usability test", "Kano survey", "test our prototype", "Van Westendorp pricing", "NPS survey", "first-click test".

## Setup

```bash
# Maze REST API — no native MCP yet (June 2026); use cli-anything + curl
curl -fsSL "https://api.maze.co/v1/teams/me" \
  -H "Authorization: Bearer $MAZE_API_KEY"
```

Auth:
- `MAZE_API_KEY` — workspace key from https://app.maze.co/settings/integrations. Paid plan required ($99/mo Starter, $249/mo Team).
- For free recruitment, use your own panel; Maze's recruitment panel adds per-respondent cost.

API surface (Maze v1):
- `POST /campaigns` (create test/survey)
- `GET /campaigns/{id}` / `GET /campaigns/{id}/responses`
- `POST /surveys` (Kano / VW PSM / NPS / SUS)
- `POST /campaigns/{id}/launch` / `POST /campaigns/{id}/close`
- `GET /campaigns/{id}/results` (aggregated metrics)
- `POST /panels` (custom recruitment panel)

## Common recipes

### Recipe 1: 5-second test on a landing page mock

```bash
curl -X POST "https://api.maze.co/v1/campaigns" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Landing 5sec test — Q3 2026",
    "type": "5_second_test",
    "blocks": [
      {"type":"image","src":"https://cdn.example.com/landing-v2.png","duration":5},
      {"type":"open_text","question":"What do you remember?"},
      {"type":"open_text","question":"What product is this?"},
      {"type":"likert","question":"How clear was the value proposition?","scale":5}
    ],
    "recruitment": {"source":"custom_panel","panel_id":"<panel-id>"},
    "sampleTarget": 50
  }'
```

### Recipe 2: Kano survey (2-question pattern per feature)

```bash
# Build a Kano survey for 5 candidate features
FEATURES=("notif-center" "dark-mode" "ai-summary" "bulk-export" "saved-views")
QUESTIONS=()

for F in "${FEATURES[@]}"; do
  QUESTIONS+=("{\"type\":\"multiple_choice\",\"question\":\"How would you feel if you HAD '$F'?\",\"options\":[\"I like it\",\"I expect it\",\"I am neutral\",\"I can tolerate it\",\"I dislike it\"]}")
  QUESTIONS+=("{\"type\":\"multiple_choice\",\"question\":\"How would you feel if you DID NOT have '$F'?\",\"options\":[\"I like it\",\"I expect it\",\"I am neutral\",\"I can tolerate it\",\"I dislike it\"]}")
done

JOINED=$(IFS=,; echo "${QUESTIONS[*]}")
curl -X POST "https://api.maze.co/v1/surveys" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
  -d "{
    \"name\":\"Kano — Q3 feature candidates\",
    \"blocks\":[$JOINED],
    \"sampleTarget\":200
  }"
```

### Recipe 3: Van Westendorp PSM (4 questions)

```bash
curl -X POST "https://api.maze.co/v1/surveys" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
  -d '{
    "name": "Van Westendorp — Pro tier pricing",
    "blocks": [
      {"type":"number","question":"At what price would you consider this product to be so EXPENSIVE that you would not consider buying it?"},
      {"type":"number","question":"At what price would you consider this product to be EXPENSIVE, but still consider buying it?"},
      {"type":"number","question":"At what price would you consider this product to be a BARGAIN — a great buy?"},
      {"type":"number","question":"At what price would you consider this product to be SO CHEAP that you would question its quality?"}
    ],
    "recruitment": {"source":"custom_panel","panel_id":"<panel-id>"},
    "sampleTarget": 150
  }'
```

### Recipe 4: Prototype usability test (with Figma)

```bash
curl -X POST "https://api.maze.co/v1/campaigns" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
  -d '{
    "name": "Onboarding prototype test",
    "type": "prototype_test",
    "blocks": [
      {"type":"figma_prototype","figmaUrl":"https://www.figma.com/proto/abc123XYZ/Onboarding?node-id=42-100&starting-point-node-id=42:100","successPath":["42:100","42:200","42:300"]},
      {"type":"likert","question":"How easy was that flow?","scale":7},
      {"type":"open_text","question":"What confused you, if anything?"}
    ],
    "sampleTarget": 30
  }'
```

### Recipe 5: NPS survey embedded via in-app trigger

```bash
# Survey URL → embed in product (in-app modal / banner)
curl -X POST "https://api.maze.co/v1/surveys" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
  -d '{
    "name":"Quarterly NPS — solo founders",
    "blocks": [
      {"type":"nps","question":"How likely are you to recommend us to a fellow founder?"},
      {"type":"open_text","question":"What is the main reason for your score?"}
    ],
    "distribution":{"link":true,"embed":true}
  }' \
| jq -r '.survey.embed_url'
```

### Recipe 6: Pull aggregated results

```bash
curl -fsSL "https://api.maze.co/v1/campaigns/$CAMPAIGN_ID/results" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
| jq '{respondents: .total_responses, completion_rate: .completion_rate, blocks: [.blocks[] | {question, summary: .summary}]}'
```

### Recipe 7: Classify Kano responses (Python)

```python
# Kano table — see Berger et al. (1993)
KANO_TABLE = {
    # (functional, dysfunctional) → category
    ("like","dislike"):"Performance",
    ("like","tolerate"):"Excitement",
    ("like","neutral"):"Excitement",
    ("like","expect"):"Excitement",
    ("like","like"):"Questionable",
    ("expect","dislike"):"Must-have",
    ("expect","tolerate"):"Indifferent",
    ("expect","neutral"):"Indifferent",
    ("expect","expect"):"Indifferent",
    ("expect","like"):"Reverse",
    ("neutral","dislike"):"Must-have",
    ("neutral","tolerate"):"Indifferent",
    ("neutral","neutral"):"Indifferent",
    ("neutral","expect"):"Indifferent",
    ("neutral","like"):"Reverse",
    ("tolerate","dislike"):"Must-have",
    ("tolerate","tolerate"):"Indifferent",
    ("tolerate","neutral"):"Indifferent",
    ("tolerate","expect"):"Indifferent",
    ("tolerate","like"):"Reverse",
    ("dislike","dislike"):"Questionable",
    ("dislike","tolerate"):"Reverse",
    ("dislike","neutral"):"Reverse",
    ("dislike","expect"):"Reverse",
    ("dislike","like"):"Reverse",
}

def classify(func, dys):
    return KANO_TABLE.get((func, dys), "Indifferent")

# Aggregate per feature
from collections import Counter
def feature_kano(responses, feature):
    cats = [classify(r["func_" + feature], r["dys_" + feature]) for r in responses]
    return Counter(cats).most_common(1)[0][0]
```

### Recipe 8: Van Westendorp price point calculation

```python
# Sort responses; find intersection points
import numpy as np

def vw_price_points(responses):
    too_exp = sorted(r["too_expensive"] for r in responses)
    exp = sorted(r["expensive"] for r in responses)
    cheap = sorted(r["bargain"] for r in responses)
    too_cheap = sorted(r["too_cheap"] for r in responses)
    n = len(responses)

    def cdf(values, price):
        return sum(1 for v in values if v <= price) / n
    def inv_cdf(values, price):
        return 1 - cdf(values, price)

    prices = np.linspace(min(too_cheap), max(too_exp), 200)
    # OPP = intersection of "too cheap" and "too expensive"
    # IPP = intersection of "cheap" and "expensive"
    # PME = intersection of "too cheap" and "expensive"
    # PMC = intersection of "too expensive" and "cheap"
    return {
        "OPP": next(p for p in prices if cdf(too_cheap, p) <= cdf(too_exp, p)),
        "IPP": next(p for p in prices if cdf(cheap, p) <= cdf(exp, p)),
    }
```

### Recipe 9: Custom panel — your own user list

```bash
curl -X POST "https://api.maze.co/v1/panels" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
  -d '{
    "name":"Solo-founder panel (Q3)",
    "members":[{"email":"a@b.com","attributes":{"plan":"pro"}}, {"email":"c@d.com","attributes":{"plan":"pro"}}]
  }'
```

### Recipe 10: Tree test / first-click test for IA validation

```bash
curl -X POST "https://api.maze.co/v1/campaigns" \
  -H "Authorization: Bearer $MAZE_API_KEY" \
  -d '{
    "name":"IA tree test — settings restructure",
    "type":"tree_test",
    "blocks":[
      {"type":"tree","tree":{"root":"Settings","children":[{"name":"Account","children":[{"name":"Profile"},{"name":"Billing"}]},{"name":"Workspace"}]},"tasks":[
        {"prompt":"Where would you go to change your password?","correctPath":["Settings","Account","Profile"]}
      ]}
    ],
    "sampleTarget":50
  }'
```

## Examples

### Example 1: Kano-driven Q3 scope decision
**Goal:** Decide which of 5 features to ship in Q3.

**Steps:**
1. Launch Kano survey (Recipe 2) targeting 200 trial users.
2. Wait for sample target; close campaign.
3. Pull responses (Recipe 6).
4. Classify each feature (Recipe 7).
5. Decision rule: ship all `Must-have`, prioritize `Performance` by adoption potential, defer `Indifferent` and `Reverse`.
6. Write findings into the Q3 roadmap doc via `notion-prds-roadmaps`.

**Result:** Defensible scope decision rooted in user data.

### Example 2: Pricing experiment kickoff
**Goal:** Validate the Pro-tier $49/mo price.

**Steps:**
1. Launch VW PSM (Recipe 3) to 150 trial users.
2. Compute OPP + IPP (Recipe 8).
3. If $49 is within the acceptable range (IPP to PME), keep; else propose alternative.
4. Validate via Statsig packaging A/B (see `pricing-packaging-experiments` skill).

**Result:** Price-point recommendation with PSM curve as evidence.

## Edge cases / gotchas

- **Paid plan only.** No free tier with API access; Starter is $99/mo.
- **Sample-target enforcement.** Maze doesn't block recruiting beyond target; bills per response if using Maze's panel.
- **Custom panel = no recruitment cost** but you must invite respondents yourself.
- **Figma prototype required public access** for prototype tests; if file is private, the test errors silently on the Maze side.
- **Kano needs ≥150 responses** for stable classification per feature; below that, categories swap on re-sample.
- **Van Westendorp needs ≥120 responses** for stable price-point intersections.
- **NPS in-app embed** uses iframe — block sites that don't allow iframes need direct-link survey.
- **No PII webhook by default.** Webhooks return survey-anonymous responses; set `include_email: true` for custom-panel responses (custom-panel only).
- **Rate limits.** 100 req/min; bulk-result downloads should be paginated.
- **Survey-vs-test distinction.** Maze "Surveys" (Pro module) and "Tests" (full suite) have slightly different APIs; check `type` field.

## Sources

- [Maze API docs](https://help.maze.co/hc/en-us/articles/maze-api)
- [Kano model methodology (ProductPlan)](https://www.productplan.com/glossary/kano-model)
- [Van Westendorp PSM (Maze guide)](https://help.maze.co/hc/en-us/articles/van-westendorp-pricing)
- [Berger et al. — Kano table](https://www.tu-ilmenau.de/qualitaetsmanagement/lehre/kano)
- [Maze panel pricing](https://maze.co/pricing)
- [System Usability Scale (SUS)](https://www.usability.gov/how-to-and-tools/methods/system-usability-scale.html)
