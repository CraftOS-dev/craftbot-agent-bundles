<!--
Sources:
NN/g — Personas — https://www.nngroup.com/articles/persona/
Indi Young — Thinking Styles — https://indiyoung.com/portfolio/thinking-styles
Alan Cooper — goal-directed personas
Dovetail v3 API — https://dovetail.com/help/api
-->
# Persona Authoring (Dovetail-Grounded) — SKILL

Behavioral personas built from research, not imagination. Backed by Dovetail tag counts ("8 of 11 mentioned trait X"). Goal-directed (Alan Cooper) or thinking-style (Indi Young) — never demographic-only. Linked to source highlights so every claim is traceable.

## When to use

- Authoring a new persona from completed JTBD or generative interviews.
- Refreshing an existing persona with new tag counts after a fresh round.
- Validating that a "persona" is actually grounded in data, not opinion.
- Building persona library for team training / democratization.

Trigger phrases: "build a persona for X", "create solo-founder persona", "is this persona evidence-based", "audit existing personas", "refresh persona from latest research".

## Setup

```bash
# Dovetail (raw evidence)
curl -fsSL "https://dovetail.com/api/v1/me" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN"

# Notion (canonical persona page)
curl -fsSL "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28"
```

## Common recipes

### Recipe 1: Behavioral persona template

```markdown
# Persona: [Name]

**Segment:** [Solo founder, B2B SaaS, $50-200K ARR]
**Research grounding:** N=[count] interviews + [analytics signal] + [support pattern]
**Last updated:** [YYYY-MM-DD] · **Owner:** [Researcher name]

## Behaviors (tag-grounded)
- **[Behavior 1]** — mentioned by X of Y participants
  - Verbatim: "..." — P3 @ 12:30 (Dovetail link)
- **[Behavior 2]** — X of Y
  - Verbatim: "..." — P7

## Goals (JTBD outcome statements)
- "[direction] the [unit] of [object] when [context]"
- "[outcome 2]"

## Pain points
- **[Pain 1]** — X of Y participants
  - Verbatim: "..." — P11 (Dovetail link)
- **[Pain 2]** — X of Y

## Anxieties + habits (JTBD forces)
- **Anxiety:** [from "what almost stopped you" interview probes]
- **Habit:** [current way of doing the job — inertia source]

## Day in the life (behavioral, not aspirational)
[1 paragraph anchored to specific interview moments — not invented]

## Tool stack (current — from research)
- [Tool A] (used by X of Y)
- [Tool B] (used by X of Y)

## Demographic context (not gating — context only)
- Role: [from screener]
- Team size: [from screener]
- Years experience: [from screener]
- Location: [from screener]

## Sources
- Interview transcripts: [Dovetail tag query link]
- Behavioral signal: [PostHog/Mixpanel cohort link]
- Support patterns: [Intercom/Zendesk view link]
- Funnel data: [link]

## Antipatterns to avoid for this persona
- Don't [marketing copy / feature framing] — fails [common assumption]
- Do [opposite]
```

### Recipe 2: Pull tag counts from Dovetail

```bash
# Get count of participants who mentioned a specific theme
curl -fsSL "https://dovetail.com/api/v1/projects/$PROJECT_ID/highlights?tag=inbox-overload" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN" \
| jq '{
    mention_count: (.highlights | map(.participant_id) | unique | length),
    total_participants: 12,
    fraction: ((.highlights | map(.participant_id) | unique | length) / 12),
    top_quotes: [.highlights[:3] | .[] | {participant_id, quote, timestamp}]
  }'
```

### Recipe 3: Behavioral grounding script (Python)

