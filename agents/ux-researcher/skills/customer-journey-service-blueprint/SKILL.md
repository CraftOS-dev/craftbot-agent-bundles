<!--
Sources:
NN/g — Customer Journey Mapping — https://www.nngroup.com/articles/customer-journey-mapping/
NN/g — Service Blueprints — https://www.nngroup.com/articles/service-blueprints-definition/
Holtzblatt + Beyer — Contextual Design
-->
# Customer Journey + Service Blueprint — SKILL

Map the user journey (persona × phase × actions × thoughts × emotions × opportunities) grounded in research, not imagination. Service blueprint adds backstage actors + systems + support processes. Output: Excalidraw visual + Notion narrative with evidence links per cell.

## When to use

- Mapping the user's end-to-end experience across phases for a feature or product.
- Visualizing emotional curve to find opportunity zones.
- Showing backstage operations + systems behind frontstage UX.
- Cross-functional alignment (design + PM + engineering + support + sales).
- Pre-PRD opportunity scoping.

Trigger phrases: "journey map", "service blueprint", "map the customer journey", "experience map for X", "where do users drop off across phases".

## Setup

```bash
# Notion (narrative + evidence links)
curl -fsSL "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28"

# Excalidraw via excalidraw-diagram-generator skill (visual)

# Session replay APIs for backstage friction proof
# FullStory: https://api.fullstory.com/sessions/v1
# Hotjar: https://api.hotjar.com/v1
# Clarity (free, dashboard export)
```

Auth: see role.md SOTA tool reference.

## Common recipes

### Recipe 1: Journey map structure (NN/g)

```markdown
# Journey Map: [Persona] × [Scenario]

**Persona:** [Solo founder, B2B SaaS, $50-200K ARR]
**Scenario:** [First-week onboarding to active use]
**Researcher:** [Name] · **Date:** [YYYY-MM-DD]

## Phases (high-level stages)
1. Discover
2. Try (signup → first session)
3. Configure (week 1)
4. Use (week 2-4)
5. Expand (month 2+)

## Per-phase grid

| Phase | Actions (what they do) | Thoughts (what they think) | Emotions (😀😐😟) | Touchpoints | Opportunities |
|---|---|---|---|---|---|
| Discover | Googles "best CRM for solo founder" | "Will this really fit me?" | 😟 | Search, blog, comparison sites | Better comparison content |
| Try | Signs up; sees onboarding | "OK what now?" | 😐 | Signup page, welcome email | Reduce time-to-first-value |
| Configure | Imports contacts; sets up team | "Where's the team page?" | 😟 (frustration) | Settings, team page | Surface team setup earlier |
| Use | Logs daily; checks pipeline | "I get value when I see deal flow." | 😀 | Dashboard, deal view | Stage-aware nudges |
| Expand | Invites teammate; pays for pro | "This is now indispensable." | 😀 | Upgrade flow | Pricing transparency |
```

### Recipe 2: Service blueprint adds backstage

```markdown
# Service Blueprint: [Scenario]

## Layered model (left-to-right = phases; top-to-bottom = layers)

| Layer | Discover | Try | Configure | Use | Expand |
|---|---|---|---|---|---|
| **Customer actions** | Google search | Signup | Import CSV | Daily check | Invite teammate |
| **Frontstage (UI / agent)** | Landing page | Onboarding wizard | Settings UI | Dashboard | Upgrade modal |
| **Backstage (employees)** | Marketing content team | Support team standby | Data engineer for imports | Customer success | Sales for paid |
| **Support processes** | CMS, SEO ops | Signup pipeline | CSV parsing service | Analytics, alerts | Billing system |
| **Evidence (artifacts)** | Blog post, ad | Welcome email | Import confirmation | Notification | Receipt, plan email |
```

### Recipe 3: Ground every cell in research

```markdown
# Evidence linking rules

## Rule
Every "thought" or "emotion" cell links to a verbatim, analytics signal, or session replay clip.

## Bad (researcher imagination)
Action: "User signs up" → Thought: "I want to get started" → Emotion: 😀

## Good (research-grounded)
Action: "User signs up"
Thought: "I want to get started quickly without entering credit card." — Source: P3 @ 4:30, P7 @ 2:15 (Dovetail link)
Emotion: 😐 — neutral until first value
Evidence: 23% drop-off at signup→activation funnel (PostHog cohort link)
```

