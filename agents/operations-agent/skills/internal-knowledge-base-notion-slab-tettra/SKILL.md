<!--
Sources: https://www.buildmvpfast.com/blog/ai-internal-wiki-knowledge-base-notion-confluence-alternative-2026
         https://slite.com/learn/knowledge-base-softwares
         https://www.taskade.com/blog/ai-wiki-tools
         https://www.docsie.io/blog/articles/confluence-vs-notion-comparison-2026/
Notion Agents 2026 = autonomous bots on teamspaces. Confluence Rovo AI fully integrated 2026.
Slab free <10 users; Tettra Slack-native $4/user.
-->
# Internal Knowledge Base — Notion / Slab / Tettra / Confluence — SKILL

Architect and run an internal KB / wiki: information architecture by team size + tool ecosystem, AI agent setup (Notion Agents, Confluence Rovo, Slab AI), cross-tool search, freshness automation, content-decay monitoring. Stage-by-team-size selection; 2026 changes integrated.

## When to use

- Standing up first wiki for a 5-25 person team.
- Migrating from sprawled Slack/Drive to a KB.
- Adding AI search / Q&A.
- Mid-size team's KB has rotted; audit + rationalize.
- Trigger phrases: "wiki", "knowledge base", "KB", "internal docs", "Notion", "Slab", "Tettra", "Confluence", "Slite", "search", "stale doc", "AI agent for docs".

## Setup

```bash
export NOTION_TOKEN="xxx"        # https://developers.notion.com — Internal integration
export SLAB_TOKEN="xxx"          # https://slab.com — API on Standard+ plans
export TETTRA_TOKEN="xxx"        # https://tettra.com
export CONFLUENCE_TOKEN="xxx"    # https://developer.atlassian.com — Confluence Cloud REST
export SLITE_TOKEN="xxx"
```

## Common recipes

### Recipe 1: Stage / team-size selection
```yaml
choose:
  team_5_to_20_unified_search:
    primary: Slab
    why: Free <10 users; unified search across Slab + Slack + Drive + Notion
  slack_heavy_team_qa_first:
    primary: Tettra
    why: Slack-native; AI-routed Q&A → KB articles; $4/user
  team_20_to_500_general_purpose:
    primary: Notion
    why: 2026 Notion Agents (autonomous bots on teamspaces); broadest authoring; databases
  team_500_plus_or_atlassian_shop:
    primary: Confluence
    why: 2026 Rovo AI fully integrated; 20+ pre-built agents; enterprise governance
  docs_focused_engineering:
    primary: GitBook
    why: Best Markdown + git-backed; engineering teams; public + private docs
  alt_clean_modern:
    primary: Slite
    why: Clean UX; AI + search
  oss_self_host:
    primary: BookStack or Docusaurus
    why: Free; self-host; engineering-friendly
```

### Recipe 2: KB information architecture template
```yaml
top_level:
  Company:
    - About + Vision + Values
    - All-Hands archive
    - Brand assets
  People:
    - Handbook
    - Compensation philosophy
    - Career framework
    - Benefits + PTO
    - Onboarding + Offboarding
  Engineering:
    - Architecture overview
    - Services catalog (service / owner / on-call / runbook link)
    - Coding standards
    - On-call runbooks
    - Postmortems
  Product:
    - PRDs / specs (by quarter)
    - Roadmap
    - Customer research
    - Pricing
  Go-to-Market:
    - Sales playbook
    - Pricing + packaging
    - Customer references / case studies
    - Competitive intel
  Marketing:
    - Brand guidelines
    - Campaign archive
    - Press kit
  Operations:
    - Vendor registry + contracts
    - SOPs / playbooks
    - SaaS audit history
    - BCP + runbooks
    - Insurance binder
  Finance:
    - Board materials archive
    - Headcount plan
    - Annual budget
    - Spend audit history
  Legal:
    - MSA + DPA templates
    - Privacy policy + ToS history
    - IP assignments archive
```

