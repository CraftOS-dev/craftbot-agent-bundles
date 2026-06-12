<!--
Sources:
Jeff Patton — https://www.jpattonassociates.com/the-new-backlog
Mountain Goat — https://www.mountaingoatsoftware.com/blog/the-advantages-of-user-story-mapping
-->
# User Story Mapping — SKILL

Jeff Patton's method: backbone (user journey activities) → epics (capabilities) → stories (chunks of work) → walking skeleton (MVP slice) → release slices. This pack outputs a story map as an Excalidraw diagram + bulk-creates the stories into Linear.

## When to use

- Translating a PRD into an executable backlog with structure.
- Identifying the walking skeleton (thinnest end-to-end slice) before scoping.
- Planning multi-release roadmaps where ordering matters.
- Cross-team scoping when work spans multiple capabilities.
- Stakeholder alignment on what's in MVP vs deferred.

Trigger phrases: "story map the feature", "what's the MVP slice", "break this PRD into stories", "what should ship first", "release plan".

## Setup

This skill orchestrates the `excalidraw-diagram-generator` (for the visual) + `linear-mcp` (for bulk story creation).

```bash
# Excalidraw — already in CraftBot defaults
mcp tool excalidraw.viewer

# Linear — see linear-product-management skill
mcp tool linear.viewer
```

## Common recipes

### Recipe 1: Story map structure (Patton)

```
Backbone (top row) — user journey activities, left-to-right
├── Activity 1: Sign up
├── Activity 2: Onboard
├── Activity 3: Take first action
├── Activity 4: Invite teammate
└── Activity 5: See result / value

Stories (vertical under each activity):
├── Activity 1: Sign up
│   ├── Story: Email + password signup form
│   ├── Story: SSO via Google
│   ├── Story: Email verification flow
│   └── Story: Marketing-consent toggle
├── Activity 2: Onboard
│   ├── Story: Step 1 welcome modal
│   ├── Story: Step 2 first-action prompt
│   ├── Story: Step 3 invite teammate prompt
│   └── Story: Skip onboarding option
...

Walking skeleton (horizontal slice through top story of each activity):
The thinnest end-to-end path that delivers value.

Release 1 = Walking skeleton (MVP)
Release 2 = Add depth to highest-friction activities
Release 3 = Add delight/excitement features
```

### Recipe 2: Generate story map as Excalidraw

```bash
# Generate an Excalidraw JSON that the agent can render or share
cat <<'EOF' > storymap.excalidraw.json
{
  "type": "excalidraw",
  "version": 2,
  "elements": [
    {"type":"rectangle","x":50,"y":50,"width":140,"height":60,"label":"Sign up","backgroundColor":"#a5d8ff"},
    {"type":"rectangle","x":210,"y":50,"width":140,"height":60,"label":"Onboard","backgroundColor":"#a5d8ff"},
    {"type":"rectangle","x":370,"y":50,"width":140,"height":60,"label":"First action","backgroundColor":"#a5d8ff"},
    {"type":"rectangle","x":530,"y":50,"width":140,"height":60,"label":"Invite","backgroundColor":"#a5d8ff"},
    {"type":"rectangle","x":690,"y":50,"width":140,"height":60,"label":"See value","backgroundColor":"#a5d8ff"},

    {"type":"rectangle","x":50,"y":130,"width":140,"height":40,"label":"Email signup","backgroundColor":"#fff3bf"},
    {"type":"rectangle","x":210,"y":130,"width":140,"height":40,"label":"Welcome modal","backgroundColor":"#fff3bf"},
    {"type":"rectangle","x":370,"y":130,"width":140,"height":40,"label":"Create workspace","backgroundColor":"#fff3bf"},
    {"type":"rectangle","x":530,"y":130,"width":140,"height":40,"label":"Invite email","backgroundColor":"#fff3bf"},
    {"type":"rectangle","x":690,"y":130,"width":140,"height":40,"label":"Dashboard","backgroundColor":"#fff3bf"},

    {"type":"line","x":40,"y":190,"width":800,"height":0,"strokeColor":"#fa5252","label":"Walking skeleton (Release 1)"}
  ]
}
EOF
```

### Recipe 3: Bulk-create stories in Linear from a map