### Recipe 4: Build the journey map in Excalidraw

```python
# Pseudo — generate Excalidraw scene JSON
def build_journey_excalidraw(phases, persona):
    scene = {"type": "excalidraw", "elements": []}

    # Row 1: Phase headers
    for i, phase in enumerate(phases):
        scene["elements"].append({
            "type": "text",
            "text": phase["name"],
            "x": i * 300, "y": 0,
            "fontSize": 20
        })

    # Row 2-6: per-row Actions / Thoughts / Emotions / Touchpoints / Opportunities
    rows = ["Actions", "Thoughts", "Emotions", "Touchpoints", "Opportunities"]
    for row_idx, row_label in enumerate(rows):
        y = 80 + row_idx * 120
        for i, phase in enumerate(phases):
            scene["elements"].append({
                "type": "rectangle", "x": i * 300, "y": y, "width": 280, "height": 100
            })
            scene["elements"].append({
                "type": "text", "text": phase.get(row_label.lower(), ""),
                "x": i * 300 + 10, "y": y + 10, "fontSize": 12
            })

    return scene

# Then use excalidraw-diagram-generator skill to render
```

### Recipe 5: Emotional curve overlay

```python
# Score emotion per phase (-2 to +2); plot as line
def emotional_curve(journey):
    emotions = []
    for phase in journey["phases"]:
        emo = phase["emotion_score"]  # -2=😡, -1=😟, 0=😐, +1=🙂, +2=😀
        emotions.append({"phase": phase["name"], "score": emo})
    # Lowest score = opportunity zone
    lowest = min(emotions, key=lambda e: e["score"])
    return emotions, lowest

# Mark opportunity zones at dips
```

### Recipe 6: Find opportunity zones

```python
def opportunity_zones(journey):
    """
    Opportunity zones live where:
    1. Emotion dips (😟 or worse)
    2. Drop-off in analytics funnel
    3. Spike in support tickets
    """
    zones = []
    for phase in journey["phases"]:
        if phase["emotion_score"] <= -1:
            zones.append({"phase": phase["name"], "reason": "emotion dip"})
        if phase["funnel_drop_pct"] >= 0.15:
            zones.append({"phase": phase["name"], "reason": "funnel drop"})
        if phase["support_ticket_count"] >= 10:
            zones.append({"phase": phase["name"], "reason": "support volume"})
    return zones
```

### Recipe 7: Notion narrative template

```markdown
# Journey Map: [Persona] × [Scenario]

**Date:** [YYYY-MM-DD] · **Researcher:** [Name]
**Excalidraw:** [link]

## Persona summary
[2-3 sentences — link to persona doc]

## Scenario
[What the user is trying to accomplish + when]

## Phases at a glance
[Excalidraw embed or screenshot]

## Per-phase narrative

### Phase 1: Discover
**Actions:** [verbatim from interviews / behavior signal]
**Thoughts:** "[quote]" — P3 (Dovetail link)
**Emotions:** 😟 — anxious about fit
**Touchpoints:** [list]
**Opportunities:**
- [Opportunity 1 — evidence + recommendation]

### Phase 2: Try
... [repeat per phase]

## Opportunity zones (prioritized)
1. **[Phase / theme]** — evidence + recommendation + owner
2. ...

## Sources
- Research: [Dovetail project link]
- Funnel data: [PostHog/Mixpanel link]
- Support tickets: [Intercom/Zendesk filter]
- Session replays: [FullStory/Hotjar/Clarity link]
```

### Recipe 8: Pull session replay evidence

```bash
# FullStory — sessions for a friction phase
curl -X POST "https://api.fullstory.com/sessions/v1/search" \
  -H "Authorization: Bearer $FULLSTORY_API_KEY" \
  -d '{
    "filters": [
      {"path": "events.event_type", "op": "eq", "value": "rage_click"},
      {"path": "user.url", "op": "contains", "value": "/onboarding"}
    ],
    "limit": 10
  }'
```