### Recipe 3: Notion page creation
```bash
curl -s -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_TOKEN" -H "Notion-Version: 2022-06-28" -H "Content-Type: application/json" \
  -d '{
    "parent":{"page_id":"<parent>"},
    "properties":{"title":{"title":[{"text":{"content":"Engineering — Services Catalog"}}]}},
    "children":[
      {"type":"heading_1","heading_1":{"rich_text":[{"text":{"content":"Services"}}]}},
      {"type":"child_database","child_database":{"title":"Services DB"}}
    ]
  }'
```

### Recipe 4: Notion Agents — autonomous teamspace bot (2026)
```yaml
# Configure a Notion Agent for the People teamspace
# In UI: Teamspace Settings → Agents → New Agent
agent_config:
  name: "HR Agent"
  scope: People teamspace
  triggers:
    - on_page_create
    - on_page_edit
    - on_database_row_change
  capabilities:
    - "Answer questions about handbook"
    - "Surface stale pages (Effective Date > 180 days)"
    - "Flag benefits-DB rows missing state-specific addenda"
    - "Suggest tags + categorization"
  permissions:
    - read: People teamspace
    - write: comments only (no destructive edits)
```

### Recipe 5: Slab — push doc + auto-categorize
```bash
curl -s -X POST "https://api.slab.com/v1/posts" \
  -H "Authorization: Bearer $SLAB_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title":"Q3 2026 OKR Worksheet",
    "content_markdown":"# OKR\n...",
    "topic_ids":["<topic-okrs>"],
    "owner_id":"<owner>"
  }'
```

### Recipe 6: Tettra — Slack Q&A → KB article
```bash
# Tettra workflow: anyone asks in Slack via /tettra → AI routes to KB or asks owner
curl -s -X POST "https://api.tettra.com/v1/cards" \
  -H "Authorization: Bearer $TETTRA_TOKEN" -H "Content-Type: application/json" \
  -d '{
    "title":"How do I expense a meal?",
    "content":"...",
    "category_id":"<category-finance>",
    "owner_id":"<finance-lead>"
  }'
```

### Recipe 7: Confluence Cloud — bulk page tree
```bash
# Create top-level space + populate
curl -s -X POST "https://<co>.atlassian.net/wiki/rest/api/space" \
  -H "Authorization: Basic $(echo -n $CONFLUENCE_USER:$CONFLUENCE_TOKEN | base64)" \
  -H "Content-Type: application/json" \
  -d '{"key":"OPS","name":"Operations","description":{"plain":{"value":"Ops docs"}}}'

# Create page
curl -s -X POST "https://<co>.atlassian.net/wiki/rest/api/content" \
  -H "Authorization: Basic ..." -H "Content-Type: application/json" \
  -d '{
    "type":"page","title":"Vendor Registry",
    "space":{"key":"OPS"},
    "body":{"storage":{"value":"<h1>Vendors</h1>","representation":"storage"}}
  }'
```

### Recipe 8: Confluence Rovo AI — pre-built agents
```yaml
rovo_pre_built_agents_2026:
  - Spec writer        # generates PRD from research notes
  - Decision logger    # tracks ADRs
  - Question answerer  # Q&A over space
  - Status summarizer  # weekly summary of changed pages
  - Style coach        # writing review
  - Doc gardener       # surfaces stale pages
  - Diagram drawer     # generates Mermaid/PlantUML
# Enable via Confluence admin → Atlassian Intelligence → Agents
```

### Recipe 9: Cross-tool unified search (Slab feature; or DIY)
```python
# DIY: query Notion + Slab + Drive + Slack in parallel; rank by relevance
import requests, asyncio, os
async def search_all(q):
    tasks = [
        notion_search(q), slab_search(q), drive_search(q), slack_search(q)
    ]
    results = await asyncio.gather(*tasks)
    return rerank_by_recency_and_owner(results)
# Slab's product does this natively across the same stack.
```

### Recipe 10: Stale-page sweep (Python)
```python
import datetime, requests, os
HEADER = {'Authorization': f"Bearer {os.environ['NOTION_TOKEN']}", 'Notion-Version':'2022-06-28'}
db = '<sop-or-kb-db>'
stale = requests.post(f"https://api.notion.com/v1/databases/{db}/query",
    headers=HEADER, json={
        'filter':{'property':'Last Reviewed','date':{'before':
            (datetime.date.today() - datetime.timedelta(days=180)).isoformat()
        }}
    }).json()
for page in stale['results']:
    owner = page['properties']['Owner']['people'][0]['name']
    title = page['properties']['Name']['title'][0]['plain_text']
    # Slack DM via slack-mcp: "Hey owner, this page is stale: <title>"
```