```python
import requests

def persona_grounding(dovetail_project_id, tag, total_participants, token):
    """Compute mention fraction + pull top 3 verbatims for a behavioral trait."""
    r = requests.get(
        f"https://dovetail.com/api/v1/projects/{dovetail_project_id}/highlights",
        params={"tag": tag},
        headers={"Authorization": f"Bearer {token}"}
    )
    highlights = r.json()["highlights"]
    participants_who_mentioned = {h["participant_id"] for h in highlights}
    return {
        "trait": tag,
        "mention_count": len(participants_who_mentioned),
        "fraction": f"{len(participants_who_mentioned)}/{total_participants}",
        "verbatims": [
            {
                "p_id": h["participant_id"],
                "quote": h["quote"],
                "timestamp": h["timestamp"],
                "dovetail_url": f"https://dovetail.com/projects/{dovetail_project_id}/highlights/{h['id']}"
            }
            for h in highlights[:3]
        ]
    }

# Use in persona doc — fraction + 1-3 verbatims per trait
```

### Recipe 4: Goal-directed vs thinking-style choice

| Persona type | When to use | Author |
|---|---|---|
| **Goal-directed** (Cooper) | Product is task-oriented; goals are clear | Alan Cooper |
| **Thinking-style** (Indi Young) | Behaviors vary by mental model; demographics don't predict | Indi Young |
| **Role-based** (NN/g hybrid) | B2B with clear functional roles | NN/g |
| **JTBD job-based** | Job is the unit of analysis, not user | Christensen / Moesta |

For most product work, **goal-directed + JTBD overlay** = behavior-led with measurable outcomes.

### Recipe 5: Push persona to Notion

```bash
PERSONA_DB="<personas-db-id>"

curl -X POST "https://api.notion.com/v1/pages" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28" \
  -d "{
    \"parent\": {\"database_id\": \"$PERSONA_DB\"},
    \"properties\": {
      \"Name\": {\"title\": [{\"text\": {\"content\": \"Solo Founder Sarah\"}}]},
      \"Segment\": {\"rich_text\": [{\"text\": {\"content\": \"B2B SaaS solo founder, \$50-200K ARR\"}}]},
      \"N\": {\"number\": 12},
      \"Dovetail project\": {\"url\": \"https://dovetail.com/projects/abc123\"}
    }
  }"
```

### Recipe 6: Persona audit — is it grounded?

```python
def audit_persona(persona_md):
    """Flag any persona claim without source link."""
    flags = []
    lines = persona_md.split("\n")
    for line in lines:
        # Behavior / pain / goal claim
        if any(p in line for p in ["mentioned", "of Y", "of 11", "of 12", "of 15"]):
            # Must include source link in next 2 lines
            if "(Dovetail" not in line and "[link]" not in line:
                flags.append({"line": line, "flag": "claim without source"})
        # Demographic-only claim (NN/g antipattern)
        demographic_terms = ["32-year-old", "loves coffee", "busy mom", "tech-savvy"]
        if any(t in line.lower() for t in demographic_terms):
            flags.append({"line": line, "flag": "demographic-only claim"})
    return flags
```

### Recipe 7: Refresh persona with new research

```markdown
# Persona refresh checklist

After each new round of interviews:
- [ ] Pull new tag counts (Recipe 2 + 3)
- [ ] Update "mention count" fractions per behavior + pain
- [ ] Add new verbatims (replace if older >12 months)
- [ ] Recompute "day in the life" if changed
- [ ] Update tool stack list (new tools added; tools deprecated)
- [ ] Bump "Last updated" date
- [ ] Note in changelog what shifted

# Changelog appendix
## 2026-06-10
- Added behavior "uses AI summarization daily" (8 of 12 in Q2 round)
- Removed "tracks Twitter mentions" (no Q2 mentions)
- Refreshed pain "inbox overload" verbatims
```

### Recipe 8: Avoid antipatterns (NN/g)

| Antipattern | Why bad | Fix |
|---|---|---|
| Demographic-only | "32yo, female, tech-savvy" = no behavior; useless | Add behavioral grounding |
| Aspirational | "loves productivity tools" projects researcher hope | Replace with observed behavior |
| Invented quotes | "Users would say..." | Every quote = real participant + timestamp |
| Persona without source | No traceability → becomes opinion | Link to Dovetail tag query |
| Too many personas | >5 = no one remembers; teams ignore | Cap at 3 primary, 1-2 secondary |
| Stale personas | Last updated >12 months ago | Quarterly refresh cadence |
| Stock-photo persona | Generic stock image → seen as marketing fiction | Skip the photo or use real-feel avatar |