```bash
# Map structure → Linear issues with parent-child via parentTitle
mcp tool linear.bulk_create_issues \
  --teamKey "PROD" \
  --projectId "<onboarding-revamp-project>" \
  --issues '[
    {"title":"Backbone: Sign up","labels":["story-map","backbone","activity"]},
    {"title":"Story: Email signup form","parentTitle":"Backbone: Sign up","estimate":2,"labels":["story-map","release-1"]},
    {"title":"Story: SSO via Google","parentTitle":"Backbone: Sign up","estimate":3,"labels":["story-map","release-2"]},
    {"title":"Story: Email verification","parentTitle":"Backbone: Sign up","estimate":2,"labels":["story-map","release-1"]},

    {"title":"Backbone: Onboard","labels":["story-map","backbone","activity"]},
    {"title":"Story: Welcome modal","parentTitle":"Backbone: Onboard","estimate":1,"labels":["story-map","release-1"]},
    {"title":"Story: First-action prompt","parentTitle":"Backbone: Onboard","estimate":3,"labels":["story-map","release-1"]},
    {"title":"Story: Personalized welcome","parentTitle":"Backbone: Onboard","estimate":5,"labels":["story-map","release-3"]},

    {"title":"Backbone: First action","labels":["story-map","backbone","activity"]},
    {"title":"Story: Create workspace","parentTitle":"Backbone: First action","estimate":2,"labels":["story-map","release-1"]},
    {"title":"Story: Workspace templates","parentTitle":"Backbone: First action","estimate":5,"labels":["story-map","release-2"]}
  ]'
```

### Recipe 4: Identify the walking skeleton

```python
def walking_skeleton(stories):
    """Pick the highest-priority story per activity for Release 1."""
    by_activity = {}
    for s in stories:
        a = s["activity"]
        if a not in by_activity or s["priority"] < by_activity[a]["priority"]:
            by_activity[a] = s
    return list(by_activity.values())

# Walking skeleton = thinnest end-to-end path. Aim for ≤8 stories total.
```

### Recipe 5: Release slice assignment

```bash
# Tag stories per release (Release 1 = walking skeleton; Release 2 = depth; Release 3 = delight)
mcp tool linear.list_issues \
  --filter '{"labels":{"name":{"eq":"story-map"}}}' \
  --first 50 \
| jq '.nodes[] | {id, title, labels: [.labels.nodes[].name]}'

# Promote a story to Release 1
mcp tool linear.update_issue \
  --id "<story-id>" \
  --labels '["story-map","release-1"]' \
  --priority 1
```

### Recipe 6: Cycle assignment from story map

```bash
# Once Release 1 is locked, assign all release-1 stories to upcoming cycles
RELEASE_1_IDS=$(mcp tool linear.list_issues \
  --filter '{"labels":{"name":{"eq":"release-1"}}}' \
  | jq -r '.nodes[].id')

# Sum estimates; if > 1 cycle of capacity, split into cycle 27 + cycle 28
echo "$RELEASE_1_IDS" | head -n 8 | while read id; do
  mcp tool linear.update_issue --id "$id" --cycleId "<cycle-27-id>"
done

echo "$RELEASE_1_IDS" | tail -n +9 | while read id; do
  mcp tool linear.update_issue --id "$id" --cycleId "<cycle-28-id>"
done
```

### Recipe 7: Map a PRD scope into stories (mechanical)

```python
# Per PRD acceptance criterion → one story
prd_acs = [
    {"activity":"Sign up", "ac":"Given a new user, when they submit the email signup form, then they receive a verification email"},
    {"activity":"Sign up", "ac":"Given SSO is enabled, when the user clicks Google, then they sign in via OAuth"},
    {"activity":"Onboard", "ac":"Given a new user, when they enter the dashboard, then a 3-step modal appears"},
]

for ac in prd_acs:
    # Each AC becomes a story under the corresponding backbone activity
    create_linear_issue(
        title=f"Story: {ac['ac'].split('then ')[1]}",
        parent_title=f"Backbone: {ac['activity']}",
        description=f"AC: {ac['ac']}"
    )
```

### Recipe 8: Story map for the discovery deck

```bash
# Export Excalidraw → PNG for pptx use in all-hands deck
# (Excalidraw skill can export; or use mermaid + excalidraw-diagram-generator)
mcp tool excalidraw.export \
  --input "storymap.excalidraw.json" \
  --format "png" \
  --output "storymap.png"
```

### Recipe 9: Vertical slice prioritization (Patton's "1st, 2nd, 3rd" labeling)