### Recipe 9: Cross-functional kickoff agenda

```markdown
# Journey map kickoff (60-min, design + PM + eng + CS)

## Pre-read (sent 24h before)
- Persona doc
- Research summary (5 bullets)
- Funnel data snapshot

## Agenda
1. **Frame (5 min)** — what decision this informs
2. **Phases (10 min)** — agree on phases (or override researcher draft)
3. **Per-phase walkthrough (40 min)** — review evidence; debate emotion scores
4. **Opportunity zones (5 min)** — vote top 3

## Output
- Updated journey map (Excalidraw)
- Top 3 opportunity backlog → `opportunity-solution-tree-jtbd-outcomes` for Linear handoff
```

### Recipe 10: Maintain journey map as living artifact

```markdown
# Journey map maintenance cadence

- **Monthly** — check funnel data for shifts; update emotion scores if drift
- **Per major release** — re-validate affected phases (one-round usability)
- **Quarterly** — re-recruit fresh interviews; refresh verbatim evidence
- **Tag in Dovetail** — `journey-evidence` tag on quotes that ground journey map
```

## Examples

### Example 1: Onboarding journey map for solo founders
**Goal:** Find the biggest opportunity in week-1 onboarding.

**Steps:**
1. Pull research: 12 JTBD interviews + funnel from PostHog + 30 days support tickets.
2. Define 5 phases (Recipe 1).
3. Grid per-phase with evidence (Recipe 3).
4. Build Excalidraw + Notion (Recipes 4, 7).
5. Find opportunity zones (Recipe 6) — biggest dip at Configure (😟, 30% funnel drop, team-setup tickets).
6. Cross-functional kickoff (Recipe 9).
7. Top opportunity → `opportunity-solution-tree-jtbd-outcomes`.

**Result:** Evidence-grounded journey map → 1 prioritized opportunity per phase.

### Example 2: Service blueprint for refund flow
**Goal:** Map the refund experience including backstage.

**Steps:**
1. Pull: 5 refund interviews + Zendesk tickets + finance team interview.
2. Build full 5-layer blueprint (Recipe 2).
3. Identify slow backstage step (Recipe 6) — 3-day finance review.
4. Recommend: auto-approve refunds <$100, surface in product.

**Result:** Frontstage + backstage opportunity backlog.

## Edge cases / gotchas

- **Imagined journeys.** "I think users feel..." is researcher projection. Every cell needs evidence.
- **Too many phases.** >7 phases = unreadable. Cluster into 3-5.
- **No emotional curve.** Skipping emotion = no opportunity zones surface.
- **Persona-less journey.** Same scenario, different personas = different journeys. Always tie to persona.
- **One-shot artifact.** Journey map without maintenance becomes folklore in 6 months. Schedule refresh.
- **No frontstage/backstage in service blueprint.** That's just a journey map. Blueprint requires backstage layer.
- **No PM in kickoff.** PM not in room = no decision authority on opportunities.
- **Touchpoints as departments.** "Marketing" is not a touchpoint. The specific blog post, ad, email is.
- **Opportunities without owner.** Opportunity backlog without owners stalls.
- **Wishlist scope creep.** Limit opportunities to top 3 per journey.
- **Sentimental painting.** Cute icons + decorative artwork distracts from evidence. Keep tidy.

## Sources

- [NN/g — Customer Journey Mapping 101](https://www.nngroup.com/articles/customer-journey-mapping/)
- [NN/g — Service Blueprints: Definition](https://www.nngroup.com/articles/service-blueprints-definition/)
- [NN/g — When to Use Customer Journey Maps](https://www.nngroup.com/articles/journey-mapping-101/)
- [Adaptive Path — Anatomy of an Experience Map](https://adaptivepath.org/ideas/the-anatomy-of-an-experience-map/)
- [Excalidraw](https://excalidraw.com/)
- [FullStory Server API](https://developer.fullstory.com/server/v1)
- [PostHog API](https://posthog.com/docs/api)
