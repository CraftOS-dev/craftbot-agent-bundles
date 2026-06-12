<!--
Sources:
Optimal Workshop Chalkmark — https://help.optimalworkshop.com/en/articles/chalkmark
NN/g — Five-Second Tests — https://www.nngroup.com/articles/five-second-tests/
NN/g — First-Click Testing — https://www.nngroup.com/articles/first-click-testing/
Lyssna API — https://help.lyssna.com/api
-->
# First-Click + 5-Second Tests — SKILL

Two cheap, fast methods for static-screen evaluation. Chalkmark (Optimal Workshop) for first-click — where does the dominant CTA / nav cue draw the click? Lyssna 5-second test for first-impression + recall — what stuck after brief exposure? Both run in 1 day, ≥30 users, < $100 typical spend.

## When to use

- A new landing page or hero section design.
- Comparing two layouts (which gets the right click?).
- Validating that the primary CTA is visually dominant.
- Testing whether the page communicates its purpose at first glance.
- Early-stage design feedback (faster than full usability test).

Trigger phrases: "first-click test", "5-second test", "test the hero", "where do users click", "what's the first impression", "Chalkmark", "Lyssna 5-second".

## Setup

```bash
# Optimal Workshop Chalkmark
curl -fsSL "https://api.optimalworkshop.com/v1/me" \
  -H "Authorization: Bearer $OPTIMAL_WORKSHOP_API_KEY"

# Lyssna
curl -fsSL "https://api.lyssna.com/v1/me" \
  -H "Authorization: Bearer $LYSSNA_API_KEY"
```

Auth + cost:
- `OPTIMAL_WORKSHOP_API_KEY` — ~$166/mo Pro (Chalkmark included).
- `LYSSNA_API_KEY` — $75-175/mo; cheapest path for 5-second tests.

## Common recipes

### Recipe 1: Chalkmark first-click test

```bash
curl -X POST "https://api.optimalworkshop.com/v1/chalkmark/studies" \
  -H "Authorization: Bearer $OPTIMAL_WORKSHOP_API_KEY" \
  -d '{
    "name": "Landing first-click — Q3 2026",
    "tasks": [
      {
        "id": "t1",
        "image_url": "https://cdn.yourco.com/landing-v2.png",
        "prompt": "Where would you click to start a free trial?",
        "correct_target": {"x_pct": 0.65, "y_pct": 0.42, "radius_pct": 0.08}
      },
      {
        "id": "t2",
        "image_url": "https://cdn.yourco.com/landing-v2.png",
        "prompt": "Where would you click to learn more about pricing?",
        "correct_target": {"x_pct": 0.85, "y_pct": 0.08, "radius_pct": 0.04}
      }
    ],
    "sample_target": 30
  }'
```

### Recipe 2: Lyssna 5-second test

```bash
curl -X POST "https://api.lyssna.com/v1/studies" \
  -H "Authorization: Bearer $LYSSNA_API_KEY" \
  -d '{
    "name": "Landing 5-second test — Q3 2026",
    "type": "five_second_test",
    "blocks": [
      {
        "type": "image",
        "src": "https://cdn.yourco.com/landing-v2.png",
        "duration_seconds": 5
      },
      {
        "type": "open_text",
        "question": "What do you remember from that page?"
      },
      {
        "type": "open_text",
        "question": "What do you think this page is for?"
      },
      {
        "type": "open_text",
        "question": "Who do you think it's for?"
      },
      {
        "type": "likert",
        "question": "How clear was the main message? (1=very unclear, 7=very clear)",
        "scale": 7
      }
    ],
    "sample_target": 30
  }'
```

### Recipe 3: Pull Chalkmark heatmap + first-click stats

```bash
curl -fsSL "https://api.optimalworkshop.com/v1/chalkmark/studies/$STUDY_ID/results" \
  -H "Authorization: Bearer $OPTIMAL_WORKSHOP_API_KEY" \
| jq '{
    respondents: .total_respondents,
    by_task: [.tasks[] | {
      prompt,
      first_click_correct_pct: .correct_pct,
      median_time_to_click: .median_time_seconds,
      heatmap_url: .heatmap_image_url,
      misclick_clusters: .misclick_clusters
    }]
  }'
```

### Recipe 4: Pull Lyssna 5-second test results

```bash
curl -fsSL "https://api.lyssna.com/v1/studies/$STUDY_ID/results" \
  -H "Authorization: Bearer $LYSSNA_API_KEY" \
| jq '{
    respondents: .total_responses,
    recall_words: [.blocks[] | select(.question | test("remember")) | .answers[]],
    purpose_perception: [.blocks[] | select(.question | test("for")) | .answers[]],
    clarity_score_median: .blocks[3].median
  }'
```

### Recipe 5: First-click design rules (Chalkmark)

```markdown
# First-click rules

## Image
- Full screen export at 1x scale; same as production user sees
- No annotations, no arrows, no highlights
- Same screen for all related tasks (don't switch between tasks)

## Tasks
- Outcome-framed: "Where would you click to [achieve outcome]?"
- NOT: "Click the Sign Up button" (gives the answer)
- 1-5 tasks per screen (more = fatigue)

## Targets
- Define correct hit zone as % of image (x, y, radius)
- Include alt-correct zones for legit alternatives ("see plans" link is also OK)

## Sample
- ≥30 per task for stable heatmap
- 50+ if comparing two designs
```

### Recipe 6: 5-second test design rules

