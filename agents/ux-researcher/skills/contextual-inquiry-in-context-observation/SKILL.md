<!--
Sources:
Holtzblatt + Beyer — Contextual Design
NN/g — Field Studies — https://www.nngroup.com/articles/field-studies-done-right/
NN/g — Contextual Inquiry — https://www.nngroup.com/articles/contextual-inquiry/
Interaction Design Foundation — https://www.interaction-design.org/literature/topics/contextual-inquiry
-->
# Contextual Inquiry — In-Context Observation — SKILL

Be where the work happens. Holtzblatt + Beyer 4 principles: context, partnership, interpretation, focus. 2-3 hours per visit, 12-15 participants for saturation. Output: thick-description field notes + 5 work models (flow, sequence, artifact, cultural, physical) + cluster diagrams.

## When to use

- Discovering what users actually do (vs what they say in interviews).
- Identifying workarounds + invisible work that surveys miss.
- Mapping cross-tool workflows (the spaces between apps).
- Pre-PRD generative when the context is unfamiliar to the team.
- B2B research where the desk-side work matters.

Trigger phrases: "contextual inquiry", "go on-site at X", "observe usage", "field study", "shadow users", "Holtzblatt", "work models".

## Setup

```bash
# Notion (field guide + work models)
curl -fsSL "https://api.notion.com/v1/users/me" \
  -H "Authorization: Bearer $NOTION_API_KEY" -H "Notion-Version: 2022-06-28"

# Otter (transcribe visit if recorded)
curl -fsSL "https://otter.ai/api/v1/me" \
  -H "Authorization: Bearer $OTTER_API_KEY"

# OCR for artifact capture (sticky notes, receipts, paper forms)
# openai-ocr-mcp or mistral-ocr-mcp

# Dovetail (synthesis)
curl -fsSL "https://dovetail.com/api/v1/me" \
  -H "Authorization: Bearer $DOVETAIL_API_TOKEN"
```

## Common recipes

### Recipe 1: The 4 Holtzblatt principles

```markdown
# Holtzblatt + Beyer — 4 principles

## 1. Context — be there when work happens
- Not a conference room demo
- Real desk, real tools, real interruptions
- 2-3 hours minimum to see arc

## 2. Partnership — master-apprentice, not interrogator
- "I'm learning from you; show me how you do it"
- Sit beside, not across
- Avoid judging or correcting

## 3. Interpretation — talk back what you see
- "It looks like you keep that spreadsheet open all day. Is that right?"
- Confirm + correct as you go
- Builds shared understanding

## 4. Focus — start with a question, follow what's interesting
- Pre-prepared focus area (e.g., "morning routine for inbox")
- But follow when something surprises you
- Flag emergent themes for next visit
```

### Recipe 2: Pre-visit prep checklist

```markdown
# Pre-visit checklist (1 day before)

## Logistics
- [ ] Visit time confirmed; calendar invite to participant
- [ ] Travel + parking + building access sorted
- [ ] Honorarium / gift logistics

## Materials
- [ ] Notebook + pen (or laptop with note template)
- [ ] Camera / phone (with permission to photo artifacts)
- [ ] Recording device + Otter setup (if recording)
- [ ] Consent form (in their language)
- [ ] Focus questions (printed, 5-7 max)

## Mental prep
- [ ] Apprentice mindset — they're the expert
- [ ] Read prior interviews / personas
- [ ] Set the 4 principles intention
```

### Recipe 3: Visit protocol (2-3 hours)

```markdown
# Visit protocol

## Arrival (10 min)
- Introduce yourself + research framing
- Walk through the consent form
- "I'd like to follow your real work. When you need to focus, pretend I'm not here. When something happens, just tell me what you're doing."

## Observation block 1 (45 min)
- Sit beside, not across
- Watch + take notes (verbatim, not interpretation)
- Note artifacts (screen, paper, post-its, phone)

## Interpretation pause (5 min)
- "Let me check my understanding. It looks like X is happening because Y. Is that right?"
- Adjust based on response

## Observation block 2 (45 min)
- Continue real work
- Flag new emerging questions

## Wrap-up interview (30 min)
- "Tell me about [thing I noticed]"
- "Walk me through the situations I didn't see today"
- "What's typical of this week vs other weeks?"
- "What didn't I see that I should have?"

## Close (10 min)
- Thank
- Hand over honorarium
- Photo of artifact library (with permission)
```

### Recipe 4: Field note template (verbatim, not interpreted)

