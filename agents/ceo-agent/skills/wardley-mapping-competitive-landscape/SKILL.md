<!--
Source: https://onlinewardleymaps.com
Wardley mapping for competitive landscape and build/buy/partner gameplay
-->
# Wardley Mapping — Competitive Landscape + Gameplay

Wardley Mapping (Simon Wardley) maps the value chain on Y-axis (visible user need → invisible commodity infrastructure) and evolution on X-axis (genesis → custom built → product → commodity). Used to identify climate, doctrine, and 12-24 month gameplays — including build/buy/partner decisions. OnlineWardleyMaps.com is the free public renderer using a text DSL.

## When to use

- Mapping the competitive landscape for an upcoming strategy doc or board update.
- Choosing build vs buy vs partner for a capability (especially agentic AI components).
- Pre-mortem on a product strategy: "what's about to evolve from product → commodity and eat our moat?"
- Board pre-read for "where do we have advantage?" and "where are we exposed?"

Trigger phrases: "Wardley map", "competitive landscape", "build vs buy", "where's the moat", "what's commoditizing", "12-24 month gameplay".

## Setup

```bash
# OnlineWardleyMaps.com is the public renderer — no install needed for solo use.
# For agent automation, use curl + their JSON export endpoint.

# Optional: clone the open-source repo for self-host
git clone https://github.com/damonsk/onlinewardleymaps && cd onlinewardleymaps
npm install && npm start  # localhost:3000
```

Auth / API key requirements:
- No auth needed for the public web tool.
- For private maps: self-host the OSS version.
- `DRAWIO_API_KEY` if you prefer drawio render via `drawio-mcp`.

## Common recipes

### Recipe 1: Write the map in text DSL

```
title CraftBot landscape — Q2 2027

anchor User [0.99, 0.5]
component Founder workflow [0.95, 0.2]
component Agent orchestration [0.80, 0.35]
component LLM provider [0.30, 0.95]
component Vector store [0.40, 0.85]
component Auth / billing [0.20, 0.95]

User -> Founder workflow
Founder workflow -> Agent orchestration
Agent orchestration -> LLM provider
Agent orchestration -> Vector store
Founder workflow -> Auth / billing

inertia Vector store
```

X-coordinate position rules: 0.0-0.17 = Genesis, 0.17-0.4 = Custom, 0.4-0.7 = Product, 0.7-1.0 = Commodity.

### Recipe 2: Render the map (free hosted tool)

```bash
# Paste DSL into https://onlinewardleymaps.com → export PNG/SVG
# OR programmatic export via headless browser
npx playwright screenshot \
  --selector "#mapCanvas" \
  --full-page \
  "https://onlinewardleymaps.com/#YOUR_MAP_ID" \
  ./fy27-landscape.png
```

### Recipe 3: Build vs Buy vs Partner gameplay overlay

```markdown
| Component | Wardley position | Decision | Rationale |
|---|---|---|---|
| Agent orchestration | Custom Built | BUILD | Differentiation lives here. Don't rent. |
| LLM provider | Commodity | BUY/RENT | Anthropic + OpenAI. Don't try to host. |
| Vector store | Product | PARTNER | Pinecone / Weaviate; abstract behind interface so swappable. |
| Auth / billing | Commodity | BUY | Stripe + Clerk; build is dead time. |
| Founder workflow UI | Genesis | BUILD | The unique IP. |
```

### Recipe 4: Climate patterns to look for

```markdown
- **Punctuated equilibrium** — capability rapidly moves from product → commodity (e.g., LLM hosting 2024→2026). What's about to move?
- **Co-evolution** — practice changes as component evolves (DevOps was co-evolved with cloud commodity).
- **Red Queen** — running to stay in place. If competitors all use the same commodity, no advantage.
- **Inertia** — incumbent resistance to evolution. Mark with `inertia <component>` in the DSL.
```

### Recipe 5: Doctrine checklist (for the map)

```markdown
- [ ] Use a common language (Wardley map = the artifact)
- [ ] Challenge assumptions (no map is final; iterate weekly)
- [ ] Focus on user needs (anchor is the user)
- [ ] Use appropriate methods per evolution stage:
  - Genesis: experiment, agile, in-house
  - Custom: lean, in-house, build for differentiation
  - Product: 6-sigma, productize, partner
  - Commodity: outsource, rent utility, focus elsewhere
- [ ] Manage inertia (named, owned, with kill criteria)
```

### Recipe 6: Gameplays — pick 1-3 per map

```markdown
| Gameplay | When to use | Example |
|---|---|---|
| Open source | Commoditize a competitor's product | Open-source the orchestration layer to kill closed alternatives |
| Bundling | Combine commodities into product | Bundle auth + billing + workflow = "everything-platform" |
| Constraint | Create a bottleneck rivals can't bypass | Own the data pipeline; competitors must rent from you |
| Co-opting | Adopt rival's standard, extend | Adopt MCP, ship superior implementation |
| Tower + Moat | Build a high-walled position around a commodity | Wrap LLM with proprietary RAG/eval moat |
| Sensible-defaults | Set the standard others must match | Define the "agent profile" schema |
```

### Recipe 7: Quarterly map refresh

