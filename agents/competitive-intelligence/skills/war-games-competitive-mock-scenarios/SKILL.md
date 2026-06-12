<!--
Sources: SCIP scenario planning pattern https://www.scip.org/page/Ethical-Intelligence
         Brainstorming + concise-planning skills (CraftBot defaults)
         Anthropic Messages API https://docs.anthropic.com/en/api/messages
Companion playbook: role.md → "War games playbook"
-->

# War games (competitive mock scenarios)

Pre-mortem on attack scenarios + red-team responses + decision-tree playbook. Format: "Competitor X attacks us in segment Y" — pre-mortem ≥5 attack vectors, red-team each, document signal-triggers + owners. Quarterly re-run with fresh signals. Output: pptx playbook + Slack alert config.

## When to use

- "Run a war-game session on [scenario X]"
- "What if Acme drops pricing 50%?"
- "What if Salesforce launches a competing tier?"
- Quarterly strategy off-site preparation
- After a credible attack vector emerges (analyst rumor, hire signal)

## When NOT to use

- Continuous monitoring → use `continuous-competitor-monitoring-klue-kompyte-crayon`
- Single-competitor profile → use `competitor-product-teardown-depth`
- Single-deal red-team → use `hot-deals-ci-deal-level`

## Setup

```bash
# Anthropic for divergent generation + adversarial cross-check
export ANTHROPIC_API_KEY="sk-ant-..."

# Python for synthesis
uv pip install anthropic pptx python-pptx jinja2

# Optional: Gemini for second-LLM adversarial cross-check
export GOOGLE_API_KEY="..."
```

MCPs in `agent.yaml`: `brainstorming`, `concise-planning`, `pptx`, `docx`, `slack-mcp`, `notion-mcp`.

## Common recipes

### Recipe 1: Scenario definition template

```yaml
# scenarios/acme-smb-attack.yaml
scenario_id: acme-smb-attack
title: "Acme announces SMB pricing tier 50% below ours"
classification: pricing_attack
likelihood: medium
impact_severity: high
trigger_signals:
  - acme careers-page surge in SMB GTM hires
  - acme messaging tracking adds "for small teams" hero
  - acme Reddit/G2 mentions "SMB tier coming"
lead_time_estimate_days: 30-60
segments_impacted: ["SMB","Mid-market"]
deal_economics_impact: "5-10% win-rate drop in SMB; ACV pressure on Mid-market"
```

### Recipe 2: Pre-mortem — divergent attack vector generation

```python
import anthropic
client = anthropic.Anthropic()
prompt = f"""You are a competitive strategist red-teaming our company.
Scenario: {scenario['title']}
Context: {scenario.get('context','')}

Generate ≥5 distinct attack vectors the competitor could use to win this scenario.
For each, output JSON:
{{
  "vector": "<1-line label>",
  "mechanism": "<how it works>",
  "trigger_signals": ["<signal 1>", "<signal 2>"],
  "lead_time_days": int,
  "segment_impact": "<segments>",
  "deal_economics": "<$ impact direction + magnitude>"
}}
Be specific; do not include 'they could be better' generic moves.
"""
resp = client.messages.create(model="claude-sonnet-4-5-20250929",
    max_tokens=3000, messages=[{"role":"user","content":prompt}])
vectors = json.loads(resp.content[0].text)
```

### Recipe 3: Red-team responses

```python
prompt = f"""For each attack vector, design our response.
Attack: {vector}
Constraints: budget <$2M Q3; engineering ~5 engineers available; PMM bandwidth limited.

Output JSON:
{{
  "response_options": [
    {{"option":"price match","cost":int,"feasibility":"high|medium|low",
      "risk":"<1 line>","timeline_days":int}},
    {{"option":"unbundle SSO into Starter","cost":int,...}},
    {{"option":"counter-launch feature X","cost":int,...}}
  ],
  "recommended":"<which option + why>"
}}
"""
resp = client.messages.create(model="claude-sonnet-4-5-20250929",
    max_tokens=2000, messages=[{"role":"user","content":prompt}])
responses = json.loads(resp.content[0].text)
```

