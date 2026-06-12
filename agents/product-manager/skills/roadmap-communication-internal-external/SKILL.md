<!--
Sources:
Productboard — https://developer.productboard.com
Lenny — https://www.lennysnewsletter.com/p/roadmap-communication
Linear roadmaps — https://linear.app/docs/roadmaps
-->
# Roadmap Communication (Internal + External) — SKILL

Internal: Linear roadmap shared link + monthly all-hands deck (pptx). External: Productboard public portal (upvotes + feedback) OR a "What's Next" page on your site. Tier-based detail per audience.

## When to use

- Sharing the roadmap with exec / board (OKR alignment view).
- All-hands monthly roadmap update.
- Customer-facing "what's next" page or portal.
- Sales enablement on what to promise vs not promise.
- Quarterly cross-team roadmap review.

Trigger phrases: "share the roadmap", "publish the public roadmap", "communicate Q3 plan", "what to tell customers", "roadmap for all-hands", "what's next page".

## Setup

```bash
# Internal: Linear roadmap + pptx skill
mcp tool linear.viewer

# External: Productboard portal (paid) OR static Notion public page (free fallback)
curl -fsSL "https://api.productboard.com/v1/products" \
  -H "Authorization: Bearer $PRODUCTBOARD_API_TOKEN"
```

Auth:
- `LINEAR_API_KEY` — see `linear-product-management`.
- `PRODUCTBOARD_API_TOKEN` — from Productboard → Workspace settings → Integrations → Public API. Paid plan ($25/maker/mo+).

## Common recipes

### Recipe 1: Linear shareable roadmap URL (internal)

```bash
# Get the shareable URL for an initiative-level roadmap
mcp tool linear.list_initiatives \
  --filter '{"status":{"type":{"eq":"active"}}}' \
  --first 10 \
| jq -r '.nodes[] | {name, url}'

# Share URL is publicly accessible if "Public" is set; otherwise needs Linear login.
# To share with non-Linear users: enable workspace-level "Public initiatives" toggle.
```

### Recipe 2: Tier-based roadmap detail matrix

| Audience | Tier | Detail level | Where |
|---|---|---|---|
| Board / exec | T1 | OKR alignment + 5-7 themes | Notion 1-pager |
| All-hands | T2 | Outcomes + themes + dates (with hypothesis caveat) | pptx deck |
| Engineering | T3 | Initiative + epic + ready-cycle | Linear roadmap |
| Sales | T4 | Themes only + "won't this quarter" list | Notion sales-enable page |
| Customers (external) | T5 | Themes only, no dates | Productboard portal OR Notion |
| Public press | T6 | Brand-level only, no specifics | Marketing site |

### Recipe 3: All-hands roadmap deck (pptx)

```bash
# Use pptx skill — generate slides from a structured roadmap JSON
mcp tool pptx.create \
  --template "roadmap-allhands" \
  --output "q3-roadmap-allhands-$(date +%F).pptx" \
  --slides '[
    {"title":"Q3 Outcomes","bullets":[
      "D7 retention 35% → 42%",
      "Time-to-first-value 14min → 5min",
      "MRR per new account $50 → $120"
    ]},
    {"title":"NOW (committed)","bullets":[
      "Onboarding revamp — shipping June 22",
      "In-product checklist — shipping July 13",
      "Analytics instrumentation — ongoing"
    ]},
    {"title":"NEXT (planned)","bullets":[
      "Personalized templates — Aug",
      "AI assistant in-product — Aug/Sep"
    ]},
    {"title":"LATER (explored)","bullets":[
      "Mobile parity",
      "Advanced analytics dashboards"
    ]},
    {"title":"NOT this quarter (explicit no)","bullets":[
      "Enterprise SSO migration",
      "API v2",
      "Reseller portal"
    ]},
    {"title":"Risks","bullets":[
      "Auth team dependency for onboarding step 2",
      "Data warehouse migration may impact analytics dashboards"
    ]}
  ]'
```

### Recipe 4: Productboard portal — publish public roadmap

