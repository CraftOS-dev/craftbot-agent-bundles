<!--
Sources: Klue — Competitive Intelligence Tools https://klue.com/topics/competitive-intelligence-tools-b2b-software
         Visualping https://visualping.io/
         GitHub REST https://docs.github.com/en/rest
Companion playbook: role.md → "Feature parity matrix template"
-->

# Feature parity tracking

Per-competitor feature matrix maintained as YAML/CSV with versioned diffs and changelog watch. Rows = features, columns = competitors + us + last-checked date. Track at three levels: feature name, sub-feature flags, pricing-tier gating. Output: `xlsx` parity matrix + GitHub-versioned `parity.yaml`.

## When to use

- "Build feature parity matrix for [comp set]"
- "Did [competitor] ship [feature X] yet?"
- "What's our gap vs Acme on [job-to-be-done Y]?"
- Quarterly comp-set parity audit
- Pre-deal: rep asks "do they have X?"

## When NOT to use

- One-off feature compare → use `competitor-product-teardown-depth`
- Pricing-tier comparison → use `competitor-pricing-tier-comparison`
- Changelog-only watch (no matrix) → set up Visualping directly via `competitor-pricing-page-visualping-distill`

## Setup

```bash
# Python + pandas + openpyxl for matrix maintenance
pipx install pandas openpyxl pyyaml
# Or use uv project:
uv pip install pandas openpyxl pyyaml requests

# Visualping for changelog auto-watch
export VISUALPING_API_KEY="..."

# GitHub for OSS competitor releases
export GITHUB_TOKEN="ghp_..."
```

MCPs in `agent.yaml`: `firecrawl-mcp`, `playwright-mcp`, `xlsx`, `github-api`, `ai-news-collectors`.

## Common recipes

### Recipe 1: parity.yaml schema

```yaml
# parity.yaml — version-controlled source of truth
competitors:
  - id: us
    name: Our Product
  - id: acme
    name: Acme Corp
    homepage: https://acme.example.com
    changelog_url: https://acme.example.com/changelog
  - id: beta
    name: Beta Inc

features:
  - id: sso-saml
    name: SSO (SAML)
    category: security
    sub_features:
      - id: sso-saml-just-in-time
        name: JIT provisioning
    levels:
      us: {present: true, tier: "Pro", confidence: high, source: "internal docs", verified: 2026-06-01}
      acme: {present: true, tier: "Enterprise", confidence: high, source: "https://acme.example.com/pricing", verified: 2026-06-08}
      beta: {present: false, confidence: medium, source: "homepage no mention", verified: 2026-06-08}

  - id: ai-summaries
    name: AI auto-summarization
    category: ai
    levels:
      us: {present: true, tier: "Pro", confidence: high, verified: 2026-06-01}
      acme: {present: roadmap, confidence: medium, source: "https://acme.example.com/changelog#2026-q2-roadmap", verified: 2026-06-09}
```

Confidence values: `high` (verified in product/docs), `medium` (changelog/case study/G2), `low` (single-source claim).

### Recipe 2: Convert parity.yaml → xlsx matrix

```python
import yaml, pandas as pd
data = yaml.safe_load(open("parity.yaml"))
rows = []
for f in data["features"]:
    row = {"Feature": f["name"], "Category": f["category"]}
    for c in data["competitors"]:
        cid = c["id"]
        lvl = f["levels"].get(cid, {})
        present = lvl.get("present", False)
        row[c["name"]] = {True:"✓", False:"✗", "roadmap":"⚠ roadmap", "partial":"⚠ partial"}.get(present, "?")
        row[f"{c['name']} conf"] = lvl.get("confidence", "")
        row[f"{c['name']} verified"] = lvl.get("verified", "")
    rows.append(row)
pd.DataFrame(rows).to_excel("parity.xlsx", index=False)
```

### Recipe 3: Auto-watch changelog with Visualping

```bash
curl -X POST https://api.visualping.io/v1/jobs \
  -H "Authorization: Bearer $VISUALPING_API_KEY" \
  -d '{
    "url":"https://acme.example.com/changelog",
    "frequency_minutes":1440,
    "selector":"article.changelog-entry",
    "webhook_url":"https://hooks.slack.com/services/..."
  }'
```

### Recipe 4: Watch GitHub releases for OSS competitor

```python
import requests
H = {"Authorization": f"Bearer {os.environ['GITHUB_TOKEN']}"}
rels = requests.get("https://api.github.com/repos/acme-org/acme/releases?per_page=10", headers=H).json()
new_features = [{"tag": r["tag_name"], "date": r["published_at"],
                 "title": r["name"], "body": r["body"][:500]} for r in rels]
```

### Recipe 5: LLM-extract features from changelog entry

```python
import anthropic
client = anthropic.Anthropic()
prompt = f"""Extract features from this changelog. Output JSON:
[{{"feature_name":..., "category":..., "kind":"new|deprecated|improvement", "tier_gated":bool}}]

Changelog:
{changelog_text}
"""
resp = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=2000,
    messages=[{"role":"user","content":prompt}],
)
features = json.loads(resp.content[0].text)
```

### Recipe 6: Diff parity.yaml across versions