### Recipe 4: Adversarial cross-check (second LLM)

```python
# Run the same scenario through Gemini and see what attack vectors / responses it generates differently
import google.generativeai as genai
genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
gem = genai.GenerativeModel("gemini-2.0-pro")
adv_resp = gem.generate_content(prompt).text
# Compare: anthropic's plan ∩ gemini's plan = robust; symmetric difference = unknowns to investigate
```

### Recipe 5: Decision tree assembly

```yaml
# decision-tree-acme-smb-attack.yaml
root: "Have we observed a confirmed trigger signal?"
branches:
  - signal: "Acme careers-page surge in SMB GTM hires (>3 per month)"
    action: "Flash brief; pre-stage Pricing v2 announcement copy"
    owner: "@cmo"
    decision_lead_time_days: 14
  - signal: "Acme launches SMB tier publicly"
    action: "Execute Response Option B (unbundle SSO into Starter)"
    owner: "@pmm-lead + @rev-ops"
    decision_lead_time_days: 7
  - signal: "Customer churn signal — 2+ logos cite Acme SMB as reason"
    action: "Emergency strategy review"
    owner: "@ceo + @cfo"
    decision_lead_time_days: 3
```

### Recipe 6: brainstorming skill for divergent fan-out

Invoke `brainstorming` skill for the pre-mortem step. Bounded by:
- 8-12 attack vectors target
- Forced diversity: 1+ pricing, 1+ product, 1+ channel, 1+ partnership, 1+ talent, 1+ messaging
- Score each by feasibility × impact

### Recipe 7: Render pptx playbook

```python
from pptx import Presentation
from pptx.util import Inches
prs = Presentation()
title = prs.slides.add_slide(prs.slide_layouts[0])
title.shapes.title.text = "War Game: Acme SMB Attack"
title.placeholders[1].text = "Q3 FY2026"

# Per attack vector: 1 slide
for v in vectors:
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = v["vector"]
    body = s.placeholders[1].text_frame
    body.text = f"Mechanism: {v['mechanism']}"
    body.add_paragraph().text = f"Trigger signals: {', '.join(v['trigger_signals'])}"
    body.add_paragraph().text = f"Lead time: {v['lead_time_days']} days"

# Per response: 1 slide
for v, r in zip(vectors, responses):
    s = prs.slides.add_slide(prs.slide_layouts[1])
    s.shapes.title.text = f"Response: {v['vector']}"
    s.placeholders[1].text_frame.text = f"Recommended: {r['recommended']}"

# Decision tree slide
# Signal-trigger config slide
# Owners + timeline slide
prs.save("war-games/acme-smb-attack.pptx")
```

### Recipe 8: Slack signal-trigger alert config

```yaml
# Wire to monitoring layer (continuous-competitor-monitoring-klue-kompyte-crayon)
alerts:
  - watch: acme careers-page SMB GTM hires
    threshold: 3/mo
    trigger_playbook: acme-smb-attack
    notify: ["#strategy","#exec","@cmo"]
  - watch: acme homepage hero contains "small teams"
    via: visualping_job_id_12345
    trigger_playbook: acme-smb-attack
```

### Recipe 9: Quarterly re-run cadence

```python
# scenarios/calendar.yaml
quarterly:
  - q3: ["acme-smb-attack","salesforce-bundle-attack","ai-inference-cost-drop"]
  - q4: ["acme-smb-attack","new-entrant-X","partner-acquisition"]
# Re-run = pull new monitoring signals + LLM regenerate + diff playbook + update owners
```

### Recipe 10: Live-fire variant — rep vs LLM-as-competitor

```python
# Stage a buyer call simulation
prompt = f"""You are an enterprise buyer comparing {our_name} vs {competitor_name}.
You strongly lean toward {competitor_name} because of {top_objection}.
Resist easy concessions; ask sharp questions; respond like a senior procurement leader.
"""
# Rep plays themselves; LLM plays buyer; record session for win/loss program
```

