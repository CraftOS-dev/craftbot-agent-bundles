<!--
Sources:
W3C WAI — Involving Users with Disabilities — https://www.w3.org/WAI/test-evaluate/involving-users/
Fable Engineering — https://makeitfable.com
axe-core / Deque — https://www.deque.com/axe/devtools/
pa11y — https://pa11y.org
WCAG 2.2 — https://www.w3.org/TR/WCAG22/
-->
# Accessibility Research with Users with Disabilities — SKILL

Two-stage protocol: (1) automated WCAG 2.2 baseline with axe-core + pa11y catches ~30-40% of issues; (2) user research with participants with disabilities using their own assistive tech surfaces the rest — including lived-experience friction tools can't detect. Recruit via Fable (default), AccessWorks, or Knowbility.

## When to use

- Pre-launch accessibility audit on a new flow or feature.
- Quarterly compliance audit (WCAG 2.2 AA).
- Validating accessibility fixes from a previous round.
- Building inclusive research practice into ResearchOps.

Trigger phrases: "accessibility test", "WCAG audit", "screen reader test", "test with users with disabilities", "axe-core", "pa11y", "a11y research", "Fable recruit".

## Setup

```bash
# Fable (recruit users with disabilities)
curl -fsSL "https://api.makeitfable.com/v1/me" \
  -H "Authorization: Bearer $FABLE_API_KEY"

# axe-core CLI (automated)
npm install -g @axe-core/cli

# pa11y CLI (automated)
npm install -g pa11y
```

Auth + cost:
- `FABLE_API_KEY` — Account → API. Paid (per-session ~$100-200).
- axe-core + pa11y — free CLI tools.
- AccessWorks (alt) — case-by-case quote.
- Knowbility "Open Access Project" — community-driven, mission-fit projects.

## Common recipes

### Recipe 1: Automated baseline — axe-core

```bash
# Single page (CLI, all WCAG 2.2 AA rules)
npx @axe-core/cli https://app.example.com/onboarding \
  --tags wcag2a,wcag2aa,wcag22aa \
  --save axe-onboarding.json

# Multi-page via list
cat > pages.txt <<EOF
https://app.example.com/
https://app.example.com/onboarding
https://app.example.com/settings
EOF

while read URL; do
  npx @axe-core/cli "$URL" --tags wcag2a,wcag2aa,wcag22aa \
    --save "axe-$(echo $URL | md5sum | cut -d' ' -f1).json"
done < pages.txt
```

### Recipe 2: Automated baseline — pa11y

```bash
# pa11y (alt scanner, complementary to axe)
npx pa11y --standard WCAG2AA --reporter json https://app.example.com/onboarding \
  > pa11y-onboarding.json

# Multi-page sitemap mode
npx pa11y-ci --sitemap https://app.example.com/sitemap.xml \
  --standard WCAG2AA --threshold 5
```

### Recipe 3: WCAG 2.2 quick reference (high-frequency criteria)

| Criterion | Test | Level |
|---|---|---|
| 1.3.1 Info & Relationships | Semantic structure: headings, landmarks, form labels | A |
| 1.4.3 Contrast (Minimum) | Text 4.5:1, large text 3:1 | AA |
| 1.4.10 Reflow | Reflows at 320px viewport (no horizontal scroll) | AA |
| 2.1.1 Keyboard | Every operation reachable via keyboard | A |
| 2.4.7 Focus Visible | Keyboard focus indicator | AA |
| 2.5.8 Target Size (Minimum) | Touch targets ≥24×24 px | AA (new in 2.2) |
| 3.3.7 Redundant Entry | Don't re-ask info user already provided | A (new in 2.2) |
| 3.3.8 Accessible Authentication (Min) | No cognitive function test for login | AA (new in 2.2) |
| 4.1.2 Name, Role, Value | All controls programmatically determinable | A |
| 4.1.3 Status Messages | Status messages programmatically announced | AA |

### Recipe 4: Fable — recruit participants with disabilities

```bash
curl -X POST "https://api.makeitfable.com/v1/projects" \
  -H "Authorization: Bearer $FABLE_API_KEY" \
  -d '{
    "title": "Onboarding flow accessibility study",
    "session_type": "moderated_remote",
    "duration_minutes": 60,
    "honorarium_amount": 150,
    "target_count": 8,
    "assistive_tech_filter": [
      {"category": "screen_reader", "tools": ["VoiceOver", "JAWS", "NVDA"]},
      {"category": "magnifier", "tools": ["ZoomText", "macOS Zoom"]},
      {"category": "switch_control"},
      {"category": "voice_control", "tools": ["Dragon", "Voice Control"]}
    ],
    "disability_categories": ["vision", "motor", "cognitive"]
  }'
```