```markdown
# Field notes — [Participant ID] — [Date]

**Site:** [Office / home / field]
**Duration:** [Start - End]
**Researcher:** [Name]

## Pre-visit context
- Role + responsibilities
- Tools they mentioned during recruit
- Focus area for this visit

## Observation log (timestamped)
- [09:02] Sits down, opens laptop. 7 apps already open (Slack, Gmail, Notion, CRM, Calendar, Spotify, Linear).
- [09:03] First action: clicks Slack DMs. Reads 4 threads in 2 minutes.
- [09:05] Switches to Gmail. Scans inbox. Reads 1 email; replies in 30 sec.
- [09:07] Picks up phone. Sends a text. Comments aloud: "Reminding Bob about the meeting."
- [09:08] Picks up paper notebook from left of laptop. Writes "follow up: invoice Q3" — but doesn't open the invoice tool.
- [09:10] Returns to Slack. ...

## Artifacts noted
- Paper notebook (left of laptop) — to-do list, also project notes
- Sticky notes on monitor — passwords (covered), bookmarks
- Phone (right of keyboard) — separate apps for personal stuff
- Slack always open + always notifying

## Verbatim quotes
- "I keep the paper notebook because Notion is for the team but I need a fast scratchpad."
- "I check Slack first because if Bob is up, he'll DM me by 9."

## Hypotheses / questions for next visit
- Pattern: paper notebook used for low-stakes; Notion for shareable
- Does the paper notebook fragment context across digital tools?
- Need: a notebook adjacent to the digital tool flow

## Workarounds observed
- Uses Slack DM for things that should be Linear tickets
- Switches between phone + laptop for context (calendar on phone, work on laptop)
```

### Recipe 5: The 5 work models (Holtzblatt + Beyer)

```markdown
# Work models — diagram after each visit (Excalidraw)

## 1. Flow model
- Who works with whom
- What info / artifact flows
- Communication channels

Example: Solo founder ↔ Cofounder (Slack DM) ↔ Outside accountant (email) ↔ Self (paper notebook)

## 2. Sequence model
- Order of steps in a task
- Triggers + intentions per step
- Branches + interruptions

Example: 9:00 AM inbox routine: open Slack → triage DMs → switch to Gmail → ... → write 1 task to paper

## 3. Artifact model
- Tools + documents created or used
- Their structure + purpose

Example: Paper notebook = today's tasks. Notion = team-shared notes. Spreadsheet = recurring tracking.

## 4. Cultural model
- Norms + influences + organizational forces
- "How we do things here"

Example: Slack DM expected response: <30 min. Email: <24 hr. Phone: emergency only.

## 5. Physical model
- Environment, layout, devices
- Interruptions, noise, focus space

Example: 1 monitor + laptop. Desk between window + Slack-notification-monitor. Phone always within reach.
```

### Recipe 6: Diagram the work models

```python
# Pseudo-code — generate Excalidraw scenes for each work model
def work_model_diagram(model_type, data):
    """
    model_type: 'flow' | 'sequence' | 'artifact' | 'cultural' | 'physical'
    data: from field notes
    """
    if model_type == "flow":
        # Boxes for actors; arrows for info flow
        return build_flow_excalidraw(data["actors"], data["flows"])
    elif model_type == "sequence":
        # Vertical timeline with steps + branches
        return build_sequence_excalidraw(data["steps"], data["timestamps"])
    elif model_type == "artifact":
        # Boxes for artifacts with annotations
        return build_artifact_excalidraw(data["artifacts"])
    elif model_type == "cultural":
        # Affinity-style diagram of cultural influences
        return build_cultural_excalidraw(data["norms"])
    elif model_type == "physical":
        # Layout sketch of environment
        return build_physical_excalidraw(data["environment"])
```

### Recipe 7: Cluster across participants (Affinity Diagram)

```markdown
# Affinity diagram — across 12-15 visits

## Procedure (4-6 hours, team of 3-5)
1. Each visit's field notes → sticky notes (1 observation per sticky)
2. Lay out all stickies on a wall (or FigJam / Miro)
3. Silently cluster — group stickies that feel related
4. Name each cluster (behavior-led labels)
5. Cluster the clusters (2nd-order themes)
6. Photograph + transcribe back to Notion

## Output
- 5-15 first-order clusters
- 3-5 second-order themes
- Top recommendations per theme
```

### Recipe 8: Sequence-model mining for opportunity

```python
def find_opportunities_in_sequence(sequence_models):
    """
    Look for:
    - Repeated workarounds across participants
    - High-friction step transitions
    - Steps where artifact-switching happens unnecessarily
    """
    opportunities = []
    workarounds = defaultdict(int)

    for model in sequence_models:
        for step in model["steps"]:
            if step.get("is_workaround"):
                workarounds[step["description"]] += 1
            if step.get("friction_score", 0) >= 3:
                opportunities.append({
                    "step": step,
                    "pid": model["participant_id"],
                    "reason": "high friction"
                })

    # Workarounds shared by ≥3 participants = strong opportunity
    strong_workarounds = {k: v for k, v in workarounds.items() if v >= 3}
    return opportunities, strong_workarounds
```

