# AI Ideation + Drafting — Claude Long-Context + Vale Slop Scrub

> Generate 30 ideas, draft long-form, then run mechanical AI-slop scrub via Vale before publishing.

## When to use

Trigger on: "help me ideate", "30 angles on this topic", "draft this newsletter / podcast script / blog post", "Vale slop scrub", "humanize this AI text", "brainstorm hook variations", "Claude long-context outline". This skill owns: structured ideation (`brainstorming` skill + Claude long-context) + drafting + mechanical slop removal via Vale. For platform-specific drafting see format-specific skills. For broad voice + brand guidelines defer to `marketing-agent`'s `vale-brand-voice`.

## Setup

```bash
# Vale (linter for prose)
brew install vale
# or via uvx for ephemeral runs:
uvx --from vale vale --version

# Claude API (when running outside the agent harness)
curl -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  https://api.anthropic.com/v1/messages

# Custom .vale.ini in repo root pointing at content-creator slop catch rules
```

Auth env vars:
- `ANTHROPIC_API_KEY` — Claude API direct calls; inside the agent harness, Claude is the host so this is not needed.
- `OPENAI_API_KEY` — optional fallback for cross-model comparison.

## Common recipes

### Recipe 1: 30-angles ideation

```markdown
# Use the `brainstorming` skill + Claude long-context to generate 30 angles on one topic

## Topic
"Why Tuesday 6am beats Sunday night for newsletter sends"

## Generate 30 distinct angles
- 10 educational angles (teach a tactic)
- 10 contrarian angles (challenge conventional wisdom)
- 10 narrative angles (tell a story)

## Then cluster + cut
- Cluster into 5-7 themes
- Identify 3 winning candidates per theme
- Rank top 10 by audience-relevance + novelty
- Top 3 = pieces to actually write
```

### Recipe 2: Long-context outline draft

```python
# Use Claude with full-context input (newsletter archive + brand voice + audience persona)
import anthropic
client = anthropic.Anthropic()

archive = open('archive_30_issues.txt').read()  # past content for voice
brand_voice = open('brand_voice.md').read()
persona = open('audience_persona.md').read()

prompt = f"""
Brand voice:
{brand_voice}

Audience persona:
{persona}

Past content (for voice reference, NOT for plagiarism):
{archive}

Write a 1500-word newsletter issue outline on:
"Why Tuesday 6am beats Sunday night for newsletter sends"

Structure:
- Hook (pattern-interrupt or surprising stat)
- Body (3 sections — thesis, proof, implication)
- Takeaway (1 sentence)
- CTA

Use active voice, second person. NO "leverage", "utilize", "in today's fast-paced world".
No em-dash storms (max 1 per paragraph). No sycophancy openers.
"""

resp = client.messages.create(
    model="claude-opus-4-1-20250805",
    max_tokens=4096,
    messages=[{"role": "user", "content": prompt}],
)
print(resp.content[0].text)
```

### Recipe 3: Vale slop scrub setup

`.vale.ini`:

```ini
StylesPath = .vale/styles
MinAlertLevel = suggestion

[*.md]
BasedOnStyles = ContentCreator
```

`.vale/styles/ContentCreator/banned-openers.yml`:

```yaml
extends: existence
message: "Banned opener: '%s' — rewrite without."
level: error
ignorecase: true
nonword: false
tokens:
  - "In today's fast-paced world"
  - "In a world where"
  - "It's no secret that"
  - "Navigating the landscape of"
  - "I've been thinking about"
  - "Look no further than"
```

`.vale/styles/ContentCreator/jargon-substitution.yml`:

```yaml
extends: substitution
message: "Use '%s' instead of '%s'"
level: warning
ignorecase: true
swap:
  leverage: use
  utilize: use
  synergize: ""
  "best-in-class": ""
  "game-changing": ""
  "cutting-edge": ""
```

`.vale/styles/ContentCreator/sycophancy.yml`:

```yaml
extends: existence
message: "Cut sycophancy: '%s'"
level: error
tokens:
  - "Great question!"
  - "Certainly!"
  - "Absolutely!"
  - "Wonderful!"
  - "Excellent!"
```

`.vale/styles/ContentCreator/em-dash-storm.yml`:

```yaml
extends: occurrence
message: "Too many em-dashes in this paragraph (max 1)."
level: warning
scope: paragraph
ignorecase: true
max: 1
token: "—"
```

`.vale/styles/ContentCreator/transitions.yml`:

