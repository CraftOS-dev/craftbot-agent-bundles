<!--
Sources:
RICE — https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers
ICE — https://growthhackers.com/articles/the-three-things-that-actually-matter-when-prioritizing-your-product-roadmap
Kano — https://www.productplan.com/glossary/kano-model
-->
# RICE / ICE / Kano Prioritization — SKILL

This pack executes RICE (Reach × Impact × Confidence / Effort), ICE (Impact × Confidence × Ease), and Kano (basic / performance / excitement / indifferent / reverse) on a backlog and writes scores back to Linear custom fields. For Kano, it pairs with the Maze survey skill.

## When to use

- Ranking a backlog of 5-100 items before sprint planning.
- Prioritizing experiment ideas (ICE is the default for experiments).
- Categorizing features by Kano (basic / performance / excitement) before scope decisions.
- Writing scores back to Linear so the ordering is shared and auditable.
- Cutting scope with MoSCoW or WSJF (covered here as alternatives).

Trigger phrases: "rank this backlog", "RICE score these features", "Kano on these candidates", "prioritize by ICE", "which experiments should we run first".

## Setup

```bash
# Pure compute — no external API beyond Linear write-back.
# Linear MCP is required for write-back; Maze is required for Kano surveys.
mcp tool linear.viewer
```

Auth:
- `LINEAR_API_KEY` — see `linear-product-management` skill.
- `MAZE_API_KEY` (optional, Kano only) — see `maze-usertesting-user-research` skill.

Linear custom fields needed (one-time team setup):
- `RICE Score` (number, decimal)
- `Reach` (number)
- `Impact` (select: 0.25 / 0.5 / 1 / 2 / 3)
- `Confidence` (select: 50% / 80% / 100%)
- `Effort` (number, person-weeks)
- `Kano Category` (select: Must-have / Performance / Excitement / Indifferent / Reverse / Questionable)

## Common recipes

### Recipe 1: RICE formula (canonical)

```
Score = (Reach × Impact × Confidence) / Effort

Reach        = # of users affected per quarter (real number, NOT 1-10)
Impact       = 3 massive / 2 high / 1 medium / 0.5 low / 0.25 minimal
Confidence   = 100% data-backed / 80% some evidence / 50% gut
Effort       = person-weeks (or person-months — be consistent)
```

```python
def rice(reach, impact, confidence, effort):
    return (reach * impact * confidence) / effort

# Example: a feature reaching 1200 quarterly users, high impact (2),
# 80% confidence, 3.5 person-weeks
print(rice(1200, 2, 0.8, 3.5))  # → 548.57
```

### Recipe 2: ICE formula (experiments)

```
Score = Impact × Confidence × Ease   (each 1-10)
```

```python
def ice(impact_1_10, confidence_1_10, ease_1_10):
    return impact_1_10 * confidence_1_10 * ease_1_10

print(ice(8, 7, 6))  # → 336 (out of 1000)
```

### Recipe 3: Score a Linear backlog and write back

```python
# Pull issues missing a RICE score; compute; update
import json, subprocess

def linear(query):
    return json.loads(subprocess.check_output(
        ["mcp", "tool", "linear.query", "--graphql", query]
    ))

issues = linear('''{
  issues(filter: {customFields: {RICE Score: {null: true}}, state: {type: {eq: "backlog"}}}, first: 50) {
    nodes { id title customFields { name value } }
  }
}''')["issues"]["nodes"]

for i in issues:
    cf = {f["name"]: f["value"] for f in i["customFields"]}
    if not all(k in cf for k in ["Reach","Impact","Confidence","Effort"]):
        print(f"SKIP {i['title']} — missing inputs")
        continue
    score = (float(cf["Reach"]) * float(cf["Impact"]) * float(cf["Confidence"])) / float(cf["Effort"])
    subprocess.run([
        "mcp","tool","linear.update_issue",
        "--id", i["id"],
        "--customFields", json.dumps([{"name":"RICE Score","value":round(score,2)}]),
    ])
    print(f"{i['title']}: {round(score,2)}")
```

### Recipe 4: Kano survey (delegate to Maze skill, then classify)