Per activity, label stories:
- **1st pass** — must work end-to-end for Release 1 to ship.
- **2nd pass** — adds depth; targeted for Release 2.
- **3rd pass** — delight; Release 3 or later.

```bash
mcp tool linear.update_issue \
  --id "<story-id>" \
  --customFields '[{"name":"Story map pass","value":"1st"}]'
```

### Recipe 10: Map maintenance — adding a late story

```bash
# A new story emerges mid-cycle — fit it into the map
# 1. Find the right backbone parent
PARENT_ID=$(mcp tool linear.list_issues \
  --filter '{"title":{"contains":"Backbone: Onboard"}}' \
  | jq -r '.nodes[0].id')

# 2. Create story with parent + appropriate release label
mcp tool linear.create_issue \
  --teamKey "PROD" \
  --title "Story: Add 'skip onboarding' option" \
  --parentId "$PARENT_ID" \
  --labels '["story-map","release-2"]' \
  --estimate 1
```

## Examples

### Example 1: From a 5-page PRD to a planned backlog
**Goal:** Translate the onboarding revamp PRD into a story map and a Release 1 cycle plan.

**Steps:**
1. Read the PRD's acceptance criteria (each maps to ≥1 story).
2. Group ACs by user-journey activity → backbone (Recipe 1).
3. Generate the Excalidraw visual (Recipe 2) — share with eng/design.
4. Identify the walking skeleton (Recipe 4) — 6-10 stories for Release 1.
5. Bulk-create in Linear with parent-child structure (Recipe 3).
6. Cycle-assign Release 1 stories (Recipe 6).
7. Label Release 2/3 stories as "next" / "later" — they appear in the Linear roadmap but aren't committed.

**Result:** A Linear backlog with story map structure + a 2-cycle Release 1 plan.

### Example 2: Stakeholder alignment workshop
**Goal:** Get exec + design + eng aligned on what ships in Release 1.

**Steps:**
1. Pre-workshop: draft the map (Recipe 2).
2. Live workshop (90 min): walk the backbone left-to-right; debate each story's release assignment.
3. Document decisions: each story has a release label (Recipe 9).
4. Post-workshop: update Linear (Recipe 5); export Excalidraw to PNG for the meeting notes.
5. Communicate the cut: "Here's what's in Release 1, here's what's deferred to Release 2, here's the rationale."

**Result:** No surprises mid-cycle; everyone signed off on the same map.

## Edge cases / gotchas

- **Map ≠ Gantt chart.** Story maps capture user journey + work breakdown, not dates. Don't conflate.
- **Backbone too granular.** If you have >12 activities, you've gone to story-level. Backbone is *activities* (verbs the user does); stories are *work* the team does.
- **Walking skeleton must be coherent.** A "minimum" Release 1 that omits sign-up isn't usable. The skeleton must deliver end-to-end value, however thin.
- **Don't over-map.** For features <5 stories, skip the map; just create Linear issues. Maps shine at feature → release scale.
- **Vertical slice over horizontal layer.** Don't ship "all sign-up stories in Release 1, all onboarding in Release 2" — that's a layer cake, not slices.
- **Parent-child in Linear vs map structure.** Linear sub-issues match the story-under-activity nesting. Keep parent issues for backbone, child for stories.
- **Estimate inflation.** Map view tempts "let's add another story." Use story-map labels to defer (Release 2/3), not just add.
- **Maps go stale.** Re-map quarterly if a roadmap shifts; outdated maps mislead.
- **Two PMs, two maps.** Cross-PM coordination requires a shared backbone — agree on the activities before independent mapping.
- **Excalidraw isn't versioned by default.** Save the JSON to git for history.

## Sources

- [Jeff Patton — User Story Mapping book](https://www.jpattonassociates.com/the-new-backlog)
- [Mountain Goat — Advantages of user story mapping](https://www.mountaingoatsoftware.com/blog/the-advantages-of-user-story-mapping)
- [Story Map Concepts (Patton)](https://www.jpattonassociates.com/wp-content/uploads/2015/03/story_mapping.pdf)
- [Atlassian Story Mapping guide](https://www.atlassian.com/agile/project-management/user-story-mapping)
- [Excalidraw docs](https://docs.excalidraw.com)
- [Linear bulk create](https://developers.linear.app/docs/sdk/issue-creation)
- [Marty Cagan on dual-track agile (discovery + delivery)](https://www.svpg.com/dual-track-agile)