```bash
# 1. Create features in Productboard
curl -X POST "https://api.productboard.com/v1/features" \
  -H "Authorization: Bearer $PRODUCTBOARD_API_TOKEN" \
  -d '{
    "data":{
      "name":"3-step guided onboarding",
      "description":"Better first-session experience for new users",
      "status":{"name":"In progress"},
      "owner":{"email":"<pm@your.com>"}
    }
  }'

# 2. Publish to portal (Public Roadmap view in Productboard UI must be enabled)
# Public URL format: https://portal.productboard.com/<workspace>/tabs/<tab-id>
```

### Recipe 5: Notion public "What's Next" page (free fallback)

```bash
# Create a public-shared Notion page; no Productboard needed
mcp tool notion.create_page \
  --parent '{"page_id":"<public-root>"}' \
  --properties '{"title":[{"text":{"content":"What we are building next"}}]}' \
  --children '[
    {"type":"callout","callout":{"icon":{"emoji":"🚀"},"rich_text":[{"text":{"content":"Last updated: '$(date +%Y-%m-%d)'. Roadmap is a hypothesis — we ship when it is ready."}}]}},
    {"type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"In progress now"}}]}},
    {"type":"bulleted_list_item","bulleted_list_item":{"rich_text":[{"text":{"content":"3-step guided onboarding (shipping June)"}}]}},
    {"type":"bulleted_list_item","bulleted_list_item":{"rich_text":[{"text":{"content":"In-product checklist (shipping July)"}}]}},
    {"type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"On the way"}}]}},
    {"type":"bulleted_list_item","bulleted_list_item":{"rich_text":[{"text":{"content":"Personalized templates"}}]}},
    {"type":"heading_2","heading_2":{"rich_text":[{"text":{"content":"Considering"}}]}},
    {"type":"bulleted_list_item","bulleted_list_item":{"rich_text":[{"text":{"content":"Mobile app"}}]}}
  ]'

# Then manually toggle "Share to web" in the Notion UI
```

### Recipe 6: Customer feedback intake — Productboard insights inbox

```bash
# Send customer feedback into Productboard for triage
curl -X POST "https://api.productboard.com/v1/notes" \
  -H "Authorization: Bearer $PRODUCTBOARD_API_TOKEN" \
  -d '{
    "data":{
      "title":"Customer request: bulk-export for projects",
      "content":"Sara at Acme asked for CSV export of all projects monthly",
      "user":{"email":"sara@acme.com","company":"Acme"},
      "tags":["bulk-export","reporting"]
    }
  }'
```

### Recipe 7: Quarterly roadmap one-pager (for exec / board)

```markdown
# Q3 2026 Roadmap — [Product] · One-pager

**Hypothesis:** This roadmap is our best current bet, not a commitment.

## OKRs (this quarter)
- O1: D7 retention 35% → 42%
- O2: Time-to-first-value 14min → 5min
- O3: Net-new MRR per quarter +30%

## Themes (5-7 max)
1. **Activation revamp** — onboarding + first-session UX. Addresses O1, O2.
2. **AI assistant** — in-product help. Addresses O1.
3. **Pricing & packaging** — new Business tier. Addresses O3.
4. **Analytics depth** — funnels + cohorts. Supports all OKRs.
5. **Enterprise readiness** — SSO + audit log. New segment foothold.

## Risks
- Auth-team dependency on onboarding step 2
- Warehouse migration may slip analytics work

## Won't (explicit no)
- Mobile parity (deferred to Q4)
- API v2 (Q1 2027)
```

### Recipe 8: Sales enablement roadmap doc

```markdown
# Sales Enablement — Q3 2026

## What's shipping (commit-quality)
- [Feature] — shipping by [date], FOR SALE
- [Feature] — shipping by [date], DO NOT PROMISE specific date

## What's coming (don't sell, but mention)
- [Feature] — exploring, no date

## What we WON'T ship this quarter
- [Feature] — sales: defer the ask

## How to handle common asks
| Customer asks for | Answer |
|---|---|
| SSO | "Yes — shipping Q3, beta available now" |
| Mobile app | "Not in 2026 — happy to discuss workarounds" |
| Custom integrations | "Available on Business tier — connect to CS" |
```