### Recipe 9: OCR artifacts for digital library

```bash
# Photograph paper artifacts + OCR
# Use openai-ocr-mcp or mistral-ocr-mcp

# Push photo, get text back
mcp tool openai-ocr.scan --image /path/to/sticky-note.jpg | jq -r '.text'
```

### Recipe 10: Contextual inquiry report template

```markdown
# Contextual Inquiry Report: [Study Name]

**Date:** [YYYY-MM-DD] · **N=[12] sites** · **Researcher:** [Name]
**Total hours observed:** [~30]

## TL;DR
- [Top 2-3 work patterns + opportunity]

## Method
- 12 in-context visits, 2-3 hours each
- Holtzblatt 4-principles
- 5 work models per visit
- Affinity cluster across all visits

## Cross-participant work models

### Flow model — common pattern
[Excalidraw diagram + narrative]

### Sequence model — morning routine
[Diagram + observation: 9 of 12 follow Slack → Gmail → 1 paper task pattern]

### Artifact model — the always-open tools
- [9 of 12] keep Slack always open
- [11 of 12] keep paper notebook within arm's reach for to-dos

### Cultural model
- "Slack reply <30 min" norm widespread; creates anxiety + interruption

### Physical model
- Monitor + laptop + phone + paper = 4-surface workspace

## Themes (from affinity cluster)

### Theme 1: [Name]
[Pattern + evidence count + verbatims + recommendation]

## Recommendations
1. [Opportunity — derived from sequence-model friction]
2. ...

## Sources
- Field notes: [Notion link]
- Photos / OCR artifacts: [link]
- Excalidraw work models: [link]
- Dovetail synthesis: [link]
```

## Examples

### Example 1: 8-site contextual inquiry on solo founder workflow
**Goal:** Discover invisible workarounds in founder daily routine.

**Steps:**
1. Recruit 8 founders + 6 cofounders via in-house network + User Interviews.
2. Pre-visit prep (Recipe 2).
3. 2-3 hr visits (Recipe 3).
4. Field notes verbatim (Recipe 4).
5. Diagram 5 work models per visit (Recipe 5-6).
6. Affinity cluster (Recipe 7).
7. Mine sequence models for opportunities (Recipe 8).
8. Report (Recipe 10).

**Result:** Pattern-grounded opportunity list with cross-tool workaround evidence.

### Example 2: Remote contextual inquiry via screen share
**Goal:** Watch users work without travel.

**Steps:**
1. Schedule 90-min Zoom screen share.
2. Same 4 principles, adapted: "Pretend I'm not here; just work."
3. Otter records + transcribes (Recipe in moderated skill).
4. Lower fidelity than on-site (no environment / physical model) but workable.

**Result:** Approximation when on-site not feasible.

## Edge cases / gotchas

- **Demo-mode bias.** Users perform "best version" when watched. Calibrate by sitting with them ≥30 min before serious observation.
- **Researcher-as-interrupter.** Constant questions break the work. Use interpretation pauses, not running commentary.
- **Note-taking that signals "got it."** Stop typing dramatically when something interesting happens → user stops; signal acknowledgment without breaking flow.
- **Skipping the wrap-up interview.** Wrap-up is where the *why* lives. Don't skip.
- **Interpreting in field notes.** Field notes = verbatim + observation. Interpretation goes in synthesis, not field notes.
- **Single visit per participant.** One day ≠ representative. Plan ≥2 visits or supplement with diary study.
- **No artifact photography permission.** Always ask; respect "no" on artifacts containing PII.
- **Skipping cultural model.** Behavior without culture = decontextualized; misses why.
- **Solo researcher.** Affinity cluster needs ≥3 people for diverse pattern surfacing.
- **Remote-only as "contextual."** Screen share misses physical + cultural model. Use as supplement, not replacement.
- **Confirming hypothesis instead of discovery.** Generative method — go in with focus area, not hypothesis to confirm.

## Sources

- [Hugh Beyer + Karen Holtzblatt — Contextual Design](https://www.amazon.com/Contextual-Design-Customer-Centered-Interactive-Technologies/dp/1558604111)
- [NN/g — Field Studies Done Right](https://www.nngroup.com/articles/field-studies-done-right/)
- [NN/g — Contextual Inquiry](https://www.nngroup.com/articles/contextual-inquiry/)
- [Interaction Design Foundation — Contextual Inquiry](https://www.interaction-design.org/literature/topics/contextual-inquiry)
- [Karen Holtzblatt — Contextual Design 2nd Edition](https://www.amazon.com/Contextual-Design-Second-Design-Centered/dp/0128008946)
- [Excalidraw](https://excalidraw.com/)
- [Dovetail v3 API](https://dovetail.com/help/api)