```yaml
extends: existence
message: "Stock transition '%s' — consider rewriting."
level: suggestion
tokens:
  - "^Moreover,"
  - "^Furthermore,"
  - "^However,"
  - "Whether you're.*or"
  - "Not only.*but also"
```

### Recipe 4: Run Vale on draft

```bash
uvx vale --config=.vale.ini --output=JSON content/issue-042.md \
  | jq '.[]|.[]|{Check,Severity,Message,Line,Span}'

# Or shape for human review
uvx vale --config=.vale.ini --output=line content/issue-042.md
```

Block publish if any `error` severity returned.

### Recipe 5: Cross-model second opinion (Claude vs Gemini)

```bash
# Generate hooks via Claude
CLAUDE_HOOKS=$(claude-cli generate --prompt "10 hooks for...")

# Generate via Gemini
GEMINI_HOOKS=$(npx @google-gemini/cli generate --prompt "10 hooks for...")

# Compare; manually pick best 3 from combined 20
```

Gemini sometimes catches angles Claude misses (and vice versa). Use for hero pieces.

### Recipe 6: Hook variation harness

```python
# Generate 10 hooks for a single topic + pick winning style
topic = "Why Tuesday 6am beats Sunday night for newsletter sends"

styles = [
    "Surprising stat",
    "Contrarian claim",
    "Specific outcome promise",
    "Question",
    "Story (mid-action)",
    "Pattern interrupt visual",
    "Direct address ('If you...')",
    "Stakes ('Most people lose...')",
    "Authority ('I tested 30 ESPs...')",
    "Reframe ('It's not X — it's Y')",
]

hooks = []
for style in styles:
    h = claude.generate(f"Write one hook in '{style}' style for: {topic}. <30 words.")
    hooks.append((style, h))

# Then A/B test top 3 across different formats
```

### Recipe 7: Voice-mirror prompt

```markdown
## Voice-mirror prompt template

When drafting a new piece in a brand voice you've defined:

System prompt:
"You are writing in <Creator>'s voice. Past samples below — match cadence, sentence length, vocabulary, rhythm. NEVER use: leverage, utilize, in today's fast-paced world. NEVER start with 'Great question'. ALWAYS active voice + second person."

User prompt:
[past sample 1]
[past sample 2]
[past sample 3]

Now write a [length]-word [format] on: <topic>
```

### Recipe 8: Iterate draft (rewrite passes)

```python
# Pass 1: Initial draft
draft_v1 = claude.generate(initial_prompt)

# Pass 2: Tighten — cut filler
draft_v2 = claude.generate(f"Tighten the following draft. Cut 20% of word count. Remove any filler. Keep core ideas:\n\n{draft_v1}")

# Pass 3: Add specificity
draft_v3 = claude.generate(f"In the following draft, replace vague claims with specific numbers + examples where possible:\n\n{draft_v2}")

# Pass 4: Vale slop scrub
# Run Recipe 4
```

### Recipe 9: Long-context series outline

```python
# Use Claude long-context (200k+ tokens) to plan a 12-week series in one call
all_past_issues = "\n\n".join(open(f).read() for f in glob('archive/*.md'))  # ~30k tokens
audience_data = open('audience_survey.md').read()  # ~10k tokens
brand_voice = open('brand_voice.md').read()  # ~5k tokens
sota_research = open('sota_2026.md').read()  # ~30k tokens

prompt = f"""
Past archive (30 issues):
{all_past_issues}

Audience research:
{audience_data}

Brand voice:
{brand_voice}

SOTA research for 2026:
{sota_research}

Plan a 12-week newsletter series. Each week: 1 tentpole thesis + 3 pillars + hook + CTA.
Cover: the 12 most important questions this audience is asking RIGHT NOW.
Cross-reference what's already been covered (don't repeat); identify gap topics.
"""

resp = claude.generate(prompt)
# Output → series plan
```

### Recipe 10: Humanize AI-text post-process

```bash
# After draft, run humanize-ai-text skill (CraftBot default) to programmatically strip slop tells
# Then Vale (Recipe 4) for residual catches
```

### Recipe 11: Hand-tuning loop

```markdown
## Drafting loop (iterate ~3-5 passes)

1. Recipe 1: 30 angles, cluster, pick top 3
2. Recipe 2: long-context outline
3. Recipe 7: voice-mirror flesh out
4. Recipe 8: 3-pass tighten + specificity + add data
5. Recipe 10: humanize-ai-text
6. Recipe 4: Vale slop scrub
7. Read aloud (catches rhythm issues Vale misses)
8. Sleep on it; reread next morning
9. Final polish
```