### Recipe 9: Persona handoff to PM / designer

```markdown
# Persona kickoff (30 min with team)

## Agenda
1. Read the persona aloud (designer reads). (5 min)
2. Q&A: "What surprised you?" / "What do you disagree with?" (10 min)
3. Walk through 3-5 Dovetail verbatim highlights live. (10 min)
4. "How would this persona's day change if we shipped [feature]?" — invite team into the persona. (5 min)

## Output
- Team can quote 3+ behaviors from memory
- Team disagreement is recorded → research backlog
```

### Recipe 10: Cross-link persona ↔ journey ↔ JTBD

```markdown
# Persona cross-link block (in Notion)

## Related artifacts
- **JTBD outcomes for this persona:**
  - "minimize the time it takes to [outcome]" → see `jtbd-interview-script-execution` study
- **Customer journey map:**
  - [Solo Founder Sarah × Onboarding] journey → see `customer-journey-service-blueprint` artifact
- **Opportunity solution tree:**
  - Outcome → opportunities → see `opportunity-solution-tree-jtbd-outcomes`
- **Dovetail project:**
  - All raw evidence: [Dovetail link]
```

## Examples

### Example 1: Author "Solo Founder Sarah" from 12 JTBD interviews
**Goal:** Build a persona grounded in Q3 generative research.

**Steps:**
1. Tag all 12 interviews in Dovetail with behavior + pain + outcome tags (see `dovetail-research-repository`).
2. Pull tag counts (Recipe 2-3) per behavior + pain.
3. Fill persona template (Recipe 1) with fractions + verbatims.
4. Audit for groundedness (Recipe 6).
5. Push to Notion (Recipe 5).
6. Cross-link to journey + JTBD outcomes (Recipe 10).
7. Team kickoff (Recipe 9).

**Result:** Defensible persona; every claim traceable.

### Example 2: Audit an existing persona for groundedness
**Goal:** Decide whether to refresh or retire "Power User Pete."

**Steps:**
1. Run audit script (Recipe 6) on Pete's Notion page.
2. Find: 4 claims without sources; 2 demographic-only blocks.
3. Pull Dovetail data — Pete's segment hasn't been interviewed in 18 months.
4. Decision: retire Pete; recruit fresh round before reauthoring.

**Result:** Better to retire a stale persona than spread bad data.

## Edge cases / gotchas

- **Demographic without behavior.** "32, female, tech-savvy" tells you nothing. Skip or add behavior.
- **Invented quotes.** Never. Every quote = real participant + timestamp.
- **One participant claim treated as theme.** Need ≥3 of N for behavioral trait.
- **Aspirational language.** "She loves productivity tools" projects hope. Observed behavior only.
- **>5 personas in library.** Teams ignore. Cap at 3 primary, 1-2 secondary.
- **Stale (>12 months without refresh).** Mark deprecated; recruit fresh.
- **No source links.** Becomes opinion in 3 months. Always link to Dovetail.
- **Persona built from sales calls only.** Sales calls = buyer signal, not user. Validate with user research.
- **Persona built from analytics only.** Quant tells you what, not why. Pair with qual.
- **Stock-photo distraction.** Decorative photo + name = treated as marketing. Use simple text-led design.
- **Persona without owner.** Maintained by no one = stale fast. Always assign a researcher.

## Sources

- [NN/g — Personas: Study Guide](https://www.nngroup.com/articles/persona/)
- [Alan Cooper — Goal-Directed Personas](https://www.alistapart.com/article/personas-make-users-memorable-for-product-team-members)
- [Indi Young — Thinking Styles](https://indiyoung.com/portfolio/thinking-styles)
- [Dovetail v3 API](https://dovetail.com/help/api)
- [Notion API — databases](https://developers.notion.com/reference/database)
- [Daniel Pidcock — Atomic UX Research](https://www.atomicresearch.co)
- [NN/g — When to Use Which Type of Persona](https://www.nngroup.com/articles/persona-stylistic-content-personas/)