```bash
# Refresh the map at every QBR — what evolved?
mcp tool notion.update_page --page-id "<wardley-map-page>" \
  --append '## Q2 2027 update

What evolved since Q1:
- Vector store: Product → moving toward Commodity (Pinecone IPO triggered price war)
- Agent orchestration: Custom Built → moving toward Product (3 frameworks competing)

Implications:
- Vector store: shift from PARTNER to BUY (lower the cost basis)
- Agent orchestration: faster ship, productize before someone else does
'
```

### Recipe 8: Map a competitor

```
title Competitor X — what they see

anchor Their user [0.99, 0.5]
component Their workflow [0.90, 0.25]
component Their orchestration [0.65, 0.50]   # Note: more productized than ours
component LLM provider [0.30, 0.95]

inertia Their orchestration
```

Then overlay: where do they NOT see what we see? That gap is the asymmetric advantage.

### Recipe 9: M&A overlay — target capability fit

```markdown
For each capability in the target's value chain:
- Where is it on our map (Genesis / Custom / Product / Commodity)?
- BUILD: target adds differentiated tech we want → strong acquisition case.
- PRODUCT: target is one of many; partnership likely cheaper.
- COMMODITY: target is a utility; lease, don't acquire.
```

### Recipe 10: Save to Notion as a Wardley library

```bash
mcp tool notion.create_database \
  --parent '{"page_id":"<strategy-hub>"}' \
  --title '[{"text":{"content":"Wardley Maps"}}]' \
  --properties '{
    "Name":{"title":{}},
    "Period":{"select":{"options":[{"name":"FY27 Q1"},{"name":"FY27 Q2"}]}},
    "Type":{"select":{"options":[{"name":"Own landscape"},{"name":"Competitor"},{"name":"M&A target"}]}},
    "DSL":{"rich_text":{}},
    "Render URL":{"url":{}},
    "Last refresh":{"date":{}}
  }'
```

### Recipe 11: drawio cleaner render (optional)

```bash
mcp tool drawio.create_diagram \
  --template wardley \
  --components-file ./fy27-components.json \
  --output ./fy27-clean-render.drawio
```

drawio gives sharper export for board decks; OnlineWardleyMaps is faster for working sessions.

## Examples

### Example 1: Build vs buy decision for agent orchestration

**Goal:** Decide whether to build our own orchestration framework or adopt LangChain / LlamaIndex.

**Steps:**
1. Write the map (Recipe 1). Place "orchestration" component.
2. Question: where is orchestration in evolution? In 2027 it's transitioning Custom → Product (multiple competing frameworks).
3. Map our differentiation: orchestration *patterns* are commoditizing, but our *agent-profile abstraction* is Custom.
4. Decision: BUY the framework (LangChain), BUILD the patterns layer on top.
5. Document in M&A memo or strategy doc with Wardley screenshot.

**Result:** 2-week build avoided; 6-month patterns roadmap clear.

### Example 2: Pre-board Wardley refresh

**Goal:** Board asks "what's changed competitively?" 2 weeks before meeting.

**Steps:**
1. Pull last quarter's map from Notion (Recipe 10).
2. Run quarterly refresh (Recipe 7) — what evolved?
3. Add 1 competitor map (Recipe 8).
4. Surface 2-3 gameplays the company should consider next quarter.
5. Render and embed in board deck.

**Result:** Board sees a concrete picture of climate change + recommended moves.

## Edge cases / gotchas

- **Maps are subjective.** Two strategists will place components differently. That's fine — the conversation is the value, not the map.
- **Resist over-mapping.** A map with 50 components is unreadable. Cap at 10-15. Drill down per-capability if needed.
- **Anchor must be the user, not a metric.** "Revenue" or "NPS" as anchor = bad map. User needs anchor; revenue follows.
- **Inertia is named, not assumed.** Mark inertia explicitly; the act of naming it is half the value.
- **Don't confuse the map with the gameplay.** Map describes climate. Gameplay is what you do. Two separate artifacts.
- **Evolution stages are not equal-width.** Components spend long in Product before moving to Commodity. Don't move them prematurely.
- **OnlineWardleyMaps tool isn't private.** Don't paste sensitive competitor info into the public tool. Self-host the OSS for sensitive maps.
- **Quarterly refresh is the minimum.** Strategy doc + Wardley map decay together; refresh both at QBR.
- **Don't share the map without the doctrine.** A map without "what we're going to do about it" invites endless debate. Pair with gameplay.
- **Coordinate ranges aren't absolute.** OnlineWardleyMaps uses 0-1 on both axes; rough proportional placement is fine.

## Sources

- [OnlineWardleyMaps (free renderer)](https://onlinewardleymaps.com)
- [Build vs Buy in 2026 — Wardley + agentic AI](https://medium.com/@haberlah/build-vs-buy-in-2026-using-wardley-mapping-to-navigate-the-agentic-ai-shift-be24d534b054)
- [Simon Wardley — Learn Wardley Mapping (free book)](https://learnwardleymapping.com/)
- [Wardley Maps book by Simon Wardley](https://medium.com/wardleymaps)
- [OnlineWardleyMaps GitHub (OSS self-host)](https://github.com/damonsk/onlinewardleymaps)