### Recipe 11: Post-mortem on executed response

When a scenario fires for real and a response is executed:

```yaml
post_mortem:
  scenario: acme-smb-attack
  fired_at: 2026-05-15
  response_executed: "Option B — unbundled SSO into Starter"
  outcome_60d: "SMB win-rate stabilized; ACV down 3% as expected"
  what_worked: ["Pre-staged announcement copy","PMM-aligned positioning"]
  what_didnt: ["Eng underestimated SSO refactor by 3 wks"]
  playbook_updates: ["Move SSO unbundle to default; add 4-wk eng buffer"]
```

## Examples

### Example 1: Pre-Q3 strategy off-site war-game

**Goal:** Run 3 war-games (Acme SMB attack, AI cost drop, new entrant) for Q3 off-site.

**Steps:**
1. Author 3 `scenarios/*.yaml` (Recipe 1).
2. For each: Recipe 6 brainstorming → Recipe 2 LLM divergent → Recipe 3 red-team.
3. Recipe 4 Gemini cross-check on top 2.
4. Recipe 5 → decision tree per scenario.
5. Recipe 7 → 3 pptx decks; combined exec summary.
6. Recipe 8 → wire signal triggers in monitoring layer.

**Result:** 3 playbooks + signal-trigger config; ready for off-site review.

### Example 2: Acme signal fires for real

**Goal:** Acme careers page surge — Recipe 8 alert. Execute playbook.

**Steps:**
1. Pull `acme-smb-attack.yaml` decision tree (Recipe 5).
2. Confirm trigger: ≥3 SMB GTM hires? Yes → Flash brief.
3. CMO + PMM kicks off pre-staged response (already documented).
4. After 60 days, Recipe 11 → post-mortem update.

**Result:** Pre-built playbook executes in 1 day instead of 2 weeks of scrambling.

## Edge cases / gotchas

- **Over-fitting to one scenario** — war-gaming Acme 5 ways doesn't help if Beta is the actual threat. Diversify across competitors quarterly.
- **Hindsight bias** — easy to "predict" the move you've already seen. Pre-mortem before you know the answer, archive the prediction.
- **Single-LLM bias** — Recipe 4 cross-check matters; one model misses vectors another sees.
- **Cost of execution** — Response Option estimates are LLM-guessed. Validate with eng/PMM before relying on them.
- **Signal-trigger drift** — careers-page surge metric drifts as company size changes. Re-calibrate thresholds quarterly.
- **Playbook decay** — playbooks authored Q1 are stale by Q4. Quarterly re-run mandatory (Recipe 9).
- **Decision-tree leaf with no owner** — alerts fire, nothing happens. Every branch needs an owner + decision lead time (Recipe 5).
- **LLM-generated quotes** — Recipe 10 live-fire variant; LLM may say things a real buyer wouldn't. Calibrate against real win/loss transcripts.
- **Confidentiality** — pre-staged response copy is sensitive. Restrict Notion / pptx access to exec + PMM lead.
- **Don't war-game everything** — 2-3 scenarios per quarter is enough; war-gaming 10 = noise + diminishing return.

## Sources

- SCIP — Ethical Intelligence (planning frame) — https://www.scip.org/page/Ethical-Intelligence
- Anthropic Messages API — https://docs.anthropic.com/en/api/messages
- Google Gemini API — https://ai.google.dev/gemini-api/docs
- role.md → "War games playbook" (this bundle)

## Related skills

- `continuous-competitor-monitoring-klue-kompyte-crayon` — signal triggers source
- `battlecard-authoring-maintenance` — playbook pairs with refreshed battlecards
- `hot-deals-ci-deal-level` — single-deal red-team variant
- `analyst-relations-watching-gartner-forrester` — analyst signals feed scenarios
- `ethical-public-source-methodology` — adversarial cross-check stays within SCIP