### Recipe 9: Customer-comms email when roadmap shifts

```bash
mcp tool gmail.send \
  --to "<all-customers>" \
  --subject "Update on what we are building" \
  --body "$(cat <<'EOF'
Hi from [PM name],

A few updates on what we are building:

**Shipping in the next 30 days**
- 3-step guided onboarding
- In-product checklist

**Now in progress**
- Personalized templates (likely August)

**Changes from our last update**
- Mobile parity — we are deferring to Q4 to focus on activation
- Why: data shows activation is the bigger lever right now

Always happy to discuss tradeoffs. Reply to this email or join our community.

[PM name]
EOF
)"
```

### Recipe 10: Roadmap diff (what changed since last month)

```bash
# Compare current Linear initiatives vs last month's saved snapshot
mcp tool linear.list_initiatives --first 50 > roadmap-now.json
diff roadmap-last-month.json roadmap-now.json > roadmap-diff.txt

# Output: "Added: ...", "Removed: ...", "Status changed: ..."
echo "## Roadmap changes since last month" > roadmap-changes.md
diff roadmap-last-month.json roadmap-now.json | grep -E "^[<>]" | head -30 >> roadmap-changes.md
```

## Examples

### Example 1: Monthly all-hands update
**Goal:** Stand up the slide deck + Q&A doc for tomorrow's all-hands.

**Steps:**
1. Pull latest Linear initiatives + projects + cycle progress (Recipe 1).
2. Build the pptx (Recipe 3) — outcomes / NOW / NEXT / LATER / not-this-quarter / risks.
3. Pull the roadmap diff vs last month (Recipe 10).
4. Pre-share the deck in #product-leads for review.
5. Deliver at all-hands; archive in Notion.

**Result:** Org has aligned context; questions get the same answer regardless of who's asked.

### Example 2: Public roadmap launch
**Goal:** First time publishing a customer-facing roadmap.

**Steps:**
1. Decide tier (T5 from Recipe 2): themes only, no dates.
2. If Productboard: enable public portal (Recipe 4).
3. If not: create Notion page (Recipe 5) + toggle Share to Web.
4. Customer comms email announcing it (Recipe 9).
5. Feedback flows back via Productboard /notes (Recipe 6) OR a Notion form to Linear.

**Result:** Customers see direction without commit-by-date traps.

## Edge cases / gotchas

- **Date promises = trust traps.** External roadmap should have NO dates. Internal can have dates with hypothesis caveat.
- **Don't lead with a list.** Lead with outcomes/themes; lists of features bury the why.
- **"Won't" is as important as "will."** Stating explicit non-goals saves dozens of "can we add X" conversations.
- **Stale public roadmap = worse than none.** Update monthly minimum; outdated public pages signal abandonment.
- **Productboard is expensive.** $25/maker/mo + viewer fees. Notion public page is the free fallback for solo founders / small teams.
- **Internal vs external desync.** Sales sells from internal context, customers see external — mismatched if you don't keep parity.
- **Customer upvotes ≠ roadmap input.** Upvotes anchor on existing features; PMs still own prioritization.
- **Board level detail.** Boards want OKR alignment + risks + "what we learned." Not feature lists.
- **Tier slippage.** Engineers want all-hands detail; exec wants T1; sales wants T4. Resist the urge to bundle.
- **Quarterly cadence on external.** Don't update the public roadmap weekly — too much noise.

## Sources

- [Productboard public API](https://developer.productboard.com)
- [Productboard public roadmap feature](https://www.productboard.com/blog/public-roadmap)
- [Linear roadmaps](https://linear.app/docs/roadmaps)
- [Lenny — Roadmap communication](https://www.lennysnewsletter.com/p/roadmap-communication)
- [Marty Cagan — Now-Next-Later](https://www.svpg.com/the-product-roadmap)
- [Reforge — Public roadmap patterns](https://www.reforge.com/blog/public-roadmap)
- [Janna Bastow — ProdPad public roadmap](https://www.prodpad.com/blog/public-roadmap)
