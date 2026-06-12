<!--
Source: https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md
Repo: anthropics/skills (OFFICIAL ANTHROPIC SKILL)
-->
---
name: doc-coauthoring
description: Structured workflow for guiding users through collaborative document creation across three stages — Context Gathering, Refinement & Structure, Reader Testing.
---

# Doc Co-Authoring Workflow

Act as an active guide, walking users through three stages: Context Gathering, Refinement & Structure, and Reader Testing.

## When to Offer This Workflow

**Trigger conditions:**
- User mentions writing documentation: "write a doc", "draft a proposal", "create a spec", "write up"
- User mentions specific doc types: "PRD", "design doc", "decision doc", "RFC"
- User seems to be starting a substantial writing task

**Initial offer:**
Offer the user a structured workflow for co-authoring the document. Explain the three stages:

1. **Context Gathering**: User provides all relevant context while Claude asks clarifying questions
2. **Refinement & Structure**: Iteratively build each section through brainstorming and editing
3. **Reader Testing**: Test the doc with a fresh Claude (no context) to catch blind spots before others read it

If user declines, work freeform. If user accepts, proceed to Stage 1.

## Stage 1: Context Gathering

**Goal:** Close the gap between what the user knows and what Claude knows.

### Initial Questions

Start by asking the user for meta-context about the document:
1. What type of document is this? (e.g., technical spec, decision doc, proposal)
2. Who's the primary audience?
3. What's the desired impact when someone reads this?
4. Is there a template or specific format to follow?
5. Any other constraints or context to know?

### Info Dumping

Encourage the user to dump all the context they have. Request:
- Background on the project/problem
- Related team discussions or shared documents
- Why alternative solutions aren't being used
- Organizational context (team dynamics, past incidents, politics)
- Timeline pressures or constraints
- Technical architecture or dependencies
- Stakeholder concerns

Advise them not to worry about organizing it — just get it all out.

### Clarifying Questions

When user signals they've done their initial dump, ask 5-10 numbered clarifying questions based on gaps. Let them answer in shorthand.

**Exit condition:** Sufficient context when questions show understanding — can ask about edge cases and trade-offs without needing basics explained.

## Stage 2: Refinement & Structure

**Goal:** Build the document section by section through brainstorming, curation, and iterative refinement.

For each section:
1. Clarifying questions about what to include
2. 5-20 options brainstormed
3. User indicates what to keep/remove/combine
4. Section drafted
5. Refined through surgical edits

### Section ordering

Suggest starting with whichever section has the most unknowns. For decision docs, that's usually the core proposal. For specs, the technical approach. Summary sections best left for last.

### Per-section workflow

**Step 1: Clarifying Questions** — Ask 5-10 specific questions about what should be included.

**Step 2: Brainstorming** — Generate 5-20 numbered options. Look for context the user might have forgotten or angles not yet mentioned.

**Step 3: Curation** — Ask what to keep/remove/combine. Examples:
- "Keep 1,4,7,9"
- "Remove 3 (duplicates 1)"
- "Remove 6 (audience already knows this)"
- "Combine 11 and 12"

**Step 4: Gap Check** — Ask if anything important is missing.

**Step 5: Drafting** — Replace placeholder with drafted content (use `str_replace`).

**Step 6: Iterative Refinement** — Make surgical edits based on feedback. Never reprint the whole doc.

After 3 consecutive iterations with no substantial changes, ask if anything can be removed without losing important information.

### Near completion

As approaching 80%+ of sections done, re-read the entire document and check for:
- Flow and consistency across sections
- Redundancy or contradictions
- Anything that feels like "slop" or generic filler
- Whether every sentence carries weight

## Stage 3: Reader Testing

**Goal:** Test the document with a fresh Claude (no context bleed) to verify it works for readers.

### With sub-agents available

1. **Predict reader questions** — generate 5-10 questions readers would realistically ask
2. **Test with sub-agent** — invoke a fresh Claude instance with just the document content + the question
3. **Run additional checks** — invoke sub-agent to check for ambiguity, false assumptions, contradictions
4. **Report and fix** — loop back to refinement for any problematic sections

### Without sub-agents

Provide testing instructions:
1. Open a fresh Claude conversation
2. Paste or share the document content
3. Ask Reader Claude the generated questions
4. Also ask: "What might be ambiguous?", "What knowledge does this doc assume?", "Any internal contradictions?"

### Exit condition

When Reader Claude consistently answers questions correctly and doesn't surface new gaps or ambiguities, the doc is ready.

## Final Review

Before completion:
1. Recommend the user does a final read-through themselves
2. Suggest double-checking any facts, links, or technical details
3. Ask them to verify it achieves the impact they wanted

## Tips for Effective Guidance

**Tone:** Direct and procedural. Explain rationale briefly when it affects user behavior. Don't try to "sell" the approach — just execute it.

**Handling Deviations:** If user wants to skip a stage, ask if they want to skip it and write freeform. If user seems frustrated, acknowledge and suggest ways to move faster. Always give user agency.

**Context Management:** Proactively ask about missing context. Don't let gaps accumulate.

**Quality over Speed:** Each iteration should make meaningful improvements. The goal is a document that actually works for readers.