### Recipe 11: KB launch playbook
```markdown
# KB rollout — 4 weeks

## Week 1: Architecture
- Recipe 2: IA template adopted.
- Top-level pages created.
- Naming convention published.

## Week 2: Migration
- Inventory existing docs in Drive / Slack pins / DM threads.
- Migrate critical 30 docs (per Pareto).
- Tag + owner per page.

## Week 3: Adoption
- Manager training on writing + tagging.
- Recipe 4 / 8 Agents enabled.
- Slack reminders: "If you Slack-ed answer twice, write a KB page."

## Week 4: Hygiene
- Recipe 10 stale sweep automated weekly.
- KB-health dashboard (page count, freshness, orphan rate).
- Quarterly "garden day" added to ops cadence.
```

## Examples

### Example 1: 30-person team — start KB from zero
**Goal:** Live wiki in 4 weeks.
**Steps:**
1. Recipe 1 → Notion.
2. Recipe 2 IA in `notion-mcp`.
3. Recipe 11 rollout.
4. Recipe 4 HR Agent on People teamspace.
5. Recipe 10 weekly stale sweep wired to ops-lead Slack DM.

**Result:** Indexed, owned, AI-assisted KB; manager-driven adoption.

### Example 2: Slack-heavy startup adds Tettra
**Goal:** Stop repeating same answers in Slack DMs.
**Steps:**
1. Recipe 1 → Tettra.
2. Install Tettra Slack app.
3. /tettra command in #ask-anything channel.
4. Recipe 6: convert FAQs to cards.
5. Owner notifications on stale cards.

**Result:** Slack-native Q&A; lower answer-repeat.

## Edge cases / gotchas

- **Search recall ≠ trust.** A KB with stale info is worse than no KB. Recipe 10 mandatory.
- **Owner orphaning.** Default ownership policy: page owner is the publisher; reassign on departure (per `onboarding-offboarding-workflows`).
- **Permission sprawl.** Granular per-page permissions are unmaintainable; default to teamspace-level with explicit exceptions.
- **Notion Agent training.** Recipe 4 — agents trained on teamspace content reflect content quality. Garbage in = bad answers.
- **Confluence Rovo licensing.** Premium / Enterprise required for Rovo. Verify before promising agents to recipient on Standard tier.
- **AI hallucination on KB Q&A.** Tools sometimes fabricate citations. Recipe 8 agents should cite source pages; verify links.
- **Cross-tool sync drift.** Recipe 9 — multiple wikis = source-of-truth conflict. Pick ONE primary.
- **Engineering vs non-engineering preferences.** Eng often prefers Markdown + git (GitBook/Docusaurus). Force-converging to Notion can backfire.
- **GitHub Wiki / Wiki.js / BookStack.** OSS options exist but require ops cycles.
- **DSAR (right to erasure).** KB content referencing departed-employee PII must be redactable. Recipe 7+10 review workflow needed.
- **Defer to `legal-counsel` for binding privacy policy, DPA, and customer-data handling docs published to a KB.**

## Sources

- BuildMVPFast — AI Internal Wiki 2026: https://www.buildmvpfast.com/blog/ai-internal-wiki-knowledge-base-notion-confluence-alternative-2026
- Slite — 12 Best KB Software 2026: https://slite.com/learn/knowledge-base-softwares
- Docsie — Confluence vs Notion 2026: https://www.docsie.io/blog/articles/confluence-vs-notion-comparison-2026/
- Taskade — Best AI Wiki Tools 2026: https://www.taskade.com/blog/ai-wiki-tools
- Notion API: https://developers.notion.com/
- Slab API: https://api.slab.com/
- Tettra: https://tettra.com/
- Confluence Cloud REST: https://developer.atlassian.com/cloud/confluence/rest/
- GitBook: https://gitbook.com/
- BookStack: https://www.bookstackapp.com/