### Recipe 5: Pre-session participant brief

```markdown
# Pre-session brief — sent 48h before

**Subject:** Your accessibility research session — Wednesday 2pm

Hi [Name],

Looking forward to talking with you Wednesday at 2pm Pacific.

## What we'll do
- 60-minute Zoom session
- I'll ask you to complete 3 tasks in our product
- Please use your normal assistive tech setup — your screen reader, your settings, your usual device
- Think out loud as you work

## What you DON'T need
- Don't change your settings for the session
- Don't speed up your screen reader for our benefit
- Don't apologize for any friction — that's data for us

## Setup
- Zoom: [link]
- Recording: yes (internal only; deleted after 90 days)
- Honorarium: $150 paid via [payment method] within 48h

## Accessibility for this session
- I will turn on automatic captions in Zoom
- I will read tasks aloud + share them in chat
- Let me know if you need anything else (BSL/ASL interpreter, written-only, etc.)

Thanks,
[Researcher]
```

### Recipe 6: Session protocol — accessibility-specific

```markdown
# Session protocol

## Pre-session (5 min)
- Rapport — talk about their assistive tech setup; what they use day-to-day
- Frame: "We're testing the product, not your assistive tech. Your real-world setup is what we want to see."
- Confirm recording consent (re-confirm; participants with disabilities often have heightened privacy concerns)

## Tasks (5-10 min each, 3 tasks)
- Outcome-framed (same as moderated usability)
- "You want to [achieve outcome]. Walk me through how you'd do it with your normal setup."

## Probes
- "What was your assistive tech saying / showing right there?"
- "What did you expect to happen?"
- "Is this typical of what you encounter in other tools?"

## DON'T do
- ❌ Suggest a workaround ("try Tab instead")
- ❌ Drive the assistive tech ("can you turn off speech for a moment?")
- ❌ Compare to "how a sighted user would do it"

## Post-task
- SUS or UMUX-Lite (with screen-reader-friendly survey UI)
- Probe emotional friction: "How does this feel compared to other tools you use?"

## Debrief
- "Was anything especially frustrating today that you encounter regularly elsewhere?"
- "What would the perfect version of this product do?"
```

### Recipe 7: Combine automated + user findings

```python
# Cross-reference axe-core findings with lived friction
def cross_reference(axe_findings, user_friction_points):
    """
    axe_findings: list of {rule, impact, wcag_criterion, selector}
    user_friction_points: list of {participant_id, description, severity}
    """
    matched = []
    for friction in user_friction_points:
        for axe in axe_findings:
            if axe["wcag_criterion"] in friction.get("relates_to", []):
                matched.append({
                    "friction": friction["description"],
                    "axe_rule": axe["rule"],
                    "wcag": axe["wcag_criterion"],
                    "participant": friction["participant_id"],
                    "validates_axe": True
                })
    return matched

# Findings that user research flagged but axe didn't = the lived-experience gap
```

### Recipe 8: Accessibility report template

```markdown
# Accessibility Research Report: [Feature]

**Date:** [YYYY-MM-DD] · **Researcher:** [Name]
**Sample:** N=[8] participants across [screen reader / magnifier / motor / cognitive]

## TL;DR
- Automated baseline: [N] WCAG 2.2 issues across [criteria list]
- User research: [N] lived-experience friction points NOT caught by automated tools
- Top fixes: [3 prioritized items]

## Methodology
1. Automated baseline: axe-core + pa11y on [pages]
2. Moderated remote sessions: 60 min, participants' own AT, $150 honorarium
3. Synthesis: Dovetail tagging + WCAG criterion mapping

## Automated findings (axe-core + pa11y)
| Severity | Count | WCAG | Pages |
|---|---|---|---|
| Critical | 3 | 4.1.2, 2.1.1 | Onboarding step 2, Settings |
| Serious | 7 | 1.3.1, 2.4.7 | All pages |
| Moderate | 12 | 1.4.3, 3.3.2 | Forms |

## User-surfaced findings (NOT in automated)

### Finding 1: Screen reader users can't dismiss the modal
- **Affected AT:** JAWS, NVDA, VoiceOver
- **WCAG (related):** 2.1.2 No Keyboard Trap
- **What we observed:** Modal traps focus; ESC doesn't dismiss
- **Verbatim:** "There's no way out of this without refreshing the page." — P3 @ 14:22
- **Severity:** Critical (blocks task)
- **Fix:** Add ESC key dismiss + close button as first focusable

### Finding 2: ...

## Recommendations (prioritized by severity × frequency)
1. [Fix] — [WCAG] — [eng owner]
2. ...

## Sources
- Dovetail project: [link]
- axe reports: [link]
- pa11y reports: [link]
```