```bash
# Versioned in git; diff at any cycle:
git log --oneline parity.yaml | head -5
git diff HEAD~1 HEAD parity.yaml
```

Or programmatic:

```python
import yaml
v_now = yaml.safe_load(open("parity.yaml"))
v_prev = yaml.safe_load(open("parity-2026-q1.yaml"))
# Diff features.levels per competitor; flag delta
```

### Recipe 7: ai-news-collectors release feed

```python
from ai_news_collectors import collect
items = collect(queries=["Acme launches", "Acme ships", "Acme releases"],
                since="2026-06-04")
```

### Recipe 8: Add a feature row after teardown

```python
# After competitor-product-teardown-depth lands a new finding,
# patch parity.yaml:
data = yaml.safe_load(open("parity.yaml"))
data["features"].append({
    "id":"workflow-automation","name":"Workflow automation","category":"automation",
    "levels":{
        "us":{"present":False,"confidence":"high","verified":"2026-06-11"},
        "acme":{"present":True,"tier":"Pro","confidence":"high",
                "source":"https://acme.example.com/workflows","verified":"2026-06-11"},
    },
})
yaml.safe_dump(data, open("parity.yaml","w"))
```

### Recipe 9: Quarterly audit script

```python
import yaml, datetime
data = yaml.safe_load(open("parity.yaml"))
stale = []
threshold = (datetime.date.today() - datetime.timedelta(days=90)).isoformat()
for f in data["features"]:
    for cid, lvl in f["levels"].items():
        if str(lvl.get("verified","")) < threshold:
            stale.append((f["id"], cid, lvl.get("verified")))
print(f"{len(stale)} stale cells")
```

### Recipe 10: Render battlecard delta from parity diff

When parity.yaml changes, auto-update battlecard pane 4 (feature parity snapshot) via Klue/Crayon API or Notion patch. See `ci-delivery-slack-crm-klue-insider`.

## Examples

### Example 1: Initial parity matrix for 3 competitors (1 day)

**Goal:** Build first parity matrix for Acme, Beta, Gamma.

**Steps:**
1. Author `parity.yaml` with 30 load-bearing features (not 200; pick the ones reps need).
2. For each competitor × feature: check public pricing page + product tour + G2 reviews + changelog. Mark `present: true|false|roadmap|partial`.
3. Run Recipe 2 → parity.xlsx → commit + share via Notion.
4. Set up Visualping changelog watches (Recipe 3) for all 3.
5. Set up GitHub release watches (Recipe 4) for OSS components.

**Result:** Source-of-truth YAML + xlsx + auto-watch wired.

### Example 2: Quarterly audit pass

**Goal:** Refresh stale cells before QBR.

**Steps:**
1. Run Recipe 9 to list stale cells.
2. For each, re-verify via pricing page / public docs / changelog.
3. Patch `parity.yaml`; commit; re-render `parity.xlsx`.
4. Diff (Recipe 6) — output "delta since last quarter" for QBR slide.

**Result:** Fresh matrix + delta narrative.

## Edge cases / gotchas

- **Feature naming inconsistency** — Acme calls it "Workflows," Beta calls it "Automations," Gamma calls it "Pipelines." Canonicalize in YAML; surface their language in the source field.
- **Roadmap claims** — competitor says "coming Q3." Tag as `present: roadmap`; never count as parity. Confirm shipped via release / public announce.
- **Tier-gated features** — feature present but only in Enterprise tier. Capture `tier` field so battlecard surfaces the gating.
- **Partial features** — feature exists but missing a key sub-flag (e.g., SSO without SCIM). Use `present: partial` + sub_features detail.
- **Confidence inflation** — single-source claims marked `high` lose battlecard credibility. Default to `medium` unless verified in product or in official docs.
- **Pricing-tier shifts retire features** — Acme moves a Pro feature to Enterprise tier; the `tier` field updates, `present` doesn't.
- **Stale matrix syndrome** — without Visualping watches, matrix decays in 4-6 weeks. Auto-watch is mandatory at scale.
- **Don't put 200 features** — reps scan; 20-40 load-bearing features beat exhaustive catalog. Cull features that don't drive deals.
- **GitHub releases ≠ shipped product** — OSS competitor's repo release ≠ available in their SaaS UI. Verify in product before flipping the cell.
- **Cross-language changelogs** — international competitors ship in non-English first. Use `deepl-mcp` to translate before LLM extraction.

## Sources

- Klue — CI tools for B2B 2026 — https://klue.com/topics/competitive-intelligence-tools-b2b-software
- Autobound — CI Tools Compared 2026 — https://www.autobound.ai/blog/top-15-competitive-intelligence-tools-2026
- Visualping — https://visualping.io/
- GitHub REST API — https://docs.github.com/en/rest
- role.md → "Feature parity matrix template" (this bundle)

## Related skills

- `competitor-product-teardown-depth` — feeds new features into parity.yaml
- `continuous-competitor-monitoring-klue-kompyte-crayon` — wires changelog watches
- `competitor-pricing-tier-comparison` — pairs with feature tier-gating
- `battlecard-authoring-maintenance` — parity snapshot is pane 4
- `competitor-messaging-tracking-diff` — LP language drift often follows new feature