```bash
# Step 1: launch the Kano survey via Maze
# (see maze-usertesting-user-research Recipe 2)

# Step 2: pull responses
curl -fsSL "https://api.maze.co/v1/campaigns/$KANO_CAMPAIGN_ID/responses" \
  -H "Authorization: Bearer $MAZE_API_KEY" > kano-responses.json

# Step 3: classify (see Maze Recipe 7 for the KANO_TABLE)

# Step 4: write Kano category to Linear
for FEATURE in $(jq -r 'keys[]' kano-categories.json); do
  CATEGORY=$(jq -r ".[\"$FEATURE\"]" kano-categories.json)
  ISSUE_ID=$(mcp tool linear.list_issues --filter "{\"title\":{\"contains\":\"$FEATURE\"}}" | jq -r '.nodes[0].id')
  mcp tool linear.update_issue --id "$ISSUE_ID" \
    --customFields "[{\"name\":\"Kano Category\",\"value\":\"$CATEGORY\"}]"
done
```

### Recipe 5: Score a Notion DB instead of Linear (alt)

```python
# Same shape; targets Notion's number property
import requests
NOTION_KEY = os.environ["NOTION_API_KEY"]
H = {"Authorization": f"Bearer {NOTION_KEY}", "Notion-Version": "2022-06-28", "Content-Type":"application/json"}

resp = requests.post(f"https://api.notion.com/v1/databases/{db_id}/query", headers=H, json={
    "filter": {"property":"RICE Score","number":{"is_empty": True}}
}).json()

for page in resp["results"]:
    props = page["properties"]
    r = props["Reach"]["number"]
    i = props["Impact"]["number"]
    c = props["Confidence"]["number"]
    e = props["Effort"]["number"]
    if None in (r,i,c,e): continue
    score = (r*i*c)/e
    requests.patch(f"https://api.notion.com/v1/pages/{page['id']}", headers=H,
                   json={"properties":{"RICE Score":{"number":round(score,2)}}})
```

### Recipe 6: Top-N output with rationale

```bash
# Generate the markdown for the Notion prioritization doc
mcp tool linear.list_issues \
  --filter '{"state":{"type":{"eq":"backlog"}},"customFields":{"RICE Score":{"null":false}}}' \
  --orderBy '{"field":"customField:RICE Score","direction":"desc"}' \
  --first 10 \
| jq -r '.nodes[] | "| \(.title) | \(.customFields[]|select(.name=="Reach").value) | \(.customFields[]|select(.name=="Impact").value) | \(.customFields[]|select(.name=="Confidence").value) | \(.customFields[]|select(.name=="Effort").value) | **\(.customFields[]|select(.name=="RICE Score").value)** |"' \
| sed '1i| Title | Reach | Impact | Confidence | Effort | RICE |\n|---|---|---|---|---|---|'
```

### Recipe 7: MoSCoW (deadline-driven scope cut)

```
M — Must:    without this, the release fails
S — Should:  important but not critical
C — Could:   nice if time permits
W — Won't (this time): explicitly deferred
```

```python
# Apply MoSCoW from a release-targeting Linear view
def moscow_apply(issues, capacity_weeks):
    sorted_issues = sorted(issues, key=lambda i: i["rice_score"], reverse=True)
    cumulative = 0
    result = {"M":[], "S":[], "C":[], "W":[]}
    for i in sorted_issues:
        if cumulative + i["effort"] <= capacity_weeks * 0.7:
            result["M"].append(i); cumulative += i["effort"]
        elif cumulative + i["effort"] <= capacity_weeks * 0.9:
            result["S"].append(i); cumulative += i["effort"]
        elif cumulative + i["effort"] <= capacity_weeks:
            result["C"].append(i); cumulative += i["effort"]
        else:
            result["W"].append(i)
    return result
```

### Recipe 8: WSJF (SAFe-aligned organizations)

```
WSJF = Cost of Delay / Job Size

Cost of Delay = User-business value + Time criticality + Risk reduction
```

```python
def wsjf(user_value, time_crit, risk_reduc, job_size):
    return (user_value + time_crit + risk_reduc) / job_size

# All fields 1-10 Fibonacci-ish (1, 2, 3, 5, 8, 13)
print(wsjf(8, 5, 3, 5))  # → 3.2
```

### Recipe 9: Multi-framework consensus (when no single score wins)

```python
# Normalize each framework to 0-1 and weighted-avg
import numpy as np

def normalize(scores):
    arr = np.array(scores)
    return (arr - arr.min()) / (arr.max() - arr.min())

rice_n = normalize([i["rice"] for i in items])
ice_n = normalize([i["ice"] for i in items])
kano_w = np.array([{"Must-have":1, "Performance":0.7, "Excitement":0.5, "Indifferent":0.1, "Reverse":0, "Questionable":0.1}[i["kano"]] for i in items])

consensus = 0.5 * rice_n + 0.3 * ice_n + 0.2 * kano_w
ranked = sorted(zip(items, consensus), key=lambda x: -x[1])
```