### Recipe 9: Continuous accessibility cadence

```markdown
# Quarterly accessibility cadence

## Sprint-level
- Per PR: run axe-core in CI (fail build on critical issues)
- Per release: pa11y CI run on changed pages

## Per-quarter
- Run accessibility user research (8 participants × 60 min)
- Refresh WCAG criterion coverage
- Triage findings into Linear (label: a11y)

## Per-year
- WCAG audit by external firm (Deque, Level Access)
- Public accessibility statement update
```

### Recipe 10: Don't-do antipatterns

```markdown
# Antipatterns in accessibility research

| Antipattern | Why bad |
|---|---|
| Researcher demos VoiceOver | Participants' real-world setups differ |
| Skipping recruitment fee differential | Participants with disabilities often face unemployment / underemployment; standard rate may not be fair |
| "Accessibility is a checkbox" framing | Decentralizes participants as data sources, not partners |
| axe-core pass = accessible | Tools catch 30-40%; lived experience is the gap |
| Recruiting only screen-reader users | Motor + cognitive + voice control matter equally |
| Asking participant to slow down screen reader | Their normal speed is the data |
| Volunteer-only ("we don't have budget") | Free labor of people with disabilities = exploitation. Pay above-standard |
| Single round + "we're accessible now" | Continuous practice required |
```

## Examples

### Example 1: Pre-launch a11y audit on checkout flow
**Goal:** Ensure new checkout is WCAG 2.2 AA + works for AT users.

**Steps:**
1. axe-core + pa11y baseline (Recipes 1-2) → 18 issues.
2. Fix critical issues from automated baseline.
3. Recruit 8 via Fable (Recipe 4) — 3 screen reader, 2 magnifier, 2 motor, 1 cognitive.
4. Run 60-min moderated remote (Recipe 6).
5. Cross-reference findings (Recipe 7) — 7 additional friction points NOT caught by axe.
6. Report (Recipe 8) → fix sprint.

**Result:** Confidence in WCAG + lived-experience launch readiness.

### Example 2: Quarterly cadence kickoff
**Goal:** Build sustainable a11y research practice.

**Steps:**
1. Define cadence (Recipe 9).
2. Build Linear "a11y" label + dashboard.
3. Train CI on axe-core (eng partnership).
4. Schedule quarterly user research in advance.

**Result:** A11y practice that doesn't depend on heroics.

## Edge cases / gotchas

- **Researcher driving the AT.** Always participants' own setup.
- **axe pass ≠ accessible.** Tools catch 30-40%; rest is lived experience.
- **Standard recruit rate.** Above-standard for participants with disabilities (we ship inclusive product = we pay inclusively).
- **One-AT category only.** Recruit across screen reader / magnifier / motor / cognitive / voice control.
- **Comparing to "sighted UX."** Not the goal; the goal is whether the experience works for them.
- **Asking to disable AT.** Never. Their AT is part of the system.
- **Recording without explicit consent.** Especially sensitive given privacy norms.
- **Volunteer recruit ("for community").** Exploitative. Pay.
- **English-only screener.** Some AT users with cognitive disabilities prefer plain language; some prefer BSL/ASL.
- **Captions off in Zoom.** Always on. Test before session.
- **Single critical issue blocks entire flow.** Flag as launch-blocker.
- **Mistaking VPAT for research.** VPAT is documentation; research is evidence.

## Sources

- [W3C WAI — Involving Users with Disabilities](https://www.w3.org/WAI/test-evaluate/involving-users/)
- [WCAG 2.2 — W3C](https://www.w3.org/TR/WCAG22/)
- [Fable Engineering](https://makeitfable.com)
- [axe-core CLI](https://www.deque.com/axe/devtools/)
- [pa11y](https://pa11y.org)
- [Knowbility — Open Access Project](https://knowbility.org)
- [Deque University](https://dequeuniversity.com)
- [Inclusive Design Principles — Microsoft](https://inclusive.microsoft.design)
- [NN/g — Accessibility Testing](https://www.nngroup.com/articles/usability-testing-disabilities/)