```markdown
# 5-second test rules

## Image
- Above-the-fold content only (what user sees in 5 sec on real device)
- Real screen resolution; don't ship a portrait of a desktop
- Test the hero + headline + primary CTA in frame

## Questions (post-exposure)
- "What do you remember?" — open recall
- "What is this page for?" — purpose perception
- "Who is it for?" — audience clarity
- Likert clarity score (1-7)

## Sample
- 15-30 for stable first-impression
- Diverse panel (not just designers / PMs)
```

### Recipe 7: Coding 5-second test recall

```python
# Simple recall coding: count concept mentions
def code_recall(responses, expected_concepts):
    """
    responses: list of free-text answers
    expected_concepts: dict {concept_name: [keyword variants]}
    """
    from collections import Counter
    counts = Counter()
    for r in responses:
        text = r.lower()
        for concept, variants in expected_concepts.items():
            if any(v in text for v in variants):
                counts[concept] += 1
    return {c: counts[c] / len(responses) for c in expected_concepts}

# Example
EXPECTED = {
    "product_name": ["acme", "acme.io"],
    "value_prop": ["save time", "automate", "scheduling"],
    "audience": ["founder", "small business", "team"],
    "cta": ["free trial", "sign up", "get started"]
}
# >50% recall = communicates clearly
# <30% recall = redesign hero
```

### Recipe 8: A vs B comparison

```python
# Both Chalkmark and Lyssna support comparison
def compare_first_click(study_a_results, study_b_results, task_id):
    a = next(t for t in study_a_results["tasks"] if t["id"] == task_id)
    b = next(t for t in study_b_results["tasks"] if t["id"] == task_id)
    return {
        "A_correct_pct": a["correct_pct"],
        "B_correct_pct": b["correct_pct"],
        "delta": b["correct_pct"] - a["correct_pct"],
        "winner": "B" if b["correct_pct"] > a["correct_pct"] + 0.10 else "A" if a["correct_pct"] > b["correct_pct"] + 0.10 else "tie"
    }
```

### Recipe 9: Report template

```markdown
# First-Click + 5-Second Test Readout: [Page Name]

**Date:** [YYYY-MM-DD] · **N=[X]** · **Researcher:** [Name]

## TL;DR
- Primary CTA first-click rate: [X%] — [pass/fail vs target 60%]
- Hero clarity score: [X / 7]
- Recall of value prop: [X% of users mentioned core concept]

## First-click results

### Task: "Where would you click to [outcome]?"
- Correct first-click: [X%]
- Most common misclick: [region — % of users]
- Heatmap: [link]
- Median time to click: [X seconds]

## 5-second test recall

### "What do you remember?"
- Top concepts: [list with % mention]
- Notable: [outlier observations]

### "What is this page for?"
- Correctly identified purpose: [X% of users]
- Top wrong interpretations: [list]

## Recommendations
1. [Specific design change → expected impact]
2. ...
```

### Recipe 10: Pair with hotjar/clarity for behavioral confirmation

```bash
# After first-click test recommends change, confirm with production heatmap
# See SOTA tool reference in role.md for session replay options
# Microsoft Clarity (free): https://clarity.microsoft.com
# Hotjar: https://help.hotjar.com/hc/en-us/articles/hotjar-api
```

## Examples

### Example 1: Validate new hero before launch
**Goal:** Confirm hero CTA gets the first click.

**Steps:**
1. Chalkmark test (Recipe 1) with 30 trial-segment users.
2. Pull results (Recipe 3).
3. Decision: ≥70% first-click on CTA → ship. <50% → redesign.
4. Pair with 5-second test (Recipe 2) for recall + purpose perception.

**Result:** Quant evidence for hero readiness or redesign trigger.

### Example 2: A vs B layout comparison
**Goal:** Pick which landing layout to push.

**Steps:**
1. Run Chalkmark on A (N=30) and B (N=30) with same task prompts.
2. Compare first-click rates (Recipe 8).
3. Run 5-second test on each layout.
4. Winner = higher first-click + higher recall + higher clarity score.

**Result:** Defensible layout choice.

## Edge cases / gotchas

- **Image quality.** Low-res screenshot = pixel hunting; participant can't see what they're clicking.
- **Tasks that reveal the answer.** "Click Sign Up" instead of "Where would you click to start a trial?"
- **Comparing across different image resolutions.** Pick consistent resolution / aspect ratio.
- **Different segments for A vs B.** Designer-heavy panels skew results.
- **Sample below 30.** Heatmaps + recall unstable.
- **5-second on too-dense screens.** Recall drops below threshold for any concept. Reserve for hero / above-fold.
- **Multiple correct targets.** Define alt-correct zones for legit options ("free trial" CTA + "see plans" link).
- **No qualitative why.** First-click tells what, not why. Pair with 5-second test or short moderated round.
- **Above-fold misread.** Test the actual viewport user sees (desktop or mobile, not generic export).
- **Click position bias toward familiar layouts.** Users click center-right by default; CTA there boosts artificially.
- **Recall coding subjectivity.** Use coder-agreement check on a sample before finalizing.
- **5-second + first-click in same study.** Lyssna supports both; check timing (recall before click test).

## Sources

- [Optimal Workshop Chalkmark](https://help.optimalworkshop.com/en/articles/chalkmark)
- [Optimal Workshop API](https://help.optimalworkshop.com/en/articles/2079834-treejack-api)
- [Lyssna API](https://help.lyssna.com/api)
- [NN/g — Five-Second Tests](https://www.nngroup.com/articles/five-second-tests/)
- [NN/g — First-Click Testing](https://www.nngroup.com/articles/first-click-testing/)
- [NN/g — First-Click Testing for the Visual Web](https://www.nngroup.com/articles/first-click-testing-mobile-web/)
- [Microsoft Clarity](https://clarity.microsoft.com/)