### Recipe 10: Prioritization doc output template

```markdown
# Prioritization — [Backlog / Sprint / Quarter]

**Framework:** [RICE / ICE / Kano / MoSCoW / WSJF]
**Scored:** [N items]
**Date:** [YYYY-MM-DD]

## Top-3 with rationale

### #1 [Item] — Score: X.X
- Reach: ... | Impact: ... | Confidence: ... | Effort: ...
- Assumptions: [stated]
- Rationale: [outcome the team is chasing]

### #2 ...

## Full ranked list
| Rank | Item | Reach | Impact | Confidence | Effort | Score |
|---|---|---|---|---|---|---|

## Cut this round (Won't / Later)
- [Item — why deferred]
```

## Examples

### Example 1: Q3 backlog → top-10 with rationale
**Goal:** Pick the top-10 RICE items for Q3.

**Steps:**
1. Populate Reach/Impact/Confidence/Effort on every Q3-labeled Linear backlog issue (manual or via Recipe 5).
2. Run Recipe 3 to write back RICE Score.
3. Generate the ranked markdown table (Recipe 6) into a Notion doc.
4. Capacity check: sum top-10 Effort; if > team velocity × quarter, cut from #11 upward.
5. Surface the top-3 with rationale paragraphs for the planning meeting.

**Result:** A defensible top-10 with audit trail; team meeting starts with "what do we cut, not what do we add."

### Example 2: Kano-driven roadmap input
**Goal:** Distinguish must-haves from delighters for the Q3 plan.

**Steps:**
1. Run Kano via Maze (Recipe 4).
2. Decision rule:
   - Must-have items → ship in Q3 NOW.
   - Performance items → rank by RICE among themselves; top-3 go NEXT.
   - Excitement items → reserve 1 for delight; defer rest.
   - Indifferent + Reverse → cut.
3. Write Kano category back to Linear; the roadmap doc filters by `Kano Category`.

**Result:** A roadmap weighted by both customer expectation (Kano) and value-vs-effort (RICE).

## Edge cases / gotchas

- **Reach in real numbers.** "Reach = 8/10" is wrong. Reach = # of users affected per quarter, real count.
- **Confidence collapsing scores.** A 50% confidence multiplier should make you re-think the estimate, not just lower the score. Surface "low-confidence top items" for further discovery.
- **Effort estimation drift.** PM-only estimates are systematically low; require engineering T-shirt sizing before scoring.
- **RICE and Kano answer different questions.** RICE = "where to invest." Kano = "what kind of feature is this." Use together, not interchangeably.
- **ICE for experiments only.** Don't ICE features (Reach matters); don't RICE experiments (Reach is fixed by traffic, not the question).
- **Custom field setup.** Recipe 3 fails if the Linear team lacks `RICE Score` etc. Add a setup-check that verifies custom-field schema before running.
- **Kano sample size.** ≥150 responses for stable classification per feature. Otherwise categories oscillate.
- **Weighted consensus (Recipe 9) is opinionated.** The 0.5/0.3/0.2 weights reflect one tradeoff; surface this in the doc.
- **MoSCoW for deadline projects only.** Don't apply MoSCoW to a regular backlog — use RICE.
- **Re-scoring cadence.** RICE inputs decay; re-score quarterly or when major user research shifts the Reach/Impact figures.

## Sources

- [RICE — Intercom blog](https://www.intercom.com/blog/rice-simple-prioritization-for-product-managers)
- [ICE — Sean Ellis growth hackers](https://growthhackers.com/articles/the-three-things-that-actually-matter-when-prioritizing-your-product-roadmap)
- [Kano model — ProductPlan](https://www.productplan.com/glossary/kano-model)
- [Kano questionnaire — UX Tigers](https://www.uxtigers.com/post/kano-model)
- [WSJF — SAFe](https://scaledagileframework.com/wsjf)
- [MoSCoW — DSDM](https://www.agilebusiness.org/dsdm-project-framework/moscow-prioririsation.html)
- [Marty Cagan on outcomes-over-outputs](https://www.svpg.com/outcomes-over-output)