### Recipe 12: Style guide enforcement

```yaml
# Create a custom style guide rule for each banned pattern
# Run Vale on every PR / commit / pre-publish hook

# Pre-commit hook example (.git/hooks/pre-commit):
#!/bin/sh
for f in $(git diff --cached --name-only --diff-filter=ACM "*.md"); do
  uvx vale --config=.vale.ini "$f"
  if [ $? -ne 0 ]; then
    echo "Vale errors in $f — fix before commit"
    exit 1
  fi
done
```

## Examples

### Example 1: 30-angle ideation → newsletter issue

**Goal:** Generate 30 newsletter angles + draft the top one.

**Steps:**
1. Recipe 1: brainstorm 30 angles on "newsletter operator metrics".
2. Cluster into 5-7 themes; pick top 1 angle ("Open rates lie — track CTR instead").
3. Recipe 2: Claude long-context outline.
4. Recipe 8: 3-pass iterate.
5. Recipe 10 humanize-ai-text.
6. Recipe 4: Vale scrub — fix 5 catches.
7. Read aloud; tweak rhythm.
8. Publish via `long-form-newsletter-substack-beehiiv-ghost`.

**Result:** Audience-specific newsletter that doesn't read like AI.

### Example 2: 12-week series plan via long-context Claude

**Goal:** Plan a 12-week series leveraging full archive + audience research.

**Steps:**
1. Recipe 9: full-context series plan.
2. Recipe 1: stress-test plan by brainstorming 30 alternative tentpoles.
3. Adjust plan based on novel angles surfaced in step 2.
4. Recipe 11 (each weekly tentpole): full drafting loop.

**Result:** Series anchored by data + free of AI tells.

### Example 3: Cross-model hook test

**Goal:** Choose between Claude and Gemini hooks for a hero piece.

**Steps:**
1. Recipe 6: 10 hook styles via Claude.
2. Recipe 5: same 10 via Gemini.
3. Manually rank combined 20 hooks; pick top 3.
4. A/B test top 3 in actual publishing across 3 weeks.
5. Identify winning style for future series.

**Result:** Hook-style preference identified via cross-model + A/B testing.

## Edge cases / gotchas

- **AI-slop is a moving target.** Banned-words lists need quarterly updates as LLM patterns shift. Refresh `.vale/styles/ContentCreator/banned-openers.yml` regularly.
- **Vale only catches mechanical patterns** — not bad ideas or weak reasoning. Always read aloud after Vale passes.
- **Vale `error` severity blocks publish; `warning` informs.** Calibrate severity per rule.
- **Don't over-rely on AI for ideation.** AI suggests safe + obvious; human judgment finds the contrarian + specific.
- **Claude long-context (200k+) tokens** is powerful but expensive. Reserve for series planning + hero pieces.
- **Voice-mirroring works best with 30+ samples** of past writing. Fewer = LLM defaults to generic.
- **Sleep-on-it** catches reads-AI-ish that hot off the press doesn't catch.
- **Read aloud** catches awkward rhythm Vale can't.
- **Vale runs locally** (Go binary, fast). Don't depend on cloud linting for pre-publish gates.
- **humanize-ai-text + Vale** combo catches ~80% of slop tells. Final 20% needs human ear.
- **Don't fight Vale on every catch.** If 3 of 10 catches are wrong, that's tolerable — fix the 7 right catches; whitelist the 3 wrong ones.
- **Whitelisting per-file** with Vale comments: `<!-- vale ContentCreator.JargonSubstitution = NO -->`
- **Cross-model second opinion** is overkill for 80% of pieces; use for hero/launch content.
- **Drafts that need ground-up rewrites probably had the wrong outline.** Loop back to Recipe 1 / Recipe 2.
- **Don't publish AI-text uncited if presented as your voice.** Disclose if substantial AI co-authorship per platform rules + audience norms.

## Sources

- [Vale linter](https://vale.sh/)
- [Vale rule writing](https://vale.sh/docs/topics/styles/)
- [Anthropic Claude API](https://docs.anthropic.com/en/api/getting-started)
- [Long-context use cases (Anthropic)](https://docs.anthropic.com/en/docs/build-with-claude/context-windows)
- [Best practices for prompt engineering (Anthropic)](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Marketing-agent vale-brand-voice skill — mirrored](https://github.com/wshobson/agents)
- [Brainstorming skill (CraftBot default)](https://github.com/anthropics/anthropic-quickstarts)
